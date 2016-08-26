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
            r = r if not (s.target*(1+INIT.ALG_ALLOWANCE_LOWER/100) <= s.illuminance <= s.target*(1+INIT.ALG_ALLOWANCE_UPPER/100)) else 0.0
            # ペナルティ関数を計算
            penalty += w * r * (s.illuminance - s.target)**2

        obj += penalty

        if next_flag:
            l.next_objective_function = obj
            l.next_objective_penalty = penalty
        else:
            l.objective_function = obj
            l.objective_penalty = penalty


def decide_next_luminosity_influence(ils):
    u"""
    全照明の次光度を照度/光度影響度から決定するメソッド

    ★次光度決定方法のポリシー★
    各照明がINIT.ALG_DB_THRESHOLD以上のセンサの中から
    INIT.ALG_DB_CHECK_SENSOR_NUM個分のセンサの現在照度と目標照度をチェックし，
    増光・中立・減光から近傍設計を選択する．
    優先度は，減光→増光→中立

    :param ils: ILSを引数に渡す
    """

    # 各照明ごとに次光度を決定
    for l in ils.lights:
        neighbor = NeighborType.dimming

        # センサに対する照度/光度影響度を降順にした時のインデックス番号
        influence = l.influence[:]

        # 離席してるセンサの影響度は0にする
        for s_i, s in enumerate(ils.sensors):
            if not s.attendance:
                influence[s_i] = 0.0

        key = sorted(range(len(influence)), key=lambda k: influence[k], reverse=True)

        # INIT.ALG_DB_CHECK_SENSOR_NUMの数だけ近くのセンサを抽出
        for i in range(0, INIT.ALG_DB_CHECK_SENSOR_NUM):
            s = ils.sensors[key[i]]
            if not s.attendance:
                continue
            # 増光対象があるかチェック
            if s.illuminance < s.target * (100.0 + INIT.ALG_ALLOWANCE_LOWER) / 100.0:
                neighbor = NeighborType.brightening
                break
            # 中立対象があるかチェック
            if s.illuminance < s.target * (100.0 + INIT.ALG_ALLOWANCE_UPPER) / 100.0:
                neighbor = NeighborType.neutral
        l.neighbor = neighbor

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
    brightening = 1
    neutral = 2
    dimming = 3

    def __str__(self):
        if self == NeighborType.brightening:
            return "BRIGHTING"
        elif self == NeighborType.neutral:
            return "NEUTRAL"
        elif self == NeighborType.dimming:
            return "DIMMING"
