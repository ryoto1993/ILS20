# coding:utf-8

from configure.config import INIT


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
        self.minLum = 0.0     # 最小点灯光度
        self.maxLum = 0.0     # 最大点灯光度
        self.beamSpread = 25  # 1/2ビーム角
        # 照度/光度影響度（ファイルから読み込んだもの）
        self.influence = []
        # ステータス
        self.isOn = True   # 照明のスイッチ
        self.signals = [0, 0]  # 通常，暖色と寒色の2系統
        self.luminosities = [0.0, 0.0]  # 現在光度
        self.temperature = 0    # 照明の現在色温度
        self.next_luminosity = 0.0
        self.previous_luminosity = 0.0  # 前の光度
        # 分散制御アルゴリズム用目的関数
        self.objective_function = 0.0  # 目的関数
        self.next_objective_function = 0.0  # 光度変化後の目的関数
        self.objective_penalty = 0.0  # 目的関数のペナルティ部分
        self.next_objective_penalty = 0.0  # 光度変化後の目的関数のペナルティ部分
        # プリンターとログ用
        self.neighbor = ""

    def __str__(self):
        return "Light" + str(self.id)
