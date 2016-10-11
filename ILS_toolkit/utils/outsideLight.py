import csv
from configure.config import *


class OutsideLight:

    data = []


def read_outside_light_data():
    file = open(INIT.FILE_OUTSIDE_LIGHT, 'r')
    c = csv.reader(file)
    for row in c:
        OutsideLight.data.append(row)
    file.close()

    print("OK")

    print(OutsideLight.data)