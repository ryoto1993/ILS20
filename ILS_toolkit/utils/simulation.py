# coding: utf-8

import random
import math

from configure.config import INIT


def calc_illuminance(ils):
    u"""照明の現在光度から各センサの現在照度を計算"""
    for s_i, s in enumerate(ils.sensors):
        s.illuminance = 0.0
        for l in ils.lights:
            if INIT.MODE_TEMPERATURE:
                for lum in l.luminosities:
                    s.illuminance += lum * l.influence[s_i]
                    # print(str(s) + " " + str(l) + " lum:" + str(lum) + ", inf: " + str(l.influence[s_i]))
            else:
                s.illuminance += l.luminosities[0] * l.influence[s_i]

        # セコニック製照度センサの誤差外乱模擬
        if INIT.MODE_SIMULATE_VOLTAGE_DISPLACEMENT:
            s.illuminance = s.illuminance + random.normalvariate(0, math.sqrt(5))

        # 収束しているかチェック
        if s.target*(100+INIT.ALG_ALLOWANCE_LOWER)/100 <= s.illuminance <= s.target+INIT.ALG_ALLOWANCE_UPPER:
            s.convergence = True
        else:
            s.convergence = False


def calc_illuminance_color_divided(ils):
    u"""色温度別に照明光度を管理する手法で，各センサの各色温度ごとの現在照度を計算"""
    for s_i, s in enumerate(ils.sensors):
        s.divided_illuminance = [0.0, 0.0]
        for l in ils.lights:
            for index, lum in enumerate(l.luminosities):
                s.divided_illuminance[index] += lum * l.influence[s_i]

        # 収束しているかチェック

