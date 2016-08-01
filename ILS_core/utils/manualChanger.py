# coding: utf-8

from configure.config import *


def change_to_max(lights):
    for l in lights:
        # 色温度制御までするとき
        if INIT.TEMPERATURE:
            for i in range(len(l.signals)):
                l.signals[i] = INIT.LIGHT_SIGNAL_MAX[i]
        # 色温度制御を行わない時
        else:
            l.signals[0] = INIT.LIGHT_SIGNAL_MAX[0]