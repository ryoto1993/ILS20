# coding: utf-8

from utils.manualChanger import *
from utils.dimmer import *
from utils.reader import *
from utils.simulation import *
from algorithm.algorithmCommon import *


class ANADB:
    u"""
    ANA/DBのアルゴリズムの実装

    ステップ数は光度値を変動させるごとに1ステップとカウントする．
    すなわち，ANA/DBでは一回のループで2ステップになる．
    """

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
        # 在離席を取得
        if INIT.CHECK_ATTENDANCE:
            sensor_attendance_reader(self.ils.sensors)

    def next_step(self):
        u"""この部分がANA/RCのループ"""
        self.step += 1
        self.update_config()

        print(self.step)

        # [1] 各照度センサと電力情報を取得
        # 現在照度値を取得
        if INIT.SIMULATION:
            calc_illuminance(self.ils.lights, self.ils.sensors)
        else:
            sensor_signal_reader(self.ils.sensors)
        # 電力情報を計算
        self.ils.power_meter.calc_power()

        # [2] 目的関数を計算する
        calc_objective_function_influence(self.ils, False)

        # [3] 次の光度値を決定し，点灯
        # 次光度決定
        decide_next_luminosity_influence(self.ils)
        # 次光度で点灯
        if INIT.SIMULATION:
            pass
        else:
            dimming(self.ils.lights)

        # [4] 各照度センサと電力情報を取得
        # 現在照度値を取得
        if INIT.SIMULATION:
            calc_illuminance(self.ils.lights, self.ils.sensors)
        else:
            sensor_signal_reader(self.ils.sensors)
        # 電力情報を計算
        self.ils.power_meter.calc_power()

        # [5] 光度変化後の目的関数を計算
        calc_objective_function_influence(self.ils, True)

        # [6] 目的関数が悪化していたら光度変化をキャンセル
        for l in self.ils.lights:
            if l.next_objective_function >= l.objective_function:
                l.luminosity = l.previous_luminosity
        # 判断後の光度値で点灯
        self.step += 1
        if INIT.SIMULATION:
            pass
        else:
            dimming(self.ils.lights)

        for s in self.ils.sensors:
            print(s.illuminance)
        for l in self.ils.lights:
            print(l.signals[0])

    def update_config(self):
        u"""
        ステップごとに目標照度と在離席を更新
        """
        # 目標照度を取得
        sensor_target_reader(self.ils.sensors)
        # 在離席を取得
        if INIT.CHECK_ATTENDANCE:
            sensor_attendance_reader(self.ils.sensors)
