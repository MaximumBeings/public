#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 12:57:59 2018

@author: oluwaseyiawoga
"""

import pandas as pd
import numpy as np
from IPython import get_ipython
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')
pd.set_option('display.precision', 2)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
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
np.warnings.filterwarnings('ignore')
from scipy.optimize import fmin



def regressionHelper(a,b):
    
    y_pred = [] # a + bX
    for item in range(len(X)):
        y_pred.append(a + b * X[item])
    return y_pred

def regressionHelper2(a,b):
    y_pred = regressionHelper(a,b)
    temp = []
    for item in range(len(X)):
        res = (y[item]-y_pred[item])**2
        temp.append(res)
    return sum(temp)


def optimizer(Guess):
    """
    Function optimize for the best buy and sell percentage.
        param1: An array of buy and sell percentages Guess
        e.g. [0.2]
    Returns:
        An optimal array of buy and sell percentages
    """

    return regressionHelper2(Guess[0],Guess[1])

def predictedY(optimizedResult):
    y_pred =optimizedResult[0] + optimizedResult[1] * X
    
    return y_pred

if __name__ == '__main__':
    
    X = np.array([1,2,3,4,5,6,7,8,9,10])
    y = X*2
    
    
    guess = [100,160]
    
    optimizedResult = fmin(optimizer, guess)
    
    print("")
    print(optimizedResult)
    
    y_pred = predictedY(optimizedResult)
    
    print()
    print(y_pred)
    
    dataTable = pd.DataFrame()
    dataTable["X"] = X
    dataTable["Y"] = y
    dataTable["Predicted"] = y_pred
    
    print("")
    print(dataTable)
    
    """
    [ 2.0000118   4.00000773  6.00000367  7.9999996   9.99999553 11.99999146
     13.99998739 15.99998333 17.99997926 19.99997519]
    
        X   Y            Predicted
    0   1   2                2.000
    1   2   4                4.000
    2   3   6                6.000
    3   4   8                8.000
    4   5  10               10.000
    5   6  12               12.000
    6   7  14               14.000
    7   8  16               16.000
    8   9  18               18.000
    9  10  20               20.000
    """
    
    from sklearn.linear_model import LinearRegression
    
    X = np.array([1,2,3,4,5,6,7,8,9,10])
    y = X*2
    
    
    lr = LinearRegression()
    
    model = lr.fit(X.reshape(-1, 1),y)
    y_pred=model.predict(X.reshape(-1, 1))
    
    dataTable = pd.DataFrame()
    dataTable["X"] = X
    dataTable["Y"] = y
    dataTable["Predicted"] = y_pred
    
    print("")
    print(dataTable)
    
    """
    
        X   Y            Predicted
    0   1   2                2.000
    1   2   4                4.000
    2   3   6                6.000
    3   4   8                8.000
    4   5  10               10.000
    5   6  12               12.000
    6   7  14               14.000
    7   8  16               16.000
    8   9  18               18.000
    9  10  20               20.000
    """
