import re
from bs4 import BeautifulSoup
import datetime
from  datetime import date
import requests


url = "https://sonnenuntergang-sonnenaufgang.info/freiburg"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

def write_into_file(res, day):
    res = re.findall(r'\d+', res)
    text = "{}; {},{}; {}.{};\n".format(day,res[0],res[1],res[2],res[3])
    path= "Sunrise"
    f = open(path + ".txt", 'a+')
    f.write(text)

start_date = datetime.datetime( 2021, 1, 1 ).strftime("%Y-%m-%d")
for day in range(365):
    date = datetime.datetime( 2021, 1, 1 ) + datetime.timedelta(days=day)
    date = date.strftime("%Y-%m-%d")
    print(date)
    found  =text.find(date)
    res = text[found+10:found+100]
    write_into_file(res, date)

