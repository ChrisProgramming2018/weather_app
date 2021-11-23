from  datetime import date
from datetime import datetime
import numpy as np
from calendar import monthrange


today = date.today().strftime("%Y-%m-%d")
now = datetime.now()
hour, minute, sec = now.hour, now.minute, now.second

sunhour_month = []
data = []
index = ['01', '02','03','04','05','06','07','08', '09', '10', '11', '12']
sunhour_month = []
num_days = monthrange(2019, 2)[1] # num_days = 28
days_month =[monthrange(2019, i)[1] for i in range(1, 13)  ]

f = open("Sunrise.txt", "r")
for x in f:
    data.append(x.split(';'))

FMT = '%H:%M:%S'
for idx in index:
    temp = []
    for d in data:
        if d[0] == today:
            data_today = d
        if idx == d[0][5:7]:
            end = d[2].replace('.',':')+ ":00"
            start = d[1].replace(',',':')+ ":00"
            #print(end[1:])
            #print(start)
            tdelta = datetime.strptime(end[1:], FMT) - datetime.strptime(start[1:], FMT)
            #print(tdelta)
            temp.append(tdelta)
    month_hour = 0
    for t in temp:
        month_hour += int(t.total_seconds())
    month_hour /=3600
    sunhour_month.append(round(month_hour,2))

sunhour_month = [int(i) for i in sunhour_month]
sunhour_month_average = [ round(i/j,2) for i,j in zip(sunhour_month, days_month)]
print("daylight total month {} ".format(sunhour_month))
print("daylight average per day for each month {} ".format(sunhour_month_average))

rise = data_today[1].replace(',', ':')
start = data_today[1].replace(',',':')+ ":00"
fall = data_today[2].replace('.',':')
end = data_today[2].replace('.',':')+ ":00"
day_length = datetime.strptime(end[1:], FMT) - datetime.strptime(start[1:], FMT)
print("Today {} sunrise at {} and sunfall at {} day length is {} ".format(today, rise, fall, day_length))
