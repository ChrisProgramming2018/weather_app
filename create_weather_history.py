import datetime
from  datetime import date
import os
import sys
import pandas as pd
import argparse
from data_weather import Weather_data




def main(args):
    """ """
    today = date.today()
    day = today.strftime("%Y-%m-%d")
    place= args.place
    year = today.year
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)
    path = "weather_data/{}/{}/{}/{}.txt".format(place, year, month, day)
    directory = "weather_data/{}/{}/{}".format(place, year, month)
    try:
        os.makedirs(directory, exist_ok = True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print(error)
    if os.path.exists(path):
        print("data already there")
        sys.exit()
    if place == "Ettenheim":
        ws = Weather_data()
    if place == "gran":
        url = "https://www.wetter.com/wetter_aktuell/wettervorhersage/16_tagesvorhersage/spanien/las-galletas/ES2515381.html"
        ws = Weather_data(url)
    if place == "Verbania":
        url = "https://www.wetter.com/wetter_aktuell/wettervorhersage/16_tagesvorhersage/italien/verbania/IT0PI0425.html"
        ws = Weather_data(url)

    days = 16
    days_list = [(datetime.datetime.today() + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    sol_dict = {}
    for key in ws.keywords:
        sol_dict.update({key:[]})

    for idx in range(len(days_list)-1):
        day = days_list[idx]
        next_day = days_list[idx+1]
        ws.get_data(day, next_day)
        for key in ws.sol:
            sol_dict[key].append(ws.sol[key])

    data = pd.DataFrame(sol_dict)
    data.set_axis(days_list[:-1])
    data.to_csv(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--place', type=str, default="Ettenheim", help="Verbania"),
    args = parser.parse_args()
    main(args)
