# coding: utf-8

import csv

from configure.config import INIT
from ILS import ILS
from algorithm.ANArank import ANARANK


def simulate():
    # ################### #
    #       実験用設定      #
    # ################### #
    days = 20
    start_hr = 9
    loop = 800
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
            INIT.SEQUENCE_NAME = "Day" + str(d) + "_Hour" + str(h)

            ils = ILS()  # ILSを初期化
            ils.algorithm = ANARANK(ils)

            for l in range(int(loop/2)):
                ils.algorithm.next_step()

    exit(0)


def force_config():
    INIT.SIMULATION = True
    INIT.CHECK_ATTENDANCE = False  # <- このプログラム内で切り替えるためOFFに！
    INIT.AUTO_ATTENDANCE_SETTING = False
    INIT.SIMULATE_VOLTAGE_DISPLACEMENT = False
    INIT.DIR_LOG = "./experiments/1日シミュレータのLOG/"
