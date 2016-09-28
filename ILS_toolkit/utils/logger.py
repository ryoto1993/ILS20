# coding: utf-8

import os
import datetime
import codecs
import csv
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

    info_name = "01_info.txt"
    illuminance_name = "02_illuminance.csv"
    luminosity_name = "03_luminosity.csv"
    power_name = "04_power.csv"
    luminosity_signal_name = "05_signal.csv"
    target_illuminance_name = "06_target_illuminance.csv"
    attendance_name = "07_attendance.csv"
    objective_function_name = "08_objective_function.csv"
    convergence_name = "09_convergence.csv"

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

        # 実験情報メモを作成
        self.make_information()
        # 照度履歴を作成
        if INIT.LOGGER_ILLUMINANCE:
            self.make_illuminance_log()
        # 光度履歴を作成
        if INIT.LOGGER_LUMINOSITY:
            self.make_luminosity_log()
        # 信号値履歴を作成
        if INIT.LOGGER_LUMINOSITY_SIGNAL:
            self.make_luminosity_signal_log()
        # 消費電力履歴を作成
        if INIT.LOGGER_POWER:
            self.make_power_log()
        # 目的関数を作成
            self.make_objective_function_log()
        # 近傍選択を作成

        # 目標照度履歴を作成
            self.make_target_illuminance_log()
        # 在離席履歴を作成
            self.make_attendance_log()
        # カスタムログを作成

    def make_information(self):
        u"""
        実験情報メモを出力するメソッド
        :return: None
        """
        file_path = self.path + "/" + self.info_name
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
        # ToDo: なおしなさい．
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

    def make_illuminance_log(self):
        u"""
        照度履歴ログを作成するメソッド
        :return: None
        """

        file_path = self.path + "/" + self.illuminance_name
        f = open(file_path, 'w')
        w = csv.writer(f, lineterminator='\n')
        row = ["Step"]
        for s in self.ils.sensors:
            row.append(str(s))
        w.writerow(row)
        f.close()

    def make_luminosity_log(self):
        u"""
        光度履歴ログを作成するメソッド
        :return: None
        """

        file_path = self.path + "/" + self.luminosity_name
        f = open(file_path, 'w')
        w = csv.writer(f, lineterminator='\n')
        row = ["Step"]
        for l in self.ils.lights:
            row.append(str(l))
        w.writerow(row)
        f.close()

    def make_luminosity_signal_log(self):
        u"""
        信号値履歴ログを作成するメソッド
        :return: None
        """

        file_path = self.path + "/" + self.luminosity_signal_name
        f = open(file_path, 'w')
        w = csv.writer(f, lineterminator='\n')
        row = ["Step"]
        for l in self.ils.lights:
            row.append(str(l))
        w.writerow(row)
        f.close()

    def make_power_log(self):
        u"""
        電力履歴ログを作成するメソッド
        :return: None
        """

        file_path = self.path + "/" + self.power_name
        f = open(file_path, 'w')
        w = csv.writer(f, lineterminator='\n')
        row = ["Step", "Power[cd]", "Power[W]"]
        w.writerow(row)
        f.close()

    def make_target_illuminance_log(self):
        u"""
        目標照度履歴ログを作成するメソッド
        :return: None
        """

        file_path = self.path + "/" + self.target_illuminance_name
        f = open(file_path, 'w')
        w = csv.writer(f, lineterminator='\n')
        row = ["Step"]
        for s in self.ils.sensors:
            row.append(str(s))
        w.writerow(row)
        f.close()

    def make_attendance_log(self):
        u"""
        在離席履歴ログを作成するメソッド
        :return: None
        """

        file_path = self.path + "/" + self.attendance_name
        f = open(file_path, 'w')
        w = csv.writer(f, lineterminator='\n')
        row = ["Step"]
        for s in self.ils.sensors:
            row.append(str(s))
        w.writerow(row)
        f.close()

    def make_objective_function_log(self):
        u"""
        目的関数ログを作成するメソッド
        :return: None
        """

        file_path = self.path + "/" + self.objective_function_name
        f = open(file_path, 'w')
        w = csv.writer(f, lineterminator='\n')
        row = ["Step"]
        for l in self.ils.lights:
            row.append(str(l) + "_Obj")
            row.append(str(l) + "_Pow")
            row.append(str(l) + "_Pen")
        w.writerow(row)
        f.close()

    def make_convergence_log(self):
        u"""
        収束ログを作成するメソッド
        :return: None
        """

        file_path = self.path + "/" + self.convergence_name
        f = open(file_path, 'w')
        w = csv.writer(f, lineterminator='\n')
        row = ["Step"]
        for s in self.ils.sensors:
            row.append(str(s))
        w.writerow(row)
        f.close()

    def append_all_log(self, step, next_flag):
        self.append_illuminance_log(step)
        self.append_luminosity_log(step)
        self.append_luminosity_signal_log(step)
        self.append_target_illuminance_log(step)
        self.append_attendance_log(step)
        self.append_power_log(step)
        self.append_objective_function_log(step, next_flag)
        self.append_convergence_log(step)

    def append_illuminance_log(self, step):
        u"""
        照度履歴ログに書き込み
        :return: None
        """

        file_path = self.path + "/" + self.illuminance_name
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(step)]
        for s in self.ils.sensors:
            row.append(str(int(s.illuminance)))
        w.writerow(row)
        f.close()

    def append_luminosity_log(self, step):
        u"""
        光度履歴ログに書き込み
        :return: None
        """

        file_path = self.path + "/" + self.luminosity_name
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(step)]
        for l in self.ils.lights:
            row.append(str(int(l.luminosity)))
        w.writerow(row)
        f.close()

    def append_luminosity_signal_log(self, step):
        u"""
        信号値履歴ログに書き込み
        :return: None
        """

        file_path = self.path + "/" + self.luminosity_signal_name
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(step)]
        for l in self.ils.lights:
            row.append(str(int(l.signals[0])))
        w.writerow(row)
        f.close()

    def append_power_log(self, step):
        u"""
        消費電力ログに書き込み
        :return: None
        """

        file_path = self.path + "/" + self.power_name
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(step), str(self.ils.power_meter.power), str(self.ils.power_meter.actual_power)]
        w.writerow(row)
        f.close()

    def append_target_illuminance_log(self, step):
        u"""
        目標照度履歴ログに書き込み
        :return: None
        """

        file_path = self.path + "/" + self.target_illuminance_name
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(step)]
        for s in self.ils.sensors:
            row.append(str(int(s.target)))
        w.writerow(row)
        f.close()

    def append_attendance_log(self, step):
        u"""
        在離席履歴ログに書き込み
        :return: None
        """

        file_path = self.path + "/" + self.attendance_name
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(step)]
        for s in self.ils.sensors:
            row.append(str(s.attendance))
        w.writerow(row)
        f.close()

    def append_objective_function_log(self, step, next_flag):
        u"""
        照度履歴ログに書き込み
        :return: None
        """

        file_path = self.path + "/" + self.objective_function_name
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(step)]
        for l in self.ils.lights:
            if next_flag:
                row.append(str(int(l.next_objective_function)))
                row.append(str(int(self.ils.power_meter.power)))
                row.append(str(int(l.next_objective_penalty)))
            else:
                row.append(str(int(l.objective_function)))
                row.append(str(int(self.ils.power_meter.power)))
                row.append(str(int(l.objective_penalty)))
        w.writerow(row)
        f.close()

    def append_convergence_log(self, step):
        u"""
        照度収束ログに書き込み
        :return: None
        """

        file_path = self.path + "/" + self.convergence_name
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(step)]
        for s in self.ils.sensors:
            if not s.attendance:
                row.append("-")
            elif s.target*(INIT.ALG_ALLOWANCE_LOWER+100)/100 <= s.illuminance <= s.target*(INIT.ALG_ALLOWANCE_UPPER+100)/100:
                row.append("True")
            else:
                row.append("False")
        w.writerow(row)
        f.close()