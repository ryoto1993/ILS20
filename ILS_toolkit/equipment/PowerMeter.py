# coding: utf-8


class PowerMeter:
    u"""
    消費電力計のオブジェクト
    """
    def __init__(self, lights):
        self.lights = lights
        self.power = 0         # cd（光度値）の合計
        self.actual_power = 0  # ワット値


def calc_power(self):
    u"""
    照明の光度値を合計するメソッド
    消費電力は各照明の光度値の総和
    """
    power = 0.0
    actual = 0.0
    for l in self.lights:
        power += l.luminosity
        # y=0.4257x + 0.3716に基づいて計算
        actual += l.signals[0] * 0.4257 + 0.3716
    self.power = power
    self.actual_power = actual

    return int(power)