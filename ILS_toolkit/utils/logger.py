# coding: utf-8

import os
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
        # ログファイルのディレクトリをINIT.DIR_LOG以下に生成
        path = INIT.DIR_LOG + "_" + INIT.SEQUENCE_NAME
        os.mkdir(path)

