# coding: utf-8


class ANADB:
    u"""ANA/DBのアルゴリズムの実装"""

    def __init__(self, ils):
        self.step = 0
        self.ils = ils

        print("Set to ANA/DB")

    def next_step(self):
        self.step += 1
