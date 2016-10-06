from ILS_toolkit.utils.dimmer import *
from ILS_toolkit.utils.reader import *
import os


class Setting:
    light_num = 0
    sensor_num = 0

if __name__ == "__main__":
    setting = Setting()
    lights = []
    sensors = []

    INIT.FILE_LIGHT = "../ILS_toolkit/configure/dataSet/Light/BACnet/light.csv"
    INIT.FILE_SENSOR = "../ILS_toolkit/configure/dataSet/Sensor/island12/sensor.csv"

    # 照明の設定を読込
    lights_config_reader(lights)
    # センサの設定を読込
    sensors_config_reader(sensors)

    # 照明を一律で点灯する
    for l in lights:
        l.signals[0] = 60
    dimming(lights)

    os.mkdir("./data")
    for l in lights:
        print("Light" + str(l.id))
        # ファイル作成
        file_path = "./data/" + str(l) + ".csv"
        f = open(file_path, 'w')
        w = csv.writer(f, lineterminator='\n')
        row = ["Signal"]
        for s in sensors:
            row.append(str(s))
        w.writerow(row)

        # init
        for ln in lights:
            ln.signals[0] = 60
        # 50
        print("sig50")
        l.signals[0] = 50
        dimming(lights)
        data50 = ["50"]
        sensor_signal_reader(sensors)
        for s in sensors:
            data50.append(s.illuminance)
        # 70
        print("sig70")
        l.signals[0] = 70
        dimming(lights)
        data70 = ["70"]
        sensor_signal_reader(sensors)
        for s in sensors:
            data70.append(s.illuminance)
        # 90
        print("sig90")
        l.signals[0] = 90
        dimming(lights)
        data90 = ["90"]
        sensor_signal_reader(sensors)
        for s in sensors:
            data90.append(s.illuminance)
        # 書き込み
        w = csv.writer(f, lineterminator='\n')
        w.writerow(data50)
        w.writerow(data70)
        w.writerow(data90)
        f.close()
