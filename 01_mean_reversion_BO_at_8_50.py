import logging
import os
import time
from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep
import datetime
import pandas as pd
import pytz
import requests
from bs4 import BeautifulSoup
import yaml

# enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

capital_per_stock = 5000
leverage = 3
trades = []
stock_count = 0
entry_taken = {}


def get_stocks():
    global stock_count, df
    # print('get stocks time :: ', dt.now(tz=zone))
    t = dt.today()

    with requests.Session() as s:
        scanner_url = 'https://chartink.com/screener/vishal-mehta-mean-reversion'
        r = s.get(scanner_url)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf

        process_url = 'https://chartink.com/screener/process'
        payload = {
            'scan_clause': '( {33489} ( latest close > latest sma( close, 200 ) and latest rsi( 2 ) > 50 and '
            'latest close > 1 day ago close * 1.03 and latest close > 50 and latest close < 5000 and latest close > ( 4 days ago close * 1.0 ) ) ) '
        }

        r = s.post(process_url, data=payload)
        data = r.json()['data']
        stock_count = len(data)
        print(f'Total stocks today : {stock_count}')
        if stock_count == 0:
            print('There are no stocks in scanner today, returning')
            return
        df = pd.DataFrame()
        for item in r.json()['data']:
            df = df.append(item, ignore_index=True)
        if len(df) > 0:
            df.sort_values(by=['per_chg'], ascending=False, inplace=True)
            df.drop('sr', axis=1, inplace=True)
            df.reset_index(inplace=True)
            df.drop('index', axis=1, inplace=True)
        print(df)
        df.to_csv(t.strftime('%Y%m%d_') +
                  'mean_reversion_chartink.csv', index=False)


def process_for_mean_reversion():
    global stock_count
    get_stocks()
    # print('process stocks time :: ', dt.now(tz=zone))
    if stock_count == 0:
        print('There were no stocks in scanner today, returning')
        return
    t = dt.today()
    df = pd.read_csv(t.strftime('%Y%m%d_') +
                     'mean_reversion_chartink.csv', index_col=None)
    print(f'number of stocks :: {len(df)}')
    df = df[['nsecode', 'per_chg', 'close']]
    trigger_price = round(0.05*(round(df['close']*1.01, 1)/0.05), 2)
    df['trigger_price'] = trigger_price
    stoploss = round(
        0.05*(round(df['trigger_price']*1.03, 1)/0.05), 2)  # 3% stoploss
    df['stoploss'] = stoploss
    target = round(0.05*round(df['trigger_price']
                   * 0.95, 1)/0.05, 2)      # 5% target
    df['target'] = target
    df['qty'] = capital_per_stock // df['trigger_price']
    df['qty'] = df['qty'].astype(int)
    # df['qty']=1
    if len(df) > 10:
        print('returning only first 10 stocks')
        df = df.head(10)
    df.to_csv(t.strftime('%Y%m%d_')+'mean_reversion.csv')


if __name__ == "__main__":
    process_for_mean_reversion()

