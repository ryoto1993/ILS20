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

    # 各照明ごとに次光度を決定する手順を実行
    for l in ils.lights:
        neighbor_design = NeighborDesign.default
        neighbor_type = NeighborType7.default

        # 各センサに対する照度光度影響度を取得
        influence = l.influence[:]

        # 離席してるセンサの影響度は0にする
        for s_i, s in enumerate(ils.sensors):
            if not s.attendance:
                influence[s_i] = 0.0

        # センサの距離でランク付けする
        for s_i, s in enumerate(ils.sensors):
            distance_rank = DistanceRank7
            comparing = Comparing

            if influence[s_i] > 0.21:
                distance = DistanceRank7.rank1
            elif influence[s_i] > 0.11:
                distance = DistanceRank7.rank2
            elif influence[s_i] > 0.05:
                distance = DistanceRank7.rank3
            else:
                distance = DistanceRank7.noRank


class NeighborType7(Enum):
    default = 0
    typeA = 1
    typeB = 2
    typeC = 3
    typeD = 4
    typeE = 5
    typeF = 6
    typeG = 7

    def __str__(self):
        if self == NeighborType7.typeA:
            return "TYPE A"
        elif self == NeighborType7.typeB:
            return "TYPE B"
        elif self == NeighborType7.typeC:
            return "TYPE C"
        elif self == NeighborType7.typeD:
            return "TYPE D"
        elif self == NeighborType7.typeE:
            return "TYPE E"
        elif self == NeighborType7.typeF:
            return "TYPE F"
        elif self == NeighborType7.typeG:
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


class DistanceRank7(Enum):
    default = 0
    rank1 = 1
    rank2 = 2
    rank3 = 3
    noRank = 10

    def __str__(self):
        if self == DistanceRank7:
            return "!default"
        elif self == DistanceRank7.rank1:
            return "RANK 1st"
        elif self == DistanceRank7.rank2:
            return "RANK 2nd"
        elif self == DistanceRank7.rank3:
            return "RANK 3rd"
        elif self == DistanceRank7.noRank:
            return "NO RANK"
