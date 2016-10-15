import time
import csv
from configure.config import *
from ILS import *

if __name__ == "__main__":
    # ILS作成
    ils = ILS()
    INIT.LOGGER_ILLUMINANCE = True  # 照度履歴を出力
    INIT.LOGGER_LUMINOSITY = False  # 光度履歴を出力
    INIT.LOGGER_LUMINOSITY_SIGNAL = False  # 信号値履歴を出力
    INIT.LOGGER_POWER = False  # 消費電力履歴を出力
    INIT.LOGGER_OBJECTIVE_FUNCTION = False  # 目的関数を出力
    INIT.LOGGER_NEIGHBOR = False  # 近傍選択を出力
    INIT.LOGGER_TARGET = False
    INIT.LOGGER_ATTENDANCE = False
    INIT.LOGGER_CUSTOM = False  # カスタムログを出力
    ils.logger = Logger()

    reader = csv.reader(open("rand.csv", "r"), delimiter=",", quotechar='"')
    data = []

    for index, i in enumerate(reader):
        data.append([])
        for s in range(12):
            data[index].append(i[s])

    for t in range(100):
        cdinfo = ""
        for s in range(12):
            cdinfo += (str(data[t][s]) + ",0,")

        print(data[t])

        while True:
            try:
                f = open("C:/Users/light/Desktop/isdl_20th/bacnet_interface/cdinfo.txt", "w")
                break
            except FileNotFoundError:
                print("can't find \"cdinfo.txt\".")
            except PermissionError:
                print("permission error")
                pass
        f.write(cdinfo)
        f.close()

        time.sleep(10.0)
