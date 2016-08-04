# coding: utf-8

import os
import datetime
import codecs
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
        self.ils = ils

        # タイムスタンプ情報の取得
        time = datetime.datetime.today()
        self.y = str(time.year)
        self.m = str(time.month).zfill(2)
        self.d = str(time.day).zfill(2)
        self.hr = str(time.hour).zfill(2)
        self.mi = str(time.minute).zfill(2)
        self.sc = str(time.second).zfill(2)

        # ログファイルのディレクトリをINIT.DIR_LOG以下に生成
        self.path = INIT.DIR_LOG + self.y + self.m + self.d + "_" + self.hr + self.mi + self.sc + "_" + INIT.SEQUENCE_NAME
        os.mkdir(self.path)

        # 実験情報メモを出力
        self.make_information()
        # 照度履歴を出力

        # 光度履歴を出力

        # 消費電力履歴を出力

        # 目的関数を出力

        # 近傍選択を出力

        # カスタムログを出力

    def make_information(self):
        u"""
        実験情報メモを出力するメソッド
        :return: None
        """
        file_path = self.path + "/" + "info.txt"
        f = codecs.open(file_path, "w", "utf-8")

        line = u"実験名　　　　： " + INIT.SEQUENCE_NAME + "\r\n"
        f.write(line)
        line = u"実験日時　　　： " + str(self.y) + u"年" + str(self.m) + u"月" + str(self.d) + u"日 "\
               + str(self.hr) + u"時" + str(self.mi) + u"分" + str(self.sc) + u"秒" + "\r\n"
        f.write(line)
        line = u"照明台数　　　： " + str(len(self.ils.lights)) + "\r\n"
        f.write(line)
        line = u"センサ台数　　： " + str(len(self.ils.sensors)) + "\r\n"
        f.write(line)
        line = u"アルゴリズム　： " + str(self.ils.algorithm) + "\r\n"
        f.write(line)
        line = u"ペナルティ重み： " + str(INIT.ALG_WEIGHT) + "\r\n"
        f.write(line)

        line = "\r\n---------------"
        f.write(line)
        line = u"以下，config.pyの内容"
        f.write(line)
        line = "---------------\r\n"
        f.write(line)

        config_path = "configure/config.py"
        cf = codecs.open(config_path, "r", "utf-8")
        lines = cf.readlines()
        cf.close()
        f.writelines(lines)

        f.close()
