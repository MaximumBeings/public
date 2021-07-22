import numpy as np
import scipy.interpolate 
import pylab
import pandas_datareader.data as web
import datetime   
from scipy.optimize import leastsq
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
from dateutil.relativedelta import relativedelta





"""
Prompt the User for a Valid Ticker and Keep prompting
Until User Supplies a Valid Ticker.
Using the Ticker Supplied, Download Stock Data for the 
Last 30 days and perform some preprocessing.

"""


def getData(prompt = "Please Enter a Valid Ticker: " ):
    """
    Helper function for accepting user input (string)
    and  it does error checking as
    well
    """
    checker = True
    while(checker):
        try:
            symbol = input(prompt).strip().upper()
            quotes = web.DataReader(symbol, 'yahoo', start, end)['Open']
            checker = False
            quotes = pd.DataFrame(quotes)
            time = [x+1 for x in range(len(quotes.index))]
            quotes['Time'] = time[:]
            return quotes[['Time', 'Open']]
        except :
            checker = True
            print("")
            print("Not a Valid Ticker, Please Try Again!!")
            print("")
            

if __name__ == '__main__':
    
    """
    Set the start and End Date Using Datetime
    """

    end = datetime.datetime.today()
    start = end - relativedelta(months=1)


    """
    Call the getData() function and save the Downloaded data into a variable
    called FinalData
    """
    
    FinalData = getData()


    """
    INTERPOLATION USING QUADRATIC FIT
    """
    """
    The Interpolation Functions in Scipy Expects
    an array of floats so we already set the 
    dates to correspond to len(dataFrame) e.g
    range(0,30)

    The range and stock prices are then converted to 
    numpy arrays.

    We also added noise to our signals or stock prices
    """


    xArray = np.array(FinalData['Time'].tolist())
    yArray = np.array(FinalData['Open'].tolist())
    yArray += yArray + 10.5 + np.random.random(len(xArray))
    xfine = np.linspace(1,len(xArray), len(xArray)*2)


    """
    Interpolate Using the Quadratic Fit Using Scipy.
    """

    y1 = scipy.interpolate.interp1d(xArray, yArray , kind = 'quadratic')

    """
    Plot the Original Data and the Interpolated Data
    """


    pylab.plot(xArray, yArray, 'ro', label = "Original Data")
    pylab.plot(xfine, y1(xfine), 'b--', label = "Interpolated Quadratic Method")
    pylab.title("Interpolated Stock Price \n Quadratic Method")
    pylab.legend(loc = 'best')
    pylab.show()
    pylab.close()
    
    """
    Least Square Regression Quadratic Fit
    """

    """
    Quadratic Equation:
    ax^2 + bx + C
    Each Element in p or parameters list represents [a,b,c]
    """

    """
    The fitfunc is the quadratic equation using lambda or functional
    programming
    """

    fitfunc = lambda p, x: p[0]*(x**2) + p[1]*x + p[2]

    """
    The errfunc minimize the sum of squared errors between the predicted 
    and the observed
    """
    errfunc = lambda p, x, y: fitfunc(p, x) - y

    """
    Initial Guess Paramters
    """

    p = [2,2,2]  #reprsents a, b, c (Initial Guess) #shd be supplied as a list.

    p1, success = leastsq(errfunc, p[:], args=(xArray,yArray))

    """
    p1 is the estimated parameters
    E.g
    array([ -4.30796715e-02,   1.16557961e+00,   3.26702857e+02])
    """

    """
    Using the estimated Parameters plot the fitted data and the Original data
    """

    yerror = fitfunc(p1,xArray) - yArray
    pylab.xticks(rotation=70)
    pylab.plot(FinalData.index.values, fitfunc(p1,xArray),'b--',label = 'Fitted Data')
    pylab.errorbar(FinalData.index.values,yArray, yerr = yerror,fmt='ro',color='red',label='Original Data & Error Bar')
    pylab.title("Interpolation & Curve Fitting in Python \n Quadratic Fit")
    pylab.legend(loc = 'best')
    pylab.show()
    
    
    """
    The data is not a good candidate for interpolation. Interpolation techniques are great for filling gaps within a dataset. 
    However, the data we are supposed to interpolate does not have missing information but rather consist of the daily stock 
    prices for a ticker over 30 days. The problem with using an interpolation methodology to fit this data is that most likely 
    you will get a perfect fit or it will most likely result in overfitting. A curve fitting technique like the least square 
    regression method is apt in this case. This is because the least square method finds the line of best fit that minimizes 
    the sum of squared errors. A good candidate for interpolation is the term structure of interest rate. This is because 
    interest rates are observable for only certain tenors and the unobservable rates have to be interpolated first before 
    bootstrapping in order to determine the zero rate. Consider, a rather simple case of LIBOR rates. These rates are only 
    observable for certain tenors and the rates for tenors that are not directly observable have to be interpolated first 
    before being bootstrapped.
    
    Another key challenge here is that the independent variable or x-axis is in date time format but the interpolation 
    techniques in Pylab, Numpy and Scipy expects an array of floats. So a walk around is to look for a way to get the 
    number representations of the dates. For example, xArray could be set as len(stockData.index.values) in which case 
    it becomes (1,2,3,4.......30) or one could use toOrdinal and fromOrdinal to convert the dates to there integer 
    representations. That said, I am happy with the output generated by the program as the interpoated data passes 
    through the original data. A sample chart of the interpolated stock data for as shown in the chart.
    """









