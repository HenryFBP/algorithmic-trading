from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import pandas as pd
import threading
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.bardata = {}  # Initialize dictionary to store bar data

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def tick_df(self, reqId, contract):
        ''' custom function to init DataFrame and request Tick Data '''
        self.bardata[reqId] = pd.DataFrame(columns=['time', 'price'])
        self.bardata[reqId].set_index('time', inplace=True)
        self.reqTickByTickData(reqId, contract, "Last", 0, True)
        return self.bardata[reqId]

    def tickByTickAllLast(self, reqId, tickType, time, price, size, tickAtrribLast, exchange, specialConditions):
        if tickType == 1:
            self.bardata[reqId].loc[pd.to_datetime(time, unit='s')] = price
