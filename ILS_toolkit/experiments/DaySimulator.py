# coding: utf-8

import csv

from configure.config import INIT
from ILS import ILS
from algorithm.ANArank import ANARANK
from equipment.Sensor import Sensor
from equipment.Light import Light
from equipment.Sensor import update_sensors
from equipment.PowerMeter import calc_power


def simulate():
    # ################### #
    #       実験用設定      #
    # ################### #
    days = 20       # <- 何日分のシミュレーションを行うか（その分の"ptn (xx).csv"を用意してね）
    start_hr = 9    # <- 1日の開始時刻（終了時刻は在離席ファイルの行数に依存）
    loop = 400      # <- ステップ数ではなくループ数，400とすると800ステップになる
    path = u"./experiments/d平均在席率3パターン_名前変更/平均在席率30%"
    # ################### #

    force_config()
    print("Set to DaySimulator experiment mode.")

    for d in range(1, days+1):
        # 1日の処理を記述
        data_path = path + "/ptn (" + str(d) + ").csv"

        print("------ Day " + str(d) + " ---------------------")

        # 在離席パターン読み込み
        reader = csv.reader(open(data_path, "r"), delimiter=",", quotechar='"')
        att_data = []
        next(reader)
        for index, i in enumerate(reader):
            att_data.append([])
            for s in range(12):
                att_data[index].append(i[s+1])

        # 毎時の処理を行う
        for h in range(start_hr, start_hr+len(att_data)):
            print("... Hour " + str(h) + " ...")
            # シーケンスネームを設定（ログ用）
            INIT.SEQUENCE_NAME = "Day" + str(d) + "_Hour" + str(h)
            # センサ番号と照明番号のリセット（ログ用）
            Sensor.id = 1
            Light.id = 1
            # ILS初期化
            ils = ILS()
            # 在離席の設定
            set_attendance(att_data[h-start_hr], ils)
            # アルゴリズムの設定
            ils.algorithm = ANARANK(ils)
            # 指定したループ数の演算を実行
            for l in range(loop):
                ils.algorithm.next_step()
            # 最終状態の電力情報とセンサ情報をアップデート
            # 現在照度値を取得
            update_sensors(self.ils)
            # 電力情報を計算
            self.ils.power_meter.calc_power()

    exit(0)


def set_attendance(data, ils):
    for s_i, s in enumerate(ils.sensors):
        if data[s_i] == "0":
            s.attendance = False
        elif data[s_i] == "1":
            s.attendance = True
        else:
            print("Attendance setting Error!\nPlease check your attendance setting data.")


def force_config():
    INIT.SIMULATION = True
    INIT.CHECK_ATTENDANCE = False  # <- このプログラム内で切り替えるためOFFに！
    INIT.AUTO_ATTENDANCE_SETTING = False
    INIT.SIMULATE_VOLTAGE_DISPLACEMENT = False
    INIT.DIR_LOG = "./experiments/1日シミュレータのLOG/"
