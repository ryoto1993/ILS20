# coding: utf-8


class PowerMeter:
    u"""
    消費電力計のオブジェクト
    """
    def __init__(self, lights):
        self.lights = lights
        self.power = 0

    def calc_power(self):
        u"""
        照明の光度値を合計するメソッド
        消費電力は各照明の光度値の総和
        """
        power = 0.0
        for l in self.lights:
            power += l.luminosity
        self.power = power

        return int(power)
