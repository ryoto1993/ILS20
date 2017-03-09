# coding: utf-8

import re
import csv

from configure.config import INIT
from equipment.Sensor import Sensor
from equipment.Light import Light
from equipment.OutsideLight import OutsideLight


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
    if INIT.MODE_CORRECT_SENSOR_DISPLACEMENT:
        correction = [[float(elm) for elm in v] for v in csv.reader(open(INIT.FILE_SENSOR_CORRECTION, "r"))]
    for i, s in enumerate(reader):
        sensors.append(Sensor())
        sensors[i].pos_x = s[0]
        sensors[i].pos_y = s[1]
        if not INIT.MODE_SIMULATION and INIT.MODE_CORRECT_SENSOR_DISPLACEMENT:
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


def update_config(ils):
    u"""
    ステップごとに目標照度と在離席を更新
    """
    # 目標照度を取得
    sensor_target_reader(ils.sensors)
    # 在離席を自動設定
    if INIT.MODE_AUTO_ATTENDANCE_SETTING:
        sensor_attendance_auto_setting(ils)
    # 在離席を取得
    if INIT.MODE_CHECK_ATTENDANCE:
        sensor_attendance_reader(ils.sensors)


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
        if INIT.MODE_CORRECT_SENSOR_DISPLACEMENT:
            s.illuminance = s.illuminance / s.correction_factor

        # 収束しているか否か
        if s.target*(100+INIT.ALG_ALLOWANCE_LOWER)/100 <= s.illuminance <= s.target+INIT.ALG_ALLOWANCE_UPPER:
            s.convergence = True
        else:
            s.convergence = False


def sensor_target_reader(sensors):
    u"""センサの目標照度および色温度を読込"""
    while True:
        try:
            f = open(INIT.FILE_SENSOR_TARGET, "r", encoding='utf-8')
            break
        except FileNotFoundError:
            print("can't find \"target.txt\" file.")
        except PermissionError:
            pass

    line = f.readline()
    tgt = line.split(",")

    # 色温度制御（MODE_TEMPERATURE）がTrueのとき
    if INIT.MODE_TEMPERATURE:
        line = f.readline()
        color_tgt = line.split(",")

    for i, s in enumerate(sensors):
        s.target = float(tgt[i])
        if INIT.MODE_TEMPERATURE:
            s.target_temperature = int(color_tgt[i])


def sensor_position_reader(sensors):
    u"""センサの座標を読み込み"""
    pass


def sensor_attendance_reader(sensors):
    u"""センサの在離席状態を読込"""
    while True:
        try:
            f = open(INIT.FILE_ATTENDANCE, "r")
            break
        except FileNotFoundError:
            print("can't find \"attendance.csv\" file.")
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
            print("Error. Please check \"attendance.csv\" format.")
            return


def sensor_attendance_auto_setting(ils):
    u"""センサの在離席を自動設定するメソッド"""
    data_steps = []
    data_sensor = []
    data_att = []
    indexes = []

    csv_reader = csv.reader(open(INIT.FILE_AUTO_ATTENDANCE, "r"), delimiter=",", quotechar='"')
    for row in csv_reader:
        data_steps.append(row[0])
        data_sensor.append(row[1])
        data_att.append(row[2])
    for i, stp in enumerate(data_steps):
        if stp == str(ils.algorithm.step):
            indexes.append(i)

    att_csv_reader = csv.reader(open(INIT.FILE_ATTENDANCE, "r"), delimiter=",", quotechar='"')
    data = []
    for row in att_csv_reader:
        data = row

    for i in indexes:
        data[int(data_sensor[i])-1] = 1 if data_att[i] == "1" else 0

    with open(INIT.FILE_ATTENDANCE, 'w') as f:
        writer = csv.writer(f, lineterminator='')
        writer.writerow(data)


def sensor_rank_reader(ils):
    u"""RANK法においてセンサのランク設定を読み込む"""
    reader = csv.reader(open(INIT.FILE_RANK, "r"), delimiter=",", quotechar='"')
    next(reader)

    for i, row in enumerate(reader):
        for l in range(len(ils.lights)):
            ils.sensors[i].rank.append(row[l+1])


##########################
#     Outside Light系     #
##########################
def read_outside_light_data():
    file = open(INIT.FILE_OUTSIDE_LIGHT, 'r')
    c = csv.reader(file)
    for row in c:
        OutsideLight.data.append(row)
    file.close()
