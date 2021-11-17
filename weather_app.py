import sys
import os
import datetime
from  datetime import date
import re
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import argparse
import calendar
import numpy as np


def save_history_file(sunhours):
    """ """
    today = date.today()
    path = datetime.datetime.today().strftime("%Y/%m")
    filename = datetime.datetime.today().strftime("%B")
    print("path ", path)
    print("filename ", filename)
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")
    keyword = "sunhours"
    path = os.path.join(path, filename)
    print("path ", path)
    last_line = None
    try:
        f = open(path + ".txt", 'r')
        content = f.read().splitlines()
        last_line = content[-1]
        print("last line : {}".format(last_line))
    except:
        print("File {}.txt not found ".format(path))
    day = datetime.datetime.today().strftime("%d-%m-%Y")
    text = "{}:_{}".format(day, sunhours)
    if text == last_line:
        print("to add ")
        print(text)
        print("alreay added")
        return
    text += "\n"
    f = open(path + ".txt", 'a+')
    f.write(text)
    print("text ", text)


def show_sunhours(sunhour_dict, day):
    """ """ 
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    days, hours = [], [] 
    for idx in sunhour_dict:
        days.append(idx)
        hours.append(sunhour_dict[idx])
    ax.bar(days, hours)
    #x_string = tuple(days)
    s = [x for x in range(len(days))]
    print(s)
    ax.set_xticks(ticks=days)
    ax.set_yticks(np.arange(0, 81, 10))
    # ax.legend()
    plt.savefig("Sunhours_{}".format(day))
    # plt.show()


def find_sunhours(res_sub, keyword):
    """ """
    s = re.search('}',res_sub)
    res_sub = res_sub[:s.start()]
    sun_idx = res_sub.find(keyword)
    res_sub =  res_sub[sun_idx:]
    s = re.search(':',res_sub)
    res_sub = res_sub[s.start()+1:]
    
    return int(res_sub)


def main(args):
    today = date.today()
    weekday = calendar.day_name[today.weekday()] 
    day = datetime.datetime.today().strftime("%d-%m-%Y")
    save_day = day
    print("Today is {} the {}".format(weekday, day))
    url = args.url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="chartdiv-16")
    string_text =  str(results.format_string)
    days = args.days
    keyword = "sunhours"
    sunhour_dict = {}
    for i in range(days):
        day_1 = datetime.datetime.today() + datetime.timedelta(days=i)
        next_Date = datetime.datetime.today() + datetime.timedelta(days=i+1)
        next_Date = next_Date.strftime("%Y-%m-%d")
        day = day_1.strftime("%Y-%m-%d")
        print(next_Date)
        found = re.search(day, string_text)
        found_1 = re.search(next_Date, string_text)
        res_sub = string_text[found.start():found_1.start()]
        hours = find_sunhours(res_sub, keyword)
        if i == 0:
            save_history_file(hours)
        sunhour_dict.update({calendar.day_name[day_1.weekday()]:hours})

    show_sunhours(sunhour_dict, save_day)






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, default= "https://www.wetter.com/wetter_aktuell/wettervorhersage/16_tagesvorhersage/deutschland/ettenheim/DE0002757.html")
    parser.add_argument('--days', type=int, default= 5)
    args = parser.parse_args()
    main(args)
