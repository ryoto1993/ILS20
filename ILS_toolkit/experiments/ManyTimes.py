# coding: utf-8

from ILS import ILS
from equipment.Sensor import Sensor
from equipment.Light import Light
from configure.config import INIT
from algorithm.ANAdb import ANADB

import os
import codecs
import random

##################################################
# 対向島型12席のレイアウト(island12)専用！
##################################################

# ################### #
#       実験用設定      #
# ################### #
time = 100        # <- 何回ILSを回すか
loop = 400        # <- ステップ数ではなくループ数，400とすると800ステップになる
name = u"M110_180F"


def start():
    print("ManyTimes start!")

    # config固定
    force_setting()
    # ログのパスを変える
    os.mkdir("../LOG/ManyTimes_" + name)
    INIT.DIR_LOG = "../LOG/ManyTimes_" + name + "/"

    for t in range(time):
        print("Time >>>>> " + str(t+1))
        set_random_target()
        # センサ番号と照明番号のリセット（ログ用）
        Sensor.id = 1
        Light.id = 1
        # ILS初期化
        ils = ILS()
        ils.algorithm = ANADB(ils)

        for l in range(loop):
            ils.algorithm.next_step()


def force_setting():
    INIT.MODE_SIMULATION = True
    INIT.MODE_CHECK_ATTENDANCE = False  # <- このプログラム内で切り替えるためOFFに！
    INIT.MODE_AUTO_ATTENDANCE_SETTING = False


def set_random_target():
    # リストをシャッフル
    officer = [x for x in range(12)]
    random.shuffle(officer)

    line = u""

    for i in range(12):
        if officer[i] == 0 or officer[i] == 1:
            line += u"300,"
        elif officer[i] == 2 or officer[i] == 3:
            line += u"700,"
        else:
            line += u"500,"

    f = codecs.open(INIT.FILE_SENSOR_TARGET, "w", "utf-8")
    f.write(line)
    f.close()

    print(line)
