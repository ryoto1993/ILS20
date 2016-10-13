# coding: utf-8

from configure.config import *


def convert_to_luminosity(lights):
    u"""信号値を光度値に変換する"""

    # TODO: 現在は1つめの信号値のみだが，色温度制御の時にはここを書き換える必要がある．
    for l in lights:
        l.luminosity = int(-0.0130119460805247 * float(l.signals[0]) * float(l.signals[0]) + 13.9104144531693 * float(l.signals[0]) - 40.0024478040349)

def convert_to_signal(lights):
    u"""光度値を信号値に変換する"""

    if INIT.TEMPERATURE:
        pass
    else:
        for l in lights:
            l.signals[0] = int(0.00000664944924261323 * float(l.luminosity) * float(l.luminosity) + 0.0711852025585447 * float(l.luminosity) + 3.06397372065703)