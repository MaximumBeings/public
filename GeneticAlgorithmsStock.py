#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 14:02:39 2017

@author: oluwaseyiawoga
"""

"""
IMPROVEMENTS - IMPROVEMENTS - IMPROVEMENTS - IMPROVEMENTS
This Approach Uses Stock Returns to perform the fitness
rather than the stock prices.
"""
"""
Predicting Stock Prices Using Genetic Algorithms - Mini Project 3 (Version 1)
Oluwaseyi Adebayo Awoga
July 2017
Source: WQU Algorithms Class Materials
        Mitchell Melanie – “An Introduction to Genetic Algorithms”, 
        MIT Press paperback edition, 1998.
"""


"""
STEPS PERFORMED:
1 - Encode the problem into chromosones.

2 - Using the encoding, develop a fitness function for use in evaluating 
each chromosome's value in solving a given problem.

3 - Initilize a population of chromosomes.

4 - Evaluate each chromosome in the population.

5 - Create new chromosomes by mating two chromosomes. This is done by
mutating and recombining two parents to form two children. We recombine
or mutate only the weak parents in terms of fitness function.

6 - Evaluate the new chromosome.

7 - Delete a member of the population that is less fit than the new chromosome,
insert the new chromosome into the population.

8 - If a stopping number of generations is reached, or time is up, then return the best
chromosome(s) or alternatively go to step 4.

9 - Use linear regression to fit the data extracted for the best individual and use the 
model to forecast the next two years.

10 - Export your forecast to a csv file.


Source: Cybernetic Trading Strategies: Developing a Profitable 
Trading System with State-of-the-Art Technologies
"""

"""
Stock Ticker Selected:
TESLA:  TSLA NASDAQ
Source: yahoo - Downloaded Using Pandas_Reader
"""

"""
Import Python Libraries and Packages
"""

import numpy as np
import pandas as pd
import math
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
import datetime as dt  
from random import randint, uniform
from sklearn import linear_model



"""
Set start and end dates and import data
"""
start = dt.datetime(2016, 7, 1)
end = dt.datetime.today().strftime("%m/%d/%Y")

data = web.DataReader('TSLA', 'yahoo', start, end)
data.describe()
data.tail()
data.rename(columns={'TSLA': 'Close',}, inplace=True)
data.dropna(subset=['Close'], inplace=True)

returns = (data.Close - data.Close.shift(1))/data.Close
returns = returns.iloc[1:]
pRice = returns.values


def originalPlot(pRice):
    """
    This helper function helps to plot
    the original data and the predicted data
    Using Matplotlip and the helper functions
    Created Above
    """
    plt.close('all')
    fig, ax = plt.subplots(1)
    ax.plot(pRice, lw=1.5, label="Stock Returns")
    plt.title('TESLA - Stock Returns \n')
    plt.legend(loc=0)
    plt.grid(True)
    plt.ylabel('Stock Returns')
    plt.xlabel('Dates')
    plt.legend(loc=0)
    plt.grid(True)
    plt.show()
    plt.close()
    
originalPlot(pRice)


def generatePopulation(numbIndividuals):
    """
    An individual in the Genetic Algorithm population
    might be represented by a set of conditions listed below
    C = [(240 <= Price of Tesla on Day 1)
    AND ($300 <= Price of Tesla on Day 2 <= $320)
    AND ($280 <= Price of Tesla on Day 3 <= $360)
    This program takes as input the number of individuals
    and generates a population of individuals with the 
    conditions or Cs randomly generated using randint.
    The Genes selected here were judgementallyy selected.
    """
    alleles = []
    for x in range(numbIndividuals):
        a = uniform(0.00,0.01)
        b = uniform(0.01,0.02)
        c = uniform(0.02,0.03)
        d = uniform(0.04,0.05)
        e = uniform(0.05,0.06)
        genes = (a,b,c,d,e)
        alleles.append(genes)
    return alleles

individuals = generatePopulation(100)
    
        
def processPopulation(individuals,pRice):
    """
    This function takes a population of Conditions and the
    observed price of the stock under consideration and then
    for each x that satifies C collects the corresponding ys
    """
    soln = []
    soln2 = {}
    for y in range(len(individuals)):
        
        for x in range(1, len(pRice)-1):
            if pRice[x-1] >= individuals[y][0] and (pRice[x] >= individuals[y][1] or \
                    pRice[x] <= individuals[y][2]) and (pRice[x+1] >= individuals[y][3] \
                         or pRice[x+1] <= individuals[y][4]):
                soln.append(pRice[x])
            soln2[individuals[y]] = soln
        soln = []
    return soln2

#print(processPopulation(individuals,pRice))

d = processPopulation(individuals,pRice)

#for kv in d.items():
#    print (kv[0],':','\n',kv[1])
#    print()


def calcFitness(processedPop, timeSeries, Constant):
    """
    Fitness Function:
        f(C) = -log2(std/std_o) - alpha/N_c
    where:
        std: standard deviation of the x set that satisfy condition C
        
        std_o: the standard deviation of the distribution of x over the entire dataset
        
        N_c: the number of data points satisfying condition C
        
        alpha: Constant
        
    """
    fitness = {}
    
    for key in processedPop: 
         a = np.std(processedPop[key])
         b = np.std(timeSeries)
         Nc= len(processedPop[key])
         fitness[key] = -1*(math.log2(a/b)) - Constant/Nc
    return fitness


#print(calcFitness(d, pRice, 300))

processed = calcFitness(d, pRice, 20)

#for kv in processed.items():
#    print (kv[0],':','\n',kv[1])
#    print()
    
def calculateAverageFitness(processedPopulation):
    'Find average fitness for a population.'
    summed = 0
    for key in processedPopulation:
        summed = summed + processedPopulation[key]
    return summed / (len(processedPopulation) * 1.0)

#print(calculateAverageFitness(processed))


"""
Helper Functions to mutate and evolve chromosones
"""

def mutateIndividuals(individual_A,individual_B):
    """
    Sample:
        Parent A: [(3.2<=x6 <=5.5)^(0.2 <= x8<= 4.8)^(3.4 <= x9 <= 9.9)]
        Parent B: [(6.5<=x2 <=6.8)^(1.4 <= x4<= 4.8)^(1.2 <= x9 <= 1.7)^(4.8<= x16 <= 5.1)]
        
        Offspring A: [(3.2 <= x6 <= 5.5)^(1.4 <= x4<= 4.8)^(3.4 <= x9 <= 9.9)]
        Offspring B: [(6.5<=x2 <=6.8)^(0.2 <= x8<= 4.8)^(1.2 <= x9 <= 1.7)^(4.8<= x16 <= 5.1)]
        
    """
    temp = []
    a = randint(0,3)
    temp = temp +(list(individual_A[:a]))
    temp = temp +(list(individual_B[a:]))
    
    temp2 = []
    a = randint(0,3)
    temp2 = temp2 +(list(individual_B[:a]))
    temp2 = temp2 +(list(individual_A[a:]))
    
    
    return [tuple(temp),tuple(temp2)]
    
a = (229, 309, 324, 353, 364)
b = (230, 301, 339, 345, 383)

#print(mutateIndividuals(a,b))


def delConditions(individual_A,):
    """
    Sample:
        [(3.2 <= x6 <= 5.5)^(0.2 <= x8 <= 4.8) ^ (3.4 <= x9 <= 9.9)]
        -> [(3.2 <= x6 <= 5.5)^(0.2 <= x8 <= 4.8)
    """
    

    temp = []
    temp = list(individual_A)
    del temp[-1]
    del temp[-1]
    return tuple(temp)

#print(delConditions(a))


a = (delConditions(a))

def addConditions(individual_A):
    """
    Sample:
        [(3.2 <= x6 <= 5.5)^(0.2 <= x8 <= 4.8)]
        -> [(3.2 <= x6 <= 5.5)^(0.2 <= x8 <= 4.8) ^ (3.4 <= x9 <= 9.9)]
    """
    temp = []
    temp = list(individual_A)
    temp.append(temp[-1] + 20)
    temp.append(temp[-1] + 30)
    return tuple(temp)

#print(addConditions(a))

def shrinkConditions(individual_A):
    """
    Sample:
        [(3.2 <= x6 <= 5.5)^(0.2 <= x8 <= 4.8)]
        -> [(3.9 <= x6 <= 5.5)^(1.2 <= x8 <= 4.8) ^ (6.4 <= x9 <= 9.9)]
    """
    temp = []
    temp = list(individual_A)
    temp = [x+15 for x in temp]
    return tuple(temp)


#print(shrinkConditions(b))

    
def expandConditions(individual_A):
    """
    Sample:
        [(3.2 <= x6 <= 5.5)^(0.2 <= x8 <= 4.8)]
        -> [(3.9 <= x6 <= 5.5)^(1.2 <= x8 <= 4.8) ^ (6.4 <= x9 <= 9.9)]
    """
    temp = []
    temp = list(individual_A)
    temp = [x-15 for x in temp]
    return tuple(temp)


#print(expandConditions(b))

    

"""
Dictionary Helper Functions
"""

def getkeybyvalue(d,i):
    for k, v in d.items():
        if v == i:
            return (k)

def dictSorter(processed):
    sortvaluelist = sorted(processed.values(),reverse=True)
    sortresult ={}
    for i1 in sortvaluelist:   
        key = getkeybyvalue(processed,i1)
        sortresult[key] = i1
    return sortresult



def mainProgram(population,timeSeries, Constant):
    """
    This is the main function and calls the different helper function.
    It ranks the individual by fitness and compares this to the average
    fitness for all the individuals.  Individuals that score less than the
    average are candidates for mutation using crossover mutation and it 
    iterates until the number of individuals with a fitness greater than the
    average is more than a certain percentage.
    """
    parentsToRetain = []
    parentsToMutate = []
    offSprings = []
    #parentsFinal = []
    passPercentage = 0.0
    
    while passPercentage < 0.90:
        processed = calcFitness(population, timeSeries, Constant)
        processed = dictSorter(processed)
        benchmark = calculateAverageFitness(processed)
        for key in processed:
            if processed[key] >= benchmark:
                parentsToRetain.append(key)
            else:
                parentsToMutate.append(key)
    
        for x in range(1,len(parentsToMutate)-1):
            offSpringA, offSpringB = (mutateIndividuals(parentsToMutate[x-1],parentsToMutate[x]))
            offSprings.append(offSpringA)
            offSprings.append(offSpringB)
        
        passPercentage = len(parentsToRetain)/(len(parentsToRetain)+len(parentsToMutate))
        population = parentsToRetain + offSprings
        population = processPopulation(population,pRice)
        parentsToRetain = []
        parentsToMutate = []
        offSprings = []
    
    return processed

population = processPopulation(individuals,pRice)

print() 
print('Fitness Ranking for the top Ranking Individuals')  
print() 
fitnessRatings = mainProgram(population,pRice, 5)
for kv in fitnessRatings.items():
    print (kv[0],':','\t',kv[1])
    print()


"""
Preview of Ratings:
(0.005667493293659439, 0.015232928108953898, 0.021543697175617074, 0.04615923129185482, 
0.0561880644855627) :    0.1892629677210969
"""


"""
Having found the individuals with the best conditions or fitness
We now use the codes below to forecast out to two years using
a linear regression model.

"""

"""
First we get the Conditions with the best fitness 
"""
modelData =   mainProgram(population,pRice, 5)
Keys = list(modelData.keys())[0]


"""
Then for every Y that passes all the conditions if ran through
the original timeseries we collect both the x and y values
"""

def generateModelData(Keys,pRice):
    """
    This function takes a population of Conditions and the
    observed price of the stock under consideration and then
    for each x that satifies C collects the corresponding ys
    """
    soln2 = {}

        
    for x in range(1, len(pRice)-1):
        if pRice[x-1] >= Keys[0] and (pRice[x] >= Keys[1] or \
                pRice[x] <= Keys[2]) and (pRice[x+1] >= Keys[3] \
                     or pRice[x+1] <= Keys[4]):
            soln2[x] = pRice[x]
    return soln2

#print(processPopulation(individuals,pRice))

regressionData = generateModelData(Keys,pRice)


"""
Sample output when d is printed to the console
"""
print() 
print('Extracted Data for the Highest Ranking Condition')
print()  
for kv in regressionData.items():
    print (kv[0],':','\t',kv[1])
    print()
    
"""
3 :      0.00387489620814

5 :      -0.000578677943468

10 :     -0.00439492142413

12 :     -0.0356462585034

14 :     0.0336507108387

15 :     -0.00217855431136

18 :     0.0178031432344

19 :     -0.0207817051433

23 :     -0.00252141025084

26 :     -0.015200531797

34 :     -0.00928542591845
"""

"""
Get the index of all the Cs in the best condition above
"""

keyIndex = list(regressionData.keys())

"""
Get the Original Data or Stock Price Using the keyIndex Above
"""

stockPrice = []

for x in keyIndex:
    stockPrice.append(data.Close[x])

"""
Using the data above build a linear regression
model using SKLEARN
"""

def fitModel(keyIndex,stockPrice):
    x = np.array(keyIndex)
    y = np.array(stockPrice)
    x = x.reshape(len(x), 1)
    y = y.reshape(len(y), 1)
    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    return regr

regr = fitModel(keyIndex,stockPrice)
print(regr)

m = regr.coef_[0]
b = regr.intercept_

print() 
print('Regression Equation Generated') 
print() 
print(' y = {0} * x + {1}'.format(m, b))

"""
y = [ 0.67873746] * x + [ 165.57487519]
"""


def fitPlot(keyIndex,stockPrice):
    """
    This helper function helps to plot
    the original data and the predicted data
    Using Matplotlip and the helper functions
    Created Above
    """
    x = np.array(keyIndex)
    y = np.array(stockPrice)
    x = x.reshape(len(x), 1)
    y = y.reshape(len(y), 1)
    plt.close('all')
    fig, ax = plt.subplots(1)
    ax.scatter(x,y, lw=1, label="Original Price")
    plt.title('TESLA - Stock Price \n Fitted Versus Original For Best Ranking Condition \n Based on Stock Returns' )
    plt.legend(loc=0)
    plt.plot(x, regr.predict(x), color='blue', linewidth=1.5, label ='Fitted - Linear Regression')
    plt.grid(True)
    plt.ylabel('Stock Price')
    plt.xlabel('Dates  \n [For the Individual that had th best Fitness Score]')
    plt.legend(loc=0)
    plt.grid(True)
    plt.show()
    plt.close()
    
fitPlot(keyIndex,stockPrice)

k0 = len(data.Close)
k = range(k0,365*2 +k0)
k2 = []
for x in k:
    k2.append(x)


def predictTwoYears(k2):
    m = regr.coef_[0]
    b = regr.intercept_
    kY = []
    for x in range(len(k2)):
        kY.append(m * k2[x] + b)
    return kY


    
kY = predictTwoYears(k2)
    

def forecastPlot(k, kY):
    """
    This helper function helps to plot
    the original data and the predicted data
    Using Matplotlip and the helper functions
    Created Above
    """
    plt.close('all')
    fig, ax = plt.subplots(1)
    ax.plot(k,kY, lw=1, label="Forecast Stock Price")
    plt.title('TESLA - Stock Price \n Forecasted Based on Stock Returns')
    plt.legend(loc=0)
    plt.grid(True)
    plt.ylabel('Forecated Stock Price')
    plt.xlabel('Dates - [Covering Next Two Years]')
    plt.legend(loc=0)
    plt.grid(True)
    plt.show()
    plt.close()
    
forecastPlot(k2, kY)


def exportPrediction(k2, kY):
    """
    """
    df = pd.DataFrame()
    temp = []
    df['Date'] = k2
    for x in kY:
        temp.append(x[0])
    df['DateValue'] = temp
    return df

version2_data = exportPrediction(k2, kY)

version2_data.head()

"""
Sample Forecasted Data:
   Date   DateValue
0   256  339.331666
1   257  340.010403
2   258  340.689141
3   259  341.367878
4   260  342.046616
"""
version2_data.to_csv('version1_Forecast_Improvements.csv',index = False)
