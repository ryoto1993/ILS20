# coding: utf-8


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
