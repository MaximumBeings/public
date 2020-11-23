#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 19:04:10 2018

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
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import seaborn
seaborn.mpl.rcParams['figure.figsize'] = (12.0, 8.0)
np.warnings.filterwarnings('ignore')


"""
  . Gather the daily high, low, and closing prices for WMTonald's stock
   (ticker symbol WMT) for January 2004 through July 2005 from an
   appropriate financial website such as Google Finance, Yahoo Finance,
   Quandl, CityFALCON, or another similar source.

  . Calculate 10-day and 60-day SMAs. Plot these two curves with a
    bar chart of the stock prices.

  . Compare and contrast the 10-day and the 60-day SMA.

  . Explain the relationship between the market trend and the
    60-day SMA during the following periods:
       . May 2004-October 2004
       . October 2004-May 2005
       . May 2005-July 2005

  . Draw the moving average oscillator of the price chart.

  . Bollinger Band is a band plotted 1.5 standard deviations
    away from a simple moving average. Calculate the Bollinger
    bands of 10-day simple moving average for Mac Donald share.

  . Develop a trading strategy based on the relation between price and
    Bollinger Bands. Graphically represent the risk-return profile of
    such a trading strategy.
"""

"""This cell defineds the plot_candles function"""


def plot_candles(
        pricing,
        title=None,
        volume_bars=True,
        color_function=None,
        technicals=None):
    """ Plots a candlestick chart using Yahoo pricing data.

    Author: Daniel Treiman
    Modified: Modified by Oluwaseyi Awoga on February 2, 2018.

    Args:
      pricing: A pandas dataframe with columns ['open_price', 'close_price',
      'high', 'low', 'volume']
      title: An optional title for the chart
      volume_bars: If True, plots volume bars
      color_function: A function which, given a row index and price series,
      returns a candle color.
      technicals: A list of additional data series to add to the chart.
      Must be the same length as pricing.

    Returns:
        None
        Plot of Candlestick and Volume.
    """
    def default_color(index, open_price, close_price, low, high):
        return 'r' if open_price[index] > close_price[index] else 'g'
    color_function = color_function or default_color
    technicals = technicals or []
    open_price = pricing['open_price']
    close_price = pricing['close_price']
    low = pricing['low']
    high = pricing['high']
    oc_min = pd.concat([open_price, close_price], axis=1).min(axis=1)
    oc_max = pd.concat([open_price, close_price], axis=1).max(axis=1)
    x = np.arange(len(pricing))

    if volume_bars:
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True,
                                       gridspec_kw={'height_ratios': [3, 1]})
    else:
        fig, ax1 = plt.subplots(1, 1)

    tenDayRolling = pricing['close_price'].rolling(window=10).mean()
    ax1.plot(x, tenDayRolling, linewidth=1, color="blue", label="10dSMA")
    sixtyDayRolling = pricing['close_price'].rolling(window=60).mean()
    ax1.plot(x, sixtyDayRolling, linewidth=1, color="fuchsia", label="60dSMA")
    if title:
        ax1.set_title(title)

    candle_colors = [
        color_function(
            i,
            open_price,
            close_price,
            low,
            high) for i in x]
    ax1.bar(
        x,
        oc_max - oc_min,
        bottom=oc_min,
        color=candle_colors,
        linewidth=0)
    ax1.vlines(x + 0.4, low, high, color=candle_colors, linewidth=1)
    ax1.xaxis.grid(False)
    ax1.xaxis.set_tick_params(
        which='major',
        length=3.0,
        direction='in',
        top='off')

    ax1.legend(loc='upper left', prop={'size': 12})

    for indicator in technicals:
        ax1.plot(x, indicator)

    if volume_bars:
        volume = pricing['volume']
        volume_scale = None
        scaled_volume = volume
        if volume.max() > 1000000:
            volume_scale = 'M'
            scaled_volume = volume / 1000000
        elif volume.max() > 1000:
            volume_scale = 'K'
            scaled_volume = volume / 1000
        ax2.bar(x, scaled_volume, color=candle_colors)
        volume_title = 'Volume'
        if volume_scale:
            volume_title = 'Volume (%s)' % volume_scale
        ax2.set_title(volume_title)
        ax2.xaxis.grid(False)
    plt.show()


"""
All the Above Functions are Called From Below
"""


if __name__ == '__main__':

    start = datetime.datetime(2004, 1, 1)
    end = datetime.datetime(2017, 5, 19)
    stockData = web.DataReader("WMT", 'yahoo', start, end)

    """
    Plot the Stock Price Evolution
    """
    stockData["Close"].plot(
        figsize=(
            12,
            8),
        title='WMTonalds Stock Price Evolution')
    plt.show()

    stockDataWMT = stockData[:]

    stockDataWMT.columns = [
        'open_price',
        'high',
        'low',
        'close_price',
        'adj_close',
        'volume']

    #stockDataWMT.drop(columns=['adj_close'], inplace=True)

    plot_candles(
        stockDataWMT,
        title='WMT 10dSMA Versus 60dSMA With Candlestick')
    plt.show()

    """
    Explain the relationship between the market trend and the
    60-day SMA during the following periods:
       . May 2004-October 2004
       . October 2004-May 2005
       . May 2005-July 2005
    """

    stockDataWMT["Date"] = stockDataWMT.index
    firstDateSubset = stockDataWMT.loc['2004-5-1':'2004-10-31']
    firstDateSubset["tenDayRolling"] = firstDateSubset['close_price'].rolling(
        window=10).mean()
    firstDateSubset["sixtyDayRolling"] = firstDateSubset['close_price'].rolling(
        window=60).mean()
    """
    Plot the Stock Price Evolution
    """
    firstDateSubset["close_price"].plot(
        figsize=(
            12,
            8),
        label="Close Price", legend=True)
    firstDateSubset["tenDayRolling"].plot(
        figsize=(
            12,
            8),
        label="10 Day SMA", legend=True)

    firstDateSubset["sixtyDayRolling"].plot(
        figsize=(
            12,
            8),
        title='WMTonalds 10dSMA & 60dSMA Versus Stock Prices \n May 2004 to October 2004',
        label="60 Day SMA",
        legend=True)

    plt.show()

    secondDateSubset = stockDataWMT.loc['2004-10-1':'2005-5-31']
    secondDateSubset["tenDayRolling"] = secondDateSubset['close_price'].rolling(
        window=10).mean()
    secondDateSubset["sixtyDayRolling"] = secondDateSubset['close_price'].rolling(
        window=60).mean()
    """
    Plot the Stock Price Evolution
    """
    secondDateSubset["close_price"].plot(
        figsize=(
            12,
            8),
        label="Close Price", legend=True)
    secondDateSubset["tenDayRolling"].plot(
        figsize=(
            12,
            8),
        label="10 Day SMA", legend=True)

    secondDateSubset["sixtyDayRolling"].plot(
        figsize=(
            12,
            8),
        title='WMTonalds 10dSMA & 60dSMA Versus Stock Prices \n October 2004 to May 2005',
        label="60 Day SMA",
        legend=True)

    plt.show()

    thirdDateSubset = stockDataWMT.loc['2005-5-1':'2005-7-31']
    thirdDateSubset["tenDayRolling"] = thirdDateSubset['close_price'].rolling(
        window=10).mean()
    thirdDateSubset["sixtyDayRolling"] = thirdDateSubset['close_price'].rolling(
        window=60).mean()
    """
    Plot the Stock Price Evolution
    """
    thirdDateSubset["close_price"].plot(
        figsize=(
            12,
            8),
        label="Close Price", legend=True)
    thirdDateSubset["tenDayRolling"].plot(
        figsize=(
            12,
            8),
        label="10 Day SMA", legend=True)

    thirdDateSubset["sixtyDayRolling"].plot(
        figsize=(
            12,
            8),
        title='WMTonalds 10dSMA & 60dSMA Versus Stock Prices \n May 2005 to July 2005',
        label="60 Day SMA",
        legend=True)

    plt.show()

    """
    Draw the moving average oscillator of the price chart.
    """

    stockDataWMT["tenDayRolling"] = stockDataWMT['close_price'].rolling(
        window=10).mean()
    stockDataWMT["sixtyDayRolling"] = stockDataWMT['close_price'].rolling(
        window=60).mean()
    stockDataWMT["MACD"] = stockDataWMT["tenDayRolling"] - \
        stockDataWMT["sixtyDayRolling"]

    stockDataWMT["MACD"].plot(
        figsize=(
            12,
            8),
        title="WMTonalds Moving Average Oscillators\n Moving Average Convergence Divergence (MACD)",
        label="WMTonalds Moving Average Oscillators",
        legend=True)
    plt.show()

    """
    Bollinger Band is a band plotted 1.5 standard deviations
    away from a simple moving average. Calculate the Bollinger
    bands of 10-day simple moving average for Mac Donald share.
    """

    window = 10
    no_of_std = 1.5

    stockDataWMT["rollingMean"] = stockDataWMT['close_price'].rolling(
        window).mean()
    stockDataWMT["rollingStd"] = stockDataWMT['close_price'].rolling(
        window).std()

    stockDataWMT['bollingerHigh'] = stockDataWMT["rollingMean"] + \
        (stockDataWMT["rollingStd"] * no_of_std)
    stockDataWMT['bollingerLow'] = stockDataWMT["rollingMean"] - \
        (stockDataWMT["rollingStd"] * no_of_std)

    """
    Plot the Stock Price Evolution
    """
    stockDataWMT["close_price"].plot(
        figsize=(
            12,
            8),
        label="Close Price", legend=True)
    stockDataWMT["bollingerHigh"].plot(
        figsize=(
            12,
            8),
        label="bollingerHigh", legend=True)

    stockDataWMT["bollingerLow"].plot(
        figsize=(
            12,
            8),
        title='WMTonalds Bollinger Band \n 10 Day Window & 1.5 Standard Deviation',
        label="bollingerLow",
        color="green",
        legend=True)

    plt.show()

    """
    Develop a trading strategy based on the relation between price and
    Bollinger Bands. Graphically represent the risk-return profile of
    such a trading strategy.
    """

    positionHigh = stockDataWMT["close_price"] - stockDataWMT["bollingerHigh"]
    positionHigh = positionHigh.apply(np.sign)
    for j in range(len(positionHigh)):
        if positionHigh[j] > 0:
            positionHigh[j] = (-100.00 / stockDataWMT["close_price"]
                               [j]) / stockDataWMT["close_price"][j]
        elif positionHigh[j] < 0:
            positionHigh[j] = (100.00 / stockDataWMT["close_price"]
                               [j]) / stockDataWMT["close_price"][j]

    positionLow = stockDataWMT["close_price"] - stockDataWMT["bollingerLow"]
    positionLow = positionHigh.apply(np.sign)
    for j in range(len(positionHigh)):
        if positionLow[j] < 0:
            positionLow[j] = (-100.00 / stockDataWMT["close_price"]
                              [j]) / stockDataWMT["close_price"][j]
        elif positionLow[j] > 0:
            positionLow[j] = (100.00 / stockDataWMT["close_price"]
                              [j]) / stockDataWMT["close_price"][j]

    position = positionLow + positionHigh
    position = position.shift(1)
    position = pd.DataFrame(position)
    position.columns = ["bollingerPosition"]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(2, 1, 1)
    plt.title("Bollinger Band Strategy Analysis\n Position Sizing")

    ax.plot(stockDataWMT["close_price"], label='Stock Price')
    ax.plot(stockDataWMT["bollingerHigh"], label='Bollinger High')
    ax.plot(stockDataWMT["bollingerLow"], label='Bollinger Low')

    ax.set_ylabel('$')
    ax.legend(loc='best')
    ax.grid(True)

    ax = fig.add_subplot(2, 1, 2)

    ax.plot(position["bollingerPosition"],
            label='Position')

    ax.set_ylabel('Position')
    plt.show()

    """
    Generate Results for the Asset & Strategy and Compare them
    Using Plots
    """

    assetLogReturns = pd.DataFrame(np.log(stockDataWMT["close_price"]).diff())
    assetLogReturns.tail()

    strategyAssetLogReturns = pd.DataFrame(assetLogReturns["close_price"])
    strategyAssetLogReturns["close_price"] = strategyAssetLogReturns["close_price"] + \
        position["bollingerPosition"] * strategyAssetLogReturns["close_price"]
    strategyAssetLogReturns.tail()
    
    

    assetLogReturns["close_price"].plot(figsize=(
        12,
        8),
        title=("Asset Returns"), label='Asset Returns', legend=True)
    strategyAssetLogReturns["close_price"].plot(figsize=(12, 8), title=(
        "Strategy Asset Returns"), label='Strategic Asset Returns', legend=True)
    plt.show()

    assetLogReturns['CumReturn'] = (
        1 + assetLogReturns["close_price"]).cumprod() - 1

    strategyAssetLogReturns['CumReturn'] = (
        1 + strategyAssetLogReturns["close_price"]).cumprod() - 1

    assetLogReturns["CumReturn"].plot(
        figsize=(
            12,
            8),
        title=("Cummulative Asset Returns"),
        label='Buy & Hold Strategy Returns',
        legend=True)
    strategyAssetLogReturns["CumReturn"].plot(
        figsize=(
            12,
            8),
        title=("Bollinger Band Trading Strategy Versus Buy & Hold"),
        label='Bollinger Band Trading Strategy Return',
        legend=True)
    plt.show()
    
    print("")

    print("The Cummulative Return on Buy & Hold Is: ")

    print("")

    print(assetLogReturns['CumReturn'][-1])

    print("")

    print("The Cummulative Return Bollinger Band Is:")

    print("")
    
    print(strategyAssetLogReturns['CumReturn'][-1])

