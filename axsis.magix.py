import asyncio
import json
import os
import time
import sys
from functools import reduce

import rx.operators as ops
from magix_client import MagixHttpClient, Message
from rx.scheduler.eventloop import AsyncIOScheduler

from pi_device import create_pi_device

kMagixHost = os.getenv('MAGIX_HOST', 'http://localhost:8080')
kChannel = 'axsis-xes'


class AxsisMessage:
    def __init__(self, ip, action, value, port=50000):
        self.ip = ip
        self.port = port
        self.action = action
        self.value = value


# TODO extract hierarchy
class ActionExecuter:
    def __init__(self, magix: MagixHttpClient, pi_device, msg: Message):
        self.magix = magix
        self.target = pi_device
        self.message = msg
        self.action = msg.payload

    async def execute(self):
        data = self.action.value
        try:
            self.target.MOV(data)
            stopped = False
            while not stopped:
                await asyncio.sleep(0.1)

                def create_message():
                    pos = self.target.qPOS()
                    return Message(id=time.time_ns(), parentId=self.message.id, target=self.message.origin,
                                   origin='axsis', payload=AxsisMessage(ip=self.action.ip, action='qPOS', value=pos))

                self.magix.broadcast(create_message(), channel=kChannel)
                stopped = not reduce(lambda a, b: a or b, self.target.IsMoving(list(data.keys())).values())

            self.magix.broadcast(Message(id=time.time_ns(), parentId=self.message.id, target=self.message.origin,
                                         origin='axsis', action='done'),
                                 channel=kChannel)
        finally:
            self.target.CloseConnection()
        pass


class AxsisObserver:
    def __init__(self, magix, loop):
        self.magix = magix
        self.loop = loop

    def on_next(self, msg):
        try:
            pi_device = create_pi_device(msg.payload.ip, msg.payload.port)
            executer = ActionExecuter(self.magix, pi_device, msg)
            asyncio.run(executer.execute())
        except Exception as err:
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


def main():
    loop = asyncio.get_event_loop()
    client = MagixHttpClient(kMagixHost)
    observer = AxsisObserver(client, loop)
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
