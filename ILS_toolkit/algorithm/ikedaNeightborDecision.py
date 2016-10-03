# coding: utf-8

from utils.manualChanger import *
from configure.config import *
from enum import Enum
from algorithm.algorithmCommon import *
import random


def decide_next_luminosity_ikeda7(ils):
    """
    池田さんの修論で使われている7近傍の方式です
    :param ils: 知的照明システムのオブジェクト
    :return: None
    """


class NeighborType(Enum):
    default = 0
    typeA = 1
    typeB = 2
    typeC = 3
    typeD = 4
    typeE = 5
    typeF = 6
    typeG = 7

    def __str__(self):
        if self == NeighborType.typeA:
            return "TYPE A"
        elif self == NeighborType.typeB:
            return "TYPE B"
        elif self == NeighborType.typeC:
            return "TYPE C"
        elif self == NeighborType.typeD:
            return "TYPE D"
        elif self == NeighborType.typeE:
            return "TYPE E"
        elif self == NeighborType.typeF:
            return "TYPE F"
        elif self == NeighborType.typeG:
            return "TYPE G"


class NeighborDesign(Enum):
    default = 0
    design1 = 1
    design2 = 2
    design3 = 3
    design4 = 4
    design5 = 5
    design6 = 6

    def __str__(self):
        if self == NeighborDesign.design1:
            return "DESIGN 1"
        elif self == NeighborDesign.design2:
            return "DESIGN 2"
        elif self == NeighborDesign.design3:
            return "DESIGN 3"
        elif self == NeighborDesign.design4:
            return "DESIGN 4"
        elif self == NeighborDesign.design5:
            return "DESIGN 5"
        elif self == NeighborDesign.design6:
            return "DESIGN 6"
