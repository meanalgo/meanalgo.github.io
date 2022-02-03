from api_helper import ShoonyaApiPy
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
logging.basicConfig(level=logging.DEBUG, filename=__file__+".log")

# start of our program
shoonya = ShoonyaApiPy()
pd.set_option('display.width', 1000)

# credentials
# yaml for parameters
with open('cred_rahul.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = shoonya.login(userid=cred['user'], password=cred['pwd'], twoFA=cred['factor2'],
                vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])


def place_bracket_orders():
    #print('place Limit orders time :: ', dt.now(tz=zone))
    t = dt.today()
    df = pd.read_csv(t.strftime('data/%Y%m%d_') +
                     'mean_reversion.csv', index_col=None)

    for stock in df.itertuples():
        print(stock.nsecode, stock.qty, stock.trigger_price,
              stock.target, stock.stoploss)
        trade = shoonya.place_order(buy_or_sell='S', product_type='B',
                                    exchange='NSE', tradingsymbol=f'{stock.nsecode}-EQ',
                                    quantity=stock.qty, discloseqty=0, price_type='LMT', price=stock.trigger_price-0.1, trigger_price=stock.trigger_price,
                                    retention='DAY', remarks='entry_at_09_15', bookloss_price=stock.stoploss, bookprofit_price=stock.target)


if __name__ == "__main__":
    place_bracket_orders()
    shoonya.logout()
