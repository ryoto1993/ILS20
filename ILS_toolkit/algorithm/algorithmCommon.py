# coding: utf-8

from utils.manualChanger import *
from configure.config import *
from enum import Enum
import random


def calc_objective_function_influence(ils, next_flag):
    u"""
    全照明の目的関数を計算するメソッド
    ANA/RC, ANA/DBなど，照度/光度影響度を使うアルゴリズムに適応

    ★ペナルティ項のポリシー★
    まず，照明とセンサが近接しているかを照度光度影響度で判断する．
    閾値はINIT.ALG_RC_THRESHOLDで設定可能．
    近接している場合…
    ・現在照度が目標照度を上回っている場合
    　　→ 目標照度の6%（最小知覚変動比）以上の場合に計上
    ・現在照度が目標照度に達していない場合
    　　→ 無条件に計上

    :param ILS ils: ILS を引数に渡す
    :param boolean next_flag: 次光度の目的関数を計算するかどうか
    """
    # ペナルティ項にかかる重み
    w = INIT.ALG_WEIGHT

    # 各照明ごとに目的関数を計算
    for l in ils.lights:
        obj = ils.power_meter.power
        penalty = 0.0

        for s_i, s in enumerate(ils.sensors):
            # 照度光度影響度数を取得
            r = l.influence[s_i]
            # r = r if r >= INIT.ALG_DB_THRESHOLD else 0.0
            r = r if s.attendance else 0.0  # 離席してる場合はペナルティ無し
            r = r if not (s.target*(1+INIT.ALG_ALLOWANCE_LOWER/100) <= s.illuminance <= s.target+INIT.ALG_ALLOWANCE_UPPER) else 0.0
            # ペナルティ関数を計算
            penalty += w * r * (s.illuminance - s.target)**2

        obj += penalty

        if next_flag:
            l.next_objective_function = obj
            l.next_objective_penalty = penalty
        else:
            l.objective_function = obj
            l.objective_penalty = penalty


def decide_next_luminosity(ils):
    # 各照明ごとに次光度を決定
    for l in ils.lights:
        neighbor = NeighborType.default

        # センサに対する照度/光度影響度を降順にした時のインデックス番号
        influence = l.influence[:]

        # 離席してるセンサの影響度は0にする
        for s_i, s in enumerate(ils.sensors):
            if not s.attendance:
                influence[s_i] = 0.0

        # センサの距離をチェックする
        for s_i, s in enumerate(ils.sensors):
            distance = Distance
            comparing = Comparing

            if influence[s_i] > 0.17:
                distance = Distance.near
            elif influence[s_i] > 0.07:
                distance = Distance.middle
            else:
                distance = Distance.distant

            # チェックしたセンサが目標照度実現してるかチェック
            if s.illuminance < s.target * (100.0 + INIT.ALG_ALLOWANCE_LOWER) / 100.0:
                comparing = Comparing.dimmer
            elif s.illuminance < s.target + INIT.ALG_ALLOWANCE_UPPER:
                comparing = Comparing.converged
            else:
                comparing = Comparing.brighter

            tmp_neighbor = NeighborType
            # neighborを決定
            if distance == Distance.near:
                if comparing == Comparing.brighter:
                    tmp_neighbor = NeighborType.neutral
                elif comparing == Comparing.converged:
                    tmp_neighbor = NeighborType.neutral
                elif comparing == Comparing.dimmer:
                    tmp_neighbor = NeighborType.brightening
            elif distance == Distance.middle:
                if comparing == Comparing.brighter:
                    tmp_neighbor = NeighborType.neutral
                elif comparing == Comparing.converged:
                    tmp_neighbor = NeighborType.neutral
                elif comparing == Comparing.dimmer:
                    tmp_neighbor = NeighborType.neutral
            elif distance == Distance.distant:
                if comparing == Comparing.brighter:
                    tmp_neighbor = NeighborType.dimming
                elif comparing == Comparing.converged:
                    tmp_neighbor = NeighborType.dimming
                elif comparing == Comparing.dimmer:
                    tmp_neighbor = NeighborType.dimming

            if neighbor == NeighborType.default:
                neighbor = tmp_neighbor
            elif neighbor == NeighborType.brightening:
                pass
            elif neighbor == NeighborType.neutral:
                if tmp_neighbor == NeighborType.dimming:
                    pass
                else:
                    neighbor = tmp_neighbor
            else:
                neighbor = tmp_neighbor

        l.neighbor = str(neighbor)

        # 次光度をneighborから決定
        change_rate = 0
        if neighbor == NeighborType.brightening:
            change_rate = random.randint(INIT.ALG_DB_BRIGHTENING_LOWER, INIT.ALG_DB_BRIGHTENING_UPPER)
        elif neighbor == NeighborType.neutral:
            change_rate = random.randint(INIT.ALG_DB_NEUTRAL_LOWER, INIT.ALG_DB_NEUTRAL_UPPER)
        elif neighbor == NeighborType.dimming:
            change_rate = random.randint(INIT.ALG_DB_DIMMING_LOWER, INIT.ALG_DB_DIMMING_UPPER)

        l.previous_luminosity = l.luminosity
        l.next_luminosity = l.luminosity * (100.0 + change_rate) / 100.
        if l.next_luminosity > INIT.LIGHT_LUMINOSITY_MAX[0]:
            l.next_luminosity = INIT.LIGHT_LUMINOSITY_MAX[0]
        elif l.next_luminosity < INIT.LIGHT_LUMINOSITY_MIN[0]:
            l.next_luminosity = INIT.LIGHT_LUMINOSITY_MIN[0]

    for l in ils.lights:
        l.luminosity = l.next_luminosity
        convert_to_signal(ils.lights)


class NeighborType(Enum):
    default = 0
    brightening = 1
    neutral = 2
    dimming = 3

    def __str__(self):
        if self == NeighborType.brightening:
            return "BRIGHTENING"
        elif self == NeighborType.neutral:
            return "NEUTRAL"
        elif self == NeighborType.dimming:
            return "DIMMING"


class Distance(Enum):
    default = 0
    near = 1
    middle = 2
    distant = 3

    def __str__(self):
        if self == Distance.default:
            return "!default"
        elif self == Distance.near:
            return "NEAR"
        elif self == Distance.middle:
            return "MIDDLE"
        elif self == Distance.distant:
            return "DISTANT"


class Comparing(Enum):
    default = 0
    brighter = 1
    converged = 2
    dimmer = 3

    def __str__(self):
        if self == Comparing.default:
            return "!default"
        elif self == Comparing.brighter:
            return "BRIGHTER"
        elif self == Comparing.converged:
            return "CONVERGED"
        elif self == Comparing.dimmer:
            return "DIMMER"


def update_config(ils):
    u"""
    ステップごとに目標照度と在離席を更新
    """
    # 目標照度を取得
    sensor_target_reader(ils.sensors)
    # 在離席を自動設定
    if INIT.AUTO_ATTENDANCE_SETTING:
        pass
    # 在離席を取得
    if INIT.CHECK_ATTENDANCE:
        sensor_attendance_reader(ils.sensors)
