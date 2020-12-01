#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 13:44:29 2017

@author: oluwaseyiawoga
"""

"""
Import Libraries & Packages
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas_datareader.data as web
import datetime as dt
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
import sys
#pd.set_option('display.max_columns', 6)
#pd.set_option('display.max_rows', None)

"""
Enter A Valid filePath to the Location of the Extracted JSON File.
"""

filePath = 'americanPresidents.csv'


def importCSVToDataframe(filePath):
    """Function to import Presidents' file.
    Args:
        param1: path to path to presidents file
    Returns:
        A dataframe of presidents file from CSV to Pandas dataframe
    """
    try:
        df = pd.read_csv(filePath)
        return df
    except IOError:
        print("")
        print("Either file is missing or is not readable")
        print("")
        print("Please Enter A Valid filePath & Re-Run the Program")
        print("")
        sys.exit("System Exiting.....")


def getDailyDemPeriods(democrats):
    """Function to generate a DataFrame of days in which a Democratic
    President was in Office.
    Args:
        param1: DataFrame of Dates (Start and End Range) in Which A
        Democrat was President
    Returns:
        A DataFrame Consisting of the Days (Daily) in Which A Democrat
        was President.This is Mapped to Daily Returns to Subset Returns
        for Democrats
    """
    democratsDaily = []
    for x in range(len(democrats)):
        row = democrats.iloc[x]
        dates = pd.date_range(row[0], row[1], freq='D')
        for date in dates:
            democratsDaily.append(date)
    democratsDaily = set(democratsDaily)
    democratsDaily = sorted(list(democratsDaily))
    return pd.DataFrame({'Period': democratsDaily})


def getDailyRepPeriods(republicans):
    """Function to generate a DataFrame of days in which a Republican
    President was in Office.
    Args:
        param1: DataFrame of Dates (Start and End Range) in Which A
        Republican was President
    Returns:
        A DataFrame Consisting of the Days (Daily) in Which A Republican
        was President.This is Mapped to Daily Returns to Subset Returns
        for Republican
    """
    republicansDaily = []
    for x in range(len(republicans)):
        row = republicans.iloc[x]
        dates = pd.date_range(row[0], row[1], freq='D')
        for date in dates:
            republicansDaily.append(date)
    republicansDaily = set(republicansDaily)
    republicansDaily = sorted(list(republicansDaily))
    return pd.DataFrame({'Period': republicansDaily})


def stockDownloader(tickers, start, end):
    """Function to Download Stock Data for the Market Indices.
    Args:
        param1: Tickers, Start and End Dates
    Returns:
        A dataframe of Adjusted Close Values of downloaded Stock
        Data
    """
    p = web.DataReader(tickers, 'yahoo', start, end)
    d = p['Adj Close']
    d.set_index('Date', inplace=True)
    return d


def dailyReturnsDF(closes):
    """Function to Calculate Daily Returns for Downloaded Stock Data.
    Args:
        param1: Downloaded Stock Prices
    Returns:
        A dataframe of Daily Returns for Downloaded Data
    """
    return np.log(closes / closes.shift(1))


def calc_annual_returns(daily_returns):
    """Function to Calculate Annual Returns From Daily Returns.
    Args:
        param1: Daily Returns
    Returns:
        A dataframe of Annual Returns.
    """
    grouped = np.exp(daily_returns.groupby(lambda date: date.year).sum()) - 1
    return grouped


def annualReturnsDemCalc(dailyReturns, dailyDemData):
    """Function to Calculate Annual Returns for Democrats Only.
    Args:
        param1: Daily Returns & Democrat Daily Returns Subset
    Returns:
        A dataframe of Democrats Annual Returns Filtered from the
        Total Population of Annual Returns
    """
    democratReturns = dailyReturns['Period'].isin(dailyDemData['Period'])
    democratReturns = dailyReturns[democratReturns]
    democratReturns = democratReturns[['^DJI', '^GSPC','^IXIC']].copy()
    annualReturnsDem = calc_annual_returns(democratReturns)
    return annualReturnsDem


def returnsByPresident(party, dailyReturns):
    import numpy as np
    import math
    """Function to generate a DataFrame Returns by  President.
    Args:
        param1: democrats or republican Presidents and Daily Returns
    Returns:
        Total Return generated During a Democratic or Republican
        Presidential Tenure
    """
    party = party.copy()
    daily = []
    temp2 = []
    temp3 = []
    temp4 = []
    for x in range(len(party)):
        daily = []
        row = party.iloc[x][:]
        dates = pd.date_range(row[0], row[1], freq='D')
        for date in dates:
            daily.append(date)
        daily = set(daily)
        daily = sorted(list(daily))
        dailyData = pd.DataFrame({'Period': daily})
        returns = dailyReturns['Period'].isin(dailyData['Period'])
        returns = dailyReturns[returns]
        returns = returns[['^GSPC', '^DJI','^IXIC']].copy()
        returns = returns['^DJI'].tolist()[:]
        toappend = np.sum(returns)
        daily = set(daily)
        daily = sorted(list(daily))
        dailyData = pd.DataFrame({'Period': daily})
        returns = dailyReturns['Period'].isin(dailyData['Period'])
        returns = dailyReturns[returns]
        returns = returns[['^GSPC', '^DJI','^IXIC']].copy()
        returns2 = returns['^GSPC'].tolist()[:]
        toappend2 = np.sum(returns2)
        returns3 = returns['^IXIC'].tolist()[:]
        toappend3 = np.sum(returns3)
        if toappend is None or toappend == 0.000 or math.isnan(toappend):
            temp2.append('No Data')
        else:
            temp2.append(toappend)

        if toappend2 is None or toappend2 == 0.000 or math.isnan(toappend2):
            temp3.append('No Data')
        else:
            temp3.append(toappend2)
            
        if toappend3 is None or toappend3 == 0.000 or math.isnan(toappend3):
            temp4.append('No Data')
        else:
            temp4.append(toappend3)
    party['^DJI'] = pd.Series(temp2[:], index=party.index)
    temp2 = []
    party['^GSPC'] = pd.Series(temp3[:], index=party.index)
    temp3 = []
    party['^IXIC'] = pd.Series(temp4[:], index=party.index)
    temp4 = []
    return party


def annualReturnsRepCalc(dailyReturns, dailyRepData):
    """Function to Calculate Annual Returns for Republicans Only.
    Args:
        param1: Daily Returns & Republican Daily Returns Subset
    Returns:
        A dataframe of Republican Annual Returns Filtered from the
        Total Population of Annual Returns
    """
    republicanReturns = dailyReturns['Period'].isin(dailyRepData['Period'])
    republicanReturns = dailyReturns[republicanReturns]
    republicanReturns = republicanReturns[['^DJI', '^GSPC','^IXIC']].copy()
    annualReturnsRep = calc_annual_returns(republicanReturns)
    return annualReturnsRep


def chartData(demChartData, repChartData):
    """Function to Extract Descriptive Statistics &
    Convert to a DataFrame.
    Args:
        param1: Democratic & Republican Descriptive Statistics
    Returns:
        A dataframe of Republican & Democratic Descriptive Statisticss
    """

    raw_data = {
        'Description': [
            'Democatic-Dow',
            'Democatic-S&P',
            'Democatic-NASDAQ',
            'Republican-Dow',
            'Republican-S&P',
            'Republican-NASDAQ'],
        'Mean': [
            demChartData['^DJI']['mean'],
            demChartData['^GSPC']['mean'],
            demChartData['^IXIC']['mean'],
            repChartData['^DJI']['mean'],
            repChartData['^GSPC']['mean'],
            repChartData['^IXIC']['mean']],
        'Median': [
            demChartData['^DJI']['50%'],
            demChartData['^GSPC']['50%'],
            demChartData['^IXIC']['50%'],
            repChartData['^DJI']['50%'],
            repChartData['^GSPC']['50%'],
            repChartData['^IXIC']['50%']],
        'Variance': [
            (demChartData['^DJI']['std'])**2,
            (demChartData['^GSPC']['std'])**2,
            (demChartData['^IXIC']['std'])**2,
            (repChartData['^DJI']['std'])**2,
            (repChartData['^GSPC']['std'])**2,
            (repChartData['^IXIC']['std'])**2]}
    df = pd.DataFrame(
        raw_data,
        columns=[
            'Description',
            'Mean',
            'Median',
            'Variance'])
    return df


def plotGroupedBarChart(df):
    """Function to Plot a Grouped Bar Chart of Descriptive Statistics.
    Args:
        param1: A DataFrame of Republican & Democratic Descriptive Statisctics
    Returns:
        A Grouped Bar Plot of the Descriptive Statistics
    """
    pos = list(range(len(df['Mean'])))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.bar(pos,
            df['Mean'],
            width,
            alpha=0.5,
            color='blue',
            label=df['Description'][0])

    plt.bar([p + width for p in pos],
            df['Median'],
            width,
            alpha=0.5,
            color='green',
            label=df['Description'][1])

    plt.bar([p + width * 2 for p in pos],
            df['Variance'],
            width,
            alpha=0.5,
            color='red',
            label=df['Description'][2])

    ax.set_ylabel('Statistics')
    ax.set_title(
        'Market Reactions to Democratic & Republican Presidents \n 1920 to Present')
    ax.set_xticks([p + 1.5 * width for p in pos])
    ax.set_xticklabels(df['Description'])
    plt.xlim(min(pos) - width, max(pos) + width * 4)
    plt.legend(['Mean Annual Return', 'Median Annual Return',
                'Annual Return Variance'], loc='best')
    plt.grid(True)
    plt.show()


"""
All the Above Functions are Called From Below
"""


if __name__ == '__main__':

    """
    Set Start Date & End Date for Data Download
    """

    start = dt.datetime(1920, 1, 1)
    end = dt.datetime(2020, 11, 23)

    """
    Set Tickers for Market Indices
    """

    tickers = ['^DJI',
               '^GSPC',
               '^IXIC']

    """
    Import the List of Presidents and the Dates they were in Office
    from the CSV manually copied from Wikipedia
    """

    presidents = importCSVToDataframe(filePath)

    """
    Subset presidents Data by Party
    """

    democrats = presidents.loc[presidents['Party'] == "Democratic"]

    republicans = presidents.loc[presidents['Party'] == "Republican"]

    dailyDemData = getDailyDemPeriods(democrats)

    dailyRepData = getDailyRepPeriods(republicans)

    """
    Download Stock Data for Market Indices
    """

    closes = web.DataReader(tickers, 'yahoo', start, end)["Adj Close"]
    #closes.set_index('Date', inplace=True)

    """
    Calculate Daily and Annual Returns and Subset by Party
    """

    dailyReturns = dailyReturnsDF(closes)

    dailyReturns['Period'] = dailyReturns.index.values

    annualReturnsDem = annualReturnsDemCalc(dailyReturns, dailyDemData)

    annualReturnsRep = annualReturnsRepCalc(dailyReturns, dailyRepData)

    """
    Generate and Print Descriptive Statistics by Party to Console
    """

    print("")
    print("Democratic Party Performance")
    print("")
    print(annualReturnsDem)
    print("")
    print("Democratic Party Performance")
    print("")
    print(annualReturnsDem.describe())
    print("")

    print("")
    print("Republican Party Performance")
    print("")
    print(annualReturnsRep)
    print("")
    print("Republican Party Performance")
    print("")
    print(annualReturnsRep.describe())
    print("")

    """
    Convert Descriptive Statistics to DataFrame and
    Print to Console
    """
    demChartData = annualReturnsDem.describe()
    repChartData = annualReturnsRep.describe()

    df = chartData(demChartData, repChartData)

    print("")
    print("Key Descriptive Statistics")
    print("")
    print(df)

    dem = returnsByPresident(democrats, dailyReturns)
    rep = returnsByPresident(republicans, dailyReturns)

    print("")
    print("Returns By Presidents - Democratic")
    print("")
    dem.columns =['Start', 'End', 'Name', 'Party', 'Dow', 'S&P500', 'NASDAQ']
    print(dem)

    print("")
    print("Returns By Presidents - Republican")
    print("")
    rep.columns =['Start', 'End', 'Name', 'Party', 'Dow', 'S&P500', 'NASDAQ']
    print(rep)
    
    """
    Plot Group Bar Chart to Console.
    """

    plotGroupedBarChart(df)
