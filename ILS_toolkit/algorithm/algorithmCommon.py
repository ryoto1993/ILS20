# coding: utf-8

from configure.config import *


def calc_objective_function(ils):
    u"""
    全照明の目的関数を計算するメソッド

    ★ペナルティ項のポリシー★
    まず，照明とセンサが近接しているかを照度光度影響度で判断する．
    閾値はINIT.ALG_RC_THRESHOLDで設定可能．
    近接している場合…
    ・現在照度が目標照度を上回っている場合
    　　→ 目標照度の6%（最小知覚変動比）以上の場合に計上
    ・現在照度が目標照度に達していない場合
    　　→ 無条件に計上
    """
    # ペナルティ項にかかる重み
    w = INIT.ALG_WEIGHT

    # 各照明ごとに目的関数を計算
    for l in ils.lights:
        obj = ils.powermeter.power

        for s_i, s in enumerate(ils.sensors):
            # 照度光度影響度数を取得
            r = l.influence[s_i]
            r = r if r >= INIT.ALG_RC_THRESHOLD else 0.0
            r = r if s.attendance else 0.0  # 離席してる場合はペナルティ無し
            # ペナルティ関数を計算
            obj += w * r * (s.illuminance - s.target)**2

        l.objective_function = obj
