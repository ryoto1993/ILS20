# coding: utf-8

from utils.manualChanger import *
from utils.dimmer import *
from utils.reader import *
from utils.simulation import *
from configure.config import *


class ANADB:
    u"""ANA/DBのアルゴリズムの実装"""

    def __init__(self, ils):
        self.step = 0
        self.ils = ils

        print("Set to ANA/DB")
        ANADB.start(self)

    def start(self):
        u"""ANA/DBの初期化部分"""
        # 各照明に照度/光度影響度（DB）を読み込む
        influence_reader(self.ils.lights)
        # 照明に初期光度の信号値を設定
        change_manually(self.ils.lights, INIT.ALG_INITIAL_SIGNAL)
        # 設定した信号値で点灯
        if INIT.SIMULATION:
            pass
        else:
            dimming(self.ils.lights)
        # 現在照度値を取得
        if INIT.SIMULATION:
            calc_illuminance(self.ils.lights, self.ils.sensors)
        else:
            sensor_signal_reader(self.ils.sensors)
        # 目標照度を取得
        sensor_target_reader(self.ils.sensors)

        for s in self.ils.sensors:
            print(s.illuminance)

    def next_step(self):
        self.step += 1
