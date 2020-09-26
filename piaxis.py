# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:32:08 2020

@author: ingvord
"""

from flask import request
from flask_restful import Resource
import time


class PiAxis(Resource):
    def get(self, controller_id, id):
        return { 'id': id }


class PiAxisReference(Resource):
    def get(self, id, **kwargs):
        return request.pi_device.qFRF()[id]


    def put(self, id, **kwargs):
        request.pi_device.FRF(id)
        pass


class PiAxisPosition(Resource):
    def get(self, id, **kwargs):
        return request.pi_device.qPOS()[id]


    def put(self, id, **kwargs):
        data = request.json
        request.pi_device.MOV(data)
        moving = True
        while moving:
            time.sleep(0.01)
            moving = request.pi_device.IsMoving()
        pass