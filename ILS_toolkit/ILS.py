# coding: utf-8

from equipment.PowerMeter import *
from utils.reader import *
from algorithm.ANAdb import *
from utils.logger import *


class ILS:
    def __init__(self):
        # 照明，センサ，電力計を生成
        self.lights = []
        self.sensors = []
        self.power_meter = PowerMeter(self.lights)
        self.algorithm = None
        self.logger = None
        self.printer = None

        # 照明の設定を読込
        lights_config_reader(self.lights)
        # センサの設定を読込
        sensors_config_reader(self.sensors)
