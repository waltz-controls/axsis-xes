# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:32:08 2020

@author: ingvord
"""


class GCSDevice():
    def __init__(self):
        print("Simulating PiController")

    def ConnectTCPIP(self, host, port):
        return None

    def IsConnected(self):
        return True

    def IsControllerReady(self):
        return True

    def qVER(self):
        return "Some version"

    def qSVO(self):
        return {
            '1': True,
            '3': True,
            '5': True
        }

    def SVO(self, values):
        pass


    def qFRF(self, **kwargs):
        return {
            '1': True,
            '3': True,
            '5': True
        }


    def FRF(self, values):
        pass


    def qPOS(self):
        return {
            '1': 12.2,
            '3': 14,
            '5': 8.3
        }

    def MOV(self, values):
        pass

    def IsMoving(self):
        return False