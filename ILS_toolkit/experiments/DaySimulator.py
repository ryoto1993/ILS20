# coding: utf-8

import csv
import os

from configure.config import INIT
from ILS import ILS
from algorithm.ANArank import ANARANK
from equipment.Sensor import Sensor
from equipment.Light import Light
from equipment.Sensor import update_sensors
from equipment.OutsideLight import OutsideLight

# ################### #
#       実験用設定      #
# ################### #
days = 1       # <- 何日分のシミュレーションを行うか（その分の"ptn (xx).csv"を用意してね）
start_hr = 1    # <- 1日の開始時刻（終了時刻は在離席ファイルの行数に依存）
loop = 400      # <- ステップ数ではなくループ数，400とすると800ステップになる
path = u"./experiments/在離席/全員常に在席"
add_outside_light = True
outside_path = u"./experiments/外光データ10minおき900_2300.csv"
par_path = u"./experiments/1日シミュレータ（700テスト）/"


outside_data = []


def simulate():
    force_config()
    print("Set to DaySimulator experiment mode.")

    for d in range(1, days+1):
        # 1日の処理を記述
        data_path = path + "/ptn (" + str(d) + ").csv"
        print("------ Day " + str(d) + " ---------------------")
        # センサ番号と照明番号のリセット（ログ用）
        Sensor.id = 1
        Light.id = 1
        # ILS初期化
        ils = ILS()
        # 1日のサマリーを作成
        make_summary(ils, d)
        # 在離席パターン読み込み
        reader = csv.reader(open(data_path, "r"), delimiter=",", quotechar='"')
        att_data = []
        next(reader)
        for index, i in enumerate(reader):
            att_data.append([])
            for s in range(12):
                att_data[index].append(i[s+1])
        # 外光データ読み込み
        if add_outside_light:
            read_outside_data()
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
            # 外光データをILSに反映
            OutsideLight.data = []
            for i in range(int(loop * 2 + 10)):
                OutsideLight.data.append(outside_data[h-1])
            # 在離席の設定
            set_attendance(att_data[h-start_hr], ils)
            # アルゴリズムの設定
            ils.algorithm = ANARANK(ils)
            # 指定したループ数の演算を実行
            for l in range(loop):
                ils.algorithm.next_step()
            # 最終状態の電力情報とセンサ情報をアップデート
            update_sensors(ils)  # 現在照度値を取得
            ils.power_meter.calc_power()         # 電力情報を計算
            # サマリーに追記
            append_summary(ils, d, h)
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
    INIT.DIR_LOG = par_path + "LOG/"
    INIT.ADD_OUTSIDE_LIGHT = True if add_outside_light else False
    if add_outside_light:
        INIT.EXT_STEP_SECOND = 1  # 外光加算を行う際の1ステップの実時間秒数
        INIT.EXT_START_LINE = 0  # 外光加算を何行目から読むかの設定（最初の行は0！）


def read_outside_data():
    reader = csv.reader(open(outside_path, "r"), delimiter=",", quotechar='"')
    for index, i in enumerate(reader):
        outside_data.append([])
        outside_data[index].append("")
        for s in range(12):
            outside_data[index].append(i[s])


def make_summary(ils, d):
    summary_path = par_path + "SUMMARY/day" + str(d) + "/"
    os.mkdir(summary_path)

    ill_f = open(summary_path + "01_illuminance.csv", 'w')
    lum_f = open(summary_path + "02_luminosity.csv", 'w')
    pow_f = open(summary_path + "03_power.csv", 'w')
    sig_f = open(summary_path + "04_signal.csv", 'w')
    cnv_f = open(summary_path + "05_convergence.csv", 'w')

    ill_w = csv.writer(ill_f, lineterminator='\n')
    lum_w = csv.writer(lum_f, lineterminator='\n')
    pow_w = csv.writer(pow_f, lineterminator='\n')
    sig_w = csv.writer(sig_f, lineterminator='\n')
    cnv_w = csv.writer(cnv_f, lineterminator='\n')

    row = ["Hour"]
    for s in ils.sensors:
        row.append(str(s))
    ill_w.writerow(row)
    row = ["Hour"]
    for l in ils.lights:
        row.append(str(l))
    lum_w.writerow(row)
    row = ["Hour", "lum_sum[cd]", "Power[w]"]
    pow_w.writerow(row)
    row = ["Hour"]
    for l in ils.lights:
        row.append(str(l))
    sig_w.writerow(row)
    row = ["Hour"]
    for s in ils.sensors:
        row.append(str(s))
    cnv_w.writerow(row)

    ill_f.close()
    lum_f.close()
    pow_f.close()
    sig_f.close()
    cnv_f.close()


def append_summary(ils, d, h):
    summary_path = par_path + "SUMMARY/day" + str(d) + "/"

    ill_f = open(summary_path + "01_illuminance.csv", 'a')
    lum_f = open(summary_path + "02_luminosity.csv", 'a')
    pow_f = open(summary_path + "03_power.csv", 'a')
    sig_f = open(summary_path + "04_signal.csv", 'a')
    cnv_f = open(summary_path + "05_convergence.csv", 'a')

    ill_w = csv.writer(ill_f, lineterminator='\n')
    lum_w = csv.writer(lum_f, lineterminator='\n')
    pow_w = csv.writer(pow_f, lineterminator='\n')
    sig_w = csv.writer(sig_f, lineterminator='\n')
    cnv_w = csv.writer(cnv_f, lineterminator='\n')

    row = [str(h)]
    for s in ils.sensors:
        row.append(str(int(s.illuminance)))
    ill_w.writerow(row)
    row = [str(h)]
    for l in ils.lights:
        row.append(str(int(l.luminosity)))
    lum_w.writerow(row)
    row = [str(h), str(int(ils.power_meter.power)), str(int(ils.power_meter.actual_power))]
    pow_w.writerow(row)
    row = [str(h)]
    for l in ils.lights:
        row.append(str(l.signals[0]))
    sig_w.writerow(row)
    row = [str(h)]
    for s in ils.sensors:
        row.append(str(s.convergence))
    cnv_w.writerow(row)

    ill_f.close()
    lum_f.close()
    pow_f.close()
    sig_f.close()
    cnv_f.close()

