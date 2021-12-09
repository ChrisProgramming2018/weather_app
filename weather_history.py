# https://meteostat.net/en/place/3WV0MB?t=2013-01-01/2013-12-31 source of data
import pandas as pd
import datetime
from  datetime import date
import calendar
import os
import numpy as np




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
        today = date.today()
        data = []
        for d in range(next_days):
            day =  today + datetime.timedelta(days=d) 
            print(day)
            day = self.map_day_to_number[(day.day, day.month)]
            print(day)
            for t in range(len(self.data_names)):
                print(self.data_of_all[t][day])


        return 
        self.fig = plt.figure()
        self.fig.set_figheight(6)
        self.fig.set_figwidth(6)
        self.ax_sim = plt.subplot2grid(shape=(4, 1), loc=(0,0), rowspan=1)
        import pdb; pdb.set_trace()




if __name__ == "__main__":
    today = date.today()
    wh = Weather_history()
    wh.init_data()
    for t in wh.data_names:
        print(wh.get_history(today, t))
    wh.show_data(7)
