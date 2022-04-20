import abc
import argparse
import asyncio
import json
import os
import time
import sys
import logging
from functools import reduce

import rx.operators as ops
from magix_client import MagixHttpClient, Message
from rx.scheduler.eventloop import AsyncIOScheduler
from pi_device import create_pi_device, Mode

kMagixHost = os.getenv('MAGIX_HOST', 'http://localhost:8080')
kChannel = 'axsis-xes'


class AxsisMessage:
    def __init__(self, ip, action, value, port=50000, mode=Mode.simulation.name):
        self.ip = ip
        self.port = port
        self.action = action
        self.value = value
        self.mode = Mode[mode]


class ActionExecutor(abc.ABC):
    def __init__(self, magix: MagixHttpClient, pi_device, msg: Message):
        self.magix = magix
        self.target = pi_device
        self.message = msg
        self.action = msg.payload

    def _send_position_message(self):
        pos = self.target.qPOS()
        mess =  Message(id=time.time_ns(), parentId=self.message.id, target=self.message.origin,
                       origin='axsis', payload=AxsisMessage(ip=self.action.ip, action='qPOS', value=pos))
        self.magix.broadcast(mess, channel=kChannel)

    def _send_done_message(self):
        self.magix.broadcast(Message(id=time.time_ns(), parentId=self.message.id, target=self.message.origin,
                                     origin='axsis', action='done'),
                             channel=kChannel)

    @abc.abstractmethod
    async def execute(self):
        pass


class StopExecutor(ActionExecutor):

    async def execute(self):
        data = self.action.value
        self.target.HLT(data, True)
        self._send_done_message()


class RebootExecutor(ActionExecutor):

    async def execute(self):
        self.target.RBT()
        self._send_done_message()


class HomeExecutor(ActionExecutor):
    pass


class PositionExecutor(ActionExecutor):
    async def execute(self):
        data = self.action.value
        self.target.MOV(data)
        while True:
            await asyncio.sleep(0.1)
            self._send_position_message()
            if reduce(lambda a, b: a or b, self.target.IsMoving(list(data.keys())).values()): break
        self._send_done_message()


class ReferenceExecutor(ActionExecutor):

    async def execute(self):
        data = self.action.value
        self.target.FRF(data)
        while True:
            await asyncio.sleep(0.1)
            self._send_position_message()
            if reduce(lambda a, b: a or b, self.target.IsMoving(list(data.keys())).values()): break
        self._send_done_message()


class ServoExecutor(ActionExecutor):
    pass


class AxsisObserver:
    # TODO(Command name)
    _executor_factory = {
        "stop" : StopExecutor,
        "reboot" : RebootExecutor,
        "MOV" : PositionExecutor,
        "reference" : ReferenceExecutor,
        "servo" : ServoExecutor
    }

    def __init__(self, magix, loop, host, port):
        self.magix = magix
        self.loop = loop
        self.host = host
        self.port = port

    def on_next(self, msg):
        try:
            pi_device = create_pi_device(self.host, self.port, msg.payload.mode)
            executor_factory = AxsisObserver._executor_factory[msg.payload.action]
            executor = executor_factory(self.magix, pi_device, msg)
            asyncio.run(executor.execute())
        except Exception as err:
            logging.debug(repr(self.action.__dict__))
            msg = Message(id=time.time_ns(), origin='axsis', action='error', parentId=msg.id,
                          payload={'error': 'Internal error has occurred: {0}.'.format(err)})
            self.magix.broadcast(msg,
                                 channel=kChannel)
        pass

    def on_error(self, err):
        self.magix.broadcast(Message(id=time.time_ns(), origin='axsis', action='error',
                                     payload={
                                         'error': 'Critical error has occurred: {0}. Please restart AXSIS Magix connector'.format(
                                             err)}),
                             channel=kChannel)
        self.loop.call_soon_threadsafe(self.loop.stop)
        print("errored")

    def on_completed(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        print("completed")
        pass


def create_argparser():
    parser = argparse.ArgumentParser(description='Start AXSIS Magix client for selected controller.')
    parser.add_argument('--host', default="localhost", help='Host of controller')
    parser.add_argument('--port', default=50000, type=int, help='Port of controller')
    parser.add_argument('--debug', action="store_true", help='Enable debug log')
    return parser



def main():
    args = create_argparser().parse_args()
    if args.debug:
        logging.root.setLevel(logging.DEBUG)

    loop = asyncio.get_event_loop()
    client = MagixHttpClient(kMagixHost)
    observer = AxsisObserver(client, loop, args.host, args.port)
    client.observe(channel=kChannel).pipe(
        ops.filter(lambda event: json.loads(event.data).get('target') == 'axsis'),
        ops.map(lambda event: Message.from_json(event.data, payload_cls=AxsisMessage)),
        # TODO ops.catch()
        # TODO proxy object or optimize somehow
    ).subscribe(observer, scheduler=AsyncIOScheduler(loop))
    loop.run_forever()
    loop.close()
    print("exited")
    sys.exit(-1)



if __name__ == "__main__":
    main()
