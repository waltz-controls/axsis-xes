# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:32:08 2020

@author: ingvord
"""

import os
import time

if os.getenv('MODE', default='simulation') == 'production':
    from pipython import GCSDevice
else:
    from gcsdevice import GCSDevice



def create_pi_device(host, port=50000):
    if host is None:
        raise Exception('host must not be None!')

    pi_device = GCSDevice()

    pi_device.ConnectTCPIP(host, port)

    connected = False
    while not connected:
        time.sleep(0.01)
        connected = pi_device.IsConnected()

    ready = False
    while not ready:
        time.sleep(0.01)
        ready = pi_device.IsControllerReady()

    return pi_device
