#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:37:05 2018

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
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
from dateutil.relativedelta import relativedelta
pd.options.display.float_format = '{:20,.3f}'.format
import scipy as sp


import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""
QUESTIONS:
    1. Write a Python program to download the historical data
    of WMT Inc. (WMT) and Target Inc (TGT) for the last 3 years.

    2. Calculate the daily return for WMT and TGT and present a
    comparative graphical analysis.

    3. Calculate and graphically represent the expected return for
    each of the stocks. To do this, we have to calculate the average
    of the daily returns of the period being analyzed and then annualize.

    4. Calculate the Standard Deviation of the portfolio. The used stocks
    on the portfolio are correlated, so remember to use the appropriate
    Variance formula (reference the PDF for that formula if needed).

    5. The United States Treasury Bonds are known as risk free because
    they always pay. For this analysis, a 5-year bond will be considered
    with an annual rate of 1.72%.  How does the return profile of the
    current portfolio compare to one that is consisting solely of
    Treasury Bonds?

    6. How does the Risk Profile of the two compare?  Use Python to
    print a comparative analysis of the two portfolio in terms of all
    the major KPIs taught in this course.
"""


def calc_annual_returns(daily_returns):
    """Function to Calculate Annual Returns From Daily Returns.
    Args:
        param1: Daily Returns
    Returns:
        A dataframe of Annual Returns.
    """
    grouped = daily_returns.groupby(lambda date: date.year).sum()
    return grouped


def geo_mean(iterable):
    a = np.array(iterable)
    return a.prod()**(1.0 / len(a))


def barPlot(objects, performance, title, ylabel):
    y_pos = np.arange(len(objects))

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def winLossCalculator(portfolioValues):
    win = 0.0
    for x in portfolioValues.columns[:-1]:
        if portfolioValues[x][-1] - portfolioValues[x][0] > 0:
            win = win + 1

    loss = 0.0
    for x in portfolioValues.columns[:-1]:
        if portfolioValues[x][-1] - portfolioValues[x][0] < 0:
            loss = loss + 1

    return(win, loss)


def AveWinLossCalculator(portfolioValues):
    win = []
    for x in portfolioValues.columns[:-1]:
        if portfolioValues[x][-1] - portfolioValues[x][0] > 0:
            win.append(portfolioValues[x][-1] - portfolioValues[x][0])
    if len(win) == 0:
        win.append(0)

    loss = []
    for x in portfolioValues.columns[:-1]:
        if portfolioValues[x][-1] - portfolioValues[x][0] < 0:
            loss.append(portfolioValues[x][-1] - portfolioValues[x][0])
    if len(loss) == 0:
        loss.append(0)

    return(np.mean(win), np.mean(loss))


"""
All the Above Functions are Called From Below
"""
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
            result = web.DataReader(tick, 'yahoo',start, end)["Adj Close"]
            result = pd.DataFrame(result)
            result.columns = [tick]
            stockData = pd.concat([stockData, result], axis=1, join='outer')
        except BaseException:
            pass

    return stockData

if __name__ == '__main__':

    Portfolio = 1000000

    """
    Set the start and end dates using datetime function
    """
    end = datetime.datetime.today()
    start = end - relativedelta(years=3)
    
    start = '2015-01-01'
    end = '2020-12-31'
    tickers = ["WMT", "TGT"]
    final = stockDownloader(tickers)
    final = final.interpolate(method='linear')
    final.dropna(inplace=True)
    
    """
    Set the tickers for the market indices
    """

    

    """
    Download Stock Prices & Plot Stock Price Chart
    """
    WMT = final[["WMT"]]

    TGT = final[["TGT"]]

    for stockDF in (WMT, TGT):
        stockDF["NormalizedReturn"] = stockDF / stockDF.iloc[0]

    for stockDF, allocation in zip([WMT, TGT], [0.5, 0.5]):
        stockDF['Allocation'] = stockDF['NormalizedReturn'] * allocation

    for stockDF in [WMT, TGT]:
        stockDF['PositionValues'] = stockDF['Allocation'] * Portfolio

    portfolioValues = pd.concat(
        [WMT['PositionValues'], TGT['PositionValues']], axis=1)

    portfolioValues.columns = tickers

    portfolioValues["TotalValue"] = portfolioValues.sum(axis=1)

    portfolioValues.plot(
        figsize=(
            8,
            6),
        title='WMT, TGT & Portfolio Stock Values')

    plt.show()

    dailyReturns = pd.DataFrame()

    dailyReturns['WMTDailyReturns'] = portfolioValues['WMT'].pct_change()

    dailyReturns['TGTDailyReturns'] = portfolioValues['TGT'].pct_change()

    dailyReturns['PortDailyReturns'] = portfolioValues['TotalValue'].pct_change()

    dailyReturns.dropna(how='any', axis=0, inplace=True)

    dailyReturns.plot(
        figsize=(
            8,
            6),
        title='WMT, TGT & Portfolio Stock Returns')

    plt.show()
    """
    Expected Returns:
        Annualized Daily Returns
        Assumes 252 days in a year
    """

    WMTER = dailyReturns['WMTDailyReturns'].mean() * 252

    TGTER = dailyReturns['TGTDailyReturns'].mean() * 252

    PortER = dailyReturns['PortDailyReturns'].mean() * 252

    objects = ('WMT', 'TGT', 'Portfolio')

    performance = [WMTER, TGTER, PortER]

    barPlot(
        objects,
        performance,
        "Expected Returns - Portfolio",
        "Expected Returns")

    PortfolioSTD = dailyReturns['PortDailyReturns'].std()

    """
    Comparison of Portfolio return to USA Treasury over 3 years.
    """
    """
    Simple Comparison: Portfolio Return Minus Treasury Rate
    """

    Treasury = 1.72 / 100
    PortER

    SimpleCompare = PortER - Treasury

    print("")

    print("The Excess Return of Portfolio Over Tresury Using Simple Average Return is: ")

    print("")

    print(SimpleCompare)

    """
    Comparison By Year
    """
    CompByYear = pd.DataFrame()
    CompByYear["WMT"] = calc_annual_returns(
        dailyReturns['WMTDailyReturns'])
    CompByYear["TGT"] = calc_annual_returns(
        dailyReturns['TGTDailyReturns'])
    CompByYear["Portfolio"] = calc_annual_returns(
        dailyReturns['PortDailyReturns'])
    CompByYear["Portfolio"] = calc_annual_returns(
        dailyReturns['PortDailyReturns'])
    CompByYear["Treasury"] = [Treasury, Treasury, Treasury,Treasury, Treasury, Treasury]
    CompByYear["Excess"] = CompByYear["Portfolio"] - CompByYear["Treasury"]

    print("")

    print("The Excess Return of Portfolio Over Treasury by Year is: ")

    print("")

    print(CompByYear)

    print("")

    CompByYear.plot(
        figsize=(
            8,
            6),
        title='Returns Comparison - Treasury Versus Portfolio')
    plt.show()

    """
    Geometric Comparison: Portfolio Return Minus Treasury Rate
    """
    from functools import reduce
    import operator
    #from cmath import log, e
    
    data = CompByYear["Portfolio"].tolist()
    PortERGM = reduce(operator.mul, data) ** (1 / len(data))
    
    TreasuryGM = sp.stats.gmean(CompByYear["Treasury"].tolist(), axis=0)

    GeoCompare = PortERGM - TreasuryGM

    objects = ('Portfolio', 'Treasury', 'Excess')

    performance = [PortERGM, TreasuryGM, GeoCompare]

    barPlot(objects, performance, "Geometric Return Comparison", "Returns")

    

    WMTGM = dailyReturns['WMTDailyReturns'].sum()
    
    TGTGM = dailyReturns['TGTDailyReturns'].sum()
    
    PortERGM = CompByYear["Portfolio"].sum()
    
    TreasuryGM =CompByYear["Treasury"].sum()

    GeoCompare = PortERGM - TreasuryGM

    objects = ('WMT', 'TGT', 'Portfolio', 'Treasury', 'Excess')

    performance = [WMTGM, TGTGM, PortERGM, TreasuryGM, GeoCompare]

    barPlot(objects, performance, "Cumulative Return Comparison", "Returns")



    """
    Key Performance Indicators:
    """

    # The risk adjusted return of treasury is 1.72/100

    """
    Sharpe Ratio - Portfolio
    """

    SR = dailyReturns['PortDailyReturns'].mean(
    ) / dailyReturns['PortDailyReturns'].std()

    # Annualized Sharpe Ratio
    ASR = (252**0.5) * SR

    """
    Sharpe Ratio - Tresury
    Assumed to be Tresury Rate
    Tresury is a Risk Free Investment
    """

    TreasurySR = Treasury
    AnnualizedTreasurySR = (252**0.5) * TreasurySR

    """
    Average Profit Per Trade
    Portfolio
    """
    NumOfTrades = 2
    TotalProfit = (portfolioValues["TotalValue"]
                   [-1] - portfolioValues["TotalValue"][0]) / 2

    AverageProfitPerTrade = TotalProfit / NumOfTrades

    """
    Average Profit Per Trade
    Treasury
    """

    NumOfTradesTreasury = 1
    # Geometric Return on Treasury Over the Period Under Considerition
    # Assumed 7 years as investment horizon for treasury
    AveProfitPerTradeTresury = (
        Portfolio * 0.0172 / NumOfTradesTreasury) * 6

    """
    WinLossRatio Calculation
    Portfolio
    """
    WinLossRatioPortfolio = winLossCalculator(portfolioValues)

    """
    WinLossRatio Calculation
    Treasury assumed to be 1
    """

    WinLossRatioTreasury = (1, 0)

    """
    Expectancy KPI for Portfolio
    """
    AveWinLossRatioPortfolio = AveWinLossCalculator(portfolioValues)

    ExpectancyPortfolio = WinLossRatioPortfolio[0] * AveWinLossRatioPortfolio[0] - \
        WinLossRatioPortfolio[1] * AveWinLossRatioPortfolio[1]

    """
    Treasury Expectancy is Assumed to be Geometric Return
    Over the Period Under Consideration
    Assumed 4 years
    """
    ExpectancyTreasury = TreasuryGM * Portfolio * 6

    """
    Build a DataFrame for the KPIs
    """
    KPI = pd.DataFrame()

    KPI["Description"] = [
        "Portfolio",
        "Sharpe Ratio",
        "Annualized Sharpe Ratio",
        "Average Profit Per Trade",
        "Win Loss Ratio",
        "Expectancy"]

    KPI["Portfolio"] = [
        Portfolio,
        SR,
        ASR,
        AverageProfitPerTrade,
        WinLossRatioPortfolio,
        ExpectancyPortfolio]

    KPI["Treasury"] = [
        Portfolio,
        TreasurySR,
        AnnualizedTreasurySR,
        AveProfitPerTradeTresury,
        WinLossRatioTreasury,
        ExpectancyTreasury]

    print("")

    print("Key Performance Indicators Comparison (Portfolio Versus Treasury): ")

    print("")

    print(KPI)

    print("")
