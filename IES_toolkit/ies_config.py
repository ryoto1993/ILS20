# coding: utf-8


class INIT:
    #####################
    #   ファイルパス設定   #
    #####################
    IES_FILE = u"./IES_file/導入可能ダウンライト/三菱_EL-D3000M3W/el-d3000m2f3w_ahz_led2910lm_m_.ies"
    IES_INFLUENCE_FILE = "./influence/三菱_EL-D3000M3W.csv"
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
