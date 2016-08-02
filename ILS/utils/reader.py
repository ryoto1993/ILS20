# coding: utf-8

import re
import csv

from equipment.Light import *


def state_reader():
    u"""ステータスファイルを読み込む"""
    while True:
        try:
            f = open(INIT.STATE_FILE, 'r', encoding='utf-8')
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
    reader = [[int(elm) for elm in v] for v in csv.reader(open(INIT.LIGHT_FILE, "r"))]
    for i, l in enumerate(reader):
        lights.append(Light())
        lights[i].pos_x = l[0]
        lights[i].pos_y = l[1]


def light_pattern_reader():
    while True:
        try:
            pattern = [[int(elm) for elm in v] for v in csv.reader(open(INIT.LIGHT_PATTERN_FILE, "r"))]
            break
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

    return pattern