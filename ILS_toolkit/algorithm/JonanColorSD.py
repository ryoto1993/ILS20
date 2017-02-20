# coding: utf-8

from configure.config import INIT
from utils import reader, manualChanger, dimmer, logger, printer, simulation


class JonanColorSD:
    u"""
    上南さん修論の方式

    色温度と照度に対する数理計画法．
    色温度から，電球色・白色それぞれの目標照度を算出し，
    それぞれの目標照度を独立した最適化問題として捉える手法．
    最適化手法には連続最適化問題の勾配法である最急降下法を用いる．
    """

    def __init__(self, ils):
        self.step = 1
        self.ils = ils

        ils.algorithm = JonanColorSD

        print("Set to JonanColorSD")

        # 色温度制御が有効になってるかチェック
        if not INIT.MODE_TEMPERATURE:
            print("色温度制御（INIT.MODE_TEMPERATURE）を有効にしてください．")
            exit(10)

        JonanColorSD.start(self)

    def __str__(self):
        return u"JonanColorSD"

    def start(self):
        u"""初期化部分"""
        # 各照明に照度/光度影響度を読み込む
        reader.influence_reader(self.ils.lights)
        # 照明に初期光度の信号値を設定
        manualChanger.change_manually(self.ils.lights, INIT.ALG_INITIAL_SIGNAL_COLOR)
        # 設定した信号値で点灯
        if INIT.MODE_SIMULATION:
            pass
        else:
            dimmer.dimming(self.ils.lights)
        # 現在照度値を取得
        if INIT.MODE_SIMULATION:
            simulation.calc_illuminance(self.ils)
        else:
            reader.sensor_signal_reader(self.ils.sensors)
        # 目標照度を取得
        reader.sensor_target_reader(self.ils.sensors)
        # 在離席を取得
        if INIT.MODE_CHECK_ATTENDANCE:
            reader.sensor_attendance_reader(self.ils.sensors)
        # ロガー生成
        self.ils.logger = logger.Logger(self.ils)
        # プリンター生成（実環境時のみ）
        if not INIT.MODE_SIMULATION:
            self.ils.printer = printer.Printer(self.ils)
        # ログ追記
        self.ils.logger.append_all_log(0, False)
        if not INIT.MODE_SIMULATION:
            self.ils.printer.info()
        # 外光取得
        if INIT.MODE_ADD_OUTSIDE_LIGHT:
            reader.read_outside_light_data()


    def next_step(self):
        for sd_step in range(INIT.ALG_SD_STEP):
            print("DEBUG : SD step " + str(sd_step))
