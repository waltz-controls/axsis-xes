# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:32:08 2020

@author: ingvord
"""


from flask import Flask, request
from pi_device import create_pi_device
import time
import os


app = Flask(__name__)

host = os.getenv('AXIS_HOST')
port = os.getenv('AXIS_PORT', 50000)

pi_device = create_pi_device(host, port)


@app.route('/version', methods=['GET'])
def get_version():
    return pi_device.qVER()


@app.route('/reference', methods=['GET'])
def get_reference():
    return pi_device.qFRF()


@app.route('/reference', methods=['POST'])
def post_reference():
    pi_device.FRF()

    referencing = True
    while referencing:
        time.sleep(0.01)
        referencing = not pi_device.IsControllerReady()

    return 'OK'


@app.route('/enable_servo', methods=['POST'])
def post_enable_servo():
    data = request.json
    pi_device.SVO(data['axes'], data['values'])

    referencing = True
    while referencing:
        time.sleep(0.01)
        referencing = not pi_device.IsControllerReady()

    return 'OK'


@app.route('/position', methods=['GET'])
def get_position():
    return pi_device.qPOS()


@app.route('/position', methods=['POST'])
def post_position():
    data = request.json
    pi_device.MOV(data['axes'], data['values'])

    moving = True
    while moving:
        time.sleep(0.01)
        moving = not pi_device.IsMoving()

    return get_position()
