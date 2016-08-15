# coding: utf-8

from ILS import *
from algorithm.algorithmCommon import *


class Printer:
    def __init__(self, ils):
        self.ils = ils

        print("Printer created.")

    def info(self):
        print("========================================================================")
        print("Step : " + str(self.ils.algorithm.step) + "  (ALG Step : " + str(self.ils.algorithm.step / 2) + ")")
        print("----- Light ------------------------------------------------------------")
        print("ID │ Lum. │ Sig │ Neighbor │ ")
        for l in self.ils.lights:
            print('{0:2d}'.format(l.id) + " │ " + '{0:4.0f}'.format(l.luminosity) + " │ " + '{0:3d}'.format(l.signals[0]) + " │ ")