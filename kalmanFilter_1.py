#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 14:58:09 2022

@author: oluwaseyiawoga
"""


"""
Import Libraries & Packages
"""
import pandas as pd
import datetime
import numpy as np

"""
Source: ilectureOnline -> YouTube

Legend:
    Kalman Gain = KG
    Error in Estimate = E_est
    Error in Measurement = E_mea
    Current Estimate = EST_t
    Previous Estimate = EST_t-1
    Measurement = MEA
    

Data:
    True Temperature = 72
    Initial Estimate = 68
    Initial E_est = 2
    Initial Measurement = 75
    Error in Measurement = 4 (Constant -> assumed)
    
Formulae:
    (1) KG = E_est/(E_est+E_mea)
    (2) EST_t = EST_t-1 + KG * [MEA - EST_t-1]
    (3) E_est = [1-KG]]*(E_est-1)

Workings:
    
    Time t:
        KG = 2/(2+4) = 2/3 = 1/3 = 0.33
        EST = 68 + 0.33(75-68) = 70.33
        E_est = (1-0.33)(2) = 1.33
        
    Time t+1:
        KG = 1.33/(1.33 + 4) = 0.25
        EST = 70.33 + 0.25(71-70.33) = 70.50
        E_est = (1-0.25) * (1.33) = 1.00
        
    Time t+2:
        KG = 1/(1+4) = 0.20
        EST = 70.5 + 0.20(70-70.5) = 70.4
        E_est = [1-0.2][1.00] = 0.80
        
    Time t+3:
        KG = 0.8/(0.8+4) = 0.17
        EST = 70.4 + 0.17(74-70.4) = 71
        E_est = (1-0.17)(0.8) = 0.66
        
Table

Time    MEA    E_mea    EST    E_est-1    KG    E_est
t-1                     68     2
t       75     4        70.33             0.33  1.33
t+1     71     4        70.50             0.25  1.00
t+2     70     4        70.40             0.20  0.80
t+3     74     4        71                0.17  0.66   
        

"""


initial_measure = 68
initial_error_estimate = 2
true_temperature = 72
initial_measurement = 75
measurements = [75, 71, 70, 74]
MeasurementError = 4 #Constant
KG = []
EST = []
E_Errors = []


def KalmanGainCalculator(E_est, E_mea):
    return E_est/(E_est+E_mea)

def estimate(EST_previous, KG_t, MEA_t):
    return EST_previous + KG_t * (MEA_t - EST_previous)


def errorEstimate(KG_t, E_Est_previous):
    return (1-KG_t)*(E_Est_previous)



for x in range(len(measurements)):
    if x == 0:
        KG.append(KalmanGainCalculator(initial_error_estimate, MeasurementError))
        EST.append(estimate(initial_measure, KG[x], measurements[x]))
        E_Errors.append(errorEstimate(KG[x], initial_error_estimate))
    if x >= 1:
        KG.append(KalmanGainCalculator(E_Errors[x-1], MeasurementError))
        EST.append(estimate(EST[x-1], KG[x], measurements[x]))
        E_Errors.append(errorEstimate(KG[x], E_Errors[x-1]))
        
        
        
finalTable = pd.DataFrame()

finalTable["Time"] =  [1,2,3,4]
finalTable["Measurement"] = [75, 71, 70, 74]
finalTable["Measurement Error"] = 4 * [4]
finalTable["Kalman Gain"] = KG
finalTable["Estimates"] = EST
finalTable["Estimate Errors"] = E_Errors


print()
print("Simple Numerical Kalman Filter Example")
print("Source -> iLectureOnline - Youtube (Refactored to Python)")
print()
print(finalTable)


    
