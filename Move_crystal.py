# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:32:08 2020

@author: ingvord
"""

from pipython import GCSDevice
import time

pi_device = GCSDevice ()	# Load PI Python Libraries

#pi_device.ConnectUSB ('123456789') 	# Connect to the controller via USB
pi_device.ConnectTCPIP('192.168.83.138') # Connect to the controller via TCP/IP
connected = False
while not connected:
    connected = pi_device.IsConnected()
    time.sleep(0.1)


pi_device.SVO ('3', 1) 	# Turn on servo control of axis "A"

pi_device.FRF('3')
referencing_finished = False
while not referencing_finished:
    referencing_finished = pi_device.IsControllerReady()

pi_device.MOV('3', 16)  # Command axis "A" to position pos
moving = True
while moving:
    moving = pi_device.IsMoving('3')
    time.sleep(0.1)

#pi_device.MOV ('1', 3.142) 	# Command axis "A" to position 3.142

position = pi_device.qPOS ('3')	# Query current position of axis "A"

reference = pi_device.qFRF('3')