# coding: utf-8

import re
import csv

from equipment.Light import *


##########################
#        Manager系        #
##########################
def state_reader():
    u"""ステータスファイルを読み込む"""
    while True:
        try:
            f = open(INIT.FILE_STATE, 'r', encoding='utf-8')
            break
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

    lines = f.readlines()
    f.close()

    for s in lines:
        pos = s.find("state")
        if pos > 0:
            r = re.compile("\d+")
            m = r.search(s)  # マッチしたらMatchObjectのインスタンスを返す
    return int(m.group(0))


def lights_config_reader(lights):
    u"""照明設定を読み込む"""
    reader = [[int(elm) for elm in v] for v in csv.reader(open(INIT.FILE_LIGHT, "r"))]
    for i, l in enumerate(reader):
        lights.append(Light())
        lights[i].pos_x = l[0]
        lights[i].pos_y = l[1]


def light_pattern_reader():
    u"""任意の点灯パターンファイルINIT.FILE_LIGHT_PATTERNを読込"""
    while True:
        try:
            pattern = [[int(elm) for elm in v] for v in csv.reader(open(INIT.FILE_LIGHT_PATTERN, "r"))]
            break
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

    return pattern


##########################
#         Light系         #
##########################
def influence_reader(lights):
    u"""照度光度影響度を読込"""
    reader = [ v for v in csv.reader(open(INIT.FILE_INFLUENCE, "r")) if len(v) != 0]
    reader.pop(0)

    for i, l in enumerate(lights):
        reader[i].pop(0)
        for s in range(len(reader[i])):
            l.influence.append(float(reader[i][s]))


##########################
#        Sensor系         #
##########################
def sensor_signal_reader(sensors):
    u"""実機のセンサ情報を読込"""
    while True:
        try:
            f = open(INIT.FILE_SENSOR_INFO, "r")
        except FileNotFoundError:
            print("can't find \"sensor.txt\" file")
        except PermissionError:
            pass

    line = f.readline()
    sigs = line.split(",")

    for i, s in enumerate(sensors):
        s.illuminance = sigs[i]


def sensor_target_reader(sensors):
    u"""センサの目標照度値を読込"""
    while True:
        try:
            f = open(INIT.FILE_SENSOR_TARGET, "r")
        except FileNotFoundError:
            print("can't find \"sensor.txt\" file")
        except PermissionError:
            pass

    line = f.readline()
    tgt = line.split(",")

    for i, s in enumerate(sensors):
        s.target = tgt[i]
        print(s.target)