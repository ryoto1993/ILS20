# coding: utf-8


class PowerMeter:
    u"""消費電力計のオブジェクト"""
    def __init__(self, lights):
        self.lights = lights

    def calc_power(self):
        u"""照明の光度値を合計するメソッド"""
        power = 0
        for l in self.lights:
            power += l.luminosity
        return power