# coding: utf-8


class INIT:
    #####################
    #   ファイルパス設定   #
    #####################
    IES_FILE = u"./IES_file/配光角調節可能ダウンライト/el-d0700l2f1w__led710lm_l_el-x0082w.ies"
    IES_INFLUENCE_FILE = "./influence/r_d700l_31.csv"
    IES_LIGHT_FILE = "./light.csv"
    IES_SENSOR_FILE = "./sensor.csv"

    #####################
    #   配光曲線読込設定   #
    #####################
    IES_LINE_LUMEN = 2  # データ部分で光束が記載されている行
    IES_LINE_ANGLE = 14  # データ部分でアングルが記載されている行
    IES_LINE_DATA = 16  # データ部分で光度が記載されている行

    #####################
    #      環境設定       #
    #####################
    IES_HEIGHT = 1985
