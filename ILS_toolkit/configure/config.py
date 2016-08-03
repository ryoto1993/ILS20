# coding:utf-8


class INIT:
    #####################
    #      動作モード     #
    #####################
    SIMULATION = True         # 実機の時はFalse
    TEMPERATURE = False       # 色温度も制御するか
    CHECK_ATTENDANCE = True   # 在離席管理を行うか

    #####################
    #  機器情報ファイルパス #
    #####################
    # FILE_CD_INFO = "C:/Users/light/Desktop/isdl_20th/bacnet_interface/cdinfo.txt"
    # FILE_SENSOR_INFO = "C:/Users/light/Desktop/isdl_20th/bacnet_interface/sensor.txt"

    # for debug
    FILE_CD_INFO = "../test_data/cdinfo.txt"
    FILE_SENSOR_INFO = "../test_data/sensor.txt"

    #####################
    #   ファイルパス設定   #
    #####################
    FILE_SENSOR = "./configure/sensor.csv"
    FILE_LIGHT = "./configure/light.csv"
    FILE_INFLUENCE = "./configure/influence.csv"
    FILE_STATE = "./configure/state.txt"
    FILE_LIGHT_PATTERN = "./configure/fixedLightPattern.csv"
    FILE_SENSOR_TARGET = "./configure/target.txt"
    FILE_ATTENDANCE = "./configure/attendance.txt"

    #####################
    # 最適化アルゴリズム設定 #
    #####################
    ALG_WEIGHT = 10
    ALG_INITIAL_SIGNAL = 30

    # ANA/RC, ANA,DBの設定
    ALG_RC_THRESHOLD = 0.07   # 目的関数内ペナルティ項の照度/光度影響度による閾値（必ず影響度の実値を見て設定すること）

    #####################
    #      照明設定       #
    #####################
    # BACnet型 三菱LEDのデータ
    LIGHT_SIGNAL_MAX = [100, 100]            # 最大点灯信号値
    LIGHT_LUMINOSITY_MAX = [1280.0, 1280.0]  # 最大点灯光度 [lx]
    LIGHT_SIGNAL_MIN = [20, 20]              # 最小点灯信号値
    LIGHT_LUMINOSITY_MIN = [248.0, 248.0]   # 最小点灯光度 [lx]
    LIGHT_WAIT_SECOND = 6.5                  # 光度を変更してからの待機時間

    #####################
    #   配光曲線読込設定   #
    #####################
    IES_FILE = "./BACnet.ies"
    IES_LINE_LUMEN = 2   # データ部分で光束が記載されている行
    IES_LINE_ANGLE = 14  # データ部分でアングルが記載されている行
    IES_LINE_DATA = 16   # データ部分で光度が記載されている行
