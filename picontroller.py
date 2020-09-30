# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:32:08 2020

@author: ingvord
"""

from flask import request
from flask_restful import Resource
import time

class PiController(Resource):
    def get(self, id):
        return { 'version': request.pi_device.qVER() }


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
        moving = True
        while moving:
            time.sleep(0.01)
            moving = request.pi_device.IsMoving()
        return request.pi_device.qPOS()


class PiControllerPosition(Resource):
    def get(self, **kwargs):
        return request.pi_device.qPOS()


    def put(self, **kwargs):
        data = request.json
        request.pi_device.MOV(data)
        moving = True
        while moving:
            time.sleep(0.01)
            moving = request.pi_device.IsMoving()
        return request.pi_device.qPOS()


class PiControllerHome(Resource):
    def put(self, **kwargs):
        #TODO send to home all axis
        pass


class PiControllerStop(Resource):
    def put(self, **kwargs):
        request.pi_device.STP()
        pass