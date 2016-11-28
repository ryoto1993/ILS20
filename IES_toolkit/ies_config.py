# coding: utf-8


class INIT:
    #####################
    #   ファイルパス設定   #
    #####################
    IES_FILE = u"./IES_file/導入可能ダウンライト/大光電機/91820fb_5700k.ies"
    IES_INFLUENCE_FILE = "./influence/INF1850_t-layout_大光電機_91820fb_5700k.csv"
    IES_LIGHT_FILE = "./light.csv"
    IES_SENSOR_FILE = "./Sensor/t-layout/sensor.csv"

    #####################
    #   配光曲線読込設定   #
    #####################
    IES_LINE_LUMEN = 2  # データ部分で光束が記載されている行
    IES_LINE_ANGLE = 10  # データ部分でアングルが記載されている行
    IES_LINE_DATA = 12  # データ部分で光度が記載されている行

    #####################
    #      環境設定       #
    #####################
    # IES_HEIGHT = 1985
    IES_HEIGHT = 1850
