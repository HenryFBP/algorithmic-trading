

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
