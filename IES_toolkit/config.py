# coding: utf-8


class INIT:
    #####################
    #   配光曲線読込設定   #
    #####################
    IES_FILE = "./BACnet.ies"
    IES_LINE_LUMEN = 2  # データ部分で光束が記載されている行
    IES_LINE_ANGLE = 14  # データ部分でアングルが記載されている行
    IES_LINE_DATA = 16  # データ部分で光度が記載されている行