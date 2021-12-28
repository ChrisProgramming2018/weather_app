import numpy as np
import pandas as pd
from  datetime import date
import datetime
import matplotlib.pyplot as plt
import itertools





def create_mean(days_ordered, data, kw):
    all_data = []
    for k in data.keys():
        for i in range(len(kw)):
            print(k)
            dict_m = {(datetime.datetime.strptime(k, '%d.%m.%Y'), kw[i]):[]}
            for idx, d in enumerate(data[k][kw[i]]):
                for key in dict_m.keys():
                    dict_m[key].append(d)
            all_data.append(dict_m)
    print(days_ordered)
    data_as_list =[]
    x_values_l = []
    data_tmin_l = []
    data_sunh_l = []
    data_rain_l = []
    data_tmax_l = []
    key_list = []
    all_days = []
    for data in all_data:
        for key in data.keys():
            if key[1] == kw[0]:
                metric= key[1]
                key_list.append(key[0])
                data_max = len(data[key])
                data_tmax_l.append(data[key])
                x_values_l.append([(key[0] + datetime.timedelta(days=i)).strftime("%d") for i in range(data_max)])
                all_days.append([(key[0] + datetime.timedelta(days=i)).strftime("%d.%m.%Y") for i in range(data_max)])
                for i in range(data_max):
                    day = (key[0] + datetime.timedelta(days=i)).strftime("%d.%m.%Y")
                    d = data[key][i]
                    data_as_list.append((day, metric, d))
            if key[1] == kw[1]:
                metric= key[1]
                data_max = len(data[key])
                for i in range(data_max):
                    day = (key[0] + datetime.timedelta(days=i)).strftime("%d.%m.%Y")
                    d = data[key][i]
                    data_as_list.append((day, metric, d))



    mean_tmax = []
    mean_tmin = []
    mean_sunh = []
    mean_rain = []
    for day in days_ordered:
        tmp= []
        tmp1= []
        for data in data_as_list:
            #import pdb; pdb.set_trace()
            if data[0] == day and data[1] == kw[0]:
                tmp.append(data[2])
            if data[0] == day and data[1] == kw[1]:
                tmp1.append(data[2])
        mean_tmax.append(tmp)
        mean_tmin.append(tmp1)

    mean_tmax_1 = []
    mean_tmin_1 = []
    mean_sunh_1 = []
    mean_rain_1 = []
    for idx, idx1 in zip(mean_tmax, mean_tmin):
        if len(idx) < 1:
            continue
        mean_tmax_1.append(np.mean(np.array(idx)))
        if len(idx1) < 1:
            continue
        mean_tmin_1.append(np.mean(np.array(idx1)))

    return mean_tmax_1, mean_tmin_1, mean_sunh_1, mean_rain_1
today = date.today()
day = today.strftime("%Y-%m-%d")
place= "Ettenheim"
year = today.year
month = today.month
day = today.day
path = "weather_data/{}/{}/{}/".format(place, year, month)


days = 16
days_list_detail = []
days_ordered = []

for i in range(days):
    day = (datetime.datetime.today() - datetime.timedelta(days=i))
    days_list_detail.append((day.year, day.month, day.day))
days_list = [(datetime.datetime.today() - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]

data = {}
for day in days_list_detail:
    y = day[0]
    m= day[1]
    d= day[2]
    path = "weather_data/{}/{}/{}/{}.txt".format(place, y, m,d)
    try:
        data.update({"{}.{}.{}".format(d,m,y):pd.read_csv(path)})
    except:
        print("Error data not found", path)
        continue

for day in reversed(days_list_detail):
    y = day[0]
    m= day[1]
    d= day[2]
    path = "weather_data/{}/{}/{}/{}.txt".format(place, y, m,d)
    try:
        pd.read_csv(path)
        days_ordered.append("{}.{}.{}".format(d,m,y))
    except:
        print("Error data not found", path)
        continue






for i in range(1, days-1):
    days_ordered.append((datetime.datetime.today() + datetime.timedelta(days=i)).strftime("%d.%m.%Y"))

kw = ["temperatureMax","temperatureMin", "sunhours", "precipitation"]

mean_tmax, mean_tmin, mean_sunh, mean_rain = create_mean(days_ordered, data, kw)


#import pdb; pdb.set_trace()


print(data.keys())
all_data = []
for k in data.keys():
    for i in range(len(kw)):
        print(kw[i])
        #dict_m = {(datetime.datetime.strptime(k, '%Y-%m-%d'), kw[i]):[]}
        dict_m = {(datetime.datetime.strptime(k, '%d.%m.%Y'), kw[i]):[]}
        for idx, d in enumerate(data[k][kw[i]]):
            for key in dict_m.keys():
                dict_m[key].append(d)
        all_data.append(dict_m)
#print(all_data)
print(days_ordered)
x_values_l = []
data_tmin_l = []
data_sunh_l = []
data_rain_l = []
data_tmax_l = []
key_list = []
all_days = {}
for data in all_data:
    for key in data.keys():
        #print(data[key])
        if key[1] == kw[0]:
            key_list.append(key[0])
            data_max = len(data[key])
            data_tmax_l.append(data[key])
            x_values_l.append([(key[0] + datetime.timedelta(days=i)).strftime("%d") for i in range(data_max)])

        if key[1] == kw[1]:
            data_tmin_l.append(data[key])
        if key[1] == kw[2]:
            data_sunh_l.append(data[key])
        if key[1] == kw[3]:
            data_rain_l.append(data[key])





fig = plt.figure()
fig.set_figheight(15)
fig.set_figwidth(15)
rows = 4
col = 1
        
ax_sun = plt.subplot2grid(shape=(rows, col), loc=(0, 0), rowspan=1)
ax_r = plt.subplot2grid(shape=(rows, col), loc=(1, 0), rowspan=1, sharex=ax_sun)
ax_tmax = plt.subplot2grid(shape=(rows, col), loc=(2, 0), rowspan=1, sharex=ax_sun)
ax_tmin = plt.subplot2grid(shape=(rows, col), loc=(3, 0), rowspan=1, sharex=ax_sun)

ax_sun.set_title(kw[2])
ax_r.set_title(kw[3])
ax_tmax.set_title(kw[0])
ax_tmin.set_title(kw[1])

# not so simple need to overlap
#mean_tmax = np.mean(np.array(data_tmax_l), axis=0)

x_values_mean =[]

for do in days_ordered:
    x_values_mean.append(do[:2])
#import pdb; pdb.set_trace()



for x_values, data_max, key in zip(reversed(x_values_l), reversed(data_tmax_l), reversed(key_list)):
    #import pdb; pdb.set_trace()
    line_width = 1.0
    if today.strftime("%Y-%m-%d") == key.strftime("%Y-%m-%d"):
        line_width = 5.0
        ax_tmax.plot(x_values, data_max, linewidth=line_width, color="r", label="{}".format(key.strftime("%Y-%m-%d")))
        continue
    ax_tmax.plot(x_values, data_max, linewidth=line_width, label="{}".format(key.strftime("%Y-%m-%d")))


#import pdb; pdb.set_trace()
print(x_values_mean)
ax_tmax.plot(x_values_mean, mean_tmax, linestyle="--",  linewidth=5, color="b", label="mean")

# ax_tmax.plot(mean_tmax, data_max, label="mean", linestyle='--', color="r")
for x_values, data_max, key in zip(reversed(x_values_l), reversed(data_sunh_l), reversed(key_list)):
    #import pdb; pdb.set_trace()
    line_width = 1.0
    if today.strftime("%Y-%m-%d") == key.strftime("%Y-%m-%d"):
        line_width = 5.0
        ax_sun.plot(x_values, data_max, linewidth=line_width, color="r", label="{}".format(key.strftime("%Y-%m-%d")))
        continue
    ax_sun.plot(x_values, data_max, linewidth=line_width, label="{}".format(key.strftime("%Y-%m-%d")))

for x_values, data_max, key in zip(reversed(x_values_l), reversed(data_tmin_l), reversed(key_list)):
    line_width = 1.0
    if today.strftime("%Y-%m-%d") == key.strftime("%Y-%m-%d"):
        line_width = 5.0
        ax_tmin.plot(x_values, data_max, linewidth=line_width, color="r", label="{}".format(key.strftime("%Y-%m-%d")))
        continue
    ax_tmin.plot(x_values, data_max, linewidth=line_width, label="{}".format(key.strftime("%Y-%m-%d")))

for x_values, data_max, key in zip(reversed(x_values_l), reversed(data_rain_l), reversed(key_list)):
    line_width = 1.0
    if today.strftime("%Y-%m-%d") == key.strftime("%Y-%m-%d"):
        line_width = 5.0
        ax_r.plot(x_values, data_max, linewidth=line_width, color="r", label="{}".format(key.strftime("%Y-%m-%d")))
        continue
    ax_r.plot(x_values, data_max, linewidth=line_width, label="{}".format(key.strftime("%Y-%m-%d")))

#import pdb; pdb.set_trace()
plt.ylabel("temp °C")
plt.xlabel("day")
plt.legend()
plt.show()
