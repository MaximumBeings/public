"""
Import Libraries & Packages
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pandas as pd
import datetime
import pandas_datareader.data as web


import os
import matplotlib.pyplot as plt
import mpld3
import matplotlib.ticker as mticker
from pandas_datareader import data as pdr
import copy
plt.style.use('ggplot')
from datetime import datetime
#import backtrader as bt
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import warnings
plt.style.use('seaborn')
#plt.rcParams['figure.figsize'] = [9, 5]
plt.rcParams['figure.dpi'] = 90
warnings.simplefilter(action='ignore', category=FutureWarning)
import base64
import glob
import logging
logging.getLogger('matplotlib.font_manager').disabled = True
from datetime import date
import warnings
warnings.filterwarnings("ignore")

#import alpaca_trade_api as tradeapi
#from alpacaConfig import APCA_API_KEY_ID, APCA_API_SECRET_KEY

#api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, 'https://paper-api.alpaca.markets')
import pandas as pd
import datetime
import time



tickers = ['^DJI','MMM', 'AXP', 'AAPL','BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DOW', 'XOM', 'GS', 'HD', 'INTC', 'IBM', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'RTX', 'UNH', 'VZ', 'V', 'WBA', 'WMT', 'DIS']

def stockDownloader(tickers, Data):
    """
    Function to download stock prices from Yahoo!.
    Args:
        param1: list of tickers and data - column to download
    Returns:
        A Dataframe of stock prices for the tickers .
    """
    d = pd.date_range(start, end, freq='D')
    stockData = pd.DataFrame(index=d)
    for tick in tickers:
        try:
            result = web.DataReader(tick, 'yahoo', start, end)[Data]
            result = pd.DataFrame(result)
            result.columns = [tick]
            stockData = pd.concat([stockData, result], axis=1, join='outer')
        except BaseException:
            pass

    return stockData

def getAggsHelper(sym,multiplier,day,start,end):
    columns = ['Date', 'Close']
    res = []
    symbol_aggs = api.get_aggs(sym,1,'day',start,end)
    length = len(symbol_aggs)
    for x in range(0,length):
        symbol_aggSet = symbol_aggs[x]._raw
        date = symbol_aggSet['timestamp']/1000
        date=datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
        close = symbol_aggSet['close']
        list = [date,close]
        res.append(list)
    df = pd.DataFrame(res, columns=columns)
    df.set_index('Date', inplace=True)
    return df

def getAggs(symbol,multiplier, timeSpan, start, end):
    columns = ['Date', 'Close']
    res = []
    symbol_aggs = api.get_aggs(symbol[0],1,'day',start,end)
    length = len(symbol_aggs)
    for x in range(0,length):
        symbol_aggSet = symbol_aggs[x]._raw
        date = symbol_aggSet['timestamp']/1000
        date=datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
        close = symbol_aggSet['close']
        list = [date,close]
        res.append(list)
    df = pd.DataFrame(res, columns=columns)
    df.set_index('Date', inplace=True)
    df.columns = [symbol[0]]
    for sym in symbol[1:]:
        try:
            result = getAggsHelper(sym,1,'day',start,end)
            result.columns = [sym]
            df = pd.concat([df, result], axis=1, join='outer')
        except BaseException:
            pass
    return df




if __name__ == '__main__':

    """
    Set the start and end dates using datetime function
    """

    start = datetime.datetime(2020, 6, 1)
    end = datetime.datetime(2020, 9, 3)

    """
    Download Stock Prices & Plot Stock Price Chart
    """


    sample = stockDownloader(tickers, 'Adj Close')


    """
    Interpolate Using Linear Methodology.
    """

    sample = sample.interpolate(method='linear')
    print(sample)

    # stocks.fillna(value=0, inplace = True)

    # stocks.to_csv('SPData.csv')

    # d = pd.read_csv('SPData.csv', index_col = 0)

    #stocks.dropna(inplace=True)
    #print(stocks.tail(50))
    # tickers = ['^DJI','MMM', 'AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DOW', 'XOM', 'GS', 'HD', 'INTC', 'IBM', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'TRV', 'RTX', 'UNH', 'VZ', 'V', 'WBA', 'WMT', 'DIS']
    # start = '2020-06-01'
    # end = '2020-09-03'
    # sample = getAggs(tickers,1, 'day', start, end)
    # sample = sample.interpolate(method='linear')
    # print(sample.tail(50))


    """
    https://www.apress.com/us/book/9781484238721
    """
    import pprint
    stock1 = '^DJI'
    last_distance_from_index = {}
    temp_series1 = sample[stock1].pct_change().cumsum()
    for stock2 in list(sample):
    # no need to process itself
        if (stock2 != stock1):
            temp_series2 = sample[stock2].pct_change().cumsum()
            # we are subtracting the stock minus the index, if stock is strong compared
            # to index, we assume a postive value
            diff = list(temp_series2 - temp_series1)
            last_distance_from_index[stock2] = diff[-1]

    print()
    pprint.pprint(last_distance_from_index)

    weakest_symbol = min(last_distance_from_index.items(), key=lambda x: x[1])
    print('Weakest symbol: %s' % weakest_symbol[0])

    strongest_symbol = max(last_distance_from_index.items(), key=lambda x: x[1])
    print('Strongest symbol: %s' % strongest_symbol[0])

    trading_budget = 10000

    # get last trading price for both stocks
    short_symbol = strongest_symbol[0]
    short_last_close = sample[strongest_symbol[0]][-1]
    print('Strongest symbol %s, last price: $%f' % (strongest_symbol[0], short_last_close))

    long_symbol = weakest_symbol[0]
    long_last_close = sample[weakest_symbol[0]][-1]
    print('Weakest symbol %s, last price: $%f' % (weakest_symbol[0], long_last_close))
    print('For %s, at $%f, you need to short %i shares' %(short_symbol, short_last_close, (trading_budget * 0.5) / short_last_close ))
    print('For %s, at $%f, you need to buy %i shares' %(long_symbol, long_last_close, (trading_budget * 0.5) / long_last_close ))

    long_trade_df = sample[long_symbol].pct_change().cumsum()
    short_trade_df = sample[short_symbol].pct_change().cumsum()
    index_symbol = ['^DJI']
    index_df = sample[index_symbol[0]].pct_change().cumsum()

    fig, ax = plt.subplots()


    ax.plot(long_trade_df.index, long_trade_df, label='go long ' + long_symbol)
    ax.plot(long_trade_df.index, short_trade_df, label='go short ' + short_symbol)
    ax.plot(long_trade_df.index, index_df, label='index bench ' + index_symbol[0])
    legend = ax.legend(loc='upper center', shadow=True)

    plt.suptitle('Above: ' + short_symbol + ', Below: ' + long_symbol + ', Index:' + index_symbol[0])

    # add zero line
    ax.axhline(y=0, color='green', linestyle='-')

    # rotate dates
    myLocator = mticker.MultipleLocator(2)
    ax.xaxis.set_major_locator(myLocator)
    fig.autofmt_xdate()

    # fix label to only show first and last date
    labels = ['' for item in ax.get_xticklabels()]
    labels[1] = temp_series2.index[0]

    # labels[int(len(labels)/2)] = temp_series2.index[int(len(labels)/2)]
    labels[-2] = temp_series2.index[-1]
    ax.set_xticklabels(labels)

    fig.savefig("pairsT.png")
