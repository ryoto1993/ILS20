import time
import csv

if __name__ == "__main__":
    reader = csv.reader(open("rand.csv", "r"), delimiter=",", quotechar='"')
    data = []

    for index, i in enumerate(reader):
        data.append([])
        for s in range(12):
            data[index].append(i[s])

    for t in range(100):
        cdinfo = ""
        for s in range(12):
            cdinfo += (str(data[t][s]) + ",0,")

        print(data[t])

        while True:
            try:
                f = open("C:/Users/light/Desktop/isdl_20th/bacnet_interface/cdinfo.txt", "w")
                break
            except FileNotFoundError:
                print("can't find \"cdinfo.txt\".")
            except PermissionError:
                print("permission error")
                pass
        f.write(cdinfo)
        f.close()

        time.sleep(10.0)
