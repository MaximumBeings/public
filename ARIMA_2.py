#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:53:41 2017

@author: oluwaseyiawoga
"""

import datetime
import pandas as pd
import statsmodels.api as sm
pd.set_option('display.precision', 10)
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import pandas_datareader.data as web
import scipy.stats as stats
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pandas.tseries.offsets import DateOffset


def printStatistics(array):
    """
    Function to Generate Statistics.
    Args:
        param1: Arrays
    Returns:
        A Set of Descriptive Statistics on An Array.
    """
    statistics = stats.describe(array)
    # print("")
    print("%14s %15s" % ('statistic', 'value'))
    print(30 * "-")
    print("%14s %15.5f" % ('Size', statistics[0]))
    print("%14s %15.5f" % ('Min', statistics[1][0]))
    print("%14s %15.5f" % ('Max', statistics[1][1]))
    print("%14s %15.5f" % ('Mean', statistics[2]))
    print("%14s %15.5f" % ('Std', np.sqrt(statistics[3])))
    print("%14s %15.5f" % ('Skew', statistics[4]))
    print("%14s %15.5f" % ('Kurtosis', statistics[5]))


def printNormailtyTest(array):
    """
    Function to Perform Normality Test.
    Args:
        param1: Arrays
    Returns:
        Prints to console Normal Test Results - does not return a value
    """

    print("Skew of Data Set  %20.3f " % (stats.skew(array)))
    print("Skew Test PValue  %20.3f" % (stats.skewtest(array)[1]))
    print("Kurt of Data Set  %20.3f" % (stats.kurtosis(array)))
    print("Kurt Test PValue  %20.3f" % (stats.kurtosistest(array)[1]))
    print("T-Stat Norm Test  %20.3f" % (stats.normaltest(array)[0]))
    print("Norm Test PValue  %20.3f" % (stats.normaltest(array)[1]))


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
    start = datetime.datetime(1975, 1, 1)
    end = datetime.datetime.today()

    """
    Download House Price Index from FRED
    """

    data = web.DataReader(["CSUSHPISA"], "fred", start, end)
    data.dropna(how='any', axis=0, inplace=True)

    """
    Preview a plot of the original timseries and its rolling means
    and rolling standard deviations
    """
    timeSeries = data['CSUSHPISA']
    timeSeries.rolling(12).mean().plot(
        label='12 Months Rolling Mean', figsize=(
            12, 8), title='TimeSeries Plot & Rolling Means')
    timeSeries.rolling(12).std().plot(label='12 Months Rolling Std')
    timeSeries.plot(label='Original Data')
    plt.legend(loc='best')
    plt.show()

    """
    Run Normal Tests and Print Descriptive Statistics of the original timeseries
    """
    printStatistics(timeSeries)
    print("")
    printNormailtyTest(timeSeries)

    """
    Plot the Seasonal Decomposition of the Data to Check
    for trend and Seasonality.
    """

    decomposition = seasonal_decompose(data['CSUSHPISA'], freq=12)
    fig = plt.figure()
    fig = decomposition.plot()
    fig.set_size_inches(12, 8)
    plt.show()

    """
    There is Trend and seasonality in the Timeseries...So we need
    to check Mathematically if it is Non-stationary.
    """
    adFullerTest(data['CSUSHPISA'].dropna())

    """
    Since Our timeseries is non-stationary based on the
    result of the Augmented Dickey-Fuller test, we need
    to take a first difference in the data
    """

    data['First Difference'] = data['CSUSHPISA'] - data['CSUSHPISA'].shift(1)

    adFullerTest(data['First Difference'].dropna())

    """
    Now we can plot the ACF and PACF in order to guide in the selection
    of the parameters.
    """

    fig_first = plot_acf(data['First Difference'].dropna())
    fig_first.set_size_inches(12, 8)
    plt.show()
    result = plot_pacf(data['First Difference'].dropna())
    result.set_size_inches(12, 8)
    plt.show()

    """
    Based on the ACF and PACF plots, We have AR(1), and MA(0) and also
    a seasonal component since our data is monthly.  We also differenced
    once.  The model chosen is the Seasonal ARIMA model
    """

    model = sm.tsa.statespace.SARIMAX(
        data['CSUSHPISA'], order=(
            1, 1, 0), seasonal_order=(
            1, 1, 1, 12))
    results = model.fit()
    print(results.summary())

    results.resid.plot(kind='kde', title='Kernel Density Plot')
    plt.show()
    results.resid.plot(title='Residual Plots')
    plt.show()

    """
    Our residuals seem to be mostly centered around zero except very early on
    when there was a great dip.
    """

    """
    Predict Out-of-Sample Population
    """

    future_dates = [data.index[-1] +
                    DateOffset(months=x) for x in range(0, 50)]
    future_dates_df = pd.DataFrame(
        index=future_dates[1:], columns=data.columns)
    future_df = pd.concat([data, future_dates_df])
    future_df['Forecast'] = results.predict(
        start=len(data), end=562, dynamic=True)
    future_df[['CSUSHPISA', 'Forecast']].plot(
        figsize=(12, 8), title='Original & Forecasted House Price Index')
    plt.show()

#    """
#    We could also have Ran a Seasonal First Difference if our initial Efforts
#    didnt lead to a stationary data as it did above
#    """
#
#    data['Seasonal First Difference'] = data['CSUSHPISA'] - \
#        data['CSUSHPISA'].shift(12)
#    data['Seasonal First Difference'].plot()
#    adFullerTest(data['Seasonal First Difference'].dropna())
#
#    fig_first = plot_acf(data['Seasonal First Difference'].dropna())
#    fig_first.set_size_inches(12, 8)
#    plt.show()
#    result = plot_pacf(data['Seasonal First Difference'].dropna())
#    result.set_size_inches(12, 8)
#    plt.show()

    


