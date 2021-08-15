#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 10:04:16 2018

@author: oluwaseyiawoga
"""

"""
Import Libraries & Packages
"""
import pandas as pd
import numpy as np
from IPython import get_ipython
import matplotlib
matplotlib.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')
pd.set_option('display.precision', 2)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from pylab import rcParams
rcParams['figure.figsize'] = 10, 8



subTickers = ['A',
              'NKE',
              'PKI',
              'HOG',
              'MSI',
              'ED',
              'PRU',
              'MCHP',
              'HBI',
              'RF',
              'ETR',
              'IFF',
              'KR',
              'COP',
              'PFG',
              'ZBH',
              'VTR',
              'URBN',
              'BWA',
              'A',
              'EXPD',
              'APD',
              'MAC',
              'DISCK',
              'YUM',
              'MHK',
              'ZION',
              'MOS',
              'PYPL',
              'JPM',
              'ETFC',
              'NAVI',
              'ROP',
              'AMGN',
              'GD',
              'LMT',
              'CVS',
              'AEE',
              'AMG',
              'BF-B',
              'MU',
              'SWN',
              'JNPR',
              'FITB',
              'CLX',
              'CBOE',
              'AIV',
              'XLNX',
              'IRM',
              'WFC',
              'REGN',
              'BAC',
              'FOXA',
              'TWX',
              'COTY',
              'SYY',
              'ORLY',
              'MSI',
              'MAA',
              'MNK',
              'ADS',
              'SHW',
              'NI',
              'STX',
              'EQR',
              'CME',
              'WMT',
              'BBBY',
              'IPG',
              'HIG',
              'BBT',
              'IR',
              'TDG',
              'KMX',
              'HD',
              'SYY',
              'FLIR',
              'EVHC',
              'NVDA',
              'BEN',
              'FLS',
              'PFE',
              'TGNA',
              'DLPH',
              'MAR',
              'CHD',
              'LNC',
              'CF',
              'BBBY',
              'PYPL',
              'AES',
              'ZTS',
              'UHS',
              'PFE',
              'PAYX',
              'URI',
              'REG',
              'CCL',
              'DNB',
              'L']


def CAGR(df):
    """Function to generate CAGR.
    Args:
        param1: Stock Adjusted Close prices DataFrame for selected tickers
    Returns:
        A dataframe of CAGRs for each ticker in data frame
    """
    columns = df.columns
    newEstDict = dict.fromkeys(columns, 0)
    df = df.loc[:,~df.columns.duplicated()][3:]
    for x in columns:
        df2 = df[x]
        df2 =pd.DataFrame(df2)
        df2.columns = [x]
        df2 = df2[(df2.T != 0).any()]
        
        years = ((df2[x].index[-1] - df2[x].index[0]).days) /365.0
        cagr = ((((df2[x][-1]) /
                  df2[x][1])) ** (1/years)) - 1
        newEstDict[x] = cagr
        
    newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2.columns = ['Tickers', 'CAGR']
    newEstDict2.set_index('Tickers', inplace=True)
    
    return newEstDict2




def monSharpeRatio(df,rf=0.01):
    """Function to generate Monthly Sharpe Ratio.
    Args:
        param1: Stock Adjusted Close prices DataFrame for selected tickers
    Returns:
        A dataframe of Monthly Sharpe Ratio for each ticker in data frame
    """
    columns = df.columns
    newEstDict = dict.fromkeys(columns, 0)
    df = df.loc[:,~df.columns.duplicated()][3:]
    for x in columns:
        df2 = df[x]
        df2 =pd.DataFrame(df2)
        df2.columns = [x]
        df2 = df2[(df2.T != 0).any()]
        df2 = df2.resample('M').sum()
        expectedReturn = df2[x].pct_change().sum()
        vol = df2[x].pct_change().std()
        sharpeRatio = (expectedReturn-rf)/vol
        newEstDict[x] = sharpeRatio
    newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2.columns = ['Tickers', 'Sharpe Ratio']
    newEstDict2.set_index('Tickers', inplace=True)
    
    return newEstDict2



def monthVol(df):
    """Function to generate Monthly Volatility.
    Args:
        param1: Stock Adjusted Close prices DataFrame for selected tickers
    Returns:
        A dataframe of Monthly Volatility for each ticker in data frame
    """
    columns = df.columns
    newEstDict = dict.fromkeys(columns, 0)
    df = df.loc[:,~df.columns.duplicated()]
    for x in columns:
        df2 = df[x]
        df2 =pd.DataFrame(df2)
        df2.columns = [x]
        df2 = df2[(df2.T != 0).any()]
        returns = df2.resample('M').sum()
        returns = returns[x].pct_change()
        newEstDict[x] = returns.std()
    newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2.columns = ['Tickers', 'Volatility']
    newEstDict2.set_index('Tickers', inplace=True)
    
    return newEstDict2



def downSideDeviation(df, threshold = 0.05):
    """Function to generate Downside Deviation.
    Args:
        param1: Stock Adjusted Close prices DataFrame for selected tickers
    Returns:
        A dataframe of Downside Deviation for each ticker in data frame
    """
    columns = df.columns
    newEstDict = dict.fromkeys(columns, 0)
    df = df.loc[:,~df.columns.duplicated()]
    for x in columns:
        df2 = df[x][2:]
        df2 =pd.DataFrame(df2)
        df2.columns = [x]
        df2 = df2[(df2.T != 0).any()]
        returns = df2.resample('M').sum()
        returns = returns[x].pct_change().tolist()
        threshold_array = np.empty(len(returns))
        threshold_array.fill(threshold)
        diff = threshold_array - returns
        diff = diff.clip(min=0)
        diff[np.isnan(diff)] = 0
        res=np.sum(diff ** 2) / len(returns)
        newEstDict[x] = res
    newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2.columns = ['Tickers', 'DownSideRisk']
    newEstDict2.set_index('Tickers', inplace=True)
    
    return newEstDict2

   
        
    

def sortinoRatio(df, threshold = 0.05, riskFree=0.01):
    """Function to generate Sortino Ratio.
    Args:
        param1: Stock Adjusted Close prices DataFrame for selected tickers
    Returns:
        A dataframe of Sortino Ratio for each ticker in data frame
    """
    columns = df.columns
    newEstDict = dict.fromkeys(columns, 0)
    df = df.loc[:,~df.columns.duplicated()]
    for x in columns:
        df2 = df[x]
        df2 =pd.DataFrame(df2)
        df2.columns = [x]
        df2 = df2[(df2.T != 0).any()]
        returns = df2.resample('M').sum()
        returns = np.array(returns[x].pct_change().tolist())
        returns[np.isnan(returns)] = 0
        threshold_array = np.empty(len(returns))
        threshold_array.fill(threshold)
        diff = threshold_array - returns
        diff = diff.clip(min=0)
        res=np.sum(diff ** 2) / len(returns)
        er = np.mean(returns)
        newEstDict[x] = (er-riskFree)/res
    newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2.columns = ['Tickers', 'SortinoRatio']
    newEstDict2.set_index('Tickers', inplace=True)
    
    return newEstDict2
    


def maxDrawDown(df, period=30):
    """Function to generate Max Drawdown.
    Args:
        param1: Stock Adjusted Close prices DataFrame for selected tickers
    Returns:
        A dataframe of Max Drawdownfor each ticker in data frame
    """
    columns = df.columns
    newEstDict = dict.fromkeys(columns, 0)
    df = df.loc[:,~df.columns.duplicated()]
    for x in columns:
        df2 = df[x]
        df2 =pd.DataFrame(df2)
        df2.columns = [x]
        df2 = df2[(df2.T != 0).any()]
        df2 = df2.resample('M').sum()
        Roll_Max = df2[x].rolling(min_periods=1, window=30).max()
        Monthly_Drawdown = df2[x] / Roll_Max - 1.0
        Max_Monthly_Drawdown = Monthly_Drawdown.rolling(min_periods=1, window=30).min()
        newEstDict[x] = abs(min(Max_Monthly_Drawdown))
    newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2.columns = ['Tickers', 'DrawDown']
    newEstDict2.set_index('Tickers', inplace=True)
    
    return newEstDict2

 

def calmarRatio(df, period=30):
    """Function to generate Calmar Ratio.
    Args:
        param1: Stock Adjusted Close prices DataFrame for selected tickers
    Returns:
        A dataframe of Calmar Ratio for each ticker in data frame
    """
    columns = df.columns
    newEstDict = dict.fromkeys(columns, 0)
    df = df.loc[:,~df.columns.duplicated()]
    for x in columns:
        df2 = df[x]
        df2 =pd.DataFrame(df2)
        df2.columns = [x]
        df2 = df2[(df2.T != 0).any()]
        years = ((df2[x].index[-1] - df2[x].index[0]).days) /365.0
        cagr = ((((df2[x][-1]) /
                  df2[x][1])) ** (1/years)) - 1
        df2 = df2.resample('M').sum()
        Roll_Max = df2[x].rolling(min_periods=1, window=30).max()
        Monthly_Drawdown = df2[x] / Roll_Max - 1.0
        Max_Monthly_Drawdown = Monthly_Drawdown.rolling(min_periods=1, window=30).min()
        maxDrawdown = min(Max_Monthly_Drawdown)
        calmarRatio = cagr / float(-maxDrawdown)
        newEstDict[x] = calmarRatio
    newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2.columns = ['Tickers', 'Calmar Ratio']
    newEstDict2.set_index('Tickers', inplace=True)
    
    return newEstDict2




def myPositiveTest(df):
    """Function to generate monthly with positive returns for a Ticker.
    Args:
        param1: Monthly Returns Ticker
    Returns:
        A dataframe of Monthly Positive Returns for Ticker
    """
    return df[df > 0]


def positiveMonthlyReturns(df):
    """Function to generate monthly average positive returns for all Tickers.
    Args:
        param1: Monthly Returns DataFrame
    Returns:
        A dataframe of Monthly Average Positive Returns for All Tickers.
    """
    columns = df.columns
    newEstDict = dict.fromkeys(columns, 0)
    df = df.loc[:,~df.columns.duplicated()]
    for x in columns:
        df2 = df[x]
        df2 =pd.DataFrame(df2)
        df2.columns = [x]
        df2 = df2[(df2.T != 0).any()]
        df2 = df2.resample('M').sum()
        df2 = df2.pct_change()
        temp = myPositiveTest(df2).mean()[0]
        newEstDict[x] = temp
    newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2.columns = ['Tickers', 'Positive Returns']
    newEstDict2.set_index('Tickers', inplace=True)
    return newEstDict2

  

def myNegativeTest(df):
    """Function to generate monthly with Negative returns for a Ticker.
    Args:
        param1: Monthly Returns Ticker
    Returns:
        A dataframe of Monthly Negative Returns for Ticker
    """
    return df[df < 0]


def negativeMonthlyReturns(df):
    """Function to generate monthly average Negative returns for all Tickers.
    Args:
        param1: Monthly Returns DataFrame
    Returns:
        A dataframe of Monthly Average Negative Returns for All Tickers.
    """
    columns = df.columns
    newEstDict = dict.fromkeys(columns, 0)
    df = df.loc[:,~df.columns.duplicated()]
    for x in columns:
        df2 = df[x]
        df2 =pd.DataFrame(df2)
        df2.columns = [x]
        df2 = df2[(df2.T != 0).any()]
        df2 = df2.resample('M').sum()
        df2 = df2.pct_change()
        temp = myNegativeTest(df2).mean()[0]
        newEstDict[x] = temp
    newEstDict2 = pd.DataFrame(newEstDict.items())
    newEstDict2.columns = ['Tickers', 'Negative Returns']
    newEstDict2.set_index('Tickers', inplace=True)
    return newEstDict2





def KPIOutputer(ranKingsList,ranKingsName):
    """Function to print the KPIs
    Args:
        param1: A list of dataframe selected based on rankings and ranking names
    Returns:
        None
        Prints the KPIs to Console
    """
    
    for x in range(len(ranKingsList)):
        df = ranKingsList[x]

        columns = list(set(df.index))
        df = stockData[columns]
        results = pd.DataFrame(index=columns)
        
        temp = CAGR(df)
        results = pd.concat([results, temp], axis=1, join='outer')
               
        temp = monSharpeRatio(df,rf=0.01)
        results = pd.concat([results, temp], axis=1, join='outer')
               
        temp = monthVol(df)
        results = pd.concat([results, temp], axis=1, join='outer')
               
        
        temp = downSideDeviation(df) 
        results = pd.concat([results, temp], axis=1, join='outer')
               
        
        temp = sortinoRatio(df)  
        results = pd.concat([results, temp], axis=1, join='outer')
               
        temp = maxDrawDown(df) 
        results = pd.concat([results, temp], axis=1, join='outer')
               
        
        temp = calmarRatio(df)  
        results = pd.concat([results, temp], axis=1, join='outer')
               
        temp = positiveMonthlyReturns(df)  
        results = pd.concat([results, temp], axis=1, join='outer')
        
        temp = negativeMonthlyReturns(df)  
        results = pd.concat([results, temp], axis=1, join='outer')
        
        
        print("")
        print("Ranking By " + str(ranKingsName[x]))
        print("")
        print(results.T)
        print("")
      
           








"""
Main Function
"""


if __name__ == '__main__':

    

    """
    Import Stock Prices from Pre-Downloaded file on Computer
    in the same directory as this file.
    """

    stockData = pd.read_csv('stockData.csv', index_col=0)
    stockData.head()
    stockData.index = pd.to_datetime(stockData.index)


    histBalSheet = pd.read_csv('histBalSheet.csv', index_col=0)
    
    histBalSheet.fillna(value=0, inplace=True)


    histincomeStmt = pd.read_csv('histincomeStmt.csv', index_col=0)
    
    histincomeStmt.fillna(value=0, inplace=True)


    histCashFlow = pd.read_csv('cashincomeStmt.csv', index_col=0)
    
    histCashFlow.fillna(value=0, inplace=True)
  
    peratio = pd.read_csv('peratio.csv', index_col=0)
    
    marketCap = pd.read_csv('marketCap.csv', index_col=0)
    
    marketCap.fillna(value=0, inplace=True)
    
    """
    Calculate the Balance Sheet Metrics
    """
    rankings = pd.DataFrame(index=subTickers)
    
    rankings["EarningsYield"] = 1.0/peratio["PE Ratio"]
    
    rankings[rankings == np.inf] = 0.0
    
    rankings["EBITA"]= histincomeStmt.loc["ebit"].tolist()
    
    currentMktPrice =  stockData.iloc[-1]
    
    histCashFlowTransposed = histCashFlow.T
    

    rankings["FCFlowYield"] = (histCashFlowTransposed["totalCashFromOperatingActivities"]-\
                                     histCashFlowTransposed["capitalExpenditures"])/marketCap["Market Cap"]

    
    histBalSheetTransposed = histBalSheet.T
    
    histincomeStmtTransposed = histincomeStmt.T
    
    
    rankings["ROCE"] = histincomeStmtTransposed["ebit"]/((histBalSheetTransposed["cash"]+histBalSheetTransposed["shortTermInvestments"]+\
                                      histBalSheetTransposed["netReceivables"] + histBalSheetTransposed["inventory"] -\
                                      histBalSheetTransposed["accountsPayable"])+histBalSheetTransposed["netTangibleAssets"])
    
    rankings["bkTomkt"] =  histBalSheetTransposed["totalStockholderEquity"]/marketCap["Market Cap"]
    
    
    """
    Rank the Balance sheet metrics and identify the lowest deciles
    """
    EarningsYieldRankings = rankings[rankings.EarningsYield < rankings.EarningsYield.quantile(.90)].sort_values(by=['EarningsYield'], ascending=False)[:20]
    EBITARankings = rankings[rankings.EBITA < rankings.EBITA.quantile(.90)].sort_values(by=['EBITA'], ascending=False)[:20]
    FCFlowYieldRankings =rankings[rankings.FCFlowYield < rankings.FCFlowYield.quantile(.10)].sort_values(by=['FCFlowYield'], ascending=False)[:20]
    ROCERankings=rankings[rankings.ROCE < rankings.ROCE.quantile(.90)].sort_values(by=['ROCE'], ascending=False)[:20]
    bkTomktRankings=rankings[rankings.bkTomkt < rankings.bkTomkt.quantile(.10)].sort_values(by=['bkTomkt'], ascending=False)[:20]
    
    ranKingsList = [EarningsYieldRankings,EBITARankings,FCFlowYieldRankings,ROCERankings,bkTomktRankings]
    
    ranKingsName= ["EarningsYieldRankings","EBITARankings","FCFlowYieldRankings","ROCERankings","bkTomktRankings"]
    
    """
    Print the Balance Sheet Metrics
    """
    
    for x in range(len(ranKingsList)):
        print("")
        print("FUNDAMENTAL BALANCE SHEET METRICS")
        print("")
        print("Ranking By " + str(ranKingsName[x]))
        print("")
        print(ranKingsList[x])
        print("")
    
    """
    Print the KPIs based on rankings Generated by the Balance Sheet Metrics
    """
    
    print("")
    print("KPI OUTPUT BY FUNDAMENTAL METRICS")
    print("")
    KPIOutputer(ranKingsList,ranKingsName)
