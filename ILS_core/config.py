# coding:utf-8


class INIT:
    #####################
    #      動作モード     #
    #####################
    SIMULATION = True

    #####################
    #  機器情報ファイルパス #
    #####################
    CD_INFO_FILE = "../test_data/cdinfo.txt"
    SENSOR_INFO_FILE = "../test_data/sensor.txt"

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
    #      照明設定       #
    #####################
    # BACnet型 三菱LEDのデータ
    LIGHT_SIGNAL_MAX = 100       # 最大点灯信号値
    LIGHT_LUMINOSITY_MAX = 1280  # 最大点灯光度 [lx]
    LIGHT_SIGNAL_MIN = 20        # 最小点灯信号値
    LIGHT_LUMINOSITY_MIN = 248   # 最小点灯光度 [lx]

    #####################
    #   配光曲線読込設定   #
    #####################
    IES_FILE = "./BACnet.ies"
    IES_LINE_LUMEN = 2   # データ部分で光束が記載されている行
    IES_LINE_ANGLE = 14  # データ部分でアングルが記載されている行
    IES_LINE_DATA = 16   # データ部分で光度が記載されている行
