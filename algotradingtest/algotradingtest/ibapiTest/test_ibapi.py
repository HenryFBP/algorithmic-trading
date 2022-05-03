# https://pypi.org/project/ibapi/

import ibapi

# https://algotrading101.com/learn/interactive-brokers-python-api-native-guide/

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)


app = IBapi()
app.connect('127.0.0.1', 7497, 123)
app.run()

import time

time.sleep(2)
app.disconnect()
