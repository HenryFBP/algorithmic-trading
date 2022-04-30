import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from stockLib import *

start = datetime.datetime(2018, 1, 1)
end = datetime.datetime(2022, 4, 1)

car_stock_list = 'TSLA GM F'.split(' ')
nickel_stock_list = 'SBSW MTRN NIC GMKN CNC POS NICK VALE 2362 GLEN BHP RRR' \
    .split(' ')  # YOINK from https://www.finder.com/nickel-mining-stocks
print(nickel_stock_list)

all_stock_list = car_stock_list + \
                 nickel_stock_list

stock_dict = dict()
for stock_ticker in all_stock_list:
    try:
        stock_dict[stock_ticker] = gimme_da_stock_disk_cache(stock_ticker, 'yahoo', start, end)
        print("Got " + stock_ticker + "!")
    except RemoteDataError as rde:
        print(rde)
        stock_dict[stock_ticker] = rde

tesla = stock_dict['TSLA']
gm = stock_dict['GM']
ford = stock_dict['F']

print(tesla.head())
print(gm.head())
print(ford.head())

generate_stock_dfs_graphs([tesla, gm, ford])
