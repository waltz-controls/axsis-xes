# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:32:08 2020

@author: ingvord
"""

version = {
  "version": "libpi_pi_gcs2.so.3.9.8.1 \nPath: /usr/local/PI/pi_gcs_translator/PISTAGES3.DB Version: 3.0.17.0 \n2: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550039, 00.039 \n3: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550040, 00.039 \n4: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550041, 00.039 \n5: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550042, 00.039 \n6: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550043, 00.039 \n7: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550044, 00.039 \n8: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550046, 00.039 \n9: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550045, 00.039 \n10: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550047, 00.039 \n11: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550048, 00.039 \n12: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550049, 00.039 \n13: (c)2017 Physik Instrumente (PI) GmbH & Co. KG, C-663.12C885, 018550051, 00.039 \nFW_ARM: V1.0.0.1 \nPIPython: 1.3.9.40\n"
}

servo = {
    "1": False,
    "3": False,
    "5": False,
    "7": False,
    "9": False,
    "11": False,
    "13": False,
    "15": False,
    "17": False,
    "19": False,
    "21": False,
    "23": False
}

reference = {
    "1": False,
    "3": False,
    "5": False,
    "7": False,
    "9": False,
    "11": False,
    "13": False,
    "15": False,
    "17": False,
    "19": False,
    "21": False,
    "23": False
}

position = {
    "1": 12.2000001,
    "3": 12.2000001,
    "5": 12.2000001,
    "7": 12.2000001,
    "9": 12.2000001,
    "11": 12.2000001,
    "13": 12.2000001,
    "15": 12.2000001,
    "17": 12.2000001,
    "19": 12.2000001,
    "21": 12.2000001,
    "23": 12.2000001
}


class GCSDevice():
    def __init__(self):
        print("Simulating PiController")

    def ConnectTCPIP(self, host, port):
        return None

    def CloseConnection(self):
        pass

    def IsConnected(self):
        return True

    def IsControllerReady(self):
        return True

    def qVER(self):
        return version

    def qSVO(self):
        return servo

    def SVO(self, values):
        pass

    def qFRF(self, **kwargs):
        return reference

    def FRF(self, values):
        pass

    def qPOS(self):
        return position

    def MOV(self, values):
        pass

    def IsMoving(self):
        return False
