import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import shutil

HKEX_SITE = 'http://www.hkexnews.hk/hyperlink/hyperlist.HTM'
YAHOO_COOKIE = "https://finance.yahoo.com/quote/0001.HK/history"


def init_db():
    print(HKEX_SITE)
    f = requests.get(HKEX_SITE)
    soup = BeautifulSoup(f.text, 'lxml')
    odd_tr_list = soup.find_all('tr', {"class": "ms-rteTableOddRow-BlueTable_ENG"})
    even_tr_list = soup.find_all('tr', {"class": "ms-rteTableEvenRow-BlueTable_ENG"})

    stock_list = ["{:04}.HK".format(int(tr.find_all('td')[0].get_text()))
                  for j, tr in enumerate(sorted(odd_tr_list + even_tr_list, key=lambda tr: tr.find_all('td')[0].get_text()))]
    df = pd.DataFrame(data={"stock": stock_list})
    df.to_csv("hkstock.csv")


if __name__ == '__main__':
    init_db()
