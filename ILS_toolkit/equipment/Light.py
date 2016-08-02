# coding:utf-8

from configure.config import *


class Light:
    u"""照明のオブジェクト"""
    id = 1

    def __init__(self):
        # 照明IDの設定
        self.id = Light.id
        Light.id += 1
        # 照明設置位置座標
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0
        # 照明属性
        self.minLum = 0.0  # 最小点灯光度
        self.maxLum = 0.0  # 最大点灯光度
        # 照度/光度影響度（ファイルから読み込んだもの）
        self.influence = []
        # ステータス
        self.isOn = True   # 照明のスイッチ
        self.signals = []  # 通常，暖色と寒色の2系統
        for s in range(len(INIT.LIGHT_SIGNAL_MAX)):
            self.signals.append(0)
        self.lumionosity = 0.0

    def __str__(self):
        return "Light" + str(self.id)