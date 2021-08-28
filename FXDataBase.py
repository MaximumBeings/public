#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 09:08:46 2018

@author: oluwaseyiawoga
"""

"""
Dependencies:
    pip install sqlalchemy
    fixer.io API Key - Get yours for free
"""

import pandas as pd
import numpy as np
from IPython import get_ipython
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas_datareader.data as web
import datetime as dt
import requests
import json
from sqlalchemy import create_engine
import seaborn
seaborn.mpl.rcParams['figure.figsize'] = (12.0, 8.0)
np.warnings.filterwarnings('ignore')
import seaborn as sns


def periodString(periods):
    """Function to generate periods and convert datetime to date strings.
    Args:
        param1: A data range of the period for the data request
    Returns:
        A list of string dates
    """
    dateString = []
    for x in range(len(periods)):
        year = periods[x].year
        month = periods[x].month
        day = periods[x].day
        if month < 10:
            month = str(0) + str(month)
        if day < 10:
            day = str(0) + str(day)
        toUse = str(year) + "-" + str(month) + "-" + str(day)
        dateString.append(toUse)
    return dateString


def createURL(dtString):
    """Function to generate URL for fixer.io for a particular day.
    Args:
        param1: date in string format e.g. "2008-01-01"
    Returns:
        A URL to pull the data for that day from
    """
    api_key= "INSERT YOUR API KEY HERE"
    
    url = f"http://data.fixer.io/api/{dtString}?access_key={api_key}"
    

    return url


def getFXData(url):
    """Function to get data from a particular URL
    Args:
        param1: URL
    Returns:
        A dictionary of FX Rates for a particular day
    """
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    rates = parsed["rates"]
    return rates


def createFXPandasDF(dateString):
    """Function to get data for a data range using all the above helper functions
    Args:
        param1: A list of date range in string format
    Returns:
        A Data Frame of rates for all the dates in date range
    """

    url = createURL(dateString[0])
    rates = getFXData(url)
    FXData = pd.DataFrame(index=rates.keys())
    for x in range(len(dateString)):
        url = createURL(dateString[x])
        rates = getFXData(url)
        result = pd.DataFrame(index=rates.keys())
        result[dateString[x]] = rates.values()
        result.columns = [dateString[x]]
        FXData = pd.concat([FXData, result], axis=1, join='outer')

    return FXData


"""
Main Function
"""


if __name__ == '__main__':

    """
    Generate the period for which the data is required
    """
    periods = pd.date_range(start='6/1/2018', end='6/20/2018', freq='D')

    """
    Parse the date to strings
    """

    dateString = periodString(periods)

    """
    Get the data from FIXER.IO and convert to pandas dataframe
    Save a copy on hard drive for reuse
    interpolate missing data
    """

    juneFXData = createFXPandasDF(dateString)
    juneFXData = juneFXData.T
    juneFXData["dateTime"] = pd.to_datetime(juneFXData.index)
    juneFXData.set_index('dateTime', inplace=True)
    juneFXData = juneFXData.interpolate(method='linear')
    juneFXData.fillna(value=0, inplace=True)
    juneFXData.to_csv('juneFXData.csv')

    print(juneFXData.head())
    
    print(juneFXData.iloc[:, 0:5].head())

    FXdata = pd.read_csv('juneFXData.csv', index_col=0)
    FXdata.index = pd.to_datetime(FXdata.index)

    """
    Sample SQL Table and Queries - Simple Implementations
    """

    engine = create_engine('sqlite://', echo=False)

    FXdata.to_sql('FXData2', con=engine, if_exists='replace')

    q1 = engine.execute("SELECT EUR,ZMK,USD FROM FXData2").fetchall()

    for row in q1:
        print(row)

    print("")
    print("")
    q2 = engine.execute(
        "SELECT EUR,USD FROM FXData2 WHERE USD>1.16").fetchall()

    for row in q2:
        print(row)

    """
    Plot a ClusterMap of a Random Subset of 10 Currencies
    """
    FXSubset = FXdata.sample(10, axis=1)
    print("")
    print("Clustermap for 10 Sample Currencies")
    print("")
    sns.clustermap(FXSubset.corr(), annot=True)
    plt.show()
