# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:32:08 2020

@author: ingvord
"""

import os
import time
from gcsdevice import GCSDevice

kModeIsProduction = os.getenv('MODE', default='simulation') == 'production'

if kModeIsProduction:
    from pipython.pidevice.gcscommands import GCSCommands
    from pipython.pidevice.gcsmessages import GCSMessages
    from pipython.pidevice.interfaces.pisocket import PISocket

def create_pi_device(host, port=50000):
    if host is None:
        raise Exception('host must not be None!')

    if kModeIsProduction:
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