import pandas as pd
import numpy as np
import math
import random
import time

import subprocess
import constants

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end):
    return strTimeProp(start, end, '%d.%m.%Y %H:%M:%S', random.random())

def generate_random_dates():
    number_rows = 2500

    lat_pos = [-20.8, -15.8, -23.55, -27.83333, -22.9, -2.53333, -5.1, -9.4, -12.96667, -5.78333, -30.03333, -15.6, 25.78333, 28.41667, 42.33333, 32.78333, 53.4, 51.5, 48.85, 41.9]
    long_pos = [-49.38333, -47.86667, -46.63333, -48.41667, -47.05, -44.3, -42.8, -40.5, -38.48333, -35.2, -51,23333, -56.1, -80.21667, -81.3, -83.05, -96.8, -2.98333, -0.11667, 2.35, 12.5]
    city_m = random.randint(0, len(lat_pos)-1)
    lat_city_m = lat_pos[city_m]
    long_city_m = long_pos[city_m]
    new_date_m = randomDate("1.1.1930 00:00:00", "1.1.2000 00:00:00")
    date_time_m = new_date_m.split(" ")
    city_f = random.randint(0, len(lat_pos)-1)
    lat_city_f = lat_pos[city_f]
    long_city_f = long_pos[city_f]
    new_date_f = randomDate("1.1.1930 00:00:00", "1.1.2000 00:00:00")
    date_time_f = new_date_f.split(" ")
    df_data = generate_data(1, date_time_m[0], date_time_m[1], lat_city_m, long_city_m, date_time_f[0], date_time_f[1], lat_city_f, long_city_f)
    for x in range(2, number_rows):
        city_m = random.randint(0, len(lat_pos)-1)
        lat_city_m = lat_pos[city_m]
        long_city_m = long_pos[city_m]
        new_date_m = randomDate("1.1.1930 00:00:00", "1.1.2000 00:00:00")
        date_time_m = new_date_m.split(" ")
        city_f = random.randint(0, len(lat_pos)-1)
        lat_city_f = lat_pos[city_f]
        long_city_f = long_pos[city_f]
        new_date_f = randomDate("1.1.1930 00:00:00", "1.1.2000 00:00:00")
        date_time_f = new_date_f.split(" ")
        data = generate_data(x, date_time_m[0], date_time_m[1], lat_city_m, long_city_m, date_time_f[0], date_time_f[1], lat_city_f, long_city_f)
        df_data = df_data.append(data)
        if x % 100 == 0:
            print("Generated {} records".format(x))
    return df_data

def generate_data(index, male_birth_date, male_birth_hour, male_lat, male_longi, female_birth_date, female_birth_hour, female_lat, female_longi):

    cmdLine = "{}/swetest -edir{} -b{} -ut{} -p0123456789DAttt -eswe -house{},{},p -flsj -g, -head".format("sweph", "sweph", male_birth_date, male_birth_hour, male_longi, male_lat)
    p = subprocess.Popen(cmdLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    data = []
    for line in p.stdout.readlines():
        row = line.decode("ASCII").strip().replace(" ","").split(",")
        #print(row)
        data.append(row);
    retval = p.wait()

    longitude1 = []
    speed1 = []
    house_pos1 = []

    longitude2 = []
    speed2 = []
    house_pos2 = []

    # Each line of output data from swetest is exploded into array $row, giving these elements:
    # 0 = longitude
    # 1 = speed
    # 2 = house position
    # planets are index 0 - index (LAST_PLANET), house cusps are index (LAST_PLANET + 1) - (LAST_PLANET + 12)
    for data_line in data:
        longitude1.append(float(data_line[0]))
        speed1.append(float(data_line[1]))
        if len(data_line) > 2:
            house_pos1.append(float(data_line[2]))
        else:
            house_pos1.append(None)

    cmdLine = "{}/swetest -edir{} -b{} -ut{} -p0123456789DAttt -eswe -house{},{},p -flsj -g, -head".format("sweph", "sweph", female_birth_date, female_birth_hour, female_longi, female_lat)
    p = subprocess.Popen(cmdLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    data = []
    for line in p.stdout.readlines():
        row = line.decode("ASCII").strip().replace(" ","").split(",")
        #print(row)
        data.append(row);
    retval = p.wait()

    for data_line in data:
        longitude2.append(float(data_line[0]))
        speed2.append(float(data_line[1]))
        if len(data_line) > 2:
            house_pos2.append(float(data_line[2]))
        else:
            house_pos2.append(None)

    #calculate the Part of Fortune
    #is this a day chart or a night chart?
    day_chart1 = False;
    if longitude1[constants.LAST_PLANET + 1] > longitude1[constants.LAST_PLANET + 7]:
        if (longitude1[0] <= longitude1[constants.LAST_PLANET + 1] and longitude1[0] > longitude1[constants.LAST_PLANET + 7]):
            day_chart1 = True
        else:
            day_chart1 = False
    else:
        if (longitude1[0] > longitude1[constants.LAST_PLANET + 1] and longitude1[0] <= longitude1[constants.LAST_PLANET + 7]):
            day_chart1 = False
        else:
            day_chart1 = True

    if day_chart1:
        longitude1[constants.SE_POF] = longitude1[constants.LAST_PLANET + 1] + longitude1[1] - longitude1[0]
    else:
        longitude1[constants.SE_POF] = longitude1[constants.LAST_PLANET + 1] - longitude1[1] + longitude1[0]

    if longitude1[constants.SE_POF] >= 360:
        longitude1[constants.SE_POF] = longitude1[constants.SE_POF] - 360

    if longitude1[constants.SE_POF] < 0:
        longitude1[constants.SE_POF] = longitude1[constants.SE_POF] + 360

    day_chart2 = False;
    if longitude2[constants.LAST_PLANET + 1] > longitude2[constants.LAST_PLANET + 7]:
        if (longitude2[0] <= longitude2[constants.LAST_PLANET + 1] and longitude2[0] > longitude2[constants.LAST_PLANET + 7]):
            day_chart2 = True
        else:
            day_chart2 = False
    else:
        if (longitude2[0] > longitude2[constants.LAST_PLANET + 1] and longitude2[0] <= longitude2[constants.LAST_PLANET + 7]):
            day_chart2 = False
        else:
            day_chart2 = True

    if day_chart1:
        longitude2[constants.SE_POF] = longitude2[constants.LAST_PLANET + 1] + longitude2[1] - longitude2[0]
    else:
        longitude2[constants.SE_POF] = longitude2[constants.LAST_PLANET + 1] - longitude2[1] + longitude2[0]

    if longitude2[constants.SE_POF] >= 360:
        longitude2[constants.SE_POF] = longitude2[constants.SE_POF] - 360

    if longitude2[constants.SE_POF] < 0:
        longitude2[constants.SE_POF] = longitude2[constants.SE_POF] + 360

    #add a planet - maybe some code needs to be put here

    #capture the Vertex longitude
    longitude1[constants.LAST_PLANET] = longitude1[constants.LAST_PLANET + 16] #Asc = +13, MC = +14, RAMC = +15, Vertex = +16
    longitude2[constants.LAST_PLANET] = longitude2[constants.LAST_PLANET + 16] #Asc = +13, MC = +14, RAMC = +15, Vertex = +16
    #get house positions of planets here
    for x in range(1,12):
        for y in range(0, constants.LAST_PLANET):
            pl = longitude1[y] + (1 / 36000)
            pl = longitude2[y] + (1 / 36000)
            if x < 12 and longitude1[x + constants.LAST_PLANET] > longitude1[x + constants.LAST_PLANET + 1]:
                if (pl >= longitude1[x + constants.LAST_PLANET] and pl < 360) or (pl < longitude1[x + constants.LAST_PLANET + 1] and pl >= 0):
                    house_pos1[y] = x
                    continue
            if x == 12 and longitude1[x + constants.LAST_PLANET] > longitude1[constants.LAST_PLANET + 1]:
                if (pl >= longitude1[x + constants.LAST_PLANET] and pl < 360) or (pl < longitude1[constants.LAST_PLANET + 1] and pl >= 0):
                    house_pos1[y] = x
                continue;
            if pl >= longitude1[x + constants.LAST_PLANET] and pl < longitude1[x + constants.LAST_PLANET + 1] and x < 12:
                house_pos1[y] = x
                continue
            if pl >= longitude1[x + constants.LAST_PLANET] and pl < longitude1[constants.LAST_PLANET + 1] and x == 12:
                house_pos1[y] = x

            if x < 12 and longitude2[x + constants.LAST_PLANET] > longitude2[x + constants.LAST_PLANET + 1]:
                if (pl >= longitude2[x + constants.LAST_PLANET] and pl < 360) or (pl < longitude2[x + constants.LAST_PLANET + 1] and pl >= 0):
                    house_pos2[y] = x
                    continue
            if x == 12 and longitude2[x + constants.LAST_PLANET] > longitude2[constants.LAST_PLANET + 1]:
                if (pl >= longitude2[x + constants.LAST_PLANET] and pl < 360) or (pl < longitude2[constants.LAST_PLANET + 1] and pl >= 0):
                    house_pos2[y] = x
                continue;
            if pl >= longitude2[x + constants.LAST_PLANET] and pl < longitude2[x + constants.LAST_PLANET + 1] and x < 12:
                house_pos2[y] = x
                continue
            if pl >= longitude2[x + constants.LAST_PLANET] and pl < longitude2[constants.LAST_PLANET + 1] and x == 12:
                house_pos2[y] = x


    #define sign based on sun longitude
    sign_num1 = math.floor(longitude1[0] / 30)
    sign_name1 = constants.sign_name[sign_num1]
    sign_num2 = math.floor(longitude2[0] / 30)
    sign_name2 = constants.sign_name[sign_num1]

    porcentages = [ [60, 65, 65, 65, 90, 45, 70, 80, 90, 50, 55, 65, 60], [60, 70, 70, 80, 70, 90, 75, 85, 50, 95, 80, 85, 60],\
                    [70, 70, 75, 60, 80, 75, 90, 60, 75, 50, 90, 50, 70], [65, 80, 60, 75, 70, 75, 60, 95, 55, 45, 70, 90, 65],\
                    [90, 70, 80, 70, 85, 75, 65, 75, 95, 45, 70, 75, 90], [45, 90, 75, 75, 75, 70, 80, 85, 70, 95, 50, 70, 45],\
                    [70, 75, 90, 60, 65, 80, 80, 85, 80, 85, 95, 50, 70], [80, 85, 60, 95, 75, 85, 85, 90, 80, 65, 60, 95, 80],\
                    [90, 50, 75, 55, 95, 70, 80, 85, 85, 55, 60, 75, 90], [50, 95, 50, 45, 45, 95, 85, 65, 55, 85, 70, 85, 50],\
                    [55, 80, 90, 70, 70, 50, 95, 60, 60, 70, 80, 55, 55], [65, 85, 50, 90, 75, 70, 50, 95, 75, 85, 55, 80, 65],\
                    [60, 65, 65, 65, 90, 45, 70, 80, 90, 50, 55, 65, 60]\
                    ]

    porcentage = porcentages[sign_num1][sign_num2]

    #prepare row by creating a dict
    columns = ["m_birth_date", "m_birth_hour", "m_born_lat", "m_born_long", "m_sign", \
                "m_{}".format(constants.pl_name_var[0]), "m_{}".format(constants.pl_name_speed[0]), "m_{}".format(constants.pl_name_house[0]),\
                "m_{}".format(constants.pl_name_var[1]), "m_{}".format(constants.pl_name_speed[1]), "m_{}".format(constants.pl_name_house[1]),\
                "m_{}".format(constants.pl_name_var[2]), "m_{}".format(constants.pl_name_speed[2]), "m_{}".format(constants.pl_name_house[2]),\
                "m_{}".format(constants.pl_name_var[3]), "m_{}".format(constants.pl_name_speed[3]), "m_{}".format(constants.pl_name_house[3]),\
                "m_{}".format(constants.pl_name_var[4]), "m_{}".format(constants.pl_name_speed[4]), "m_{}".format(constants.pl_name_house[4]),\
                "m_{}".format(constants.pl_name_var[5]), "m_{}".format(constants.pl_name_speed[5]), "m_{}".format(constants.pl_name_house[5]),\
                "m_{}".format(constants.pl_name_var[6]), "m_{}".format(constants.pl_name_speed[6]), "m_{}".format(constants.pl_name_house[6]),\
                "m_{}".format(constants.pl_name_var[7]), "m_{}".format(constants.pl_name_speed[7]), "m_{}".format(constants.pl_name_house[7]),\
                "m_{}".format(constants.pl_name_var[8]), "m_{}".format(constants.pl_name_speed[8]), "m_{}".format(constants.pl_name_house[8]),\
                "m_{}".format(constants.pl_name_var[9]), "m_{}".format(constants.pl_name_speed[9]), "m_{}".format(constants.pl_name_house[9]),\
                "m_{}".format(constants.pl_name_var[10]), "m_{}".format(constants.pl_name_speed[10]), "m_{}".format(constants.pl_name_house[10]),\
                "m_{}".format(constants.pl_name_var[11]), "m_{}".format(constants.pl_name_speed[11]), "m_{}".format(constants.pl_name_house[11]),\
                "m_{}".format(constants.pl_name_var[12]), "m_{}".format(constants.pl_name_speed[12]), "m_{}".format(constants.pl_name_house[12]),\
                "m_{}".format(constants.pl_name_var[13]), "m_{}".format(constants.pl_name_speed[13]), "m_{}".format(constants.pl_name_house[13]),\
                "m_{}".format(constants.pl_name_var[14]), "m_{}".format(constants.pl_name_speed[14]), "m_{}".format(constants.pl_name_house[14]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 1]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 1]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 2]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 2]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 3]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 3]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 4]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 4]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 5]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 5]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 6]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 6]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 7]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 7]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 8]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 8]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 9]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 9]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 10]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 10]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 11]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 11]),\
                "m_{}".format(constants.pl_name_var[constants.LAST_PLANET + 12]), "m_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 12]),\
                "f_birth_date", "f_birth_hour", "f_born_lat", "f_born_long", "f_sign", \
                "f_{}".format(constants.pl_name_var[0]), "f_{}".format(constants.pl_name_speed[0]), "f_{}".format(constants.pl_name_house[0]),\
                "f_{}".format(constants.pl_name_var[1]), "f_{}".format(constants.pl_name_speed[1]), "f_{}".format(constants.pl_name_house[1]),\
                "f_{}".format(constants.pl_name_var[2]), "f_{}".format(constants.pl_name_speed[2]), "f_{}".format(constants.pl_name_house[2]),\
                "f_{}".format(constants.pl_name_var[3]), "f_{}".format(constants.pl_name_speed[3]), "f_{}".format(constants.pl_name_house[3]),\
                "f_{}".format(constants.pl_name_var[4]), "f_{}".format(constants.pl_name_speed[4]), "f_{}".format(constants.pl_name_house[4]),\
                "f_{}".format(constants.pl_name_var[5]), "f_{}".format(constants.pl_name_speed[5]), "f_{}".format(constants.pl_name_house[5]),\
                "f_{}".format(constants.pl_name_var[6]), "f_{}".format(constants.pl_name_speed[6]), "f_{}".format(constants.pl_name_house[6]),\
                "f_{}".format(constants.pl_name_var[7]), "f_{}".format(constants.pl_name_speed[7]), "f_{}".format(constants.pl_name_house[7]),\
                "f_{}".format(constants.pl_name_var[8]), "f_{}".format(constants.pl_name_speed[8]), "f_{}".format(constants.pl_name_house[8]),\
                "f_{}".format(constants.pl_name_var[9]), "f_{}".format(constants.pl_name_speed[9]), "f_{}".format(constants.pl_name_house[9]),\
                "f_{}".format(constants.pl_name_var[10]), "f_{}".format(constants.pl_name_speed[10]), "f_{}".format(constants.pl_name_house[10]),\
                "f_{}".format(constants.pl_name_var[11]), "f_{}".format(constants.pl_name_speed[11]), "f_{}".format(constants.pl_name_house[11]),\
                "f_{}".format(constants.pl_name_var[12]), "f_{}".format(constants.pl_name_speed[12]), "f_{}".format(constants.pl_name_house[12]),\
                "f_{}".format(constants.pl_name_var[13]), "f_{}".format(constants.pl_name_speed[13]), "f_{}".format(constants.pl_name_house[13]),\
                "f_{}".format(constants.pl_name_var[14]), "f_{}".format(constants.pl_name_speed[14]), "f_{}".format(constants.pl_name_house[14]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 1]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 1]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 2]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 2]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 3]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 3]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 4]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 4]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 5]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 5]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 6]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 6]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 7]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 7]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 8]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 8]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 9]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 9]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 10]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 10]),
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 11]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 11]),\
                "f_{}".format(constants.pl_name_var[constants.LAST_PLANET + 12]), "f_{}".format(constants.pl_name_speed[constants.LAST_PLANET + 12]),\
                "success_rate"\
                ]
    row_data = [(male_birth_date, male_birth_hour, male_lat, male_longi, sign_name1, \
                longitude1[0], speed1[0], house_pos1[0],\
                longitude1[1], speed1[1], house_pos1[1],\
                longitude1[2], speed1[2], house_pos1[2],\
                longitude1[3], speed1[3], house_pos1[3],\
                longitude1[4], speed1[4], house_pos1[4],\
                longitude1[5], speed1[5], house_pos1[5],\
                longitude1[6], speed1[6], house_pos1[6],\
                longitude1[7], speed1[7], house_pos1[7],\
                longitude1[8], speed1[8], house_pos1[8],\
                longitude1[9], speed1[9], house_pos1[9],\
                longitude1[10], speed1[10], house_pos1[10],\
                longitude1[11], speed1[11], house_pos1[11],\
                longitude1[12], speed1[12], house_pos1[12],\
                longitude1[13], speed1[13], house_pos1[13],\
                longitude1[14], speed1[14], house_pos1[14],\
                longitude1[constants.LAST_PLANET + 1], speed1[constants.LAST_PLANET + 1],\
                longitude1[constants.LAST_PLANET + 2], speed1[constants.LAST_PLANET + 2],\
                longitude1[constants.LAST_PLANET + 3], speed1[constants.LAST_PLANET + 3],\
                longitude1[constants.LAST_PLANET + 4], speed1[constants.LAST_PLANET + 4],\
                longitude1[constants.LAST_PLANET + 5], speed1[constants.LAST_PLANET + 5],\
                longitude1[constants.LAST_PLANET + 6], speed1[constants.LAST_PLANET + 6],\
                longitude1[constants.LAST_PLANET + 7], speed1[constants.LAST_PLANET + 7],\
                longitude1[constants.LAST_PLANET + 8], speed1[constants.LAST_PLANET + 8],\
                longitude1[constants.LAST_PLANET + 9], speed1[constants.LAST_PLANET + 9],\
                longitude1[constants.LAST_PLANET + 10], speed1[constants.LAST_PLANET + 10],\
                longitude1[constants.LAST_PLANET + 11], speed1[constants.LAST_PLANET + 11],\
                longitude1[constants.LAST_PLANET + 12], speed1[constants.LAST_PLANET + 12],\
                female_birth_date, female_birth_hour, female_lat, female_longi, sign_name2, \
                longitude2[0], speed2[0], house_pos2[0],\
                longitude2[1], speed2[1], house_pos2[1],\
                longitude2[2], speed2[2], house_pos2[2],\
                longitude2[3], speed2[3], house_pos2[3],\
                longitude2[4], speed2[4], house_pos2[4],\
                longitude2[5], speed2[5], house_pos2[5],\
                longitude2[6], speed2[6], house_pos2[6],\
                longitude2[7], speed2[7], house_pos2[7],\
                longitude2[8], speed2[8], house_pos2[8],\
                longitude2[9], speed2[9], house_pos2[9],\
                longitude2[10], speed2[10], house_pos2[10],\
                longitude2[11], speed2[11], house_pos2[11],\
                longitude2[12], speed2[12], house_pos2[12],\
                longitude2[13], speed2[13], house_pos2[13],\
                longitude2[14], speed2[14], house_pos2[14],\
                longitude2[constants.LAST_PLANET + 1], speed2[constants.LAST_PLANET + 1],\
                longitude2[constants.LAST_PLANET + 2], speed2[constants.LAST_PLANET + 2],\
                longitude2[constants.LAST_PLANET + 3], speed2[constants.LAST_PLANET + 3],\
                longitude2[constants.LAST_PLANET + 4], speed2[constants.LAST_PLANET + 4],\
                longitude2[constants.LAST_PLANET + 5], speed2[constants.LAST_PLANET + 5],\
                longitude2[constants.LAST_PLANET + 6], speed2[constants.LAST_PLANET + 6],\
                longitude2[constants.LAST_PLANET + 7], speed2[constants.LAST_PLANET + 7],\
                longitude2[constants.LAST_PLANET + 8], speed2[constants.LAST_PLANET + 8],\
                longitude2[constants.LAST_PLANET + 9], speed2[constants.LAST_PLANET + 9],\
                longitude2[constants.LAST_PLANET + 10], speed2[constants.LAST_PLANET + 10],\
                longitude2[constants.LAST_PLANET + 11], speed2[constants.LAST_PLANET + 11],\
                longitude2[constants.LAST_PLANET + 12], speed2[constants.LAST_PLANET + 12],\
                porcentage\
                )]
    singleDF = pd.DataFrame(row_data, columns=columns, index=[index])

    return singleDF
print("Generating data...")
data = generate_random_dates()
print("Saving....")
data.index.name = "record_num"
data.to_csv("data.csv")
