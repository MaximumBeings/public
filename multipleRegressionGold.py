#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:00:09 2017

@author: oluwaseyiawoga
"""

import datetime
import pylab
import pandas as pd
pd.set_option('display.precision', 10)
import matplotlib
matplotlib.style.use('ggplot')
import pandas_datareader.data as web
import statsmodels.api as sm
import warnings
warnings.simplefilter('ignore')
import seaborn
seaborn.mpl.rcParams['figure.figsize'] = (10.0, 6.0)
seaborn.mpl.rcParams['savefig.dpi'] = 90
import random
#"/anaconda3/lib/python3.6/site-packages"

"""
QUESTION - Implement an econometric model for predicting gold price
evolution (use the latest available data). The econometric model can
be ARMA, VAR, VEC, GARCH, Multiple Regression, Bayesian regression,
Machine Learning methods or any other method that you consider suitable.
Explain your model choice for this excercise. Provide the Python code
and the final forecasts.
"""

marketIndices = [
    "^DJI",
    "^GSPC",
    "^GDAXI",
    "^N225",
    "^NSEI",
    "000001.SS"
]


currencyIndices = ["DEXUSEU"]


# def stockDownloader(tickers):
#     downLoadChecker = True
#     while (downLoadChecker):
#         stockData = pd.DataFrame()

#         try:
#             for tick in tickers:
#                 stockData[tick] = web.DataReader(
#                     tick, 'yahoo', start, end)['Close']
#                 stockData.dropna(how='any', axis=0, inplace=True)
#             downLoadChecker = False
#             return stockData
#         except BaseException:
#             random.shuffle(tickers)
#             downLoadChecker = True
            
            
def stockDownloader(tickers):
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
            result = web.DataReader(tick, 'yahoo', start, end)['Close']
            result = pd.DataFrame(result)
            result.columns = [tick]
            stockData = pd.concat([stockData, result], axis=1, join='outer')
        except BaseException:
            pass

    return stockData


"""
All the Above Functions are Called From Below
"""


if __name__ == '__main__':

    """
    Set the start and end dates using datetime function
    """
    start = datetime.datetime(2021, 1, 1)
    end = datetime.datetime.today()

    """
    Download House Price Index from Yahoo
    """

    stockData = stockDownloader(marketIndices)
    stockData.columns = [
        "DOW",
        "S&P",
        "DAX",
        "NIKKEI",
        "NIFTY50",
        "SHANGAI"]

    goldPrices = web.DataReader(["GOLDAMGBD228NLBM"],
                                "fred",
                                start,
                                end)

    goldPrices.dropna(how='any', axis=0, inplace=True)
    goldPrices.columns = ["GOLD"]

    oilPrices = web.DataReader(["DCOILWTICO"],
                               "fred",
                               start,
                               end)
    oilPrices.columns = ["OIL"]

    currencyPrices = web.DataReader(currencyIndices,
                                    "fred",
                                    start,
                                    end)
    currencyPrices.columns = ["USDEUR"]
    currencyPrices.dropna(how='any', axis=0, inplace=True)

    combined = pd.concat(
        [goldPrices, stockData, oilPrices, currencyPrices], axis=1)
    combined.dropna(how='any', axis=0, inplace=True)

    """
    Implement a Multiple variable regression
    """

    y1 = combined['GOLD']
    X = combined.iloc[:, 1:]
    X = sm.add_constant(X)
    model = sm.OLS(y1, X,)

    results = model.fit()

    forecasted = results.fittedvalues

    print("")

    print(forecasted)

    print("")

    print(results.summary())

    """
    Plot Gold & Forecasted Gold Prices
    """
    pylab.plot(forecasted, label="Forecasted Gold Prices")
    pylab.plot(y1, label="Actual Gold Prices")
    pylab.title("Multiple Regression \n Forecasted Gold Prices")
    pylab.legend(loc='best')
    pylab.xlabel("Date")
    pylab.xticks(rotation=45)
    pylab.ylabel("Prices")
    pylab.show()

