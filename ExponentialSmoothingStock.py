#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import libraries and packages

#Anaconda Version 3.5 and above required

"""
ADDITIONAL NOTE ON REQUIRED PACKAGES:
Requires pandas-datareader (install as shown below):
from Terminal on a mac if you already have Anaconda 
installed conda install -c anaconda pandas-datareader=0.2.1
or pip install pandas-reader
"""

import numpy as np
import math
import pandas_datareader.data as web
import datetime   
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')




"""
Part 1: Obtain the stock price information from www.nasdaq.com. in this
part, go to www.nasdaq.com, choose a company to analyze, click the "historical
quotes" link on the left side after picking a company.  Pick the stock prices
for at least 8 months picking one data point out of each month as close to the
first of the month as possible.  The x values will be from 1 to 8 
(where 1 indicates the first month looked at) while the y values will be the
stock price.

NOTE: The data for this analysis was limited to the first occurence of the 
stock price on a mpnthly basis per requirements in the final project 
specifications. However, the code below can be easily resampled to use
mean, median or last data
"""

start = datetime.datetime(2015, 1, 1)
end = datetime.datetime.today().strftime("%m/%d/%Y")
symbol = 'AAPL'

def downLoadData(start,end,symbol):
    """
    CSCO or the Company CISCO was chosen from the list of companies 
    quoted on NASDAQ.
    This funtions helps to download the data directly from Yahoo Finance
    Using pandas_datareader.data
    """
    quotes = web.DataReader(symbol, 'yahoo', start, end)['Open'][-360:]
    MonthStart = quotes.resample('MS').first()
    MonthStart = pd.DataFrame(MonthStart)
    time = [x+1 for x in range(len(MonthStart))]
    MonthStart['Time'] = time[:]
    return MonthStart[['Time', 'Open']]


FinalData = downLoadData(start,end,symbol)

#FinalData.to_csv('/Users/oluwaseyiawoga/Desktop/CSCO.csv', sep='\t')

#print(FinalData)


"""
            Time       Open
Date                       
2015-11-01     1  27.250000
2015-12-01     2  27.200001
2016-01-01     3  26.389999
2016-02-01     4  23.459999
2016-03-01     5  26.450001
2016-04-01     6  28.299999
2016-05-01     7  27.480000
2016-06-01     8  28.840000
2016-07-01     9  28.780001
2016-08-01    10  30.700001
2016-09-01    11  31.420000
2016-10-01    12  31.309999
2016-11-01    13  30.850000
2016-12-01    14  29.840000
2017-01-01    15  30.370001
2017-02-01    16  30.850000
2017-03-01    17  34.279999
2017-04-01    18  33.700001
2017-05-01    19  34.110001
"""


FinalData.set_index('Time', inplace=True)
#print(FinalData)

#Replace index with 1 to len(dataframe)

"""
           Open
Time           
1     27.250000
2     27.200001
3     26.389999
4     23.459999
5     26.450001
6     28.299999
7     27.480000
8     28.840000
9     28.780001
10    30.700001
11    31.420000
12    31.309999
13    30.850000
14    29.840000
15    30.370001
16    30.850000
17    34.279999
18    33.700001
19    34.11000
"""

"""
"""


"""
Part 2: Write a Python program that asks the user for the information from 
part 1 and performs exponential smoothing based on it. The perfect program 
will allow the user to input alpha, display the graph of the original data 
and the “smoothed data” and have the user verify if this model is appropriate.
If it is not then it should loop asking for new entries for alpha until the 
user indicates the model is appropriate. At this point, it should use the 
exponential smoothing model to predict time period 9 (x = 9). Read the 
explanation above closely to understand what exponential smoothing provides
for the next month based on the previous month.
"""


"""
Split data into Training and Test sets
Per specifications in the final project
"""


#Training Set
trainingSetTime = FinalData.index.values[:-1][:]
trainingSetPrices = FinalData["Open"].tolist()[:-1]


#Testing Set
testingSetTime = FinalData.index.values[-1]
testingSetPrices = FinalData["Open"].tolist()[-1]



#Modules and Helper Functions

def predict(trainingSetTime,trainingSetPrices, alpha):
    """
    Exponential Smoothing Function 
    Source: WQU Final Projects
    F_t+1 = alpha*Y_t + (1 - alpha) * F_t
    where
    F_t+1 = Forecast for time period t + 1
    Y_t = Time series Value
    F_t = Forecast for time period t
    alpha = Smoothing Constant (Between 0 and 1)
    Note: F_1 = Y_1
    """
    forecast = []
    for x in range(len(trainingSetTime)):
        if x == 0:
            forecast.append(trainingSetPrices[x])
        elif x > 0:
            forecast.append(alpha * trainingSetPrices[x] + (1-alpha)*forecast[x-1])
    return forecast
        

#Out of Sample Prediction:

def OutOfSamplePrediction(Forecast,testingSetTime,testingSetPrices, alpha):
    """
    This helper function helps to predict the testing Set
    That is the Out of Sample Population for Next Month
    By Calling the predict function
    """
    Output=[]
    predicted = alpha * testingSetPrices + (1-alpha)*Forecast[-1]
    Forecast.append(predicted)
    Output = pd.DataFrame(
    {'Time': FinalData.index.values[:],
     'Forecast': Forecast[:]
    })
    Output = Output[['Time', 'Forecast']]
    return Output


def plotChart(Output):
    """
    This helper function helps to plot
    the original data and the predicted data
    Using Matplotlip and the helper functions
    Created Above
    """
    plt.close('all')
    fig, ax = plt.subplots(1)
    ax.plot(Output['Time'],Output['Forecast'],'g',lw=1.5, \
            label='Forecast')
    plt.title(symbol + ' Exponential Smoothing Forecast\n Vs. Actual')
    plt.legend(loc=0)
    plt.grid(True)
    plt.plot(FinalData['Open'], 'r', lw=1.5, label='Observed Prices')
    plt.ylabel('Prices')
    plt.xlabel('Months')
    plt.legend(loc=0)
    plt.grid(True)
    plt.show()


def input_float(prompt):
    """
    Helper function for accepting user input
    for the Alpha and it does error checking as
    well
    """
    while True:
        try:
            x =  float(input(prompt))
            if x < 0 or x > 1:
                print(" ")
                print('That is not a valid alpha.')
            elif x >= 0 or x <= 1:
                return x
        except ValueError:
            print('That is not a valid number.')
            
def input_string(prompt):
    """
    Helper function for accepting user input (string)
    and  it does error checking as
    well
    """
    while True:
        try:
            x = input(prompt).strip().lower()
            if x in ('yes','no'):
                return x
            print(" ")
            print('That is not a valid choice.')
        except ValueError:
            print('That is not a valid choice.')
            

"""
Part 3: In the same Python program, the information from NASDAQ should be 
used to develop a linear regression model that is used to predict time 
period 9. It should show the correlation coefficient to indicate the strength 
of the model. No other tool is necessary for this project to test the 
appropriateness of using a linear regression model.

NOTE: This could have also be done using SKLEARN library but was done
using the class material instead.
"""            
            
def CorrelationCoefficient(x,y):
    """
    Helper Function to calculate
    Pearson Correlation Cooefficient
    Formula:
    numerator = n*(sum_xy) - (sum_x*sum_y)
    denominator = sqrt([(n*sum_x**2)-(sum_x**2)][(n*sum_y**2)-(sum_y**2)])
    r = numerator / denominator
    Source: WQU Class Notes (Statistics & Python)
    """
    n = len(x)
    assert len(x) == len(y)  #Error Checking
    sum_x = sum(x)
    sum_y = sum(y)
    xy = sum([i*j for i,j in zip(x,y)])
    x_squared = sum([i**2 for i in x ])
    y_squared = sum([i**2 for i in y ])
    
    numerator = (n * xy) - (sum_x*sum_y)
    denominator = math.sqrt((n*x_squared-sum_x**2)*(n*y_squared-sum_y**2))
    
    return numerator / denominator

    

def leastSquares_Regression(x,y):
    """
    Function to calculate least square Regression
    Formula:
    b_1 = r_(x,y) * S_y/S_x
    b_0 = y_bar - B-1*x_bar
    Source: WQU Class Materials
    """
    b1 = CorrelationCoefficient(x,y)*np.std(y)/np.std(x)
    b0 = np.mean(y) - b1*np.mean(x)
    return b1,b0
    


def outPutPrinter(Output):
    """
    To help print Outputs from the main function
    Called by the main function once user is 
    satisfied with the model
    """
    print("")
    print("Forecast including Out of Sample Prediction")
    print("")
    print(Output.to_string(index=False))
    print("")
    print("Predicted - Out of Sample Row Only")
    print("")
    print(Output.tail(1).to_string(index=False))
    print("")
    print("Least Square Regression Equation")
    b1,b0 = leastSquares_Regression(trainingSetTime,trainingSetPrices)
    print("")
    print ("y = " + str(b0) + " + " + str(b1)+"x")  
    print("")
    print("Pearson Correlation Coefficient")
    print("")
    print(CorrelationCoefficient(trainingSetTime,trainingSetPrices))
    print("")
    print("Prediction for Next Month Using Linear Regression:")
    print("")
    print ("y = " + str(b0 + b1*testingSetTime))  
    
            
"""
Main Function
"""
def finalProgram():
    """
    Accepts user input for alpha and generates the smoothed data
    and once the user is satisfied generated the linear model using
    regression.
    Calls all the functions above
    """
    satisfied = 'no'
    alpha = input_float('Please Enter Alpha (0 to 1 inclusive): ')
    while (satisfied == 'no'):
        Forecast = predict(trainingSetTime,trainingSetPrices,alpha)[:]
        Output = OutOfSamplePrediction(Forecast,testingSetTime,testingSetPrices, alpha)
        plotChart(Output)
        satisfied=input_string('Are you satisfied with the chart? (yes/no): ')
        if satisfied == 'no':
            alpha = input_float('Please Enter Alpha (0 to 1 inclusive): ')
            Forecast = predict(trainingSetTime,trainingSetPrices,alpha)[:]
            Output = OutOfSamplePrediction(Forecast,testingSetTime,testingSetPrices, alpha)
            #plotChart(Output)
        elif satisfied == 'yes':
            outPutPrinter(Output)
            break
            
#This is how to call the main function
       
finalProgram()   


