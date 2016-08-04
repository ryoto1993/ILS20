# coding: utf-8

from ILS import *
from utils.manualChanger import *
from utils.dimmer import *
from algorithm.ANAdb import *
import time


if __name__ == "__main__":
    u"""ILSの動作をコントロールするメインモジュール"""

    print("Intelligent Lighting System ver.20th")

    ils = ILS()

    while True:
        # state.txtから状態を取ってくるよ
        state = state_reader()

        # 消灯
        if state == 0:
            change_to_zero(ils.lights)
            dimming(ils.lights)
        # 点灯（fixed_pattern.csv）
        elif state == 1:
            change_to_fixed_pattern(ils.lights)
            dimming(ils.lights)
        # 最小点灯
        elif state == 2:
            change_to_min(ils.lights)
            dimming(ils.lights)
        # 最大点灯
        elif state == 3:
            change_to_max(ils.lights)
            dimming(ils.lights)
        # 知的照明システム一時停止
        elif state == 4:
            time.sleep(0.1)
            pass
        # SHC
        elif state == 5:
            pass
        # ANA/RC
        elif state == 6:
            pass

        # ANA/DB
        elif state == 7:
            if type(ils.algorithm) != ANADB:
                ils.algorithm = ANADB(ils)
            else:
                ils.algorithm.next_step()
        # ANA/RANK
        elif state == 8:
            pass
        # matrix探索
        elif state == 9:
            pass
        # 数理計画法
        elif state == 10:
            pass
