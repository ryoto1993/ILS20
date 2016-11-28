# coding: utf-8

from ILS import ILS

from algorithm.ANArank import ANARANK
from equipment.Sensor import Sensor
from equipment.Light import Light

########################################
#        EXPERIMENTS CONFIGURE         #
TRY = 300   # Time of trial            #
LOP = 600   # Num of loop in one trial #
AVR = 6    # converged phase range    #
########################################


def start():
    print("Calculate target growth rate mode")

    for t in range(TRY):
        # センサ番号と照明番号のリセット（ログ用）
        Sensor.id = 1
        Light.id = 1
        # ILS初期化
        ils = ILS()
        # 実現数カウンタを作成
        achieve = []
        for s in ils.sensors:
            achieve.append(0)
        # アルゴリズム設定
        ils.algorithm = ANARANK(ils)
        # 指定回数ループを回す
        for l in range(LOP):
            ils.algorithm.next_step()
            if l > LOP-AVR:
                print(l)
                for s in ils.sensors:
                    achieve.append(0)
