# coding: utf-8

from configure.config import *
import time


def dimming(lights):
    cdinfo = ""
    for l in lights:
        for sig in l.signals:
            cdinfo += str(sig) + ","

    while True:
        try:
            f = open(INIT.FILE_CD_INFO, "w")
            break
        except FileNotFoundError:
            pass
        except PermissionError:
            pass
    f.write(cdinfo)
    f.close()

    time.sleep(INIT.LIGHT_WAIT_SECOND)