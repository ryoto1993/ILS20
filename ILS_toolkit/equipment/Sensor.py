# coding: utf-8

from algorithm.ikedaNeightborDecision import DistanceRank7
from configure.config import *
from utils.simulation import *
from utils.reader import *


class Sensor:
    u"""照度センサのオブジェクト"""
    id = 1

    def __init__(self):
        # センサIDの設定
        self.id = Sensor.id
        Sensor.id += 1
        # センサ設置位置座標
        self.posX = 0.0
        self.posY = 0.0
        self.posZ = 0.0
        # ステータス
        self.attendance = True  # 在離席状態
        self.illuminance = 0.0  # 現在照度値
        self.target = 0.0       # 目標照度値
        self.convergence = False
        # Sekonic補正率
        self.correction_factor = 0.0
        # ランクぎめの一時変数
        self.tmp_rank = DistanceRank7.default

    def __str__(self):
        return "Sensor" + str(self.id)


def update_sensors(ils):
    if INIT.SIMULATION:
        calc_illuminance(ils)
    else:
        sensor_signal_reader(ils.sensors)
