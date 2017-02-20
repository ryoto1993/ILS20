# coding: utf-8

import time

from configure.config import INIT


# cdinfo.txtに直書きする方式
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
            print("can't find \"cdinfo.txt\".")
        except PermissionError:
            print("permission error")
            pass
        f.write(cdinfo)
        f.close()

    time.sleep(INIT.LIGHT_WAIT_SECOND)