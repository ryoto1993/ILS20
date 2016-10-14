# coding: utf-8

from algorithm.ikedaNeightborDecision import DistanceRank7
from utils.simulation import *
from equipment.OutsideLight import *
import utils.reader


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
        # ランク法のランク
        self.rank = []

    def __str__(self):
        return "Sensor" + str(self.id)


def update_sensors(ils):
    if INIT.SIMULATION:
        calc_illuminance(ils)
    else:
        utils.reader.sensor_signal_reader(ils.sensors)

    # 外光データの外光照度を加算
    if INIT.ADD_OUTSIDE_LIGHT and ils.algorithm:
        data_line = int(1 + INIT.EXT_START_LINE + ils.algorithm.step * INIT.EXT_STEP_SECOND)
        for s in ils.sensors:
            s.illuminance += int(OutsideLight.data[data_line][s.id])
