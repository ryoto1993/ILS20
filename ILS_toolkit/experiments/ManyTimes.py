# coding: utf-8

from ILS import ILS
from equipment.Sensor import Sensor
from equipment.Light import Light
from configure.config import INIT
from algorithm.ANAdb import ANADB
from algorithm.JonanColorSD import JonanColorSD
from utils.logger import Logger

import os
import codecs
import random

##################################################
# 対向島型12席のレイアウト(island12)専用！
##################################################

# ################### #
#       実験用設定      #
# ################### #
time = 30        # <- 何回ILSを回すか
loop = 4        # <- ステップ数ではなくループ数，400とすると800ステップになる
name = u"DL_CLR_FIX_26_60"
mode = "COLOR"    # "COLOR": 二系統分離数理計画 "DB": ANA/DB
ifix = True       # 照度を500lxに固定する


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
        # ロガーのパスを強制変更
        Logger.PATH = str(t+1)

        # アルゴリズム指定
        if mode == "DB":
            ils.algorithm = ANADB(ils)
        elif mode == "COLOR":
            ils.algorithm = JonanColorSD(ils)

        for l in range(loop):
            ils.algorithm.next_step()


# ManyTimes用にconfigの設定をoverwrite
def force_setting():
    INIT.MODE_SIMULATION = True
    INIT.MODE_CHECK_ATTENDANCE = False  # <- このプログラム内で切り替えるためOFFに！
    INIT.MODE_AUTO_ATTENDANCE_SETTING = False


def set_random_target():
    # リストをシャッフル
    officer = [x for x in range(12)]
    random.shuffle(officer)

    line = u""
    c_line = u""

    # 300, 500, 700lx を以下の割合で設定
    for i in range(12):
        if officer[i] == 0 or officer[i] == 1:
            line += u"300,"
        elif officer[i] == 2 or officer[i] == 3:
            line += u"700,"
        else:
            line += u"500,"

    if ifix:
        line = u"500,500,500,500,500,500,500,500,500,500,500,500,"

    # 色温度が有効の場合は3000K~5500Kの範囲でランダムに割り当てる
    if mode == "COLOR":
        random.shuffle(officer)
        for i in range(12):
            if officer[i] % 6 == 0:
                c_line += u"3000,"
            elif officer[i] % 6 == 1:
                c_line += u"3500,"
            elif officer[i] % 6 == 2:
                c_line += u"4000,"
            elif officer[i] % 6 == 3:
                c_line += u"4500,"
            elif officer[i] % 6 == 4:
                c_line += u"5000,"
            elif officer[i] % 6 == 5:
                c_line += u"4000,"

    # target.txtに書き込み
    f = codecs.open(INIT.FILE_SENSOR_TARGET, "w", "utf-8")
    f.write(line)
    if mode == "COLOR":
        f.write("\n")
        f.write(c_line)
    f.close()

    print(line)
