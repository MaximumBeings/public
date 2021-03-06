#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:23:41 2018

@author: oluwaseyiawoga
"""

"""
Import Libraries & Packages
"""
import pandas as pd
import datetime
import datetime as dt
import numpy as np
import pandas_datareader.data as web
from IPython import get_ipython
import matplotlib.pyplot as plt
import matplotlib
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
from fredapi import Fred
fred = Fred(api_key='622bb361c6b1caea6948f814a60563af')
from scipy.optimize import fmin


def getMacroEconomicDataFRED(FRED_API_KEY, start):
    """Function to import data from FRED.
    Args:
        param1: FRED_API_KEY & start_date
    Returns:
        A dataFrame of the requested data
    """
    data = fred.get_series_as_of_date(FRED_API_KEY, start)
    data['Date'] = data["date"]
    data = data.drop_duplicates(subset='Date', keep="last")
    data.set_index('Date', inplace=True)
    data = data[["value"]]

    return data


def importSPTickers():
    """Function to import Good and Acceptable S&P Tickers from file.
    Args:
        param1: None
    Returns:
        A list of Valid S&P500 tickers
    """

    with open('tickers.txt', 'r') as f:
        x = f.readlines()

    tickers = [y.replace('\n', '') for y in x]

    return tickers


def getMarketIndex(
        prompt="Please Enter a Valid Market Ticker (Without Quotes - eg WMT): "):
    """
    Helper function for accepting user input (string)
    and  it does error checking as
    well
    """

    checker = True
    while(checker):
        marketIndex = input(prompt).strip().upper()
        if marketIndex in tickers:
            checker = False
            return marketIndex
        else:
            print("")
            print("Not a Valid S&P Market Ticker - \n Please Enter a Valid Ticker")
            print("")
            checker = True


def calVolatilityRatio(macroEcoData, stockData, N=10):
    """Function to Calculate Volatility Ratio.
    Args:
        param1: MacroEconomic Data, Stock Data and N-Days
    Returns:
        A DataFrame of Volatility Ratio for the MacroEconomic Data Selected.
    """

    result = []
    dates = []
    for dtt in macroEcoData.index[:]:
        if dtt in stockData.index:
            indexToUse = stockData.index.get_loc(dtt)
            newStock = stockData[indexToUse - N:indexToUse]
            todaysRange = stockData.iloc[indexToUse]["High"] - \
                stockData.iloc[indexToUse]["Low"]
            nPastDaysTrueRange = newStock["High"].max() - newStock["Low"].min()
            volatilityRatio = todaysRange / nPastDaysTrueRange
            result.append(volatilityRatio)
            dates.append(dtt)
    newEstDict = pd.DataFrame(index=dates)
    newEstDict["Volatility_Ratio"] = result
    newEstDict.dropna(inplace=True)
    return newEstDict


def positionVolRatio(df, macroEcoDF, cutOff=0.5):
    """Function to generate position crossovers.
    Args:
        param1: Stock Data, Macroeconomic Data and Volatility Ratio CutOff
    Returns:
        A DataFrame of Position Entries - Sell or Buy.
    """
    dftoUse = df.copy()
    sell = macroEcoDF[macroEcoDF["Volatility_Ratio"] < 0.0]
    buy = macroEcoDF[macroEcoDF["Volatility_Ratio"] > cutOff]
    sell_dates = sell.index
    buy_dates = buy.index

    positionIndices = dftoUse.index

    newEstDict = dict.fromkeys(positionIndices, 0)

    for y in range(len(positionIndices)):
        if positionIndices[y] in sell_dates:
            newEstDict[positionIndices[y]] = -100 / dftoUse['Close'][y]

    #newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2=pd.DataFrame.from_dict(newEstDict, orient='index')
    newEstDict2.columns = ['Sell Position']
    #newEstDict2.set_index('Date', inplace=True)

    sellPositionDF = newEstDict2

    positionIndices = dftoUse.index

    newEstDict = dict.fromkeys(positionIndices, 0)

    for y in range(len(positionIndices)):
        if positionIndices[y] in buy_dates:
            newEstDict[positionIndices[y]] = 100 / dftoUse['Close'][y]

    #newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2=pd.DataFrame.from_dict(newEstDict, orient='index')
    newEstDict2.columns = ['Buy Position']
    #newEstDict2.set_index('Date', inplace=True)

    buyPositionDF = newEstDict2

    position = pd.DataFrame()
    position["Strategy"] = buyPositionDF["Buy Position"] + \
        sellPositionDF["Sell Position"]

    return position


class Output(object):
    """
    Source: Risk Management Starter Code
    """
    """Function to generate KPIs.
    Args:
        param1: A dataframe of Returns
    Returns:
        A DataFrame of KPIs.
    """

    def __init__(self, returns_df, date_freq='D'):
        self.returns_df = returns_df if isinstance(
            returns_df, pd.DataFrame) else pd.DataFrame(returns_df)
        self.wealthpaths = self.returns_df.apply(self._calc_wealthpath)
        self._date_freq = str(date_freq).upper()
        if self._date_freq == 'D':
            self._freq = 252
        elif self._date_freq == 'M':
            self._freq = 12

    def _calc_annualized_return(self, series):
        avg_daily_return = series.mean()
        ann_return = avg_daily_return * self._freq
        return ann_return

    def _calc_annualized_std_dev(self, series):
        series_std = series.std()
        ann_std = series_std * (np.sqrt(self._freq))
        return ann_std

    def _calc_sharpe(self, ann_returns, ann_stds):
        sharpe = ann_returns.divide(ann_stds)
        return sharpe

    def _calc_hwm(self, wealthpath):
        hwm = wealthpath.expanding().max()
        return hwm

    def _calc_wealthpath(self, series):
        if series.iloc[0] != 0:
            first_dt = series.index[0]
            set_dt = first_dt - dt.timedelta(days=1)
            series.loc[set_dt] = 0.0
            series = series.sort_index()

        cum_prod = (1.0 + series).cumprod()
        return cum_prod

    def _calc_drawdowns(self, wealthpath):
        hwm = self._calc_hwm(wealthpath)
        drawdowns = wealthpath.divide(hwm).subtract(1.0)
        return drawdowns

    def _calc_lake_ratios(self, hwm, wps):
        lakes = hwm.subtract(wps)
        mountains = hwm.subtract(lakes)
        lake_ratios = lakes.sum() / mountains.sum()
        return lake_ratios

    def _calc_gain_to_pain_ratio(self, series):
        total_return_series = (1.0 + series).cumprod().subtract(1.0)
        total_return = total_return_series.iloc[-1]

        loss_returns_series = self.__get_loss_returns(series).abs()
        if not loss_returns_series.empty:
            total_loss_return_series = (
                1.0 + loss_returns_series).cumprod().subtract(1.0)
            total_loss_return = total_loss_return_series.iloc[-1]

            gpr = total_return / total_loss_return
        else:
            gpr = np.nan
        return gpr

    def __get_win_returns(self, series):
        win_returns = series[series >= 0.0]
        return win_returns

    def __get_loss_returns(self, series):
        loss_returns = series[series < 0.0]
        return loss_returns

    def _calc_win_rate(self, series):
        win_returns = self.__get_win_returns(series)
        rate = float(len(win_returns)) / float(len(series))
        return rate

    def _calc_loss_rate(self, series):
        loss_returns = self.__get_loss_returns(series)
        rate = float(len(loss_returns)) / float(len(series))
        return rate

    def _calc_avg_win_return(self, series):
        win_returns = self.__get_win_returns(series)
        avg = win_returns.mean()
        return avg

    def _calc_avg_loss_return(self, series):
        loss_returns = self.__get_loss_returns(series)
        avg = loss_returns.mean()
        return avg

    def _calc_winloss_ratio(self, series):
        wins = self.__get_win_returns(series)
        losses = self.__get_loss_returns(series)
        if len(losses) == 0.0:
            wl_ratio = np.nan
        else:
            wl_ratio = len(wins) / len(losses)
        return wl_ratio

    def _calc_expectancy(self, win_rates, avg_win, loss_rates, avg_loss):
        w_win = win_rates.multiply(avg_win)
        w_loss = loss_rates.multiply(avg_loss)
        exp = w_win.subtract(w_loss)
        return exp

    def _calc_monthly_return(self, series):
        avg_daily_return = series.mean()
        mth_return = ((1 + avg_daily_return) ** 21) - 1
        return mth_return

    def _calc_mth_drawdown(self, series):
        mth_drawdown = series.add(1).groupby(
            pd.Grouper(freq='M')).cumprod() - 1

        return mth_drawdown

    def generate_output(self):
        hwms = self.wealthpaths.apply(self._calc_hwm)
        lake_ratios = self._calc_lake_ratios(hwms, self.wealthpaths)
        lake_ratios.name = "Lake Ratio"

        drawdowns = self.wealthpaths.apply(self._calc_drawdowns)
        max_dds = drawdowns.min()
        max_dds.name = "Max Drawdown"

        ann_returns = self.returns_df.apply(self._calc_annualized_return)
        ann_returns.name = "Annualized Return"

        ann_stds = self.returns_df.apply(self._calc_annualized_std_dev)
        ann_stds.name = "Annualized Std Dev"

        sharpes = self._calc_sharpe(ann_returns, ann_stds)
        sharpes.name = "Sharpe Ratio"

        win_rates = self.returns_df.apply(self._calc_win_rate)
        win_rates.name = "Win Rate"

        loss_rates = self.returns_df.apply(self._calc_loss_rate)
        loss_rates.name = "Loss Rate"

        avg_win_returns = self.returns_df.apply(self._calc_avg_win_return)
        avg_win_returns.name = "Avg Win Return"

        avg_loss_returns = self.returns_df.apply(self._calc_avg_loss_return)
        avg_loss_returns.name = "Avg Loss Return"

        win_loss_ratio = self.returns_df.apply(self._calc_winloss_ratio)
        win_loss_ratio.name = "Win Loss Ratio"

        expectancy = self._calc_expectancy(
            win_rates, avg_win_returns, loss_rates, avg_loss_returns)
        expectancy.name = "Trade Expectancy"

        gpr = self.returns_df.apply(self._calc_gain_to_pain_ratio)
        gpr.name = 'Gain to Pain Ratio'

        mth_drawdown = self.returns_df.apply(self._calc_mth_drawdown)
        mth_drawdown = mth_drawdown.min()
        mth_drawdown.name = "Monthly Drawdown"

        mth_returns = self.returns_df.apply(self._calc_monthly_return)
        mth_returns.name = "Average Monthly Return"

        output_df = pd.concat([lake_ratios,
                               max_dds,
                               ann_returns,
                               mth_drawdown,
                               mth_returns,
                               ann_stds,
                               sharpes,
                               win_rates,
                               loss_rates,
                               avg_win_returns,
                               avg_loss_returns,
                               expectancy,
                               gpr,
                               ],
                              axis=1).round(4)

        return output_df.T.sort_index()


def strategyReturn(cutOff):
    """Function to Generate Dollar Returns By Year.
        param1: None
    Returns:
        A dataframe of Dollar Returns By Year.
    """

    positionCrossOver = positionVolRatio(stock, unEmployVolRatio, cutOff)
    assetLogReturns = pd.DataFrame(stock["Close"].pct_change())
    assetLogReturns.columns = ["Returns"]

    strategyAssetLogReturns = pd.DataFrame(assetLogReturns["Returns"])

    strategyAssetLogReturns["Returns"] = strategyAssetLogReturns["Returns"] + \
        (positionCrossOver["Strategy"] * strategyAssetLogReturns["Returns"])

    strategyAssetLogReturns['CumReturn'] = (
        1 + strategyAssetLogReturns["Returns"]).cumprod() - 1

    return strategyAssetLogReturns["CumReturn"][-1]


def optimizer(x):
    """
    Function optimize for the best buy and sell percentage.
        param1: An array of buy and sell percentages Guess
        e.g. [0.2]
    Returns:
        An optimal array of buy and sell percentages
    """

    return -1 * strategyReturn(x[0])


if __name__ == '__main__':

    """
    Import list of Valid Tickers from the Directory
    """

    tickers = importSPTickers()

    """
    Prompt the User for a Ticker to Analyze
    """

    stockToAnalyze = getMarketIndex()

    """
    Set the start and end dates using datetime function
    """
    start = datetime.datetime(2008, 1, 1)
    end = datetime.datetime.today()

    """
    Download MacroEconomic Events from FRED
    """

    nonFarmPay = getMacroEconomicDataFRED("PAYEMS", end)
    unEmployData = getMacroEconomicDataFRED("UNRATE", end)
    retailData = getMacroEconomicDataFRED("RSXFS", end)
    cpiData = getMacroEconomicDataFRED("CPIAUCSL", end)

    """
    Download the Stock to analyze from Yahoo
    """

    stock = web.DataReader(stockToAnalyze, 'yahoo', start, end)

    """
    Calculate Volatility Ratios for Macroeconomic Events
    """

    nonFarmVolRatio = calVolatilityRatio(nonFarmPay, stock, N=10)
    unEmployVolRatio = calVolatilityRatio(unEmployData, stock, N=10)
    retailVolRatio = calVolatilityRatio(retailData, stock, N=10)
    cpiVolRatio = calVolatilityRatio(cpiData, stock, N=10)

    """
    Combine NonFarm Payroll data  with stock data...calculate 10 day
    and 50 days Moving Averages and Plot
    """

    stockDataNonFarm = pd.concat(
        [nonFarmVolRatio, stock], axis=1, join='inner')

    stockDataNonFarm["10dSMA"] = stockDataNonFarm['Close'].rolling(
        10).mean()
    stockDataNonFarm["50dSMA"] = stockDataNonFarm['Close'].rolling(
        50).mean()

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(2, 1, 1)
    plt.title("Non Farm Payroll")

    ax.plot(stockDataNonFarm["Close"], label='Stock Price')
    ax.plot(stockDataNonFarm['10dSMA'], label='10dSMA')
    ax.plot(stockDataNonFarm['50dSMA'], label='50dSMA')

    ax.set_ylabel('$')
    ax.legend(loc='best')
    ax.grid(True)

    ax = fig.add_subplot(2, 1, 2)

    nonFarmVolRatio["Volatility_Ratio"].plot()

    ax.set_ylabel('Volatility_Ratio')
    plt.show()

    """
    Combine Employment Data  with stock data...calculate 10 day
    and 50 days Moving Averages and Plot with Volatility Data
    """

    stockDataEmp = pd.concat([unEmployVolRatio, stock], axis=1, join='inner')

    stockDataEmp["10dSMA"] = stockDataEmp['Close'].rolling(
        10).mean()
    stockDataEmp["50dSMA"] = stockDataEmp['Close'].rolling(
        50).mean()

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(2, 1, 1)
    plt.title("Employment Numbers")

    ax.plot(stockDataEmp["Close"], label='Stock Price')
    ax.plot(stockDataEmp['10dSMA'], label='10dSMA')
    ax.plot(stockDataEmp['50dSMA'], label='50dSMA')

    ax.set_ylabel('$')
    ax.legend(loc='best')
    ax.grid(True)

    ax = fig.add_subplot(2, 1, 2)

    stockDataEmp["Volatility_Ratio"].plot()

    ax.set_ylabel('Volatility_Ratio')
    plt.show()

    """
    Combine Retail Data  with stock data...calculate 10 day
    and 50 days Moving Averages and Plot with Volatility Data
    """

    stockDataRetail = pd.concat([retailVolRatio, stock], axis=1, join='inner')

    stockDataRetail["10dSMA"] = stockDataRetail['Close'].rolling(
        10).mean()
    stockDataRetail["50dSMA"] = stockDataRetail['Close'].rolling(
        50).mean()

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(2, 1, 1)
    plt.title("Retail Numbers")

    ax.plot(stockDataRetail["Close"], label='Stock Price')
    ax.plot(stockDataRetail['10dSMA'], label='10dSMA')
    ax.plot(stockDataRetail['50dSMA'], label='50dSMA')

    ax.set_ylabel('$')
    ax.legend(loc='best')
    ax.grid(True)

    ax = fig.add_subplot(2, 1, 2)

    stockDataRetail["Volatility_Ratio"].plot()

    ax.set_ylabel('Volatility_Ratio')
    plt.show()

    """
    Combine CPI Data  with stock data...calculate 10 day
    and 50 days Moving Averages and Plot with Volatility Data
    """

    stockDataCPI = pd.concat([cpiVolRatio, stock], axis=1, join='inner')

    stockDataCPI["10dSMA"] = stockDataCPI['Close'].rolling(
        10).mean()
    stockDataCPI["50dSMA"] = stockDataCPI['Close'].rolling(
        50).mean()

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(2, 1, 1)
    plt.title("Consumer Price Index")

    ax.plot(stockDataCPI["Close"], label='Stock Price')
    ax.plot(stockDataCPI['10dSMA'], label='10dSMA')
    ax.plot(stockDataCPI['50dSMA'], label='50dSMA')

    ax.set_ylabel('$')
    ax.legend(loc='best')
    ax.grid(True)

    ax = fig.add_subplot(2, 1, 2)

    cpiVolRatio["Volatility_Ratio"].plot()

    ax.set_ylabel('Volatility_Ratio')
    plt.show()

    """
    Call the position cross over function and plot position sizing
    """

    positionCrossOver = positionVolRatio(stock, unEmployVolRatio)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(2, 1, 1)
    plt.title("Position Sizing - Unemployment Data")

    ax.plot(stock["Close"], label='Stock Price')
    ax.plot(stockDataNonFarm["10dSMA"], label='10dSMA')
    ax.plot(stockDataNonFarm["50dSMA"], label='50dSMA')

    ax.set_ylabel('$')
    ax.legend(loc='best')
    ax.grid(True)

    ax = fig.add_subplot(2, 1, 2)

    positionCrossOver["Strategy"].plot()

    ax.set_ylabel('Position')
    plt.show()

    """
    Generate Results for the Asset & Strategy and Compare them
    Using Plots Using FMIN optimization library to get the best CutOff
    """

    guess = [0.5]

    optimizedResult = fmin(optimizer, guess)
    print("")
    print(optimizedResult)

    cutOff2 = optimizedResult[0]
    positionCrossOver = positionVolRatio(stock, unEmployVolRatio, cutOff2)

    assetLogReturns = pd.DataFrame(stock["Close"].pct_change())
    assetLogReturns.columns = ["Returns"]
    assetLogReturns.tail()

    strategyAssetLogReturns = pd.DataFrame(assetLogReturns["Returns"])

    strategyAssetLogReturns["Returns"] = strategyAssetLogReturns["Returns"] + \
        (positionCrossOver["Strategy"] * strategyAssetLogReturns["Returns"])
    strategyAssetLogReturns.tail()

    assetLogReturns["Returns"].plot(figsize=(
        12,
        8),
        title=("Asset Returns"), label='Asset Returns', legend=True)
    strategyAssetLogReturns["Returns"].plot(figsize=(12, 8), title=(
        "Strategy Asset Returns"), label='Strategic Asset Returns', legend=True)
    plt.show()

    assetLogReturns['CumReturn'] = (
        1 + assetLogReturns["Returns"]).cumprod() - 1

    strategyAssetLogReturns['CumReturn'] = (
        1 + strategyAssetLogReturns["Returns"]).cumprod() - 1

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
        title=("UnEmployment Data Strategy Versus Buy & Hold"),
        label='UnEmployment Data CrossOver Strategy Return',
        legend=True)
    plt.show()

    print("")

    print("The Cummulative Return on Buy & Hold is: ")

    print("")

    print(assetLogReturns['CumReturn'][-1])

    print("")

    print("Employment Data CrossOver Strategy Return:")

    print("")

    print(strategyAssetLogReturns['CumReturn'][-1])

    STrategyReturn = pd.DataFrame(index=strategyAssetLogReturns.index)
    STrategyReturn["Returns"] = strategyAssetLogReturns["Returns"]

    STrategyReturn['Date'] = pd.to_datetime(STrategyReturn.index)

    STrategyReturn.set_index('Date', inplace=True)

    KPI = Output(STrategyReturn, 'D')
    KPIRSI = KPI.generate_output()

    print("")
    print("Unemployment Data CrossOver Strategy Return")
    print("")
    print(KPIRSI)
