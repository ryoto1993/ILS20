# coding: utf-8

from equipment.Light import *
from equipment.Sensor import *
from equipment.PowerMeter import *
from configure.config import *
import random
import math


def calc_illuminance(ils):
    u"""照明の現在光度から各センサの現在照度を計算"""
    for s_i, s in enumerate(ils.sensors):
        s.illuminance = 0.0
        for l in ils.lights:
            s.illuminance += l.luminosity * l.influence[s_i]

        # セコニック製照度センサの誤差外乱模擬
        if INIT.SIMULATE_VOLTAGE_DISPLACEMENT:
            s.illuminance = s.illuminance + random.normalvariate(0, math.sqrt(5))

        # 収束しているかチェック
        if s.target*(100+INIT.ALG_ALLOWANCE_LOWER)/100 <= s.illuminance <= s.target+INIT.ALG_ALLOWANCE_UPPER:
            s.convergence = True
        else:
            s.convergence = False
