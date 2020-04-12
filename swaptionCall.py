"""
Author: Oluwaseyi Awoga
IDE: CS50 IDE on Cloud 9/AWS
Topic: ARRC Swaption - LIBOR-SOFR Transition
Sources: David R. Smith - Financial Analyst Journal - May/June 1991
Location: Milky-Way Galaxy
"""

from __future__ import division
import math
from scipy.optimize import fsolve
import sys
import copy
import scipy.stats
import datetime
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta


tIME = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7]

yTM = [8.8700, 9.0400, 9.155, 9.2700, 9.3150, 9.3600,
       9.3850, 9.4100, 9.4350, 9.4600, 9.4700, 9.4800,
       9.4900, 9.5000]


def spotHelper(guess, timeSoFar, semiAYield, soln):
    s = guess[0]
    ans = []
    s = s/100
    a = 0.0
    for x in range(0, len(timeSoFar)):
        if x == len(timeSoFar) - 1:
            a = (100+semiAYield/2.0)/(1+s/2.0)**(x+1)
            ans.append(a)

        elif x != len(timeSoFar) - 1:
            y = soln[x]
            a = (semiAYield/2.0)/((1+y/2.0)**((x+1)))
            ans.append(a)
            a = 0.0
    return (100.00 - sum(ans))


def spotRates(time, ytm, sofRSpread=[0.0]):
    soln = []
    guess = [0.12]
    for x in range(len(time)):
        if x == 0:
            soln.append((ytm[0]+sofRSpread[0])/100)
        else:
            semiAYield = ytm[x] + sofRSpread[0]
            timeSoFar = copy.deepcopy(time[:x+1])
            data = (timeSoFar, semiAYield, soln)
            temp = fsolve(spotHelper, guess, args=data, xtol=1.49012e-8,)[0]
            soln.append(temp/100)
    return soln


def discountFactorCalculator(zeroRates, tIME):
    """
    Helper Function to Calculate Discount Rates from Spot Rates
    Args:
        param1: (a) Spot Rates
                (b) Payment Dates
    Returns:
        A list of Discount Rates for all Payment Dates.
    """
    discountRates = []
    for x in range(len(zeroRates)):
        discountRates.append(1/((1+zeroRates[x]/2.0)**(x+1)))
    return discountRates

#discountFactors2 = discountFactorCalculator(zeroRates2,tIME)


def futureValueCurve(discountFactors):
    """
    Helper Function to Calculate Future Value from Discount Rates
    Args:
        param1: (a) Discount Rates
    Returns:
        A list of Future Values for all Payment Dates.
    """
    futureValueCurve = []
    for x in range(len(discountFactors)):
        futureValueCurve.append(1/discountFactors[x])
    return futureValueCurve

#futureValueCurve2 = futureValueCurve(discountFactors2)


def forwardRateCurve(futureValueCurve, zeroRates):
    """
    Helper Function to Calculate Forward Rates
    Args:
        param1: (a) Future Values
    Returns:
        A list of Forward Rates for all Payment Dates.
    """
    forwardRateCurve = []
    for x in range(len(futureValueCurve)):
        if x == 0:
            forwardRateCurve.append(zeroRates[0])
        else:
            forwardRateCurve.append((((futureValueCurve[x]
                                       / futureValueCurve[x-1])**(1/(0.5*2))) - 1)*2)
    return forwardRateCurve

#forwardRateCurve2 = forwardRateCurve(futureValueCurve2)


def forwardRateCurve3(zeroRates, tIME):
    forwardRateCurve2 = []
    for x in range(len(zeroRates)):
        if x == 0:
            forwardRateCurve2.append(zeroRates[0])
        else:
            a = (1+zeroRates[x]/2)**(tIME[x]*2)
            b = (1+zeroRates[x-1]/2)**(tIME[x-1]*2)
            c = a**(0.5*2)/b**(0.5*2)
            d = c**(1/(0.5*2))
            e = d - 1
            f = e * 2
            forwardRateCurve2.append(f)
    return forwardRateCurve2


def annualSpotRate(zeroRates):
    """
    Helper Function to Calculate Annual Spot Rates
    Args:
        param1: (a) Forward Rates
    Returns:
        A list of Annual Spot Rates for all Payment Dates.
    """
    annualSpotRate = []
    for x in range(len(zeroRates)):
        annualSpotRate.append((1 + zeroRates[x]/2)**2 - 1)
    return annualSpotRate

#annualSpotRate2 = annualSpotRate(zeroRates2)


def forwardRateCalculator(zeroRates, sTART, sTOP):
    """
    Helper Function to Calculate Underlying Forward Rate
    Args:
        param1: (a) Zero Rates, Start, Stop
    Returns:
        The underlying forward rate for the swaption.
    """
    a = (1+zeroRates[sTOP*2-1]/2)**(sTOP*2)
    b = (1+zeroRates[sTART*2-1]/2)**(sTART*2)
    c = a/b
    d = c**(1.0/(2*2))
    e = d - 1
    f = e * 2
    return f


"""
Declare the variables
"""


def cumm_dens_function_scipy(t):
    """
    Function to Calculate Cummulative Density Function
    Args:
        param1: (a) Time
    Returns:
        Cummulative Density Function.
    """
    return scipy.stats.norm.cdf(t)


def blackSeventySix(SP, EP, r, v, t):
    """
    Helper Function to calculate Swaption Call & Put Prices
    Args:
        param1: (a) Security price, Strike, Spot Rate at the Start of Swap, Volatility
    Returns:
        Swaption Call & Put Prices.
    """
    d1 = (math.log(SP/EP) + (0.5 * v * v * t/365.0))/(v * math.sqrt(t/365.0))
    d2 = d1 - v * math.sqrt(t/365.0)
    ND1 = cumm_dens_function_scipy(d1)
    ND2 = cumm_dens_function_scipy(d2)
    call_Value = (SP * ND1 - EP * ND2) * (1 + 0.5 * r)**(t/(-365.0/2)) * 100.0
    put_Value = call_Value - (SP - EP) * (1 + 0.5 * r)**(t/(-365.0/2)) * 100.0
    result = {'call': call_Value, 'put': put_Value}
    return result


print()


def anuitizedModelPricePutSwaption(cashflow, period, spot):

    sum = 0.0
    for x in range(1, period+1):
        sum = sum + (1/((1+spot)**(x))) * cashflow
    return sum


Settlement_Date = datetime.date(1990, 3, 14)
Maturity_Date = datetime.date(1995, 3, 14)


def calPrice(Settlement_Date, Maturity_Date, zeroRates, sTart, sTop, vol, strike, type, display=False):
    t = (Maturity_Date - Settlement_Date).days
    SP = forwardRateCalculator(zeroRates, sTart, sTop)
    if sTart == 0:
        r = zeroRates[sTart]
    elif sTart != 0:
        r = zeroRates[sTart*2-1]
    EP = strike/100
    v = vol
    price = blackSeventySix(SP, EP, r, v, t)
    period = 2 * 2
    cashflow = price[type]/2.0
    spot = SP/2.0
    ans = anuitizedModelPricePutSwaption(
        cashflow, period, spot)/100 * 100000000
    if display == True:
        print(f"Call Value is: {round(price[type],4)}")
        print()
    return ans


def calculateSwaptionPriceLIBOR(display=False):
    guess = [0.10]
    zeroRates2 = spotRates(tIME, yTM)
    discountFactors2 = discountFactorCalculator(zeroRates2, tIME)
    futureValueCurve2 = futureValueCurve(discountFactors2)
    forwardRateCurve2 = forwardRateCurve(futureValueCurve2, zeroRates2)
    annualSpotRate2 = annualSpotRate(zeroRates2)
    result = calPrice(Settlement_Date, Maturity_Date,
                      zeroRates2, 5, 7, 0.11, 9.500, "call", display)
    if display == True:
        print(
            f"Present Value of a Put Swaption with a Notional of $100 Million is: ${round(result,4)}")
    return result


zeroRates2 = spotRates(tIME, yTM)
discountFactors2 = discountFactorCalculator(zeroRates2, tIME)
futureValueCurve2 = futureValueCurve(discountFactors2)
forwardRateCurve2 = forwardRateCurve(futureValueCurve2, zeroRates2)
annualSpotRate2 = annualSpotRate(zeroRates2)


d = {'Time': pd.Series(tIME), 'YTM': pd.Series(yTM), 'Spot Rates': pd.Series(zeroRates2),
     'Disc_Factors': pd.Series(discountFactors2), 'Future_Value': pd.Series(futureValueCurve2),
     'Forward_Rate': pd.Series(forwardRateCurve2), 'Annual_Spot_Rate': pd.Series(annualSpotRate2)}


df = pd.DataFrame(d, columns=['Time', 'YTM', 'Spot Rates', 'Disc_Factors',
                              'Future_Value', 'Forward_Rate', 'Annual_Spot_Rate'])

print("BootStrap Curve - LIBOR")
print()
print(df.to_string(index=False))
print()
print("Results: ")
forwardRateUnderlying = forwardRateCalculator(zeroRates2, 5, 7)
print()
print("The 7 year Forward Rate Starting in year 5 is: %s " %
      round(forwardRateUnderlying, 4))
print()
calculateSwaptionPriceLIBOR(display=True)
print()
print("***************************************************************************************")
print("***************************************************************************************")
print()


def calculateSwaptionPriceSOFR(SOFR_Spread, display=False):
    guess = [0.12]
    zeroRates2 = spotRates(tIME, yTMS, SOFR_Spread)
    discountFactors2 = discountFactorCalculator(zeroRates2, tIME)
    futureValueCurve2 = futureValueCurve(discountFactors2)
    forwardRateCurve2 = forwardRateCurve(futureValueCurve2, zeroRates2)
    annualSpotRate2 = annualSpotRate(zeroRates2)
    result = calPrice(Settlement_Date, Maturity_Date,
                      zeroRates2, 5, 7, 0.11, 9.500, "call", display)
    if display == True:
        print(
            f"Present Value of a Put Swaption with a Notional of $100 Million is: ${round(result,4)}")
    return result


def optimizationfunc(spread):
    a = calculateSwaptionPriceLIBOR()
    b = calculateSwaptionPriceSOFR(spread)
    return (a - b)


yTMS = [8.8700/1.5, 9.0400/1.5, 9.155/1.5, 9.2700/1.5, 9.3150/1.5, 9.3600/1.5,
        9.3850/1.5, 9.4100/1.5, 9.4350/1.5, 9.4600/1.5, 9.4700/1.5, 9.4800/1.5,
        9.4900/1.5, 9.5000/1.5]


solutions = fsolve(optimizationfunc, [0.4/100], xtol=1.49012e-08,)
spreadtoUse = solutions[0]
print(
    f"The Spread Required on SOFR to Equate the Original Present Value is {round(spreadtoUse,4)}")
print()

for x in range(len(yTMS)):
    yTMS[x] = spreadtoUse + yTMS[x]

zeroRates2 = spotRates(tIME, yTMS, solutions)
discountFactors2 = discountFactorCalculator(zeroRates2, tIME)
futureValueCurve2 = futureValueCurve(discountFactors2)
forwardRateCurve2 = forwardRateCurve(futureValueCurve2, zeroRates2)
annualSpotRate2 = annualSpotRate(zeroRates2)


print("BootStrap Curve - SOFR Plus Spread")
print()
d = {'Time': pd.Series(tIME), 'YTM': pd.Series(yTMS), 'Spot Rates': pd.Series(zeroRates2),
     'Disc_Factors': pd.Series(discountFactors2), 'Future_Value': pd.Series(futureValueCurve2),
     'Forward_Rate': pd.Series(forwardRateCurve2), 'Annual_Spot_Rate': pd.Series(annualSpotRate2)}


df = pd.DataFrame(d, columns=['Time', 'YTM', 'Spot Rates', 'Disc_Factors',
                              'Future_Value', 'Forward_Rate', 'Annual_Spot_Rate'])

print(df.to_string(index=False))
print()
print("Results: SOFR Plus Spread")
forwardRateUnderlying = forwardRateCalculator(zeroRates2, 5, 7)
print()
print("The 7 year Forward Rate Starting in year 5 is: %s " %
      round(forwardRateUnderlying, 4))
print()
calculateSwaptionPriceSOFR([0.0], display=True)
print()
print("**************************************************************************************")
print("**************************************************************************************")
print()


yTMS = [8.8700/1.5, 9.0400/1.5, 9.155/1.5, 9.2700/1.5, 9.3150/1.5, 9.3600/1.5,
        9.3850/1.5, 9.4100/1.5, 9.4350/1.5, 9.4600/1.5, 9.4700/1.5, 9.4800/1.5,
        9.4900/1.5, 9.5000/1.5]

print()

zeroRates2 = spotRates(tIME, yTMS, [0.0])
discountFactors2 = discountFactorCalculator(zeroRates2, tIME)
futureValueCurve2 = futureValueCurve(discountFactors2)
forwardRateCurve2 = forwardRateCurve(futureValueCurve2, zeroRates2)
annualSpotRate2 = annualSpotRate(zeroRates2)

d = {'Time': pd.Series(tIME), 'YTM': pd.Series(yTMS), 'Spot Rates': pd.Series(zeroRates2),
     'Disc_Factors': pd.Series(discountFactors2), 'Future_Value': pd.Series(futureValueCurve2),
     'Forward_Rate': pd.Series(forwardRateCurve2), 'Annual_Spot_Rate': pd.Series(annualSpotRate2)}


df = pd.DataFrame(d, columns=['Time', 'YTM', 'Spot Rates', 'Disc_Factors',
                              'Future_Value', 'Forward_Rate', 'Annual_Spot_Rate'])

print("BootStrap Curve - SOFR Without Spread")
print()
print(df.to_string(index=False))
print()
print()
print("Results: SOFR Without Spread")
forwardRateUnderlying = forwardRateCalculator(zeroRates2, 5, 7)
print()
print("The 7 year Forward Rate Starting in year 5 is: %s " %
      round(forwardRateUnderlying, 4))
print()
calculateSwaptionPriceSOFR([0.0], display=True)
print()
print("***************************************************************************************")
print("***************************************************************************************")
print()
