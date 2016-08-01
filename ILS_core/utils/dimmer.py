# coding: utf-8

from configure.config import *


def dimming(lights):
    cdinfo = ""
    for l in lights:
        for sig in l.signals:
            cdinfo += str(sig) + ","

    f = open(INIT.CD_INFO_FILE, "w")
    f.write(cdinfo)
    f.close()