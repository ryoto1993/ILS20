# coding: utf-8

from utils.reader import *
import time

# TODO: 信号値から消費電力を計算するやつつくれ


def change_to_max(lights):
    u"""すべての照明の信号値をLIGHT_SIGNAL_MAXに切り替えるメソッド"""
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
    u"""すべての照明の信号値をLIGHT_SIGNAL_MINに切り替えるメソッド"""
    for l in lights:
        # 色温度制御までするとき
        if INIT.TEMPERATURE:
            for i in range(len(l.signals)):
                l.signals[i] = INIT.LIGHT_SIGNAL_MIN[i]
        # 色温度制御を行わない時
        else:
            l.signals[0] = INIT.LIGHT_SIGNAL_MIN[0]
    time.sleep(0.1)


def change_to_zero(lights):
    u"""すべての照明の信号値を0に切り替えるメソッド"""
    for l in lights:
        for i in range(len(l.signals)):
            l.signals[i] = 0
    time.sleep(0.1)


def change_to_fixed_pattern(lights):
    u"""LIGHT_PATTERN_FILEで定義した点灯パターンの信号値に切り替えるメソッド"""
    pattern = light_pattern_reader()

    if not len(pattern[0]) == len(lights[0].signals):
        print("Error, pattern config file isn't match to number of light signals.")
        return
    for i, l in enumerate(lights):
        for j in range(len(l.signals)):
            l.signals[j] = pattern[i][j]
    time.sleep(0.1)


def change_manually(lights, sig):
    u"""すべての照明を信号値sigに変更するメソッド"""
    for l in lights:
        # 色温度制御までするとき
        if INIT.TEMPERATURE:
            for i in range(len(l.signals)):
                l.signals[i] = sig
        # 色温度制御を行わない時
        else:
            l.signals[0] = sig

    convert_to_luminosity(lights)


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
