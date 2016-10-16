# coding: utf-8

from configure.config import INIT
from utils import reader, manualChanger, dimmer, simulation
from utils.logger import Logger
from utils.printer import Printer
from equipment.Sensor import update_sensors
from algorithm.algorithmCommon import calc_objective_function_rank
from algorithm.ikedaNeightborDecisionRank import decide_next_luminosity_ikeda7_rank


class ANARANK:
    u"""
    ANA/DBのアルゴリズムの実装

    ステップ数は光度値を変動させるごとに1ステップとカウントする．
    すなわち，ANA/DBでは一回のループで2ステップになる．
    """

    def __init__(self, ils):
        self.step = 1
        self.ils = ils

        print("Set to ANA/RANK")
        ANARANK.start(self)

    def __str__(self):
        return u"ANA/RANK"

    def start(self):
        u"""ANA/DBの初期化部分"""
        # ランクを読み込む
        reader.sensor_rank_reader(self.ils)
        # 各照明に照度/光度影響度（DB）を読み込む
        reader.influence_reader(self.ils.lights)
        # 照明に初期光度の信号値を設定
        manualChanger.change_manually(self.ils.lights, INIT.ALG_INITIAL_SIGNAL)
        # 設定した信号値で点灯
        if INIT.SIMULATION:
            pass
        else:
            dimmer.dimming(self.ils.lights)
        # 現在照度値を取得
        if INIT.SIMULATION:
            simulation.calc_illuminance(self.ils)
        else:
            reader.sensor_signal_reader(self.ils.sensors)
        # 目標照度を取得
        reader.sensor_target_reader(self.ils.sensors)
        # 在離席を取得
        if INIT.CHECK_ATTENDANCE:
            reader.sensor_attendance_reader(self.ils.sensors)
        # ロガー生成
        self.ils.logger = Logger(self.ils)
        # プリンター生成（実環境時のみ）
        if not INIT.SIMULATION:
            self.ils.printer = Printer(self.ils)
        # ログ追記
        self.ils.logger.append_all_log(0, False)
        if not INIT.SIMULATION:
            self.ils.printer.info()
        # 外光取得
        if INIT.ADD_OUTSIDE_LIGHT:
            reader.read_outside_light_data()

    def next_step(self):
        u"""この部分がANA/DBのループ"""
        reader.update_config(self.ils)

        # [1] 各照度センサと電力情報を取得
        # 現在照度値を取得
        update_sensors(self.ils)
        # 電力情報を計算
        self.ils.power_meter.calc_power()

        # [2] 目的関数を計算する
        calc_objective_function_rank(self.ils, False)

        # ログ追記
        self.ils.logger.append_all_log(self.step, False)
        if not INIT.SIMULATION:
            self.ils.printer.info()

        # [3] 次の光度値を決定し，点灯
        # 次光度決定
        # decide_next_luminosity(self.ils)
        # decide_next_luminosity_ikeda7(self.ils)
        decide_next_luminosity_ikeda7_rank(self.ils)
        # 次光度で点灯
        if INIT.SIMULATION:
            pass
        else:
            dimmer.dimming(self.ils.lights)
        self.step += 1

        if self.step % 100 == 0:
            print("Step " + str(self.step))

        # [4] 各照度センサと電力情報を取得
        # 現在照度値を取得
        update_sensors(self.ils)
        # 電力情報を計算
        self.ils.power_meter.calc_power()

        # [5] 光度変化後の目的関数を計算
        calc_objective_function_rank(self.ils, True)

        # ログ追記
        self.ils.logger.append_all_log(self.step, True)
        if not INIT.SIMULATION:
            self.ils.printer.info()

        # [6] 目的関数が悪化していたら光度変化をキャンセル
        for l in self.ils.lights:
            if l.next_objective_function >= l.objective_function:
                l.luminosity = l.previous_luminosity
        # 判断後の光度値で点灯
        if INIT.SIMULATION:
            pass
        else:
            dimmer.dimming(self.ils.lights)
        self.step += 1

        if self.step % 100 == 0:
            print("Step " + str(self.step))
