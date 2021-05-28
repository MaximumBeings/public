#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:08:07 2017

@author: oluwaseyiawoga
"""

import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime
import pandas_datareader.data as web
import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6
import matplotlib
matplotlib.style.use('ggplot')


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
    start = datetime.datetime(2000, 1, 1)
    end = datetime.datetime.today()

    goldPrices = web.DataReader(["GOLDAMGBD228NLBM"],
                                "fred",
                                start,
                                end)
    goldPrices.columns = ['GOLD']
    ts = goldPrices['GOLD']
    plt.plot(ts.index.to_pydatetime(), ts.values)
    ts_week = ts.resample('W').mean()
    plt.plot(ts_week.index.to_pydatetime(), ts_week.values)
    plt.show()

    """
    Preview a plot of the original timseries and its rolling means
    and rolling standard deviations
    """

    ts_week.rolling(12).mean().plot(
        label='12 Months Rolling Mean', figsize=(
            12, 8), title='TimeSeries Plot & Rolling Means')
    ts_week.rolling(12).std().plot(label='12 Months Rolling Std')
    ts_week.plot(label='Original Data')
    plt.legend(loc='best')
    plt.show()

    """
    Run Normal Tests and Print Descriptive Statistics of the original timeseries
    """
    printStatistics(ts_week)
    print("")
    printNormailtyTest(ts_week)

    """
    Plot the Seasonal Decomposition of the Data to Check
    for trend and Seasonality.

    """

    decomposition = seasonal_decompose(ts_week, freq=12)
    fig = plt.figure()
    fig = decomposition.plot()
    fig.set_size_inches(12, 8)
    plt.show()

    """
    There is Trend and seasonality in the Timeseries...So we need
    to check Mathematically if it is Non-stationary.
    """
    adFullerTest(ts_week)
    
    """
    Take a log of the weekly prices and perform adf test again
    """

    ts_week_log = np.log(ts_week)

    adFullerTest(ts_week_log)

    decomposition = seasonal_decompose(ts_week_log)
    fig = plt.figure()
    fig = decomposition.plot()
    fig.set_size_inches(12, 8)
    plt.show()
    
    """
    Subset the weekly prices and perform the adf test again
    """

    ts_week_log_select = ts_week_log[-1000:]

    decomposition = seasonal_decompose(ts_week_log_select, freq=12)
    fig = plt.figure()
    fig = decomposition.plot()
    fig.set_size_inches(12, 8)
    plt.show()

    ts_week_log_diff = ts_week_log - ts_week_log.shift()
    plt.plot(ts_week_log_diff.index.to_pydatetime(), ts_week_log_diff.values)
    plt.show()

    ts_week_log_diff.dropna(inplace=True)
    adFullerTest(ts_week_log_diff)

    fig_first = plot_acf(ts_week_log_diff)
    fig_first.set_size_inches(12, 8)
    plt.show()
    result = plot_pacf(ts_week_log_diff)
    result.set_size_inches(12, 8)
    plt.show()
    
    """
    Build the model and print summary results.
    """
    model = ARIMA(ts_week_log, order=(0, 1, 1))
    results_ARIMA = model.fit(disp=-1)
    plt.plot(ts_week_log_diff.index.to_pydatetime(), ts_week_log_diff.values)
    plt.plot(ts_week_log_diff.index.to_pydatetime(),
             results_ARIMA.fittedvalues, color='red')
    plt.title('RSS: %.4f' %
              sum((results_ARIMA.fittedvalues - ts_week_log_diff)**2))
    plt.show()

    print(results_ARIMA.summary())

    residuals = DataFrame(results_ARIMA.resid)
    residuals.plot(kind='kde')
    print(residuals.describe())

    """
    Predict or Forecast Gold Prices
    """
    predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    print(predictions_ARIMA_diff.head())

    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    predictions_ARIMA_log = pd.Series(
        ts_week_log.iloc[0], index=ts_week_log.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(
        predictions_ARIMA_diff_cumsum, fill_value=0)

    size = int(len(ts_week_log) - 15)
    train, test = ts_week_log[0:size], ts_week_log[size:len(ts_week_log)]
    history = [x for x in train]
    predictions = list()

    """
    Compared Observed to Forecasted Prices.
    """
    print('Printing Predicted vs Expected Values...')
    print("")
    for t in range(len(test)):
        model = ARIMA(history, order=(0, 1, 1))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(float(yhat))
        obs = test[t]
        history.append(obs)
        print('predicted=%f, expected=%f' % (np.exp(yhat), np.exp(obs)))

    error = mean_squared_error(test, predictions)

    print("")
    print('Printing Mean Squared Error of Predictions...')
    print('Test MSE: %.6f' % error)

    predictions_series = pd.Series(predictions, index=test.index)
    
    """
    Plot Observed Versus Forecasted Price
    """

    fig, ax = plt.subplots()
    ax.set(title='ARIMA \n Gold Price Versus Forecasted Gold Prices',
           xlabel='Date', ylabel='Prices')
    ax.plot(ts_week[-50:], 'o', label='Observed Gold Prices')
    ax.plot(np.exp(predictions_series), 'g',
            label='Forecasted Gold Price')
    legend = ax.legend(loc='upper left')
    legend.get_frame().set_facecolor('w')
    plt.show()
