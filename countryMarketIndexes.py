#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 10:42:49 2017

@author: oluwaseyiawoga
"""


import numpy as np
import scipy.interpolate
import pylab
import pandas_datareader.data as web
import datetime
from scipy.optimize import leastsq
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
from dateutil.relativedelta import relativedelta
import seaborn as sns
import random


countryIndices = {
    "USA": [
        "^DJI",
        "^GSPC",
        "^IXIC",
        "^RUT",
        "^VIX",
        "^XAX"],
    "TAIWAN": ["^TWII"],
    "SWITZERLAND": ["^STOXX50E"],
    "SOUTH KOREA": ["^KS11"],
    "SINGAPORE": ["^STI"],
    "RUSSIA": ["MICEXINDEXCF.ME"],
    "NEW ZEALAND": ["^NZ50"],
    "MEXICO": ["^MXX"],
    "JAPAN": ["^N225"],
    "INDIA": [
        "^NSEI",
        "^BSESN"],
    "HONG KONG": ["^HSI"],
    "FRANCE": [
        "^N100",
        "^FCHI"],
    "GERMANY": ["^GDAXI"],
    "CHINA": ["000001.SS"],
    "CHILE": ["^IPSA"],
    "CANADA": ["^GSPTSE"],
    "BRAZIL": ["^BVSP"],
    "BELGIUM": ["^BFX"],
    "AUSTRALIA": [
        "^AXJO",
        "^AORD"],
    "ARGENTINA": ["^MERV"],
    "INDONESIA": ["^JKSE"],
    "MALAYSIA": ["^KLSE"],
    "NORWAY": ["^OSEAX"]}


countryNames = countryIndices.keys()


def getCountry(prompt="Please Enter a Country Name (No Quotes): "):
    """
    Helper function for accepting user input (string)
    and  it does error checking as
    well
    """
    print (" ")

    print ("Please select from the List Below (No Quotes): ")
    print ("--------------------------------------------")
    print("")
    print (countryNames)

    checker = True
    while(checker):
        countryName = input(prompt).strip().upper()
        if countryName in countryNames:
            checker = False
            return countryName
        else:
            print("")
            print ("Not a Valid Country Name (No Quotes) ")
            print("")
            checker = True


def getMarketIndex(
        countryName,
        prompt="Please Enter a Valid Market Index (No Quotes): "):
    """
    Helper function for accepting user input (string)
    and  it does error checking as
    well
    """

    checker = True
    while(checker):
        marketIndex = input(prompt).strip().upper()
        if marketIndex in countryIndices[countryName]:
            checker = False
            return marketIndex
        else:
            print("")
            print ("Not a Valid Market Index")
            print("")
            checker = True


def mainPrompt(finalSet=set()):
    while(len(finalSet) < 5):
        countryName = getCountry(
            prompt="Please Enter a Country Name (No Quotes):  ")
        print("")
        print("These are the Names of Indices Available for this Country ")
        print("")
        print(countryIndices[countryName])
        print("")
        marketIndex = getMarketIndex(
            countryName, prompt="Please Enter a Valid Market Index (No Quotes): ")
        finalSet.add(marketIndex)
        print("")
        print("These are the Market Indices You Have Selected So Far:")
        print("")
        print(list(finalSet))
    return list(finalSet)


def stockDownloader(tickers):
    downLoadChecker = True
    while (downLoadChecker):
        stockData = pd.DataFrame()

        try:
            for tick in tickers:
                stockData[tick] = web.DataReader(
                    tick, 'yahoo', start, end)['Close']
                stockData.dropna(how='any', axis=0, inplace=True)
            downLoadChecker = False
            return stockData
        except BaseException:
            random.shuffle(tickers)
            downLoadChecker = True


def calculateReturns(stockData):
    returns = pd.DataFrame()
    for tick in tickers:
        returns[tick + ' Return'] = stockData[tick].pct_change()
    return returns


if __name__ == '__main__':
    """
    Get a list of tickers by prompting the user using
    the functions above
    """

    tickers = sorted(mainPrompt(finalSet=set()))[:]
    #tickers = ['^DJI', '^FTSE', '^JKSE', '^KLSE', '^TASI.SR']

    """
    Set the start and end dates using datetime function
    """
    end = datetime.datetime.today()
    start = end - relativedelta(years=10)

    """
    Download the data for all the tickers using yahoo
    """

    stockData = stockDownloader(tickers)

    print("")
    print("........Generating Results & Charts......")

    """
    Calculate returns using pct_change() function in pandas
    """

    returns = calculateReturns(stockData)

    """
    Resample the daily data to monthly
    """

    returns = returns.resample('MS').mean()

    """
    Generate the Correlation Matrix
    """
    print("")
    print(returns.corr())
    print("")

    """
    Generate the Pairplot
    """

    sns.pairplot(returns)


    """
    Generate the cluster plot
    """

    sns.clustermap(returns.corr(), annot=True)

    """
    SAMPLE DISCUSSION:
        Based on the tickers analyzed, the strongest correlation (0.86)
        occurred between FTSE 100 and NS 100 the market indices of two
        European countries, UK and France respectively.  This makes sense
        since they are based in the same geographical zone and probably
        share similar market dynamics and hence are not good candidates
        from a diversification standpoint. Conversely, India's NSEI
        (Nifty 50) and Japan's N225 (or Nikkei) seem to have the least
        correlation of 0.55 meaning that, they are good candidates from
        a diversification standpoint because they are less correlated
        with each other.  The FTSE 100 also has a relatively low
        correlation with Nikkei.  This is understandable because UK and
        Japan are in totally different regions and the economies are
        shaped by different dynamics.  Same with India and Japan.
    """
