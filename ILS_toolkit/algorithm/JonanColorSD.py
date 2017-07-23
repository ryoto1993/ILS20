# coding: utf-8

from configure.config import INIT
from utils import reader, manualChanger, dimmer, logger, printer, simulation, signalConverter
from equipment.Sensor import update_sensors, update_temperature

import math


class JonanColorSD:
    u"""
    上南さん修論の方式

    色温度と照度に対する数理計画法．
    色温度から，電球色・白色それぞれの目標照度を算出し，
    それぞれの目標照度を独立した最適化問題として捉える手法．
    最適化手法には連続最適化問題の勾配法である最急降下法を用いる．
    """

    def __init__(self, ils):
        self.step = 0
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
        manualChanger.change_manually(self.ils.lights, INIT.ALG_INITIAL_SIGNALS)
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
        # 目標照度と色温度を取得
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
        self.step += 1
        # print("Step : " + str(self.step) + "  Start")
        # [1] 各照度センサと電力情報を取得
        # 現在照度値を取得（デバッグ用に，実センサから）
        update_sensors(self.ils)
        # 目標照度と色温度を取得
        reader.sensor_target_reader(self.ils.sensors)
        # 在離席を取得
        if INIT.MODE_CHECK_ATTENDANCE:
            reader.sensor_attendance_reader(self.ils.sensors)
        # 目標照度と色温度を基に，各色温度ごとの目標照度を求める
        self.split_illuminance_by_temperature()
        # 電力情報を計算
        self.ils.power_meter.calc_power()

        # [2] 最急降下法で最適な点灯列を探索
        # 反復数分，勾配ベクトルによる点灯列の更新を行う
        for sd_step in range(INIT.ALG_SD_STEP):
            # print("DEBUG : SD step " + str(sd_step))
            # <1> 各色温度ごとの目的関数を点灯列より算出する
            obj = [0.0, 0.0]  # 目的関数値
            pwr = [0.0, 0.0]  # 消費電力項
            err = [0.0, 0.0]  # 照度誤差項
            stop_flag = [False, False]
            for i in range(2):
                pwr[i] = sum(l.luminosities[i] for l in self.ils.lights)
                for s_i, s in enumerate(self.ils.sensors):
                    if s.attendance:
                        # センサの現在照度を計算する
                        ill = sum(l.luminosities[i]*l.influence[s_i] for l in self.ils.lights)
                        err[i] += (ill - s.divided_target[i])**2
                obj[i] = pwr[i] * INIT.ALG_SD_POWER_WEIGHT + err[i] * INIT.ALG_SD_ERROR_WEIGHT

            # <2> 各色温度ごとの勾配ベクトルを算出する
            grd_v = [[], []]
            for i in range(2):
                for l in self.ils.lights:
                    # 各照明ごとの勾配
                    grd_tmp = INIT.ALG_SD_POWER_WEIGHT
                    for s_i, s in enumerate(self.ils.sensors):
                        if s.attendance:
                            # ToDo: ここがなんでこうなるか，調べないと…
                            # grd_tmp += 2 * INIT.ALG_SD_ERROR_WEIGHT * l.influence[s_i] * (l.influence[s_i]*l.luminosities[i] - s.divided_target[i])
                            tmp = sum(al.influence[s_i]*al.luminosities[i] for al in self.ils.lights)
                            grd_tmp += 2 * INIT.ALG_SD_ERROR_WEIGHT * l.influence[s_i] * (tmp - s.divided_target[i])
                    grd_v[i].append(grd_tmp)

            # <3> 各色温度ごとの降下ベクトル（勾配ベクトルの逆ベクトル）のステップ幅（ノルム）を求める

            # <4> 点灯列を更新し，照度を更新する
            # 点灯列更新
            for l_s, l in enumerate(self.ils.lights):
                l.luminosities[0] -= grd_v[0][l_s] * 0.05
                l.luminosities[1] -= grd_v[1][l_s] * 0.05
                if l.luminosities[0] < 0:
                    l.luminosities[0] = 0
                if l.luminosities[1] < 0:
                    l.luminosities[1] = 0
                if l.luminosities[0] > INIT.LIGHT_LUMINOSITY_MAX[0]:
                    l.luminosities[0] = INIT.LIGHT_LUMINOSITY_MAX[0]
                if l.luminosities[1] > INIT.LIGHT_LUMINOSITY_MAX[1]:
                    l.luminosities[1] = INIT.LIGHT_LUMINOSITY_MAX[1]

            simulation.calc_illuminance_color_divided(self.ils)

        # [3] 探索した点灯列で照明を点灯
        signalConverter.convert_to_signal(self.ils.lights)
        # ToDo: これによって少し誤差が生じてしまう
        signalConverter.convert_to_luminosity(self.ils.lights)

        if INIT.MODE_SIMULATION:
            pass
        else:
            dimmer.dimming(self.ils.lights)

        # 現在照度値を取得（デバッグ用に，実センサから）
        update_sensors(self.ils)
        # 電力情報を計算
        self.ils.power_meter.calc_power()
        # 色温度を計算
        update_temperature(self.ils)
        # ログ追記
        self.ils.logger.append_all_log(self.step, False)
        if not INIT.MODE_SIMULATION:
            self.ils.printer.info()

    # 照度を各色の信号値の比から分離する
    def split_illuminance_by_temperature(self):
        # y = ax-2 + bx + c の係数
        # y: temperature, x: ratio of white
        a = 0.183
        b = 9.125
        c = 2689.3

        for s in self.ils.sensors:
            ratio = (-b + math.sqrt(b**2 - 4*a*(c-s.target_temperature))) / (2 * a)
            ratio /= 100.0
            s.divided_target[0] = s.target * ratio
            s.divided_target[1] = s.target * (1.0-ratio)