# coding: utf-8

import os
import datetime
from configure.config import *


class Logger:
    u"""
    知的照明システムの動作ログを作成するクラス

    ★出力可能な情報
    ・光度履歴（ステップ単位/指定秒数単位）
    ・照度履歴（ステップ単位/指定秒数単位）
    ・電力履歴（ステップ単位/指定秒数単位）
    ・目的関数履歴（ステップ単位）
    ・変動比選択（ステップ単位）
    """

    def __init__(self, ils):
        # タイムスタンプ情報の取得
        time = datetime.datetime.today()
        y = str(time.year)
        m = str(time.month).zfill(2)
        d = str(time.day).zfill(2)
        hr = str(time.hour).zfill(2)
        mi = str(time.minute).zfill(2)
        sc = str(time.second).zfill(2)

        # ログファイルのディレクトリをINIT.DIR_LOG以下に生成
        path = INIT.DIR_LOG + y + m + d + "_" + hr + mi + sc + "_" + INIT.SEQUENCE_NAME
        os.mkdir(path)

        # 実験情報メモを出力

        # 照度履歴を出力

        # 光度履歴を出力

        # 消費電力履歴を出力

        # 目的関数を出力

        # 近傍選択を出力

        # カスタムログを出力