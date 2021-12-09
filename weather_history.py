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
        for tyP in self.data_names:
            tmp = {i:[] for i in range(366)}
            for y in range(len(self.years)):
                for idx, day in enumerate(self.all_data[y]["tsun"]):
                    #print(day)
                    tmp[idx].append(day)
            self.data_of_all.append(tmp)
    def get_history(self, day, typ="sun"):
        return self.data_of_all[0][self.map_day_to_number[(day.day, day.month)]]




if __name__ == "__main__":
    today = date.today()
    wh = Weather_history()
    wh.init_data()
    print(wh.get_history(today))
