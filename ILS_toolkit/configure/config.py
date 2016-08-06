# coding:utf-8


class INIT:
    #####################
    # シーケンシャル名設定 #
    #####################
    # シーケンシャル名は，ログファイルの格納ディレクトリの名前に含まれます．
    # 行うデモ/実験/シミュレーションの概要を簡潔に入力してください．
    SEQUENCE_NAME = u"目的関数ログテスト"

    #####################
    #      動作モード     #
    #####################
    SIMULATION = True         # 実機の時はFalse
    TEMPERATURE = False       # 色温度も制御するか
    CHECK_ATTENDANCE = True   # 在離席管理を行うか

    #####################
    #      ロガー設定     #
    #####################
    LOGGER_ILLUMINANCE = True  # 照度履歴を出力
    LOGGER_LUMINOSITY = True   # 光度履歴を出力
    LOGGER_LUMINOSITY_SIGNAL = True   # 信号値履歴を出力
    LOGGER_POWER = True        # 消費電力履歴を出力
    LOGGER_OBJECTIVE_FUNCTION = True  # 目的関数を出力
    LOGGER_NEIGHBOR = True     # 近傍選択を出力
    LOGGER_CUSTOM = True       # カスタムログを出力
    LOGGER_CUSTOM_FILE = "./configure/customLog.txt"  # カスタムログの設定ファイル

    #####################
    #  機器情報ファイルパス #
    #####################
    FILE_CD_INFO = "C:/Users/light/Desktop/isdl_20th/bacnet_interface/cdinfo.txt"
    FILE_SENSOR_INFO = "../sekonicAnalog/sensor.txt"

    # for debug
    # FILE_CD_INFO = "../test_data/cdinfo.txt"
    # FILE_SENSOR_INFO = "../test_data/sensor.txt"

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
    DIR_LOG = "../LOG/"

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
    # 最適化アルゴリズム設定 #
    #####################
    ALG_WEIGHT = 10
    ALG_INITIAL_SIGNAL = 30

    # ANA/RC, ANA,DBの設定
    ALG_DB_THRESHOLD = 0.07          # 目的関数内ペナルティ項の照度/光度影響度による閾値（必ず影響度の実値を見て設定すること）
    ALG_DB_CHECK_SENSOR_NUM = 7      # 次光度の近傍選択時に各照明がチェックするセンサ数の上限
    ALG_DB_BRIGHTENING_UPPER = 7.0   # 増光変動幅上限（％指定）
    ALG_DB_BRIGHTENING_LOWER = 4.0   # 増光変動幅下限（％指定）
    ALG_DB_NEUTRAL_UPPER = 2.0       # 中立変動幅上限（％指定）
    ALG_DB_NEUTRAL_LOWER = -2.0      # 中立変動幅下限（％指定）
    ALG_DB_DIMMING_UPPER = -2.0      # 減光変動幅上限（％指定）
    ALG_DB_DIMMING_LOWER = -7.0      # 減光変動幅下限（％指定）
    ALG_DB_ALLOWANCE_UPPER = 2.0     # 目標照度収束許容範囲上限（％指定）
    ALG_DB_ALLOWANCE_LOWER = -1.0    # 目標照度収束許容範囲下限（％指定）
