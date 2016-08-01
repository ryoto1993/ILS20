# coding: utf-8

from utils.reader import *
from utils.dimmer import *
from equipment.Light import *

if __name__ == "__main__":
    print("Intelligent Lighting System ver.20th")

    lights = []
    for i in range(12):
        lights.append(Light())

    dimming(lights)

    while True:
        # state.txtから状態を取ってくるよ
        state = state_reader()

        # 消灯
        if state == 0:
            pass
        # 点灯（fixed_pattern.csv）
        elif state == 1:
            pass
        # 最小点灯
        elif state == 2:
            pass
        # 最大点灯
        elif state == 3:
            pass
        # 知的照明システム一時停止
        elif state == 4:
            pass

        # SHC
        elif state == 5:
            pass
        # ANA/RC
        elif state == 6:
            pass
        # ANA/DB
        elif state == 7:
            pass
        # ANA/RANK
        elif state == 8:
            pass
        # matrix探索
        elif state == 9:
            pass
        # 数理計画法
        elif state == 10:
            pass
