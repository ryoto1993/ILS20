# coding:utf-8


class INIT:
    #####################
    # シーケンシャル名設定 #
    #####################
    # シーケンシャル名は，ログファイルの格納ディレクトリの名前に含まれます．
    # 行うデモ/実験/シミュレーションの概要を簡潔に入力してください．
    SEQUENCE_NAME = u"IEEJスマートファシリティ_8-J_ロールバックバグフィックス"

    #####################
    #      動作モード     #
    #####################
    SIMULATION = True         # 実機の時はFalse
    TEMPERATURE = False       # 色温度も制御するか
    CHECK_ATTENDANCE = True   # 在離席管理を行うか
    AUTO_ATTENDANCE_SETTING = False      # 在離席の自動設定を行うか
    SIMULATE_VOLTAGE_DISPLACEMENT = True    # Sekonicアナログ照度センサの電圧変位誤差をシミュレート
    CORRECT_SENSOR_DISPLACEMENT = True      # Sekonicアナログ照度センサの誤差を補正

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
    FILE_SENSOR = "./configure/dataSet/Sensor/island12/sensor.csv"
    FILE_LIGHT = "./configure/dataSet/Light/BACnet/light.csv"
    FILE_INFLUENCE = u"./configure/dataSet/Influence/ahoえいきょうど_Oct06_スマファシ_行列正しい.csv"
    FILE_STATE = "./configure/state.txt"
    FILE_LIGHT_PATTERN = "./configure/fixedLightPattern.csv"
    FILE_SENSOR_TARGET = "./configure/target.txt"
    FILE_SENSOR_CORRECTION = "../sekonicAnalog/correction_factor.txt"
    FILE_ATTENDANCE = "./configure/attendance.csv"
    FILE_AUTO_ATTENDANCE = "./configure/auto_attendance.csv"
    FILE_OUTSIDE_LIGHT = "./configure/dataSet/OutsideLight/03_外光データ_Oct.10, 1019-1740_晴時々曇.csv"
    FILE_RANK = "./configure/dataSet/Rank/island12_rank.csv"
    DIR_LOG = "../LOG/"

    #####################
    #      照明設定       #
    #####################
    # BACnet型 三菱LEDのデータ
    LIGHT_SIGNAL_MAX = [100, 100]            # 最大点灯信号値
    LIGHT_LUMINOSITY_MAX = [1280.0, 1280.0]  # 最大点灯光度 [cd] [1280]
    LIGHT_SIGNAL_MIN = [10, 10]              # 最小点灯信号値[20]
    LIGHT_LUMINOSITY_MIN = [128.0, 128.0]   # 最小点灯光度 [cd][248.0]
    LIGHT_WAIT_SECOND = 6.5                  # 光度を変更してからの待機時間

    #####################
    # 最適化アルゴリズム設定 #
    #####################
    ALG_WEIGHT = 50000000
    ALG_INITIAL_SIGNAL = 20     # 初期信号値
    ALG_ALLOWANCE_UPPER = 50  # 目標照度収束許容範囲上限（lx指定）[50lx]
    ALG_ALLOWANCE_LOWER = -0.0  # 目標照度収束許容範囲下限（％指定）[0.0]

    # ANA/RC, ANA,DBの設定
    ALG_DB_BRIGHTENING_UPPER = 10.0   # 増光変動幅上限（％指定）[10.0]
    ALG_DB_BRIGHTENING_LOWER = -3.0   # 増光変動幅下限（％指定）[-3.0]
    ALG_DB_NEUTRAL_UPPER = 5.0       # 中立変動幅上限（％指定）[5.0]
    ALG_DB_NEUTRAL_LOWER = -5.0      # 中立変動幅下限（％指定）[5.0]
    ALG_DB_DIMMING_UPPER = 3.0      # 減光変動幅上限（％指定）
    ALG_DB_DIMMING_LOWER = -10.0      # 減光変動幅下限（％指定）[-10.0]
