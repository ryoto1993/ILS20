# coding: utf-8

from equipment.Light import *
from equipment.Sensor import *
from equipment.PowerMeter import *
from utils.reader import *
from algorithm.ANAdb import *


class ILS:
    def __init__(self):
        # 照明，センサ，電力計を生成
        self.lights = []
        self.sensors = []
        self.powermeter = PowerMeter()
        self.algorithm = None

        # TODO:ロガーを生成，初期化

        # 照明の設定を読込
        lights_config_reader(self.lights)