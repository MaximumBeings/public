#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 08:27:22 2018

@author: oluwaseyiawoga
"""


"""
Import Libraries & Packages
"""

import csv
import datetime
import datetime as dt
import numpy as np
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader as web
from IPython import get_ipython
import matplotlib.pyplot as plt
import matplotlib
import talib as ta
import talib
from talib.abstract import *
import talib.abstract
matplotlib.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')
pd.set_option('display.precision', 2)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from pylab import rcParams
rcParams['figure.figsize'] = 10, 8
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
pd.options.display.float_format = '{:20,.3f}'.format
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import seaborn
seaborn.mpl.rcParams['figure.figsize'] = (12.0, 8.0)
np.warnings.filterwarnings('ignore')
import pandas as pd
import matplotlib
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn
seaborn.mpl.rcParams['figure.figsize'] = (12.0, 8.0)
np.warnings.filterwarnings('ignore')
from pylab import rcParams
rcParams['figure.figsize'] = 10, 8
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor


def positionCrossOver(df, position):
    """
    Function to Generate Trading Signals.
    Args:
        param1: DataFrame with Input Features and Y_PRED
    Returns:
        A DataFrame of Buy & Sell Positions
    """

    dftoUse = df.copy()
    positionIndices = dftoUse.index

    newEstDict = dict.fromkeys(positionIndices, 0)

    for y in range(len(positionIndices)):
        if position[y] < 0:
            newEstDict[positionIndices[y]] = -10000 / dftoUse['Adj Close'][y]
        else:
            newEstDict[positionIndices[y]] = 0

    newEstDict2 = pd.DataFrame.from_dict(newEstDict, orient='index')
    newEstDict2.columns = ['Sell Position']
    #newEstDict2.set_index('Date', inplace=True)
    newEstDict2.sort_index(inplace=True)

    sellPositionDF = newEstDict2

    positionIndices = dftoUse.index

    newEstDict = dict.fromkeys(positionIndices, 0)

    for y in range(len(positionIndices)):
        if position[y] > 0:
            newEstDict[positionIndices[y]] = 10000 / dftoUse['Adj Close'][y]
        else:
            newEstDict[positionIndices[y]] = 0

    newEstDict2 = pd.DataFrame.from_dict(newEstDict, orient='index')
    newEstDict2.columns = ['Buy Position']
    #newEstDict2.set_index('Date', inplace=True)

    newEstDict2.sort_index(inplace=True)

    buyPositionDF = newEstDict2

    positionFinal = pd.DataFrame()
    positionFinal["Strategy"] = buyPositionDF["Buy Position"] + \
        sellPositionDF["Sell Position"]

    return positionFinal


if __name__ == '__main__':

    """
    Set the ticker of stock to analyze.
    """

    stockToAnalyze = "INTC"

    """
    Set the start and end dates using datetime function
    """
    start = datetime.datetime(2010, 1, 1).strftime("%m/%d/%Y")
    end = datetime.datetime.today().strftime("%m/%d/%Y")

    stock = web.DataReader(stockToAnalyze, 'yahoo', start, end)
    stock["Volume"] = stock["Volume"].astype(float)

    """
    Pass the stock data into a JSON file for
    consumption by ta-lib library
    """

    inputs = {
        'open': stock.Open.values,
        'high': stock.High.values,
        'low': stock.Low.values,
        'close': stock.Close.values,
        'volume': stock.Volume.values
    }

    """
    GENERATE DIFFERENT INDICATORS TO USE
    AS INPUT FEATURES
    """
    """
    Moving Averages
    """

    stock["SMA"] = SMA(inputs, timeperiod=20)
    stock["EMA"] = EMA(inputs, timeperiod=20)

    """
    Momentum Indicators
    """
    stock["ADX"] = ADX(inputs, timeperiod=20)
    macd, macdsignal, macdhist = MACD(
        inputs, fastperiod=12, slowperiod=26, signalperiod=9)
    stock["MACD"] = macd
    stock["RSI"] = RSI(inputs, timeperiod=20)

    """
    Volume Indicators
    """
    stock["AD"] = AD(inputs)
    stock["ADOSC"] = ADOSC(inputs, fastperiod=3, slowperiod=10)
    stock["OBV"] = OBV(inputs)

    """
    Volatility Indicators
    """

    stock["ATR"] = ATR(inputs, timeperiod=14)
    stock["NATR"] = NATR(inputs, timeperiod=14)
    stock["TRANGE"] = TRANGE(inputs)

    """
    Create a list of Indicators Used
    """

    indicatorsUsed = [
        "SMA",
        "EMA",
        "ADX",
        "MACD",
        "RSI",
        "AD",
        "ADOSC",
        "OBV",
        "ATR",
        "NATR",
        "TRANGE"]

    """
    Subset the stock table and delete NaNs - Use "Adj Close" as Target Label
    """

    stockDataToUse = stock[["SMA",
                            "EMA",
                            "ADX",
                            "MACD",
                            "RSI",
                            "AD",
                            "ADOSC",
                            "OBV",
                            "ATR",
                            "NATR",
                            "TRANGE",
                            "Adj Close"]]

    stockDataToUse = stockDataToUse.dropna(how='any', axis=0)

    #X, y = stockDataToUse.iloc[:, 0:-1].values, stockDataToUse.iloc[:, -1].values

    X = stockDataToUse[["SMA", "EMA", "ADX", "MACD", "RSI",
                        "AD", "ADOSC", "OBV", "ATR", "NATR", "TRANGE"]]

    y = stockDataToUse[["Adj Close"]]

#    X_train = X.head(int(len(X)*(70/100))).values
#
#    X_test = X.tail(int(len(X)*(30/100))).values
#
#    y_train = y.head(int(len(y)*(70/100))).values
#
#    y_test = y.tail(int(len(y)*(30/100))).values

    """
    Test and Train Model on Entire X or Independent Labels Using a Simple
    Linear Regression and Normalize the Data Using Standard Scaler
    """

    pipe_lr = make_pipeline(
        Normalizer(), RandomForestRegressor())

    pipe_lr.fit(X, y)
    y_pred = pipe_lr.predict(X)

    print("")
    print("Linear Regression Test Accuracy: ")
    print("")
    print('Test Accuracy: %.3f' % pipe_lr.score(X, y))
    print("")

    toplot = y.copy()
    toplot["y_pred"] = y_pred

    toplot.plot()
    plt.show()

    """
    Classification Machine Learning Methods:
    """

    stockDataToUse = stock[["SMA",
                            "EMA",
                            "ADX",
                            "MACD",
                            "RSI",
                            "AD",
                            "ADOSC",
                            "OBV",
                            "ATR",
                            "NATR",
                            "TRANGE",
                            "Adj Close"]]

    stockDataToUse = stockDataToUse.dropna(how='any', axis=0)

    stockDataToUse2 = stock[["SMA",
                             "EMA",
                             "ADX",
                             "MACD",
                             "RSI",
                             "AD",
                             "ADOSC",
                             "OBV",
                             "ATR",
                             "NATR",
                             "TRANGE",
                             "Adj Close"]]

    stockDataToUse2 = stockDataToUse2.dropna(how='any', axis=0)

    stockDataToUse["ReturnsFlag"] = stockDataToUse["Adj Close"].pct_change()

    """
    Change the return column for adjusted close to a categorical
    vairable of 0s and 1s
    """

    ReturnsClass = []

    for x in stockDataToUse["ReturnsFlag"].values:
        if x > 0:
            ReturnsClass.append(1)
        else:
            ReturnsClass.append(0)

    stockDataToUse["ReturnsClass"] = ReturnsClass

    X = stockDataToUse[["SMA", "EMA", "ADX", "MACD", "RSI",
                        "AD", "ADOSC", "OBV", "ATR", "NATR", "TRANGE"]]

    y = stockDataToUse[["ReturnsClass"]]

    """
    Test and Train Model on Entire X or Independent Labels Using a Simple
    Linear Regression and Normalize the Data Using Standard Scaler
    """

    pipe_lr = make_pipeline(
        Normalizer(), PCA(
            n_components=2), DecisionTreeClassifier())

    pipe_lr.fit(X, y)
    y_pred = pipe_lr.predict(X)

    print("")
    print("Logistic Regression Test Accuracy: ")
    print("")
    print('Test Accuracy: %.3f' % pipe_lr.score(X, y))
    print("")

    print("")
    print("Confusion Matrix of the Ensemble Model: ")
    print("")
    data = metrics.confusion_matrix(y, y_pred)
    confusionMatrix = pd.DataFrame({'Pred: 0': data[:,
                                                    0],
                                    'Pred: 1': data[:,
                                                    1]})
    confusionMatrix["Actual"] = [0, 1]
    confusionMatrix.set_index(confusionMatrix["Actual"], inplace=True)
    del confusionMatrix["Actual"]
    print(confusionMatrix)
    print("")

    """
    Construct a portfolio and use
    buy and hold as the benchmark
    Use the predicted y-values to generate trading
    signal.
    """

    Portfolio = 1000000.00
    Weight = 1
    tradeAmount = 10000.00

    stockDF = pd.DataFrame()

    stockDF["NormalizedReturn"] = stockDataToUse2["Adj Close"] / \
        stockDataToUse2.iloc[0]["Adj Close"]

    stockDF['Allocation'] = stockDF['NormalizedReturn'] * Weight

    stockDF['PositionValues'] = stockDF['Allocation'] * Portfolio

    portfolioValues = pd.DataFrame()

    portfolioValues['PositionValues'] = stockDF['PositionValues'].tolist()

    portfolioValues.columns = ["Ticker"]

    portfolioValues["TotalValue"] = portfolioValues.sum(axis=1)

    portfolioValues.plot(
        figsize=(
            12,
            8),
        title='Ticker & Portfolio Stock Values')

    plt.show()

    dailyReturns = pd.DataFrame()

    dailyReturns['DailyReturns'] = portfolioValues['Ticker'].pct_change(1)

    dailyReturns['PortDailyReturns'] = portfolioValues['TotalValue'].pct_change(
        1)

    dailyReturns.dropna(how='any', axis=0, inplace=True)

    dailyReturns.plot(
        figsize=(
            12,
            8),
        title='Buy Hold & Machine Learning Stock Returns')

    plt.show()

    portfolioValues["UnitOfStocks"] = [
        Portfolio / stockDataToUse2["Adj Close"][0]] * len(portfolioValues)

    portfolioValues["pricePerUnit"] = stockDataToUse2["Adj Close"].tolist()

    portfolioValues["recalculatedStockValue"] = portfolioValues["UnitOfStocks"] * \
        portfolioValues["pricePerUnit"]

    portfolioValues["pricePerUnit"].plot(
        figsize=(
            12,
            8),
        label='Stock Prices',
        legend=True)
    plt.show()

    position = []

    for j in range(len(y_pred)):
        if y_pred[j] == 1:
            position.append(
                1 *
                tradeAmount /
                portfolioValues["pricePerUnit"][j])
        elif y_pred[j] == 0:
            position.append(-1 * tradeAmount /
                            portfolioValues["pricePerUnit"][j])

    shiftedPosition = pd.DataFrame()
    shiftedPosition["Position"] = position

    position = shiftedPosition["Position"].shift(-1).tolist()
    portfolioValues["Positions"] = position

    """
    Call the function to generate buy and hold signals
    """
    A = positionCrossOver(stockDataToUse2, position)
    portfolioValues["Positions"] = A["Strategy"].tolist()

    portfolioValues["RebalancedUnitofStocks"] = portfolioValues["Positions"] + \
        portfolioValues["UnitOfStocks"]

    portfolioValues["rebalancedStockValue"] = portfolioValues["RebalancedUnitofStocks"] * \
        portfolioValues["pricePerUnit"]

    """
    Plot a chart to compare the results
    """
    fig = plt.figure(figsize=(12, 8))

    ax = fig.add_subplot(3, 1, 1)
    plt.title(
        "Machine Learning Signals Strategy Analysis - Position Sizing \n Without Slippages & Commsisions")

    ax.plot(portfolioValues["rebalancedStockValue"],
            label='Rebalanced Portfolio', color="blue")
    ax.set_ylabel('$')
    ax.legend(loc='best')
    ax.grid(True)

    ax = fig.add_subplot(3, 1, 2)

    ax.plot(portfolioValues["recalculatedStockValue"],
            label='Buy & Hold Stock Value', color="red")

    ax.set_ylabel('$')
    ax.legend(loc='best')
    ax.grid(True)

    ax = fig.add_subplot(3, 1, 3)

    ax.plot(portfolioValues["Positions"],
            label='Position', color="green")

    ax.set_ylabel('Position')
    plt.show()

    """
    Generate Results for the Asset & Strategy and Compare them
    Using Plots
    """

    assetLogReturns = pd.DataFrame(
        np.log(portfolioValues["recalculatedStockValue"]).diff())
    assetLogReturns.tail()
    assetLogReturns.columns = ["BuyAndHold"]

    strategyLogReturns = pd.DataFrame(
        np.log(portfolioValues["rebalancedStockValue"]).diff())
    strategyLogReturns.tail(1)
    strategyLogReturns.columns = ["20DEMAReturns"]

    assetLogReturns['CumReturn'] = (
        1 + assetLogReturns["BuyAndHold"]).cumprod() - 1

    strategyLogReturns['CumReturn'] = (
        1 + strategyLogReturns["20DEMAReturns"]).cumprod() - 1

    assetLogReturns["CumReturn"].plot(
        figsize=(
            12,
            8),
        title=("Cummulative Asset Returns"),
        label='Buy & Hold Strategy Returns',
        legend=True)
    strategyLogReturns["CumReturn"].plot(
        figsize=(
            12,
            8),
        title=("Machine Learning Signals Versus Buy & Hold\n Cumulative Returns"),
        label='2Machine Learning Signals Strategy Return',
        legend=True)
    plt.show()

    assetLogReturns['CumReturn'] = (
        1 + assetLogReturns["BuyAndHold"]).cumprod() - 1

    strategyLogReturns['CumReturn'] = (
        1 + strategyLogReturns["20DEMAReturns"]).cumprod() - 1

    assetLogReturns["CumReturn"].plot(
        figsize=(
            12,
            8),
        title=("Cummulative Asset Returns"),
        label='Buy & Hold Strategy Returns',
        legend=True)
    strategyLogReturns["CumReturn"].plot(
        figsize=(
            12,
            8),
        title=("Machine Learning Signals CrossOver Strategy Versus Buy & Hold"),
        label='Machine Learning Signals CrossOver Strategy Strategy Return',
        legend=True)
    plt.show()

    print("")

    print("The Cummulative Return on Buy & Hold is: ")

    print("")

    print(assetLogReturns['CumReturn'].iloc[-1, ])

    print("")

    print("The Cummulative Machine Learning Strategy:")

    print("")

    print(strategyLogReturns['CumReturn'].iloc[-1, ])
"""
Spyder Editor

This is a temporary script file.
"""

