# coding: utf-8

from equipment.Light import *
from equipment.Sensor import *
from equipment.PowerMeter import *
from configure.config import *


def calc_illuminance(lights, sensors):
    u"""照明の現在光度から各センサの現在照度を計算"""