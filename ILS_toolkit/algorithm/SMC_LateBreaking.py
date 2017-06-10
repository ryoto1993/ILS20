# coding: utf-8

from configure.config import INIT
from utils import reader, dimmer, manualChanger, simulation
from utils.logger import Logger
from utils.printer import Printer
from equipment.Sensor import update_sensors
from algorithm.algorithmCommon import calc_objective_function_influence
from algorithm.algorithmCommon import decide_next_luminosity_3type

import math
import csv
import os
import datetime


class SMCLB:
    u"""
    SMC LateBreakingに向けた進捗用
    ANA/DBで調光した後、ランダムに1灯選んで配光角を5度ずつ下げる方式
    """

    flux = 2000
    height = 1850

    def __init__(self, ils):
        self.step = 1
        self.ils = ils

        ils.algorithm = SMCLB

        print("Set to SMCLB")

        INIT.FILE_INFLUENCE = u"./experiments/smclb_active_influence.csv"
        INIT.DIR_LOG = u"../LOG_SMCLB/"
        time = datetime.datetime.today()
        self.y = str(time.year)
        self.m = str(time.month).zfill(2)
        self.d = str(time.day).zfill(2)
        self.hr = str(time.hour).zfill(2)
        self.mi = str(time.minute).zfill(2)
        self.sc = str(time.second).zfill(2)
        self.path = INIT.DIR_LOG + self.y + self.m + self.d + "_" + self.hr + self.mi + self.sc
        os.mkdir(self.path)

        # すべての照明を45度にして影響度作成
        SMCLB.make_coefficient(self)

        # ANA/DB開始(100steps)
        SMCLB.ana_start(self)

    def __str__(self):
        return u"ANA/DB"

    def ana_start(self):
        # 動的影響度を読み込み
        INIT.FILE_INFLUENCE = u"./experiments/smclb_active_influence.csv"

        u"""ANA/DBの初期化部分"""
        # 各照明に照度/光度影響度（DB）を読み込む
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
        # 目標照度を取得
        reader.sensor_target_reader(self.ils.sensors)
        # 在離席を取得
        if INIT.MODE_CHECK_ATTENDANCE:
            reader.sensor_attendance_reader(self.ils.sensors)
        # ロガー生成
        # self.ils.logger = Logger(self.ils)
        # プリンター生成（実環境時のみ）
        if not INIT.MODE_SIMULATION:
            self.ils.printer = Printer(self.ils)
        # ログ追記
        # self.ils.logger.append_all_log(0, False)
        # if not INIT.MODE_SIMULATION:
        #     self.ils.printer.info()
        # 外光取得
        if INIT.MODE_ADD_OUTSIDE_LIGHT:
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
        calc_objective_function_influence(self.ils, False)

        # ログ追記
        self.ils.logger.append_all_log(self.step, False)
        if not INIT.MODE_SIMULATION:
            self.ils.printer.info()

        # [3] 次の光度値を決定し，点灯
        # 次光度決定
        decide_next_luminosity_3type(self.ils)
        # decide_next_luminosity_ikeda7(self.ils)
        # 次光度で点灯
        if INIT.MODE_SIMULATION:
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
        calc_objective_function_influence(self.ils, True)

        # ログ追記
        self.ils.logger.append_all_log(self.step, True)
        if not INIT.MODE_SIMULATION:
            self.ils.printer.info()

        # [6] 目的関数が悪化していたら光度変化をキャンセル
        for l in self.ils.lights:
            if l.next_objective_function >= l.objective_function:
                l.luminosities[0] = l.previous_luminosity
        # 判断後の光度値で点灯
        if INIT.MODE_SIMULATION:
            pass
        else:
            dimmer.dimming(self.ils.lights)
        self.step += 1

        if self.step % 100 == 0:
            print("Step " + str(self.step))

    # 照明配光角に基づいて照度/光度影響度係数を作成
    def make_coefficient(self):
        f = open(INIT.FILE_INFLUENCE, 'w')
        writer = csv.writer(f, lineterminator='\n')

        lights = [[int(elm) for elm in v] for v in csv.reader(open(INIT.FILE_LIGHT, "r"))]
        sensors = [[int(elm) for elm in v] for v in csv.reader(open(INIT.FILE_SENSOR, "r"))]

        # ライト読み込みとヘッダ記述
        tmp = [""]
        for i in range(0, len(lights)):
            tmp.append("Light" + str(i+1))
        writer.writerow(tmp)

        # センサ読み込みと影響度計算
        for i, s in enumerate(sensors):
            tmp.clear()
            tmp.append("Sensor" + str(i+1))
            for l_i, l in enumerate(lights):
                tmp.append(str(self.solve_coefficient(self.dist(s, l), l_i)))
            writer.writerow(tmp)
        f.close()

    # 距離から影響度を算出するメソッド
    def solve_coefficient(self, dist, l_i):
        # 直下1mの照度=光度を計算
        luminance = self.flux

        # 測光点の水平面照度を計算
        rdegree = math.atan(float(dist) / float(self.height))
        degree = math.degrees(rdegree)
        # 配光曲線のその角度の値
        raw = (0.5 + 0.5*math.cos(math.pi/2/math.radians(self.ils.lights[l_i].beamSpread)*rdegree)) * self.flux
        illuminance = raw / ((dist/1000)**2 + (self.height/1000)**2) * math.cos(rdegree)

        # 照度/光度影響度を計算
        inf = illuminance/luminance
        return inf if inf > 0.001 else 0.0

    def dist(self, p1, p2):
        p1x = float(p1[0])
        p1y = float(p1[1])
        p2x = float(p2[0])
        p2y = float(p2[1])

        d = (p1x-p2x)**2 + (p1y-p2y)**2
        dist = math.sqrt(d)

        return dist
