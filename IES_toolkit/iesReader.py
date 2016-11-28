# coding: UTF-8

import csv
import math
from IES_toolkit.ies_config import *


class IESreader:
    def __init__(self):
        self.profile = ""
        self.manufac = ""
        self.test = ""
        self.date = ""
        self.lumcat = ""
        self.lamp = ""
        self.lampcat = ""
        self.luminaire = ""
        self.tilt = ""
        self.angles = []
        self.data = []
        self.flux = 0

        self.read_ies()
        self.make_coefficient()

    def read_ies(self):
        # ヘッダ以降のデータが始まる行
        start_line = 0

        f = open(INIT.IES_FILE, 'r')
        lines = f.readlines()

        self.profile = lines[0][6:]

        print(self.profile)

        # ヘッダ部分を読み込む

        i = 1
        while True:
            if lines[i].find("[MANUFAC]") > -1:
                self.manufac = lines[i][9:]
            elif lines[i].find("[TEST]") > -1:
                self.test = lines[i][6:]
            elif lines[i].find("[DATE]") > -1:
                self.date = lines[i][6:]
            elif lines[i].find("[LUMCAT]") > -1:
                self.lumcat = lines[i][8:]
            elif lines[i].find("[LAMP]") > -1:
                self.lamp = lines[i][6:]
            elif lines[i].find("[LAMPCAT]") > -1:
                self.lampcat = lines[i][8:]
            elif lines[i].find("[LUMINAIRE]") > -1:
                self.luminaire = lines[i][11:]
            elif lines[i].find("TILT") > -1:
                self.tilt = lines[i][4:]
            else:
                start_line = i-1
                break
            i += 1

        # ヘッダ以降のデータを読み込む
        self.angles = lines[start_line + INIT.IES_LINE_ANGLE][:-1].split(' ')
        self.data = lines[start_line + INIT.IES_LINE_DATA][:-1].split(' ')
        self.flux = float(lines[start_line + INIT.IES_LINE_LUMEN])

        f.close()

    def make_coefficient(self):
        f = open(INIT.IES_INFLUENCE_FILE, 'w')
        writer = csv.writer(f, lineterminator='\n')

        lights = [[int(elm) for elm in v] for v in csv.reader(open(INIT.IES_LIGHT_FILE, "r"))]
        sensors = [[int(elm) for elm in v] for v in csv.reader(open(INIT.IES_SENSOR_FILE, "r"))]

        # ライト読み込みとヘッダ記述
        tmp = [""]
        for i in range(0, len(lights)):
            tmp.append("Light" + str(i+1))
        writer.writerow(tmp)

        # センサ読み込みと影響度計算
        for i, s in enumerate(sensors):
            tmp.clear()
            tmp.append("Sensor" + str(i+1))
            for l in lights:
                tmp.append(str(self.solve_coefficient(self.dist(s, l))))
            writer.writerow(tmp)
        f.close()

    # 距離から影響度を算出するメソッド
    def solve_coefficient(self, dist):
        # 直下1mの照度=光度を計算
        luminance = float(self.data[0]) * self.flux / 1000

        # データ間の角度
        deg_interval = int(self.angles[1]) - int(self.angles[0])

        # 測光点の水平面照度を計算
        rdegree = math.atan(float(dist) / float(INIT.IES_HEIGHT))
        degree = math.degrees(rdegree)
        degree_index = int(degree / deg_interval)
        floor = (degree_index + 1) * deg_interval
        sub = float(degree - floor)
        raw = float(self.data[degree_index]) + float(sub / float(deg_interval)) * (float(self.data[degree_index + 1]) - float(self.data[degree_index]))
        illuminance = raw * self.flux / 1000 / ((dist/1000)**2 + (INIT.IES_HEIGHT/1000)**2) * math.cos(rdegree)

        # 照度/光度影響度を計算
        inf = illuminance/luminance
        return inf if inf > 0.001 else 0.0

    def dist(self, p1, p2):
        p1x = float(p1[0])
        p1y = float(p1[1])
        p2x = float(p2[0])
        p2y = float(p2[1])

        d = (p1x-p2x)**2 + (p1y-p2y)**2
        dist = math.sqrt(d)

        return dist


if __name__ == "__main__":
    IESreader()
