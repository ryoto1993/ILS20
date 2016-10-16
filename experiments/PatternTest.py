# coding: utf-8

from ILS import *
from utils.manualChanger import *
from utils.dimmer import *
from algorithm.ANAdb import *
import time


if __name__ == "__main__":
    u"""ILSの動作をコントロールするメインモジュール"""

    print("Intelligent Lighting System ver.20th")

    path = INIT.DIR_LOG + "_signal_hikaku"

    # 実機
    ils = ILS()

    file_path = path + "/" + "actual_illuminance.csv"
    f = open(file_path, 'w')
    w = csv.writer(f, lineterminator='\n')
    row = ["Step"]
    for s in ils.sensors:
        row.append(str(s))
    w.writerow(row)
    f.close()

    file_path = path + "/" + "actual_luminosity.csv"
    f = open(file_path, 'w')
    w = csv.writer(f, lineterminator='\n')
    row = ["Step"]
    for l in ils.lights:
        row.append(str(l))
    w.writerow(row)
    f.close()

    u"""照度光度影響度を読込"""
    reader = [v for v in csv.reader(open(u"./configure/ies_influence_hosei.csv", "r")) if len(v) != 0]
    reader.pop(0)

    for s in range(len(reader)):
        reader[s].pop(0)
        for l_i, l in enumerate(ils.lights):
            l.influence.append(float(reader[s][l_i]))

    # シミュ
    ils2 = ILS()

    file_path2 = path + "/" + "simulator_illuminance.csv"
    f = open(file_path2, 'w')
    w = csv.writer(f, lineterminator='\n')
    row = ["Step"]
    for s in ils2.sensors:
        row.append(str(s))
    w.writerow(row)
    f.close()

    file_path = path + "/" + "simulator_luminosity.csv"
    f = open(file_path, 'w')
    w = csv.writer(f, lineterminator='\n')
    row = ["Step"]
    for l in ils2.lights:
        row.append(str(l))
    w.writerow(row)
    f.close()

    u"""照度光度影響度を読込"""
    reader2 = [v for v in csv.reader(open(u"./configure/完璧な電気照度光度影響度_mirror.csv", "r")) if len(v) != 0]
    reader2.pop(0)

    for s in range(len(reader2)):
        reader2[s].pop(0)
        for l_i, l in enumerate(ils2.lights):
            l.influence.append(float(reader2[s][l_i]))

    print(ils2.lights[0].influence)


    for i in range(1000):
        # 12個の信号値を生成
        for j in range(12):
            num = random.randint(10, 100)
            ils.lights[j].signals[0] = num
            ils2.lights[j].signals[0] = num
        convert_to_luminosity(ils.lights)
        convert_to_luminosity(ils2.lights)

        calc_illuminance(ils)
        calc_illuminance(ils2)

        # 照度履歴保存
        file_path = path + "/" + "actual_illuminance.csv"
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(i)]
        for s in ils.sensors:
            row.append(str(int(s.illuminance)))
        w.writerow(row)
        f.close()

        file_path2 = path + "/" + "simulator_illuminance.csv"
        f = open(file_path2, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(i)]
        for s in ils2.sensors:
            row.append(str(int(s.illuminance)))
        w.writerow(row)
        f.close()

        # 光度履歴保存
        file_path = path + "/" + "actual_luminosity.csv"
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(i)]
        for l in ils.lights:
            row.append(str(int(l.luminosity)))
        w.writerow(row)
        f.close()

        file_path = path + "/" + "simulator_luminosity.csv"
        f = open(file_path, 'a')
        w = csv.writer(f, lineterminator='\n')
        row = [str(i)]
        for l in ils2.lights:
            row.append(str(int(l.luminosity)))
        w.writerow(row)
        f.close()