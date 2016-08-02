# coding: utf-8


class Sensor:
    u"""照度センサのオブジェクト"""
    def __init__(self):
        # センサ設置位置座標
        self.posX = 0.0
        self.posY = 0.0
        self.posZ = 0.0
        # ステータス
        self.attend = True  # 在離席状態
