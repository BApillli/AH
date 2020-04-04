import csv
import re

class ReadList():
    """
        This class is used to read in lists of the cities and 
        cuisines from their respective csv files.
    """

    @staticmethod
    def get_city():

        city_list = []
        with open('./data/cities.csv') as city_csv:
            read_city = [tuple(line) for line in csv.reader(city_csv)]
        line = 0
        for row in read_city:
            if (line != 0):
                for city_name in row:
                    city_list.append(city_name)
            line = line + 1
        #x = ["city"] * len(city_list)
        #cit = list(zip(x,city_list))
        cit = list(zip(city_list,city_list))

        return cit

    @staticmethod
    def get_cus():

        with open('./data/cuisines.csv') as cus_csv:
            read_cus = list(csv.reader(cus_csv))
        cus_list = []
        line = 0
        for row in read_cus:
            if (line != 0):
                for rw in row:
                    cus_name = re.split("[\{ |\: |\}]",rw)
                    k = list(filter(None, cus_name))
                    s = ' '.join(k[1:])
                    cus_list.append(s)
            line = line + 1
        #x = ["cuisine"] * len(cus_list)
        #cus = list(zip(x, cus_list))
        cus = list(zip(cus_list, cus_list))

        return cus