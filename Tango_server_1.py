# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:27:17 2020

@author: ingvord
"""

from tango.server import Device, attribute, command, pipe, device_property
from pipython import GCSDevice
import time

host = '192.168.83.138'

PiDevice = GCSDevice()
PiDevice.ConnectTCPIP(host)

while not PiDevice.IsConnected():
    time.sleep(0.1)

while not PiDevice.IsControllerReady():
    time.sleep(0.1)

class OneAxis(Device):

    axis = device_property(dtype=str, default_value='1')

    def init_device(self):
        self.axis = self.get_name().split('/')[2]

        self.pi_device = PiDevice

        try:
            self.pi_device.FRF(self.axis)
        except:
            print(self.pi_device.qERR())
        print("done")
        #TODO query axises and reference every

    @attribute(dtype=float)
    def position(self):
        return self.pi_device.qPOS().get(self.axis)

    @attribute(dtype=bool)
    def servo(self):
        return self.pi_device.qSVO().get(self.axis)

    @attribute(dtype=bool)
    def referenced(self):
        return self.pi_device.qFRF().get(self.axis)

    def state(self):
        return self.pi_device.qSVO(self.axis)

    def status(self):
        return "IsConnected: " + self.pi_device.IsConnected()

    @command(dtype_in=None)
    def enable_servo(self):
        self.pi_device.SVO(self.axis, 1)

    @command(dtype_in=None)
    def disable_servo(self):
        self.pi_device.SVO(self.axis, 0)

    @command(dtype_in=float, dtype_out=None)
    def move(self, pos):
        if not self.pi_device.qSVO(self.axis):
            raise Exception("not in servo mode, enable first")

        self.pi_device.MOV(self.axis, pos)  # Command axis "A" to position pos

    @command(dtype_in=None)
    def stop(self):
        self.pi_device.HLT(self.axis)

    @command(dtype_in=None)
    def stop_all(self):
        self.pi_device.STP()


if __name__ == "__main__":
    OneAxis.run_server()
