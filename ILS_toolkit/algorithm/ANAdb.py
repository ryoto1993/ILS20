# coding: utf-8

from utils.manualChanger import *
from utils.dimmer import *
from utils.reader import *
from configure.config import *


class ANADB:
    u"""ANA/DBのアルゴリズムの実装"""

    def __init__(self, ils):
        self.step = 0
        self.ils = ils

        influence_reader(self.ils.lights)

        print("Set to ANA/DB")
        ANADB.start(self)

    def start(self):
        u"""ANA/RCの初期化部分"""
        # 照明に初期光度の信号値を設定
        change_manually(self.ils.lights, INIT.ALG_INITIAL_SIGNAL)
        # 設定した信号値で点灯
        dimming(self.ils.lights)

    def next_step(self):
        self.step += 1
