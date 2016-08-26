# coding: utf-8

import re
import csv

from equipment.Light import *
from equipment.Sensor import *


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


def sensors_config_reader(sensors):
    u"""センサ設定を読み込む"""
    reader = [[int(elm) for elm in v] for v in csv.reader(open(INIT.FILE_SENSOR, "r"))]
    if INIT.CORRECT_SENSOR_DISPLACEMENT:
        correction = [[float(elm) for elm in v] for v in csv.reader(open(INIT.FILE_SENSOR_CORRECTION, "r"))]
    for i, s in enumerate(reader):
        sensors.append(Sensor())
        sensors[i].pos_x = s[0]
        sensors[i].pos_y = s[1]
        if not INIT.SIMULATION and INIT.CORRECT_SENSOR_DISPLACEMENT:
            sensors[i].correction_factor = correction[i][0]


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
    reader = [v for v in csv.reader(open(INIT.FILE_INFLUENCE, "r")) if len(v) != 0]
    reader.pop(0)

    for s in range(len(reader)):
        reader[s].pop(0)
        for l_i, l in enumerate(lights):
            l.influence.append(float(reader[s][l_i]))


##########################
#        Sensor系         #
##########################
def sensor_signal_reader(sensors):
    u"""実機のセンサ情報を読込"""
    while True:
        try:
            f = open(INIT.FILE_SENSOR_INFO, "r")
            line = f.readline()
            if not line == "":
                break
        except FileNotFoundError:
            print("can't find \"sensor.txt\" file.")
        except PermissionError:
            pass

    sigs = line.split(",")

    for i, s in enumerate(sensors):
        s.illuminance = int(sigs[i])
        if INIT.CORRECT_SENSOR_DISPLACEMENT:
            print("補正前:" + str(s.illuminance))
            s.illuminance = s.illuminance / s.correction_factor
            print("補正後:" + str(s.illuminance))

        # 収束しているか否か
        if s.target*(1+INIT.ALG_ALLOWANCE_LOWER/100) <= s.illuminance <= s.target*(1+INIT.ALG_ALLOWANCE_UPPER/100):
            s.convergence = True
        else:
            s.convergence = False


def sensor_target_reader(sensors):
    u"""センサの目標照度値を読込"""
    while True:
        try:
            f = open(INIT.FILE_SENSOR_TARGET, "r")
            break
        except FileNotFoundError:
            print("can't find \"target.txt\" file.")
        except PermissionError:
            pass

    line = f.readline()
    tgt = line.split(",")

    for i, s in enumerate(sensors):
        s.target = float(tgt[i])


def sensor_attendance_reader(sensors):
    u"""センサの在離席状態を読込"""
    while True:
        try:
            f = open(INIT.FILE_ATTENDANCE, "r")
            break
        except FileNotFoundError:
            print("can't find \"attendance.txt\" file.")
        except PermissionError:
            pass

    line = f.readline()
    tgt = line.split(",")

    for i, s in enumerate(sensors):
        if tgt[i] == "1":
            s.attendance = True
        elif tgt[i] == "0":
            s.attendance = False
        else:
            print("Error. Please check \"attendance.txt\" format.")
            return
