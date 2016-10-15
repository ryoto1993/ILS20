import time
import csv
from ILS import *
from utils.reader import *

if __name__ == "__main__":
    # ILS作成
    ils = ILS()
    print(len(ils.sensors))
    print(len(ils.lights))
    influence_reader(ils.lights)

    # reader
    reader = csv.reader(open("../rand.csv", "r"), delimiter=",", quotechar='"')
    data = []

    for index, i in enumerate(reader):
        data.append([])
        for s in range(12):
            data[index].append(i[s])

    # ファイル作成
    file_path = "sigs_to_illuminance.csv"
    f = open(file_path, 'w')
    w = csv.writer(f, lineterminator='\n')
    f.close()

    file_path = "sigs_to_illuminance.csv"
    f = open(file_path, 'a')
    w = csv.writer(f, lineterminator='\n')

    # 試行
    for t in range(100):
        line = []

        for i in range(12):
            ils.lights[i].signals[0] = data[t][i]
        convert_to_luminosity(ils.lights)
        update_sensors(ils)

        for s in ils.sensors:
            line.append(int(s.illuminance))
        w.writerow(line)

    f.close()
