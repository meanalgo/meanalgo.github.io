from api_helper import ShoonyaApiPy
import logging 
import pandas as pd

#enable dbug to see request and responses 
 
logging.basicConfig(level=logging.DEBUG)

 
#start of our program
 
shoonya = ShoonyaApiPy()

 
pd.set_option('display.width',1000)

 
#credentials
 
user        = 'FA30940'
 
pwd       = 'Chillal01@'
 
factor2     = 'BSMPC4047C'

vc          = 'FA30940_U' 
 
app_key     = 'APILi04122021ASDJIUSAHD123'

 
imei        = 'abc1234'

ret = shoonya.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)

import datetime 
from datetime import datetime as dt 
if str(dt.now().strftime('%X'))>str(datetime.time(15,15)):
	a=shoonya.get_positions()

	a=pd.DataFrame(a)

	for i in a.itertuples():
		a=int(float(i.netqty))
		if a<0:             
			shoonya.place_order(buy_or_sell='B', product_type='I',
					exchange='NSE', tradingsymbol=i.tysm, 
					quantity=i.netqty, discloseqty=0,price_type='MKT', price=0, trigger_price=None,
					retention='DAY', remarks='my_order_001')

			print(f'exit order placed in {i.tsym}')

			logging.info(f'exit order placed in {i.tsym}')
