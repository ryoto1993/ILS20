# coding: utf-8

from utils.reader import *
import time


def change_to_max(lights):
    for l in lights:
        # 色温度制御までするとき
        if INIT.TEMPERATURE:
            for i in range(len(l.signals)):
                l.signals[i] = INIT.LIGHT_SIGNAL_MAX[i]
        # 色温度制御を行わない時
        else:
            l.signals[0] = INIT.LIGHT_SIGNAL_MAX[0]
    time.sleep(0.1)


def change_to_min(lights):
    for l in lights:
        # 色温度制御までするとき
        if INIT.TEMPERATURE:
            for i in range(len(l.signals)):
                l.signals[i] = INIT.LIGHT_SIGNAL_MIN[i]
        # 色温度制御を行わない時
        else:
            l.signals[0] = INIT.LIGHT_SIGNAL_MIN[0]
    time.sleep(0.1)


def change_to_fixed_pattern(lights):
    pattern = light_pattern_reader()

    for i, l in enumerate(lights):
        for j in range(len(l.signals)):
            l.signals[j] = pattern[i][j]
    time.sleep(0.1)

def change_to_zero(lights):
    for l in lights:
        for i in range(len(l.signals)):
            l.signals[i] = 0
    time.sleep(0.1)