import pandas as pd
from  datetime import date
import datetime
import matplotlib.pyplot as plt



today = date.today()
day = today.strftime("%Y-%m-%d")
place= "Ettenheim"
year = today.year
month = today.month
day = today.day
path = "weather_data/{}/{}/{}/".format(place, year, month)


days = 16
days_list_detail = []
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
        data.update({"{}-{}-{}".format(y,m,d):pd.read_csv(path)})
    except:
        print("Error data not found", path)
        continue


kw = ["temperatureMax","temperatureMin", "sunhours", "precipitation"]

all_data = []
for k in data.keys():
    for i in range(len(data.keys())):
        print(kw[i])
        dict_m = {(datetime.datetime.strptime(k, '%Y-%m-%d'), kw[i]):[]}
        for idx, d in enumerate(data[k][kw[i]]):
            for key in dict_m.keys():
                dict_m[key].append(d)
        all_data.append(dict_m)
#print(all_data)

x_values_l = []
data_tmin_l = []
data_sunh_l = []
data_rain_l = []
data_tmax_l = []
key_list = []
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

print(key_list)
#import pdb; pdb.set_trace()

fig = plt.figure()
fig.set_figheight(6)
fig.set_figwidth(6)
rows = 4
col = 1
        
ax_sun = plt.subplot2grid(shape=(rows, col), loc=(0, 0), rowspan=1)
ax_r = plt.subplot2grid(shape=(rows, col), loc=(1, 0), rowspan=1, sharex=ax_sun)
ax_tmax = plt.subplot2grid(shape=(rows, col), loc=(2, 0), rowspan=1, sharex=ax_sun)
ax_tmin = plt.subplot2grid(shape=(rows, col), loc=(3, 0), rowspan=1, sharex=ax_sun)



for x_values, data_max, key in zip(reversed(x_values_l), reversed(data_tmax_l), reversed(key_list)):
    ax_tmax.plot(x_values, data_max, label="{}".format(key.strftime("%Y-%m-%d")))

for x_values, data_max, key in zip(reversed(x_values_l), reversed(data_sunh_l), reversed(key_list)):
    ax_sun.plot(x_values, data_max, label="{}".format(key.strftime("%Y-%m-%d")))

for x_values, data_max, key in zip(reversed(x_values_l), reversed(data_tmin_l), reversed(key_list)):
    ax_tmin.plot(x_values, data_max, label="{}".format(key.strftime("%Y-%m-%d")))

for x_values, data_max, key in zip(reversed(x_values_l), reversed(data_rain_l), reversed(key_list)):
    ax_r.plot(x_values, data_max, label="{}".format(key.strftime("%Y-%m-%d")))

#plt.ylabel("temp °C")
#plt.xlabel("day")
#plt.legend()
plt.show()
