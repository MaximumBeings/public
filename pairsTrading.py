#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 07:37:50 2018

@author: oluwaseyiawoga
"""

"""
Import Libraries & Packages
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime
import pandas_datareader.data as web
from statsmodels.tsa.stattools import adfuller
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
from dateutil.relativedelta import relativedelta
pd.options.display.float_format = '{:20,.3f}'.format
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import seaborn
seaborn.mpl.rcParams['figure.figsize'] = (12.0, 8.0)
from sklearn import linear_model
np.warnings.filterwarnings('ignore')
import random


"""
. Study the above for Dow Jones Transportation Average
  and Dow Jones Industrial Average.

. Make a note of the technical indicator panels provided
  – The stochastic and the Moving Average Convergence Divergence (MACD).

. Using all the technical information available, provide a pairs trading
  recommendation. Provide concrete reasoning to support your choice. Did
  the Stochastics and MACD help you in deciding on the direction of pairs
  trade? If not, which indicator would have been ideal?

. Write a Python program to download data for Dow Jones Transportation
  Average and Dow Jones Industrial Average for the last 5 Years.

. Create and calculate any one indicator that would allow you to decide on
  making a pairs trade between these 2 indices.

. Based on the historical values of that indicator, calculate and graphically
  represent the return profile of a pairs trading strategy
"""


def stockDownloader(tickers):
    downLoadChecker = True
    while (downLoadChecker):
        stockData = pd.DataFrame()

        try:
            for tick in tickers:
                stockData[tick] = web.DataReader(
                    tick, 'yahoo', start, end)['Adj Close']
                stockData.dropna(how='any', axis=0, inplace=True)
            downLoadChecker = False
            return stockData
        except BaseException:
            random.shuffle(tickers)
            downLoadChecker = True


def fitModel(stockData):
    """
    Function to generate Linear Regression fit.
    Args:
        param1: Regression Data
    Returns:
        A linear model fit.
    """
    y = np.array(stockData["DJI"])
    x = np.array(stockData["DJT"])
    x = x.reshape(len(x), 1)
    y = y.reshape(len(y), 1)
    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    return regr


def adFullerTest(timeSeries):
    """
    Function to Perform Augmented Dickey Fuller Test.
    Args:
        param1: Arrays
    Returns:
        Prints to console Whether a timeseries is Stationary or not
    """

    result = adfuller(timeSeries)

    print("")
    print('Augmented Dickey-Fuller Test:')
    labels = [
        'ADF Test Statistic',
        'p-value',
        'No. of Lags Used',
        'Number of Observations Used']

    print("")
    for value, label in zip(result, labels):
        print(label + ' : ' + str(value))

    if result[1] <= 0.05:
        print("Strong Evidence Against the Null Hypothesis, Reject the Null Hypothesis. Data has no Unit Root and is Stationary")
        print("")
    else:
        print("Weak Evidence Against Null Hypothesis, Time Series has a Unit Root, indicating it is Non-stationary ")
        print("")


"""
All the Above Functions are Called From Below
"""


if __name__ == '__main__':

    """
    Set the start and end dates using datetime function
    """

    tickers = ['^DJI', '^DJT']

    end = datetime.datetime.today()
    start = end - relativedelta(years=5)

    """
    Download S&P Data into a DataFrame
    """
    stockData = stockDownloader(tickers)
    stockData.columns = ['DJI', 'DJT']

    """
    Plot the Stock Price Evolution
    """
    stockData["DJI"].plot(
        figsize=(
            12,
            8),
        title='DJI Stock Prices', legend=True)

    stockData["DJT"].plot(
        figsize=(
            12,
            8),
        title='DJI Versus DJT Stock Prices', legend=True)

    plt.show()
    plt.close()

    """
    Calculate the correlation between the two stock prices
    """

    stockCorrelation = stockData["DJI"].corr(stockData["DJT"])

    """
    Calculate Stock returns and drop NAs
    """
    daily_returns = stockData.pct_change()
    daily_returns.dropna(how='any', axis=0, inplace=True)

    """
    Calculate the correlation between the two stock returns
    """

    returnsCorrelation = daily_returns["DJI"].corr(daily_returns["DJT"])

    print("")

    print("The Stock Correlation is: ")

    print("")

    print(stockCorrelation)

    print("")

    print("The Returns Correlation is:")

    print("")

    print(returnsCorrelation)

    daily_returns.plot(
        title="Plot of Disney Returns Versus S&P (Daily)",
        figsize=(
            12,
            8))
    plt.show()

    """
    Using SKLEARN & Linear Regression calculate the spread using
    the formula below

    s = y - bX

    Alternatively this could have been calculated as
    s = Price of Instrument A/ Price of Instrument B
    """
    regr = fitModel(stockData)

    m = regr.coef_[0]
    b = regr.intercept_

    stockData['SpreadRegMethod'] = stockData['DJI'] - m[0] * stockData['DJT']

    Fig, ax = plt.subplots()
    ax.plot(stockData["SpreadRegMethod"])
    ax.axhline(
        stockData["SpreadRegMethod"].mean(),
        color="orange",
        label="Mean")
    ax.legend(loc="best")
    plt.title(
        'DJI-DJT Spread Regression Method\n s = DJI - (Regression Coefficient * DJT)')
    plt.show()
    plt.close()

    """
    Calculate Spread Using the Alternative Formula
    s = Price of Instrument A/Price of Instrument B
    """

    stockData["SpreadAltMethod"] = stockData['DJI'] / stockData['DJT']

    Fig, ax = plt.subplots()
    ax.plot(stockData["SpreadAltMethod"])
    ax.axhline(
        stockData["SpreadAltMethod"].mean(),
        color="orange",
        label="Mean")
    ax.legend(loc="best")
    plt.title('DJI-DJT Spread Alternative Method\n DJI/DJT')
    plt.show()
    plt.close()

    """
    Test for Stationarity
    """
    adFullerTest(stockData['DJI'].dropna())
    adFullerTest(stockData['DJT'].dropna())

    stockData['DJIFirstDifference'] = stockData['DJI'] - \
        stockData['DJI'].shift(1)
    adFullerTest(stockData['DJIFirstDifference'].dropna())

    stockData['DJTFirstDifference'] = stockData['DJT'] - \
        stockData['DJT'].shift(1)
    adFullerTest(stockData['DJTFirstDifference'].dropna())
    
    
    """
    Calculate the Rolling Covariance, Rolling Variance & Rolling
    Beta and Plot the Chart
    """

    rollingCovariance = stockData[['DJI', 'DJT']].rolling(
        window=30).cov(stockData[['DJI', 'DJT']], pairwise=True)
    idx = pd.IndexSlice
    rollingCovariance = rollingCovariance.loc[idx[:, 'DJI'], 'DJT']
    rollingCovariance = rollingCovariance.reset_index(level=1)

    rollingVariance = stockData['DJT'].rolling(window=252).var()
    stockData['rollingBeta'] = rollingCovariance['DJT'] / rollingVariance

    Fig, ax = plt.subplots()
    ax.plot(stockData["rollingBeta"])
    ax.axhline(m, color="orange", label="Constant Beta")
    ax.legend(loc="best")
    plt.title('DJI-DJT Spread Alternative Method\n DJI/DJT')
    plt.show()
    plt.close()
    
    """
    Calculate the Rolling Spread Using
    spread = DJI - Coefficient * DJT
    This will be used to estimate the Z Score and the Pairs Trading
    Signal and Pairs Trading Positions.
    """

    stockData['rollingSpread'] = stockData['DJI'] - \
        stockData['rollingBeta'] * stockData['DJT']

    Fig, ax = plt.subplots()
    ax.plot(stockData['rollingSpread'])
    ax.legend(loc="best")
    plt.title('DJI-DJT Rolling Spread')
    plt.show()
    
    """
    Calculate the Z Score Using a 30 day window and shift it forward by 1 
    and 2 data points
    Using the rolling spread and plot the charts
    """

    stockData['zScore'] = (stockData['rollingSpread'] - stockData['rollingSpread'].rolling(
        window=30).mean()) / stockData['rollingSpread'].rolling(window=30).std()

    Fig, ax = plt.subplots()
    ax.plot(stockData['zScore'], label="Z Score")
    ax.axhline((-2), color="green")
    ax.axhline((-1), color="green", linestyle='--')
    ax.axhline((2), color="red")
    ax.axhline((1), color="red", linestyle='--')
    ax.legend(loc="best")
    plt.suptitle('DJI-DJT Rolling Spread Z-Score')
    plt.show()

   
    stockData['ZScoreShiftedOne'] = stockData['zScore'].shift(1)
    stockData['ZScoreShiftedTwo'] = stockData['zScore'].shift(2)
    signal = 0.0
    temp = []
    for x in range(len(stockData)):
        if stockData['ZScoreShiftedTwo'][x] > - \
                2 and stockData['ZScoreShiftedTwo'][x] < -2:
            signal = -2
        elif stockData['ZScoreShiftedTwo'][x] < -1 and stockData['ZScoreShiftedOne'][x] > -1:
            signal = -1
        elif stockData['ZScoreShiftedTwo'][x] < 2 and stockData['ZScoreShiftedOne'][x] > 2:
            signal = 2
        elif stockData['ZScoreShiftedTwo'][x] > 1 and stockData['ZScoreShiftedOne'][x] < 1:
            signal = 1
        else:
            signal = 0
        temp.append(signal)

    stockData['integerSignal'] = temp

    Fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(stockData['zScore'])
    ax[0].axhline((-2), color="green")
    ax[0].axhline((-1), color="green", linestyle='--')
    ax[0].axhline((2), color="red")
    ax[0].axhline((1), color="red", linestyle='--')
    ax[0].legend(loc="best")
    ax[1].plot(stockData['integerSignal'], marker='o', linestyle='')
    ax[1].legend(loc='best')
    plt.suptitle('DJI-DJT Trading Strategy Signals')
    plt.show()

    position = 0
    stockData['Position'] = 0
    temp = []
    for x in range(len(stockData)):
        if stockData['integerSignal'][x] == -2:
            position = 1
        elif stockData['integerSignal'][x] == -1:
            position = 0
        elif stockData['integerSignal'][x] == 2:
            position = -1
        elif stockData['integerSignal'][x] == 1:
            position = 0
        else:
            position = stockData['integerSignal'][x - 1]
        temp.append(position)
    stockData['Position'] = temp

    Fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(stockData['zScore'])
    ax[0].axhline((-2), color="green")
    ax[0].axhline((-1), color="green", linestyle='--')
    ax[0].axhline((2), color="red")
    ax[0].axhline((1), color="red", linestyle='--')
    ax[0].legend(loc="upper left")
    ax[1].plot(stockData['Position'], marker='o', linestyle='')
    ax[1].legend(loc='best')
    plt.title('DJI-DJT Trading Strategy Positions')
    plt.show()
    
    """
    Compare Buy & Hold Strategy and Pairs Trading Strategy
    The return of the Buy & Hold is the addition of the returns of 
    DJI and DJT.
    
    The Pairs Trading Strategy Returns is increased/decreased by the
    Position Signal
    """
    
    
    returnsTable = pd.DataFrame()
    returnsTable['noPairsTrading'] = daily_returns['DJI'] + \
        daily_returns['DJT']

    returnsTable['SpreadReturn'] = (stockData['SpreadAltMethod']).pct_change()[1:]

    returnsTable['PairsTrading'] = returnsTable['noPairsTrading'] + \
        (returnsTable['SpreadReturn'] * stockData['Position'][1:])

    returnsTable['CumReturnNoPairsTrading'] = (
        1 + returnsTable["noPairsTrading"]).cumprod() - 1

    returnsTable['CumReturnPairsTrading'] = (
        1 + returnsTable["PairsTrading"]).cumprod() - 1

    returnsTable['CumReturnNoPairsTrading'].plot(
        figsize=(
            12,
            8),
        title=("Cummulative Asset Returns"),
        label='Buy & Hold',
        legend=True)
    returnsTable['CumReturnPairsTrading'].plot(
        figsize=(
            12,
            8),
        title=("Cummulative Returns - Buy & Hold Versus Pairs Trading"),
        label='Pairs Trading',
        legend=True)
    plt.show()
    
    print("")

    print("The Cummulative Return on Buy & Hold Is: ")

    print("")

    print(returnsTable['CumReturnNoPairsTrading'][-1])

    print("")

    print("The Cummulative Return on Pairs Trading Is:")

    print("")
    
    print(returnsTable['CumReturnPairsTrading'][-1])


   
