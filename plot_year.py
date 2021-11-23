import sys
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from  datetime import date


def format_x_date_month_day(ax):   
    # Standard date x-axis formatting block, labels each month and ticks each day
    days = mdates.DayLocator()
    months = mdates.MonthLocator()  # every month
    dayFmt = mdates.DateFormatter('%D')
    monthFmt = mdates.DateFormatter('%Y-%m')
    ax.figure.autofmt_xdate()
    ax.xaxis.set_major_locator(months) 
    ax.xaxis.set_major_formatter(monthFmt)
    ax.xaxis.set_minor_locator(days)

def df_stacked_bar_formattable(df, ax, **kwargs):
    P = []
    lastBar = None

    for col in df.columns:
        print(col)
        X = df.index
        Y = df[col]
        if lastBar is not None:
            P.append(ax.bar(X, Y, bottom=lastBar, **kwargs))
        else:
            #import pdb; pdb.set_trace()
            clrs = ['red' if i.strftime("%Y-%m-%d") == today else 'yellow' for i in X]

            # import pdb; pdb.set_trace()
            P.append(ax.bar(X, Y, color=clrs, **kwargs))
        lastBar = Y
    plt.legend([p[0] for p in P], df.columns)





f = open("Sunrise.txt", "r")
data = []
for x in f:
    data.append(x.split(';'))

day_length = []
for d in data:
    end = d[2].replace('.',':')+ ":00"
    start = d[1].replace(',',':')+ ":00"
    #print(end[1:])
    #print(start)
    FMT = '%H:%M:%S'
    tdelta = datetime.datetime.strptime(end[1:], FMT) - datetime.datetime.strptime(start[1:], FMT)
    day_length.append(round(tdelta.total_seconds()/3600,2))


span_days = 365
start = pd.to_datetime("1-1-2021")
idx = pd.date_range(start, periods=span_days).tolist()

delta= 1
diff = []
for i,d in enumerate(day_length):
    diff.append(day_length[i] - day_length[i-delta])

today = date.today().strftime("%Y-%m-%d")
delta = date(int(today[:4]), int(today[5:7]), int(today[8:])) - date(2021, 1, 1) 
print(delta.days)

df=pd.DataFrame(index=idx, data={'A':day_length, 'B':diff})

# import pdb; pdb.set_trace()
plt.close('all')
fig, ax = plt.subplots(1)
df_stacked_bar_formattable(df, ax)
format_x_date_month_day(ax)
plt.ylim([8,17])
plt.show()
