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
for d in data_list:
    sun_last_years.append(round(d["tsun"].to_numpy()[0] / 60))


sun_last_years_pre = np.array(sun_last_years) / len(years)

unique, counts = np.unique(sun_last_years, return_counts=True)
sun_hours= [0 for i in range(18)]
for h in range(18):
    count = 0
    for last in sun_last_years:
        if last == h:
            count += 1
    sun_hours[h]= count

sun_hours_per = np.round(np.array(sun_hours) / len(years), decimals=2 )

hours = [i for i in range(18)]


ax1 = plt.subplot(1,1,1)
w = 0.3
#plt.xticks(), will label the bars on x axis with the respective country names.
#plt.xticks(x + w /2, datasort['country'], rotation='vertical')
amount =ax1.bar(hours, sun_hours, color='b', align='center', alpha=0.1)
#The trick is to use two different axes that share the same x axis, we have used ax1.twinx() method.
ax2 = ax1.twinx()
#We have calculated GDP by dividing gdpPerCapita to population.
perc =ax2.bar(hours, sun_hours_per, color='g',align='center', alpha=0.8)
#Set the Y axis label as GDP.
plt.ylabel('percent')
#To set the legend on the plot we have used plt.legend()
plt.legend([amount, perc],['ocurrent last year', 'percent'])
#To show the plot finally we have used plt.show().
plt.show()















