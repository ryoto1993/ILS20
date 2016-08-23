# coding: utf-8


class INIT:
    #####################
    #   ファイルパス設定   #
    #####################
    IES_FILE = "./91820fb_5700k.ies"
    IES_INFLUENCE_FILE = "./downlight_influence.csv"
    IES_LIGHT_FILE = "./downlight.csv"
    IES_SENSOR_FILE = "./sensor.csv"

    #####################
    #   配光曲線読込設定   #
    #####################
    IES_LINE_LUMEN = 2  # データ部分で光束が記載されている行
    IES_LINE_ANGLE = 10  # データ部分でアングルが記載されている行
    IES_LINE_DATA = 12  # データ部分で光度が記載されている行

    #####################
    #      環境設定       #
    #####################
    IES_HEIGHT = 1985
