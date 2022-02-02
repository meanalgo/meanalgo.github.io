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
import yaml

# enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

# start of our program
shoonya = ShoonyaApiPy()
pd.set_option('display.width', 1000)

# credentials
# yaml for parameters
with open('cred_pushkar.yml') as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

ret = shoonya.login(userid=cred['user'], password=cred['pwd'], twoFA=cred['factor2'],
                vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])


def exit_all():
    a = shoonya.get_positions()
    a = pd.DataFrame(a)
    print(a)
    a.to_csv('positions_pushkar_02feb2022.csv')
    # print(a.iloc[-1])
    if a.empty:
        print('no positions found, returning empty')
        return
    print(a[['tsym', 'exch', 'prd', 'netqty',
          'token', 'lp', 'urmtom', 'rpnl', 'actid']])
    print(f'realized profit :: {a["rpnl"].astype(float).sum().round(2)}')
    print(f'unrealized mtm :: {a["urmtom"].astype(float).sum().round(2)}')

    # for i in a.itertuples():
    #     a = int(float(i.netqty))
    #     if a < 0:
    #         shoonya.place_order(buy_or_sell='B', product_type='I',
    #                             exchange='NSE', tradingsymbol=i.tysm,
    #                             quantity=i.netqty, discloseqty=0, price_type='MKT', price=0, trigger_price=None,
    #                             retention='DAY', remarks='exit_at_15_15')

    #         print(f'exit order placed in {i.tsym}')

    #         logging.info(f'exit order placed in {i.tsym}')


if __name__ == "__main__":
    exit_all()
