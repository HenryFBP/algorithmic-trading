import shutil
from functools import lru_cache
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Dict
import os

'''
useful stock utils
'''

rectFig = (15, 7)


@lru_cache  # cache so we dont download shit all the time. this is only per-python-repl...
def gimme_da_stock_lru_cache(ticker: str,
                             source: str,
                             start: datetime.datetime,
                             end: datetime.datetime, ) -> pd.DataFrame:
    retDF = web.DataReader(ticker, source, start, end)
    retDF['Stock Ticker'] = ticker
    return retDF


# and this is persistent across disks...
def gimme_da_stock_disk_cache(ticker, source, start, end, cache_folder="./.stock-cache/") -> pd.DataFrame:
    fp = f"{ticker}-{source}-{start}-{end}.cache.csv"

    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)

    fp = cache_folder + fp
    fp = os.path.abspath(fp)

    if os.path.exists(fp):
        print("HIT for {} at {}".format(ticker, fp))
        return pd.read_csv(fp)
    else:
        print("MISS for " + ticker)
        df = gimme_da_stock_lru_cache(ticker, source, start, end)
        df.to_csv(fp, )
        return pd.read_csv(fp)


# khanacademy stats courses -- do it!!!!!
# need calc 1 at least
# if you do any distributions, you must do calc
# R and Stata libs are good


def generate_stock_dfs_graphs(stock_dfs: List[pd.DataFrame], figsize=rectFig, folder=None) -> str:
    stock_names: List[str] = [sdf['Stock Ticker'][0] for sdf in stock_dfs]

    if not folder:
        folder = '-'.join(stock_names)
        folder = "./" + folder
        folder = os.path.abspath(folder)

    print(f"Saving to {folder}.")

    if os.path.exists(folder):
        shutil.rmtree(folder)

    if not os.path.exists(folder):
        os.mkdir(folder)

    # make a simple price graph
    for stock_df in stock_dfs:
        stock_df.set_index('Date', inplace=True)
        stock_df['Open'].plot(x='Date', y='Open', label=stock_df['Stock Ticker'][0], figsize=rectFig)
    plt.legend()
    plt.ylabel("Stock Price in USD")
    plt.xlabel("Date")
    plt.title("Stock prices of {}".format(','.join(stock_names)))
    plt.savefig(os.path.join(folder, 'price.generated.png'))
    plt.close()

    # make a volume graph
    for stock_df in stock_dfs:
        # stock_df.set_index('Date', inplace=True)
        stock_df['Volume'].plot(x='Date', y='Volume', label=stock_df['Stock Ticker'][0], figsize=rectFig)
    plt.legend()
    plt.ylabel("Volume Traded in Stock Units")
    plt.xlabel("Date")
    plt.title("Volume Traded of {}".format(','.join(stock_names)))
    plt.savefig(os.path.join(folder, 'volume.generated.png'))
    plt.close()

    # make a "total traded" graph
    for stock_df in stock_dfs:
        stock_df['Total Traded'] = stock_df['Open'] * stock_df['Volume']
        stock_df['Total Traded'].plot(x='Date', y='Total Traded', label=stock_df['Stock Ticker'][0], figsize=rectFig)
    plt.legend()
    plt.ylabel("Total $USD Traded in Stock Units")
    plt.xlabel("Date")
    plt.title("$USD Traded of {}".format(','.join(stock_names)))
    plt.savefig(os.path.join(folder, 'total_traded_usd.generated.png'))
    plt.close()

    return folder
