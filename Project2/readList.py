import csv
import re

class ReadList():

    @staticmethod
    def get_city():
        li = []
        with open('./data/cities.csv') as csvin:
            read = [tuple(line) for line in csv.reader(csvin)]
        line = 0
        for row in read:
            if (line != 0):
                for orr in row:
                    li.append(orr)
            line = line + 1
        x = ["city"] * len(li)
        c = list(zip(x,li))

        return c

    @staticmethod
    def get_cus():
        with open('./data/cuisines.csv') as csvine:
            rd = list(csv.reader(csvine))
        y = []
        line = 0
        for rw in rd:
            if (line != 0):
                for kk in rw:
                    ok = re.split("[\{ |\: |\}]",kk)
                    k = list(filter(None, ok))
                    s = ' '.join(k[1:])
                    y.append(s)
            line = line + 1
        xo = ["cuisine"] * len(y)
        cuu = list(zip(xo, y))

        return cuu
