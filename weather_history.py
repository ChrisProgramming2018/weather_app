# https://meteostat.net/en/place/3WV0MB?t=2013-01-01/2013-12-31 source of data
import pandas as pd
import datetime
from  datetime import date
import calendar
import os
import numpy as np
import matplotlib.pyplot as plt



class Weather_history():
    def __init__(self, path="/home/programmer/Downloads", place="ettenheim"):
        self.path = path
        self.place = place
        self.all_data = []
        self.years = ["2016","2017","2018","2019","2020"]
        self.data_names = ["tsun", "snow", "tavg", "tmin", "tmax"]
        starting_day_of_current_year = datetime.datetime.now().date().replace(month=1, day=1)
        self.list_of_days = [starting_day_of_current_year + datetime.timedelta(days=i) for i in range(365)]
        self.map_day_to_number = {(day.day, day.month):idx for idx, day in enumerate(self.list_of_days)}
        self.all_sun_data = {i:[] for i in range(366)}

    def init_data(self):
        for year in self.years:
            self.all_data.append(pd.read_csv(os.path.join(self.path, self.place + "_{}.csv".format(year))))
        assert len(self.all_data) == len(self.years) 
        #print(self.all_data[0])
        self.data_of_all = []
        for typ in self.data_names:
            tmp = {i:[] for i in range(366)}
            for y in range(len(self.years)):
                for idx, day in enumerate(self.all_data[y][typ]):
                    #print(day)
                    tmp[idx].append(day)
            self.data_of_all.append(tmp)
    
    def get_history(self, day, typ="sun"):
        idx = 0
        if typ == "tsun":
            idx=0
        elif typ == "snow":
            idx=1
        elif typ == "tavg":
            idx=2
        elif typ == "tmin":
            idx=3
        else:
            idx=4
        print("typ {} use {} ".format(typ, idx))
        return self.data_of_all[idx][self.map_day_to_number[(day.day, day.month)]]

    def show_data(self, next_days):
        days_list = []
        today = date.today()
        data = []
        for d in range(next_days):
            day =  today + datetime.timedelta(days=d) 
            days_list.append(day)
            print(day)
            day = self.map_day_to_number[(day.day, day.month)]
            print(day)
            tmp = []
            for t in range(len(self.data_names)):
                tmp.append(np.mean(self.data_of_all[t][day]))
                #print(self.data_of_all[t][day])
            data.append(tmp)
        print(data)
        sun_data = []
        snow_data = []
        min_t_data = []
        max_t_data = []
        avg_t_data = []
        for d in data:
            sun_data.append(d[0]/ 60)
            snow_data.append(d[1])
            avg_t_data.append(d[2])
            min_t_data.append(d[3])
            max_t_data.append(d[4])
        
        self.fig = plt.figure()
        self.fig.set_figheight(6)
        self.fig.set_figwidth(6)
        self.ax_tmp = plt.subplot2grid(shape=(2, 1), loc=(1,0), rowspan=1)
        self.ax_w = plt.subplot2grid(shape=(2, 1), loc=(0,0), rowspan=1)
        
        self.ax_tmp.plot(days_list, avg_t_data, label="avg tmp", color="yellow")
        self.ax_tmp.plot(days_list, min_t_data, label="avg min", color="blue")
        self.ax_tmp.plot(days_list, max_t_data, label="avg max", color="red")
        self.ax_tmp.legend()
        self.ax_w.bar(days_list, sun_data, color="yellow", label="sunshine")
        self.ax_w.bar(days_list, snow_data, color="white", label="snow")
        self.ax_w.set_title("Sun and snow next 7 days")
        self.ax_w.set_ylabel("hours")
        plt.show()
        return 




if __name__ == "__main__":
    today = date.today()
    wh = Weather_history()
    wh.init_data()
    for t in wh.data_names:
        print(wh.get_history(today, t))
    wh.show_data(7)
