from meteostat import Point, Daily, Stations, Hourly
from datetime import datetime
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from datetime import datetime
import numpy as np

def get_data(lat, longi, year, month, day):
    start = datetime(year, month , day)
    end = datetime(year, month, day)
    # Get closest weather station
    stations = Stations()
    stations = stations.nearby(lat, longi)
    stations = stations.inventory("daily", (start, end))
    station = stations.fetch(1)
    # Get daily data
    data = Daily(station, start, end)
    data = data.fetch()
    return data


def create_frq(x_hours, last_years):
    for h in range(len(x_hours)):
        count = 0
        for last in last_years:
            if last == h:
                count += 1
            x_hours[h]= count
    return x_hours


geolocator = Nominatim(user_agent="weather")
years = ["20{}".format(i) if i > 9 else "200{}".format(i)  for i in range(21)]

now = datetime.today()
now.month, now.day

location = geolocator.geocode("Freiburg")
month = now.month
day = now.day
lat = location.latitude
longi = location.longitude

data_list = []
for year in years:
    data_list.append(get_data(lat, longi, int(year), month, day))

sun_last_years = []
snow_last_years = []
avt_last_years = []
mint_last_years = []
maxt_last_years = []
rain_last_years= []
for d in data_list:
    sun_last_years.append(round(d["tsun"].to_numpy()[0] / 60))
    snow_last_years.append(round(d["snow"].replace(np.nan, 0)))
    rain_last_years.append(round(d["prcp"]).to_numpy()[0])
    avt_last_years.append(round(d["tavg"].to_numpy()[0]))
    mint_last_years.append(round(d["tmin"].to_numpy()[0]))
    maxt_last_years.append(round(d["tmax"].to_numpy()[0]))

min_a = np.min(np.array(avt_last_years))
min_m = np.min(np.array(mint_last_years))
min_ma = np.min(np.array(maxt_last_years))
max_a = np.max(np.array(avt_last_years))
max_m = np.max(np.array(mint_last_years))
max_ma = np.max(np.array(maxt_last_years))
max_r = np.max(np.array(rain_last_years)).astype(np.int)
min_r = np.min(np.array(rain_last_years)).astype(np.int)

a_hours = [0 for i in range(min_a, max_a)]
m_hours = [0 for i in range(min_m, max_m)]
ma_hours = [0 for i in range(min_ma, max_ma)]
r_hours = [0 for i in range(min_r, max_r)]
s_hours= [0 for i in range(16)]




sun_hours = create_frq(s_hours, sun_last_years)
sun_hours_per = np.round(np.array(sun_hours) / len(years), decimals=2)
hours_s = [i for i in range(16)]

rain_hours = create_frq(r_hours, rain_last_years)
rain_hours_per = np.round(np.array(rain_hours) / len(years), decimals=2)
hours_r = [i for i in range(min_r, max_r)]

max_hours = create_frq(ma_hours, maxt_last_years)
maxt_hours_per = np.round(np.array(max_hours) / len(years), decimals=2)
hours_ma = [i for i in range(min_ma, max_ma)]

avt_hours = create_frq(a_hours, avt_last_years)
avt_hours_per = np.round(np.array(avt_hours) / len(years), decimals=2)
hours_a = [i for i in range(min_a, max_a)]


min_hours = create_frq(m_hours, mint_last_years)
mint_hours_per = np.round(np.array(min_hours) / len(years), decimals=2)
hours_m = [i for i in range(min_m, max_m)]



fig = plt.figure()
fig.set_figheight(6)
fig.set_figwidth(6)
rows = 5
col = 1

ax1 = plt.subplot2grid(shape=(rows, col), loc=(0, 0), rowspan=1)
amount =ax1.bar(hours_s, sun_hours, color='b', align='center', alpha=0.1)
ax2 = ax1.twinx()
perc =ax2.bar(hours_s, sun_hours_per, color='g',align='center', alpha=0.8)
plt.ylabel('percent')
plt.legend([amount, perc],['ocurrent last year', 'percent'])


ax3 = plt.subplot2grid(shape=(rows, col), loc=(1, 0), rowspan=1)
amount =ax3.bar(hours_r, rain_hours, color='b', align='center', alpha=0.1)
ax4 = ax3.twinx()
perc =ax4.bar(hours_r, rain_hours_per, color='g',align='center', alpha=0.8)
plt.legend([amount, perc],['rain last {} years'.format(len(years)), 'percent'])


ax5 = plt.subplot2grid(shape=(rows, col), loc=(2, 0), rowspan=1)
amount =ax5.bar(hours_ma, max_hours, color='b', align='center', alpha=0.1)
ax6 = ax5.twinx()
perc =ax6.bar(hours_ma, maxt_hours_per, color='g',align='center', alpha=0.8)
plt.legend([amount, perc],['max temp last {} years'.format(len(years)), 'percent'])

ax7 = plt.subplot2grid(shape=(rows, col), loc=(3, 0), rowspan=1)
amount =ax7.bar(hours_a, avt_hours, color='b', align='center', alpha=0.1)
ax8 = ax7.twinx()
perc =ax8.bar(hours_a, avt_hours_per, color='g',align='center', alpha=0.8)
plt.legend([amount, perc],['ave temp last {} years'.format(len(years)), 'percent'])


ax9 = plt.subplot2grid(shape=(rows, col), loc=(4, 0), rowspan=1)
amount =ax9.bar(hours_m, m_hours, color='b', align='center', alpha=0.1)
ax8 = ax9.twinx()
perc =ax8.bar(hours_m, mint_hours_per, color='g',align='center', alpha=0.8)
plt.legend([amount, perc],['min temp last {} years'.format(len(years)), 'percent'])







plt.show()














