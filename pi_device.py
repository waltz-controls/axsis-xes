# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:32:08 2020

@author: ingvord
"""
import os
import time
from enum import Enum, auto
from functools import lru_cache

from gcsdevice import GCSDevice


class Mode(Enum):
    simulation = auto()
    production = auto()


# TODO(MODE in query string)
MODE = Mode[os.getenv('MODE', default='simulation')]


@lru_cache()
def create_pi_device(host, port=50000, mode = Mode.simulation):
    if host is None:
        raise Exception('host must not be None!')

    if mode == Mode.production:
        from pipython.pidevice.gcscommands import GCSCommands
        from pipython.pidevice.gcsmessages import GCSMessages
        from pipython.pidevice.interfaces.pisocket import PISocket

        gateway = PISocket(host, port)
        messages = GCSMessages(gateway)
        pi_device = GCSCommands(messages)

        connected = False
        while not connected:
            time.sleep(0.01)
            connected = messages.connected

        ready = False
        while not ready:
            time.sleep(0.01)
            ready = pi_device.IsControllerReady()

        return pi_device
    else:
        return GCSDevice()