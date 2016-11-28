# coding: utf-8

from ILS import ILS
from utils import signalConverter, logger, reader
from equipment.Sensor import Sensor, update_sensors
from equipment.Light import Light


def start():
    print("Play Ground!")

    # センサ番号と照明番号のリセット（ログ用）
    Sensor.id = 1
    Light.id = 1
    # ILS初期化
    ils = ILS()
    # 各照明に照度/光度影響度（DB）を読み込む
    reader.influence_reader(ils.lights)
    # ログを作る
    ils.logger = logger.Logger(ils)

    # Let's play!
    for l in ils.lights:
        l.signals[0] = 0

    ils.lights[28].signals[0] = 100

    # 信号値を光度値に変更
    signalConverter.convert_to_luminosity(ils.lights)
    # 現在照度値を取得
    update_sensors(ils)
    # 電力情報を計算
    ils.power_meter.calc_power()
    # ロガーに追記
    ils.logger.append_all_log(1, False)
