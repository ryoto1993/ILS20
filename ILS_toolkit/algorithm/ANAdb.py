# coding: utf-8

from utils.manualChanger import *
from utils.dimmer import *
from utils.reader import *
from utils.simulation import *
from algorithm.algorithmCommon import *


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

    def next_step(self):
        u"""この部分がANA/RCのループ"""
        self.step += 1

        # [1] 各照度センサと電力情報を取得
        # 現在照度値を取得
        if INIT.SIMULATION:
            calc_illuminance(self.ils.lights, self.ils.sensors)
        else:
            sensor_signal_reader(self.ils.sensors)
        # 電力情報を計算
        self.ils.powermeter.calc_power()

        # [2] 目的関数を計算する
        calc_objective_function(self.ils)

        for l in self.ils.lights:
            print(l.id)
            print(l.objective_function)

        for s in self.ils.sensors:
            print(s.id)
            print(s.illuminance)
