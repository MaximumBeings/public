#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 08:30:31 2018

@author: oluwaseyiawoga
"""

"""
Import Libraries & Packages
"""

import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy as sp
import pandas_datareader.data as web
import datetime   


"""
    QUESTION - Problem 1:
        
    (a) A company is investing in two securities, x1 and x2.  
        Fictitious Portfolio - (Source: Investopedia):
        Stock A is worth $50,000 and has a standard deviation of 20%. 
        Stock B is worth $100,000 and has a standard deviation of 10%. 
        The correlation between the two stocks is 0.85. 
    
        The capital market division
        of the company indicated the following constraints to the investment strategy:

    (b) Short selling is not allowed. Specifically, the portfolio must consist of at least
        10% of either stock A or B.
    
    (c) The company wants to maximize the sharpe ratio (defined here as return/vol)
    
    (d) Assume that the portfolio return is 5% or 0.05
        
    (e) The company requests the following from you:
        
        . Indicate the objective function.
        . Write the optimization problem.
        . Find w1 and w2 values that minimizes the objective function 
          and explain the algorithm.
          
    (f) Use the pulp modeler for Python.
    
    (g) Using optimization techniques calculate the weight that Maximizes risk-adjusted return
    
    SOLUTION:
        
    Objective Function:
        
        Maximiize : return/portfolio variance 
        where portfolio variance = w1**2 * 0.2**2 + w2**2 * 0.1**2 + 2 * w1 * w2 * 0.85 * 0.2 * 0.1
        
    Subject to:
        
        Constraints:
             
        w1 + w2 == 1
            
        Non-Negativity Constraints:
            
            w1,w2 >= 0
            w1 >= 0.1
            w2 >= 0.1
            
    The above example is a rather simple toyish example? Suppose we want to mimic the dow
    jones index but want to buy the underlying stocks in a manner that maximizes the sharpe ratio
    or the risk-adjusted return. How may we achieve this. The second Github link shows how
    one may implement this in Python. Specifically, the program fetches data for the underlying
    stocks from 2015 to July 27, 2021 and then using a Monte Carlo like approach finds the
    weights that maximizes the risk-adjusted return. This is a slight refactor of the code by
    Jose Portilla in Finance and Trading Algorithms in Python on Udemy.

"""

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

"""
Main Function
"""



if __name__ == '__main__':
    
    def con(w):
        return w[0] + w[1] - 1
    
    def portfolioVariance(x):
        risk = x[0]**2 * 0.2**2 + x[1]**2 * 0.1**2 + 2 * x[0] * x[1] * 0.85 * 0.2 * 0.1
        return 0.05/risk
    
    def optimizer(x):
        """
        Function optimize for the best buy and sell percentage.
            param1: An array of buy and sell percentages Guess
            e.g. [0.2,0.1]
        Returns:
            An optimal array of buy and sell percentages
        """
    
        return -1 * (portfolioVariance(x))
    
    cons = {'type':'eq', 'fun': con}
    guess = [0.2, 0.1]
    
    optimizedResult = scipy.optimize.minimize(optimizer, guess,constraints=cons,bounds=[(0.1,1),(0.1,1)])
    print("")
    print(optimizedResult)


    start = '2015-01-01'
    end = '2021-07-27'
    final = stockDownloader(dow)
    final=final.pct_change()
    final.dropna(inplace=True)
    tickers = final.columns
    print(final.head())

    num_ports = 15000*6
    
    all_weights = np.zeros((num_ports,len(final.columns)))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)
    
    for ind in range(num_ports):
    
        # Create Random Weights
        weights = np.array(np.random.random(len(final.columns)))
    
        # Rebalance Weights
        weights = weights / np.sum(weights)
        
        # Save Weights
        all_weights[ind,:] = weights
    
        # Expected Return
        ret_arr[ind] = np.sum((final.mean() * weights) *252)
    
        # Expected Variance
        vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(final.cov() * 252, weights)))
    
        # Sharpe Ratio
        sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]
        
        
    best = sharpe_arr.argmax()
    
    
    print("")
    print("Optimal Weights:")
    print("")
    print(all_weights[best,:])
    
    max_sr_ret = ret_arr[best]
    max_sr_vol = vol_arr[best]
    
    
    
    plt.figure(figsize=(12,8))
    plt.scatter(vol_arr,ret_arr,c=sharpe_arr,cmap='plasma')
    plt.colorbar(label='Sharpe Ratio')
    plt.title(" Portfolio Efficient Frontier")
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    
    
    # Add red dot for max SR
    plt.scatter(max_sr_vol,max_sr_ret,c='yellow',s=300,edgecolors='red')
    plt.show()
    
    
   
