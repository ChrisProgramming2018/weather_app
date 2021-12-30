import sys
from time import sleep
from  datetime import date
from datetime import datetime, timedelta
import numpy as np
from calendar import monthrange, month_name




class Sunhours():
    def __init__(self):
        self.today = date.today().strftime("%Y-%m-%d")
        self.tomorrow= (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        now = datetime.now()
        self.hour, self.minute, self.sec = now.hour, now.minute, now.second
        self.sunhour_month = []
        self.data = []
        self.index = ['01', '02','03','04','05','06','07','08', '09', '10', '11', '12']
        self.sunhour_month = []
        self.num_days = monthrange(2019, 2)[1] # num_days = 28
        self.days_month =[monthrange(2019, i)[1] for i in range(1, 13)  ]
        self.FMT = '%H:%M:%S'
        self.longest_day = ""
        self.shortest_day = ""
        self.times = []
        for i in range(8 ,17):
            self.times.append(timedelta(hours=i))
            self.times.append(timedelta(hours=i, minutes=30))
        self.first_day= []
        self.second_day = []
        self.current_interval= None
        self.intervals = []
    
    def check_interval(self, tdelta, current_day):
        old_current_time = self.current_time
        for t in self.times:
            if tdelta > t:
                self.current_time = t
                # break
        if old_current_time != self.current_time:
            self.intervals.append("change from {} to {} at {} ".format(old_current_time, self.current_time, current_day))
        # print("current time ", self.current_time)

    
    def read_data(self):
        f = open("Sunrise.txt", "r")
        for x in f:
            self.data.append(x.split(';'))
        d = self.data[0]
        end = d[2].replace('.',':')+ ":00"
        start = d[1].replace(',',':')+ ":00"
        sd = datetime.strptime(end[1:], self.FMT) - datetime.strptime(start[1:], self.FMT)
        ld = sd
        for t in self.times:
            if sd > t:
                self.current_time = t
                break
        # import pdb; pdb.set_trace()
        # loop of each month
        for idx in self.index:
            temp = []
            # loop over data
            for d in self.data:
                if d[0] == self.today:
                    data_today = d
                if d[0] == self.tomorrow:
                    data_tomorrow = d
                if idx == d[0][5:7]:
                    end = d[2].replace('.',':')+ ":00"
                    start = d[1].replace(',',':')+ ":00"
                    tdelta = datetime.strptime(end[1:], self.FMT) - datetime.strptime(start[1:], self.FMT)
                    self.check_interval(tdelta, d[0])
                    #print(d[0])
                    #print("current time ", self.current_time)
                    if tdelta > ld:
                        ld = tdelta
                        #import pdb; pdb.set_trace()
                        self.longest_day ="longest day is at {}  with {} hours".format(d[0], ld)

                    if tdelta < sd:
                        sd = tdelta
                        self.shortest_day = "Shortest day is at {} with {} hours".format(d[0],sd)
                    temp.append(tdelta)
            month_hour = 0
            for t in temp:
                month_hour += int(t.total_seconds())
            month_hour /=3600
            self.sunhour_month.append(round(month_hour,2))

        self.sunhour_month = [int(i) for i in self.sunhour_month]
        self.sunhour_month_average = [ round(i/j,2) for i,j in zip(self.sunhour_month, self.days_month)]

        self.rise = data_today[1].replace(',', ':')
        start = data_today[1].replace(',',':')+ ":00"
        self.sun_rise = data_today[1].replace(',',':')+ ":00"
        self.fall = data_today[2].replace('.',':')
        self.sun_fall = data_today[2].replace('.',':') + ":00"
        end = data_today[2].replace('.',':')+ ":00"
        self.day_length = datetime.strptime(end[1:], self.FMT) - datetime.strptime(start[1:], self.FMT)
        self.sun_rise_t = data_tomorrow[1].replace(',',':')+ ":00"
        end_interval = []
        for inter in self.intervals[:int(len(self.intervals) /2)]:
            end_interval.append(inter[-6:])
            #print("int ", inter)
        #print("sec")
        start_interval = []
        for inter in reversed(self.intervals[int(len(self.intervals) /2):]):
            start_interval.append(inter[-6:])
        #print(len(self.times), len(start_interval)) 
        for t,s,e  in zip(self.times, start_interval, end_interval) :
            m = s[:2]
            m1 = month_name[int(m)]
            m = e[:2]
            m2 = month_name[int(m)]
            print("Time under {} start {} {} and ends {} {} ".format(t,s[-3:], m1,e[-3:], m2))
    
    def time_of_day_hour(self, seconds):
        for s in range(seconds):
            now = datetime.now()
            current_time = "{}:{}:{}".format(now.hour, now.minute, now.second)
            # 3 cases 
            # first before sun rise

            # import pdb; pdb.set_trace() 
            diff =  datetime.strptime(self.sun_rise[1:], self.FMT) - datetime.strptime(current_time, self.FMT)
            diff2 =  datetime.strptime(self.sun_fall[1:], self.FMT) - datetime.strptime(current_time, self.FMT)
            if diff.total_seconds() > 0:
                text = "Time is {} and time to sun rise {} of {} \r ".format(current_time, diff, self.day_length)
            #case to sun is out
            elif diff2.total_seconds() > 0 and diff.total_seconds() < 0:
                text = "Time is {} and time to sun down {} of {} \r ".format(current_time, diff2, self.day_length)
            else:
                rest_of_day = datetime.strptime("23:59:59", self.FMT) - datetime.strptime(current_time, self.FMT)
                # import pdb; pdb.set_trace() 
                time_until_tomorrow = datetime.strptime(self.sun_rise_t[1:], self.FMT) + rest_of_day 
                #print(rest_of_day)
                #print(time_until_tomorrow[10:])
                text = "\n Time is {} and time to sun up {} of {} \r ".format(current_time, time_until_tomorrow.time(), self.day_length)
            print(text, end='\r', flush=True)
            #import pdb; pdb.set_trace() 
            # case 3 the sun was up and is now down time to next day TODO: 
            # print("Time is {} and time to sun down {} ".format(current_time, diff2))
            #diff = datetime.strptime(end[1:], self.FMT) - datetime.strptime(start[1:], self.FMT)
            sleep(1)
        #tdelta = datetime.strptime(end[1:], self.FMT)
        




if __name__ == "__main__":
    s = Sunhours()
    s.read_data()
    print("Today {} sunrise at {} and sunfall at {} day length is {} ".format(s.today, s.rise, s.fall, s.day_length))
    print("daylight total month {} ".format(s.sunhour_month))
    print("daylight average per day for each month {} ".format(s.sunhour_month_average))
    print(s.longest_day)
    print(s.shortest_day)
    s.time_of_day_hour(10)
