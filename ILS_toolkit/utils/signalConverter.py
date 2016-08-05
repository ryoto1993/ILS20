﻿# coding: utf-8

from configure.config import *


def convert_to_luminosity(lights):
    u"""信号値を光度値に変換する"""
    # 1次関数の傾き
    factor = (INIT.LIGHT_LUMINOSITY_MAX[0] - INIT.LIGHT_LUMINOSITY_MIN[0]) / \
             (float(INIT.LIGHT_SIGNAL_MAX[0]) - float(INIT.LIGHT_SIGNAL_MIN[0]))
    # 1次関数の切片
    intercept = INIT.LIGHT_LUMINOSITY_MAX[0] - factor * float(INIT.LIGHT_SIGNAL_MAX[0])

    # TODO: 現在は1つめの信号値のみだが，色温度制御の時にはここを書き換える必要がある．
    for l in lights:
        l.luminosity = l.signals[0] * factor + intercept


def convert_to_signal(lights):
    u"""光度値を信号値に変換する"""
    # 1次関数の傾き
    factor = (INIT.LIGHT_SIGNAL_MAX[0] - INIT.LIGHT_SIGNAL_MIN[0]) / \
             (INIT.LIGHT_LUMINOSITY_MAX[0] - INIT.LIGHT_LUMINOSITY_MIN[0])
    # 1次関数の切片
    intercept = INIT.LIGHT_SIGNAL_MAX[0] - factor * float(INIT.LIGHT_LUMINOSITY_MAX[0])

    if INIT.TEMPERATURE:
        pass
    else:
        for l in lights:
            l.signals[0] = int(l.luminosity * factor + intercept)
