# coding:utf-8


class Light:
    u"""照明のオブジェクト"""
    def __init__(self):
        # 照明設置位置座標
        self.posX = 0.0
        self.posY = 0.0
        self.posZ = 0.0
        # 照明属性
        self.minLum = 0.0  # 最小点灯光度
        self.maxLum = 0.0  # 最大点灯光度
        # ステータス
        self.isOn = True  # 照明のスイッチ
