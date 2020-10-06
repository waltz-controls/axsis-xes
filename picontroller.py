# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:32:08 2020

@author: ingvord
"""

from flask import request
from flask_restful import Resource
from functools import reduce
import time


class PiController(Resource):
    def get(self, id):
        return {'version': request.pi_device.qVER()}


class PiControllerServoMode(Resource):
    def get(self, **kwargs):
        return request.pi_device.qSVO()

    def put(self, **kwargs):
        data = request.json
        request.pi_device.SVO(data)
        return request.pi_device.qSVO()


class PiControllerReference(Resource):
    def get(self, **kwargs):
        return request.pi_device.qFRF()

    def put(self, **kwargs):
        data = request.json
        request.pi_device.FRF(data)
        stopped = False
        while not stopped:
            time.sleep(0.1)
            stopped = not reduce(lambda a, b: a or b, request.pi_device.IsMoving(data).values())
        return request.pi_device.qPOS()


class PiControllerPosition(Resource):
    def get(self, **kwargs):
        return request.pi_device.qPOS()

    def put(self, **kwargs):
        data = request.json
        request.pi_device.MOV(data)
        stopped = False
        while not stopped:
            time.sleep(0.1)
            stopped = not reduce(lambda a, b: a or b, request.pi_device.IsMoving(list(data.keys())).values())
        return request.pi_device.qPOS()


class PiControllerHome(Resource):
    def put(self, **kwargs):
        # TODO send to home all axis
        pass


class PiControllerStop(Resource):
    def put(self, **kwargs):
        data = request.json
        request.pi_device.HLT(data, True)
        pass
