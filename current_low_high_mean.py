#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 08:26:33 2022

@author: oluwaseyiawoga
"""



"""
Import Libraries & Packages
"""
import pandas as pd
import datetime
import pandas_datareader.data as web
import numpy as np


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




if __name__ == '__main__':

    """
    Set the start and end dates using datetime function
    """
    
    tickers = sorted(["PTON","AAPL","AMZN","V","MA", "AAL", "DAL", "PYPL","PFE","DFS", "AXP", "SQ","TWTR","FB","ROKU","XOM","MMM","ADBE","COST","GE", "MRNA","MSFT","TSLA", "GOOG", "WMT", "TGT", "NVDA", "CSCO", "BLK","COIN","^DJI", "^IXIC", "^GSPC"])
    
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2022, 2, 22)

    """
    Download Stock Prices & Plot Stock Price Chart
    """
    
    
    stocks = stockDownloader(tickers, 'Adj Close')
    #stocks.dropna(inplace = True)
    
    
    """
    Interpolate Using Linear Methodology.
    """

    stocks.head()
    
    resultsDF = pd.DataFrame()
    high = []
    low = []
    average = []
    current = []
    name = []
    for tick in tickers:
        stocks2 = stocks[tick].dropna()
        name.append(tick)
        high.append(max(stocks2.tolist()))
        low.append(min(stocks2.tolist()))
        average.append(np.mean(stocks2.tolist()))
        current.append(stocks2.tolist()[-1])
        
    resultsDF["Ticker"] = name
    resultsDF["High"] = high
    resultsDF["Low"] = low
    resultsDF["Mean"] = average
    resultsDF["Current"] = current
    resultsDF["Current/High"] = resultsDF["Current"]/resultsDF["High"]
    resultsDF["Current/Low"] = resultsDF["Current"]/resultsDF["Low"]
    resultsDF["Current/Mean"] = resultsDF["Current"]/resultsDF["Mean"]
    

    print()
    print("Dizzle Algorithms Inc - Current Stock Prices Versus Low, Mean and High Stock Prices for Sample Tickers \n [Time Span - 1/1/2020 - 2/22/2022]\n Dizzle Ratings - A MetaSignal Rating Agency")
    print()
    print(resultsDF)
        
        
        
        

    
