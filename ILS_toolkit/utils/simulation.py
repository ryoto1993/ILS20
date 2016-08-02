# coding: utf-8

from equipment.Light import *
from equipment.Sensor import *
from equipment.PowerMeter import *
from configure.config import *


def calc_illuminance(lights, sensors):
    u"""照明の現在光度から各センサの現在照度を計算"""
    for s_i, s in enumerate(sensors):
        illuminance = 0.0
        for l in lights:
            illuminance += l.luminosity * l.illuminance[s_i]