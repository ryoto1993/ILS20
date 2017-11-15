# coding: utf-8


class INIT:
    #########################
    #   file path config.   #
    #########################
    IES_FILE = u"./IES_file/BACnet.ies"
    IES_INFLUENCE_FILE = "./influence/mh_R.csv"
    IES_LIGHT_FILE = "./light/mh_light.csv"
    IES_SENSOR_FILE = "./Sensor/mh_sensor.csv"

    #########################
    #   IES parser config.  #
    #########################
    IES_LINE_LUMEN = 2   # line which declare flux(lumen) of light
    IES_LINE_ANGLE = 15  # line which declare angle interval
    IES_LINE_DATA = 17   # line of distribution curve data

    #########################
    #   Enironment config.  #
    #########################
    # IES_HEIGHT = 1985
    IES_HEIGHT = 1850
