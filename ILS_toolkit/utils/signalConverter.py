# coding: utf-8

from configure.config import *


def convert_to_luminosity(lights):
    u"""信号値を光度値に変換する"""
    factor = (INIT.LIGHT_LUMINOSITY_MAX[0] - INIT.LIGHT_LUMINOSITY_MIN[0]) / \
             (float(INIT.LIGHT_SIGNAL_MAX[0]) - float(INIT.LIGHT_SIGNAL_MIN[0]))
    seppen = INIT.LIGHT_LUMINOSITY_MAX[0] - factor * float(INIT.LIGHT_SIGNAL_MAX[0])

    # TODO: 現在は1つめの信号値のみだが，色温度制御の時にはここを書き換える必要がある．
    for l in lights:
        l.luminosity = l.signals[0] * factor + seppen


# TODO: このメソッド，間違ってる．1次関数でいう切片がない
def convert_to_signal(lights):
    u"""光度値を信号値に変換する"""
    factor = (INIT.LIGHT_SIGNAL_MAX[0] - INIT.LIGHT_SIGNAL_MIN[0]) / \
             (INIT.LIGHT_LUMINOSITY_MAX[0] - INIT.LIGHT_LUMINOSITY_MIN[0])

    for l in lights:
        for i in range(len(l.signals)):
            l.signals[i] = l.luminosity * factor
