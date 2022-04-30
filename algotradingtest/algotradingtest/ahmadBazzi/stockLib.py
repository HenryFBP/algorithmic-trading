from functools import lru_cache
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Dict
import os
import logging

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
    fp = cache_folder + fp
    fp = os.path.abspath(fp)

    os.makedirs(fp)

    if os.path.exists(fp):
        logging.info("HIT for {} at {}".format(ticker, fp))
        return pd.read_csv(fp)
    else:
        logging.info("MISS for " + ticker)
        df = gimme_da_stock_lru_cache(ticker, source, start, end)
        df.to_csv(fp, )
        return pd.read_csv(fp)


def generate_stock_dfs_graphs(stock_dfs: List[pd.DataFrame], figsize=rectFig, folder=None) -> str:
    if not folder:
        folder = '-'.join(sdf['Stock Ticker'][0] for sdf in stock_dfs)
        folder = "./" + folder
        folder = os.path.abspath(folder)

    print(f"Saving to {folder}.")
    if not os.path.exists(folder):
        os.mkdir(folder)

    for stock_df in stock_dfs:
        #
        pass



    return folder
