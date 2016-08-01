# coding:utf-8


class Config:
    def __init__(self):
        #####################
        #      動作モード     #
        #####################
        self.SIMULATION = True

        #####################
        #  機器情報ファイルパス #
        #####################
        self.CD_INFO_FILE = ""
        self.SENSOR_INFO_FILE = ""

        #####################
        #   ファイルパス設定   #
        #####################
        self.SENSOR_FILE = "./configure/sensor.csv"
        self.LIGHT_FILE = "./configure/light.csv"
        self.INFLUENCE_FILE = "./configure/influence.csv"
        self.STATE_FILE = "./configure/state.txt"

        #####################
        # 最適化アルゴリズム設定 #
        #####################
        self.WEIGHT = 10

        #####################
        #   配光曲線読込設定   #
        #####################
        self.IES_FILE = "./BACnet.ies"
        self.IES_LINE_LUMEN = 2   # データ部分で光束が記載されている行
        self.IES_LINE_ANGLE = 14  # データ部分でアングルが記載されている行
        self.IES_LINE_DATA = 16   # データ部分で光度が記載されている行