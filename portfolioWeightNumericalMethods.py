#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 14:20:33 2017

@author: oluwaseyiawoga
"""

#SOURCE: Finance and Trading Algorithms in Python by Jose Portilla on Udemy


#import quandl
import numpy as np
np.set_printoptions(suppress=True)
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy as sp
import pandas_datareader.data as web
import datetime   
plt.style.use('ggplot')

import scipy




dow = ["AXP","AMGN","AAPL","BA","CAT","CSCO","CVX","GS","HD","HON",\
             "IBM","INTC","JNJ","KO","JPM","MCD","MMM","MRK","MSFT","NKE","PG",\
                 "TRV","UNH","CRM","VZ","V","WBA","WMT","DIS","DOW"]


#pip install pandas-datareader --upgrade

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
            result = web.DataReader(tick, 'yahoo',start, end)["Close"]
            result = pd.DataFrame(result)
            result.columns = [tick]
            stockData = pd.concat([stockData, result], axis=1, join='outer')
        except BaseException:
            pass

    return stockData


if __name__ == "__main__":
    
    start = '2015-01-01'
    end = '2021-07-27'
    final = stockDownloader(dow)
    final=final.pct_change()
    final.dropna(inplace=True)
    tickers = final.columns
    print(final.head())

    
    #all_weights = np.zeros((num_ports,len(final.columns)))
    #ret_arr = np.zeros(num_ports)
    #vol_arr = np.zeros(num_ports)
    #sharpe_arr = np.zeros(num_ports)
    
    
    
        
    def con(w):
        return sum(w) - 1

    
    
    def optimizer(weights):
        """
        Function optimize for the best buy and sell percentage.
            param1: An array of buy and sell percentages Guess
            e.g. [0.2,0.1]
        Returns:
            An optimal array of buy and sell percentages
        """
        retToUse =  np.sum((final.mean() * weights) *252)
        return_arr.append(retToUse)
    
        volToUse = np.sqrt(np.dot(weights.T, np.dot(final.cov() * 252, weights)))
        
        vol_arr.append(volToUse)

        sharpeRatio = retToUse/volToUse
        
        #sharpeRatio = portFolioVariance(x)
        
        sharpe_arr.append(sharpeRatio)
        
        return -1 * sharpeRatio
    
    cons = {'type':'eq', 'fun': con}
    guess = list(np.array(np.random.random(len(final.columns))))
    
    sharpe_arr = []
    return_arr = []
    vol_arr = []
    
    optimizedResult = scipy.optimize.minimize(optimizer, guess,constraints=cons)
    print("")
    print(optimizedResult)
    
    sharpe_arr = np.array(sharpe_arr)
    best = sharpe_arr.argmax()
    
    print("")
    print("Optimal Weights:")
    print("")
    
    
    max_sr_ret = return_arr[best]
    max_sr_vol = vol_arr[best]
    plt.figure(figsize=(12,8))
    plt.scatter(vol_arr[500:],return_arr[500:],c=sharpe_arr[500:],cmap='plasma')
    
    plt.colorbar(label='Sharpe Ratio')
    plt.title(" Portfolio Efficient Frontier")
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    
     # Add red dot for max SR
    plt.scatter(max_sr_vol,max_sr_ret,c='yellow',s=300,edgecolors='red')
    plt.plot(vol_arr[500:],return_arr[500:])
    plt.show()
    
    
    
    
    
    
    sharpe_arr = []
    return_arr = []
    vol_arr = []
    
    def optimizer2(weights):
       """
       Function optimize for the best buy and sell percentage.
           param1: An array of buy and sell percentages Guess
           e.g. [0.2,0.1]
       Returns:
           An optimal array of buy and sell percentages
       """
       retToUse =  np.sum((final.mean() * weights) *252)
       return_arr.append(retToUse)
   
       volToUse = np.sqrt(np.dot(weights.T, np.dot(final.cov() * 252, weights)))
       
       vol_arr.append(volToUse)

       sharpeRatio = retToUse/volToUse
       
       #sharpeRatio = portFolioVariance(x)
       
       sharpe_arr.append(sharpeRatio)
       
       return -1 * sharpeRatio
    
    def con2(w):
        return sum(w) - 100
    
    cons2 = {'type':'eq', 'fun': con2}
    guess = [1.00 for x in range(len(final.columns))]
    boundsToUse = [(1.00,100.00) for x in range(len(final.columns))]
    
    optimizedResult = scipy.optimize.minimize(optimizer2, guess,constraints=cons2,bounds=boundsToUse)
    print("")
    print(optimizedResult)
    
    sharpe_arr = np.array(sharpe_arr)
    best = sharpe_arr.argmax()
    
    print("")
    print("Optimal Weights:")
    print("")
    
    
    max_sr_ret = return_arr[best]
    max_sr_vol = vol_arr[best]
    plt.figure(figsize=(12,8))
    plt.scatter(vol_arr[100:],return_arr[100:],c=sharpe_arr[100:],cmap='plasma')
    
    plt.colorbar(label='Sharpe Ratio')
    plt.title(" Portfolio Efficient Frontier")
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    
     # Add red dot for max SR
    plt.scatter(max_sr_vol,max_sr_ret,c='yellow',s=300,edgecolors='red')
    plt.plot(vol_arr[100:],return_arr[100:])
    plt.show()
    
    
    sharpe_arr = []
    return_arr = []
    vol_arr = []
    
    def optimizer2(weights):
       """
       Function optimize for the best buy and sell percentage.
           param1: An array of buy and sell percentages Guess
           e.g. [0.2,0.1]
       Returns:
           An optimal array of buy and sell percentages
       """
       retToUse =  np.sum((final.mean() * weights) *252)
       return_arr.append(retToUse)
   
       volToUse = np.sqrt(np.dot(weights.T, np.dot(final.cov() * 252, weights)))
       
       vol_arr.append(volToUse)

       sharpeRatio = retToUse/volToUse
       
       #sharpeRatio = portFolioVariance(x)
       
       sharpe_arr.append(sharpeRatio)
       
       return -1 * sharpeRatio
    
    def con2(w):
        return sum(w) - 100
    
    cons2 = {'type':'eq', 'fun': con2}
    guess = [1.00 for x in range(len(final.columns))]
    boundsToUse = [(0.00,100.00) for x in range(len(final.columns))]
    
    optimizedResult = scipy.optimize.minimize(optimizer2, guess,constraints=cons2,bounds=boundsToUse)
    print("")
    print(optimizedResult)
    
    sharpe_arr = np.array(sharpe_arr)
    best = sharpe_arr.argmax()
    
    print("")
    print("Optimal Weights:")
    print("")
    
    
    
    
    
