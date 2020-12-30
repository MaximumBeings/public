#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 11:36:51 2017

@author: oluwaseyiawoga
"""

"""
Sources: WQU MSFE Mini Project
"""

"""
Import Libraries & Packages
"""
import pandas as pd
import numpy as np
import pylab
from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn
import matplotlib.pyplot as plt
import matplotlib
import datetime
import pandas_datareader.data as web
import matplotlib.dates as mdates
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
from dateutil.relativedelta import relativedelta
import random
import scipy.stats as stats




def stockDownloader(tickers):
    """
    Function to download stock prices from Yahoo!.
    Args:
        param1: list of tickers
    Returns:
        A Dataframe of stock prices for the tickers .
    """
    downLoadChecker = True
    while (downLoadChecker):
        stockData = pd.DataFrame()

        try:
            for tick in tickers:
                stockData[tick] = web.DataReader(
                    tick, 'yahoo', start, end)['Adj Close']
                #stockData.dropna(how='any', axis=0, inplace=True)
            downLoadChecker = False
            return stockData
        except BaseException:
            random.shuffle(tickers)
            downLoadChecker = True



def monteCarloSimulation(N, Mu, Sigma, S0, NSim):
    """
    Function to perform monte carlo simulation.
    Args:
        param1:
            N = Time to Maturity
            Mu = Mean of data
            Sigma: std deviation of data
            S0 : starting price
            NSim: Number of simulation
    Returns:
        A list of simulated prices for each path or trajectory
    """
    sim2 = []
    t = 0.1 / N

    for y in range(NSim):
        sim = []
        sim.append(S0)
        for x in range(N):
            sim.append(
                ((1 + Mu * t) + (Sigma * np.random.normal(0, 1) * np.sqrt(t))) * sim[x])
        sim2.append(sim)
    return sim2


def calcCrashProb(simResult, S0, CrashPercentage):
    """
    Function to calculation probability of a crash.
    Args:
        param1:
            simResult: Simulated Prices - list of list
            S0: starting price
            CrashPercentage: Crash Percentage
    Returns:
        Probability of stock market crash over the next 365 days
    """
    threshold = S0 * (1 - CrashPercentage)
    count = 0.0
    for x in range(len(simResult)):
        if simResult[x][-1] < threshold:
            count = count + 1
    result = count / len(simResult)
    return result


def plotSimulation(ticker, simResult, N):
    """
    Function to print line plots of simulated results to console.
    Args:
        param1:
            simResult: Simulated Prices - list of list
            N: Time to maturity

    Returns:
        Prints to console - does not return a value
    """
    tIME = range(0, N + 1)
    plt.close('all')
    fig, ax = plt.subplots(1)
    for x in range(len(simResult)):
        ax.plot(tIME, simResult[x], lw=1.0)
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    if ticker == '^IXIC':
        ticker = 'NASDAQ'
    if ticker == '^DJI':
        ticker = 'Dow Jones Index'
    if ticker == '^GSPC':
        ticker = 'S&P 500'
    plt.title('Geometric Brownian Motion \n' +  \
              ticker + ' Price Trajectory')
    #plt.legend(loc=0)
    plt.grid(True)
    plt.ylabel('Stock Price')
    plt.xlabel('Dates in Days')
    plt.show()




"""
All the Above Functions are Called From Below
"""


if __name__ == '__main__':

    """
    Set the start and end dates using datetime function
    """
    
    """
    Set the tickers for the market indices
    """
    ticker = '^GSPC'  #'^IXIC' for NASDAQ and '^DJI' for Dow Jones


    end = datetime.datetime.today()
    start = end - relativedelta(years=2)

    """
    Download Stock Prices & Plot Stock Price Chart
    """
    stocks = stockDownloader([ticker])

    (stocks / stocks.iloc[0] * 100).plot(figsize=(8, 6), title='Stock Prices')

    """
    Calculate Stock returns and drop NAs
    """
    daily_returns = stocks.pct_change()
    daily_returns.dropna(how='any', axis=0, inplace=True)

    
    """
    Perform monte carlo simulation and generate prob of a crash
    plot the random price evolution
    """
    def performMonteCarloSim(ticker):
        
        Mu = np.mean(daily_returns[ticker])
        Sigma = 0.2
        S0 = stocks[ticker][-1]
        NSim = 200
        N = 365
        simResult = monteCarloSimulation(N, Mu, Sigma, S0, NSim)
        prob = calcCrashProb(simResult, S0, 0.113)
        if ticker == '^IXIC':
            ticker = 'NASDAQ'
        if ticker == '^DJI':
            ticker = 'Dow Jones Index'
        if ticker == '^GSPC':
            ticker = 'S&P 500'
        print("")
        print(
            "The Prob of an 11.3 Percent Fall in " +  ticker + " over the Next 365 Days is:  %2.13f " %
            (prob))
        plotSimulation(ticker, simResult, N)
        plt.show()
    
    performMonteCarloSim(ticker)
  

    
