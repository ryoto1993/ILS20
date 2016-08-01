# coding:utf-8


class INIT:
    #####################
    #      動作モード     #
    #####################
    SIMULATION = True

    #####################
    #  機器情報ファイルパス #
    #####################
    CD_INFO_FILE = ""
    SENSOR_INFO_FILE = ""

    #####################
    #   ファイルパス設定   #
    #####################
    SENSOR_FILE = "./configure/sensor.csv"
    LIGHT_FILE = "./configure/light.csv"
    INFLUENCE_FILE = "./configure/influence.csv"
    STATE_FILE = "./configure/state.txt"

    #####################
    # 最適化アルゴリズム設定 #
    #####################
    WEIGHT = 10

    #####################
    #   配光曲線読込設定   #
    #####################
    IES_FILE = "./BACnet.ies"
    IES_LINE_LUMEN = 2   # データ部分で光束が記載されている行
    IES_LINE_ANGLE = 14  # データ部分でアングルが記載されている行
    IES_LINE_DATA = 16   # データ部分で光度が記載されている行