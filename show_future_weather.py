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
        dict_m = {datetime.datetime.strptime(k, '%Y-%m-%d'):[]}
        for idx, d in enumerate(data[k][kw[i]]):
            for key in dict_m.keys():
                dict_m[key].append(d)
    all_data.append(dict_m)
#print(all_data)
x_values_l = []
data_max_l = []
key_list = []
for data in all_data:
    for key in data.keys():
        key_list.append(key)
        data_max = len(data[key])
        data_max_l.append(data[key])
        x_values_l.append([(key + datetime.timedelta(days=i)).strftime("%d") for i in range(data_max)])

print(key_list)



for x_values, data_max, key in zip(reversed(x_values_l), reversed(data_max_l), reversed(key_list)):
    plt.plot(x_values, data_max, label="{}".format(key.strftime("%Y-%m-%d")))
plt.ylabel("temp °C")
plt.xlabel("day")
plt.legend()
plt.show()
