# YOINK from https://blog.devgenius.io/algorithmic-trading-backtesting-a-strategy-in-python-3a136be16ece

# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pyfolio as pf
import datetime as dt
import pandas_datareader.data as web
import os
import warnings

# print all outputs
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# downloading historical necessary data for backtesting and analysis
_start = dt.date(2015, 1, 2)
_end = dt.date(2020, 4, 30)
ticker = 'MSFT'
df = yf.download(ticker, start=_start, end=_end)

# calculating buy and hold strategy returns
df['bnh_returns'] = np.log(df['Adj Close']/df['Adj Close'].shift(1))
df.head(3)
