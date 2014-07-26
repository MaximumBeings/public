
"""
********************************************************************************************************

This is the OIS Discounting version of an earlier program to calculate the market value of an
interest rate swap that is collateralized and centrally cleared. See you next time!!

********************************************************************************************************


TITLE: Valuing Interest Rate Swaps Using OIS Discounting (Part B)

SOURCE: Boston University School of Management Research Paper Series (No.2012-­‐11)
Valuing Interest Rate Swaps Using OIS Discounting By Donald J. Smith
Electronic copy available at: http://ssrn.com/abstract=2036979


OBJECTIVE: Compare Swap Market Value using both LIBOR discounting and OIS discounting
and discuss the python implementation of the two methodologies using the
above article as the main source. In this part of the series we  discuss
swap valuation using OIS discounting. Previously, we  discussed the LIBOR
discounting methodology. To read about the relative merit of OIS discounting over
LIBOR discounting refer to the above article or other sources.



Consider a 2-year, USD 100,000,000.00 (100 million USD) notional principal,
5.26% fixed versus 3-month LIBOR, quarterly settlement swap at a time when the
otherwise comparable at-market fixed rate is 3.40%.

LIBOR & SWAP FIXED RATES:
__________________________________
Time         Description     Rate
__________________________________
3-month      LIBOR           0.50%
6-month      LIBOR           1.00%
9-month      LIBOR           1.60%
12-month     LIBOR           2.10%
15-month     SFR             2.44%
18-month     SFR             2.76%
21-month     SFR             3.08%
24-month     SFR             3.40%

OIS RATES:
__________________________________
Time         Description     Rate
___________________________________
3-month      OIS             0.10%
6-month      OIS             0.60%
9-month      OIS             1.20%
12-month     OIS             1.70%
15-month     OIS             2.00%
18-month     OIS             2.30%
21-month     OIS             2.60%
24-month     OIS             2.90%

Date Count Convention -> Actual/360

Valuation Date is March 15th 2010.


"""

import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_ALL, '')

"""
THE FOLLOWING SECTION IS USED TO GENERATE THE LIBOR DISCOUNT RATES
"""

#Declare Variables
val_date = datetime.date(2010, 3, 15)
rate = [0.50,1.00,1.60,2.10,2.44,2.76,3.08,3.40] #in percentage
lenOfMaturity = len(rate)
lenOfMaturityPlusValueDate = len(rate) + 1
numberOfDays=0
result=0.0
dayCountBase = 360
LIBOR = []
fixedRate = 0.0526
notionalPrincipal = 100000000
SFRStartingIndex = 4
valuationDate = datetime.date(2010, 3, 15)
compounding = 3
 

#Generate a list of cashflow payment dates
def maturities(x,compounding):
    maturities = []
    for y in range(1,lenOfMaturityPlusValueDate):
        maturities.append((x)+relativedelta(months=compounding*y))
    return maturities
    
maturities = maturities(valuationDate,compounding)

#Calculate the discount rate for LIBOR
def discountLIBOR():
    for x in range(SFRStartingIndex):
        numberOfDays = (maturities[x] - val_date).days
        result = 1/(1+ (rate[x]/100.0 * numberOfDays/dayCountBase))
        LIBOR.append(result)
        result=0.0
    return LIBOR

#Helper function used in calculating the Swap Fixed Rate
def discountSFRhelper(LIBORlist,n):
    final = 0.0
    ans = 0.0
    for x in range(n):
        if x == 0:
            numberOfDays = (maturities[x] - val_date).days
            ans = numberOfDays/360.0 * LIBORlist[x]
            final = final + ans
            
        else:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            ans = numberOfDays/360.0 * LIBORlist[x]
            final = final + ans
    return final

#Another helper function - to help copy one list to another to avoid list mutation
#Source: StackOverFlow
def deepcopy(A):
    rt = []
    for elem in A:
        if isinstance(elem,list):
            rt.append(deepcopy(elem))
        else:
            rt.append(elem)
    return rt
    
#Function to calculate Swap Fixed Rate
def swapRateCalculator():
    final = 0.0
    ans = 0.0
    LIBOR = deepcopy(discountLIBOR())
    SFRRate = deepcopy(rate[SFRStartingIndex:])
    for x in range(SFRStartingIndex,lenOfMaturity):
        numberOfDays = (maturities[x] - maturities[x-1]).days
        ans = (1 - SFRRate[x-SFRStartingIndex]/100.0 * discountSFRhelper(LIBOR,x))
        final=ans/(1 + SFRRate[x-SFRStartingIndex]/100.0 * numberOfDays/360.0)
        LIBOR.append(final)
    return LIBOR
    

LIBOR = deepcopy(swapRateCalculator()) #Update LIBOR list by passing the result of swapRateCalculator function to a variable called LIBOR


#Functuion to calculate the implied forward rate
def impliedForwardRate():
    fRate = []
    result = 0.0
    for x in range(0,lenOfMaturity,1):
        if x == 0:
            fRate.append(rate[0]/100.0)
        elif x > 0:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            result = ((LIBOR[x-1]/LIBOR[x]) - 1) * (1/(numberOfDays/360.0))
            
            fRate.append(result)
            result = 0.0
    return fRate
    
fRate = deepcopy(impliedForwardRate())
"""
THE FOLLOWING SECTION IS USED TO GENERATE THE OIS DISCOUNT RATES
"""

#Declare Variables
val_date = datetime.date(2010, 3, 15)
rateOIS = [0.10,0.60,1.20,1.70,2.00,2.30,2.60,2.90] #OIS Rates
lenOfMaturity = len(rateOIS)
lenOfMaturityPlusValueDate = len(rateOIS) + 1
numberOfDays=0
result=0.0
dayCountBase = 360
OIS = []
fixedRate = 0.0526
notionalPrincipal = 100000000
OISShorterm = 4  #denotes less than 4 quarters or one year
valuationDate = datetime.date(2010, 3, 15)
compounding = 3  #denotes every thress months
 

#Generate a list of cashflow payment dates

def maturities(x,compounding):
    maturities = []
    for y in range(1,lenOfMaturityPlusValueDate):
        maturities.append((x)+relativedelta(months=compounding*y))
    return maturities
    
maturities = maturities(valuationDate,compounding)

#Calculate the discount rate for OIS rates less than 4 quarters or one year

def shortTermOIS():
    for x in range(OISShorterm):
        numberOfDays = (maturities[x] - val_date).days
        result = 1/(1+ (rateOIS[x]/100.0 * numberOfDays/dayCountBase))
        OIS.append(result)
        result=0.0
    return OIS
    
#Helper function used in calculating the long term discount rates for OIS payments > four(4) quarters or one 1 year

def oisHelper(oisList,n):
    final = 0.0
    ans = 0.0
    for x in range(n):
        if x == 0:
            numberOfDays = (maturities[x] - val_date).days
            ans = numberOfDays/360.0 * oisList[x]
            final = final + ans
            
        else:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            ans = numberOfDays/360.0 * oisList[x]
            final = final + ans
    return final

   
#Function to calculate OIS discount rates for payments greater than 4 quarters or one year

def longTermOIS():
    final = 0.0
    ans = 0.0
    OIS=[]
    OIS = deepcopy(shortTermOIS())
    SFRRate = deepcopy(rateOIS[OISShorterm:])
    for x in range(OISShorterm,lenOfMaturity):
        numberOfDays = (maturities[x] - maturities[x-1]).days
        ans = (1 - SFRRate[x-OISShorterm]/100.0 * oisHelper(OIS,x))
        final=ans/(1 + SFRRate[x-OISShorterm]/100.0 * numberOfDays/360.0)
        OIS.append(final)
    return OIS
    
OIS2 = []
OIS2 = deepcopy(longTermOIS()) #Update LIBOR list by passing the result of swapRateCalculator function to a variable called LIBOR


#Helper function used in calculating the Swap Fixed Rate
def impliedForwardhelperA(OIS2,IFR,n):
    final = 0.0
    ans = 0.0
    for x in range(1,n+1):
        #final = 0.0
        numberOfDays = (maturities[x] - maturities[x-1]).days
        ans = numberOfDays/360.0 * OIS2[x-1]*IFR[x-1] * 100.0
        final = final + ans
    return final

def impliedForwardhelperB(OIS2,n):
    final = 0.0
    ans = 0.0
    for x in range(n+1):
        if x == 0:
            numberOfDays = (maturities[x] - val_date).days
        elif x > 0:
            numberOfDays = (maturities[x] - maturities[x-1]).days
        ans = rate[n] * numberOfDays/360.0 * 100.0 * OIS2[x]
        final = final + ans
    return final


def ifrOISShortTermCalculator():
    IFR = []
    result = 0.0
    for x in range(0,8,1):
        result = 0.0
        if x == 0:
            IFR.append(rate[0])
        elif x > 0:
            result = (impliedForwardhelperB(OIS2,x) - impliedForwardhelperA(OIS2,IFR,x)) / (((maturities[x] - maturities[x-1]).days)/360.0 * OIS2[x]*100.0)
            IFR.append(result)
            
    return IFR

oisImpFR = LIBOR = deepcopy(ifrOISShortTermCalculator())

#To Display Rates - Original LIBOR/Swap Fixed Rates, Discount Rates and Implied Forward Rates
def ratePrinter():
    print ""
    print "ORIGINAL RATE, OIS DISCOUNT RATE AND OIS IMPLIED FORWARD RATE"
    print "_________________________________________________________"
    print ""
    rateTable = pd.DataFrame.from_items([('Period', range(1,lenOfMaturityPlusValueDate,1)),('Rate', rate), ('Disc_Rate', OIS2),('Imp_For_Rate(%)', oisImpFR)])
    print(rateTable.to_string())
    print ""

    
#To Calculate the Market Value of Fixed Rate Note/Leg
def fixedRateLeg():
    result = 0.0
    ans = 0.0
    for x in range(0,lenOfMaturity,1):
        if x == 0:
            numberOfDays = (maturities[x] - val_date).days
            ans = ans + numberOfDays/360.0 * OIS2[x]
        else:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            ans = ans + numberOfDays/360.0 * OIS2[x]
 
        result = ans *notionalPrincipal * fixedRate + notionalPrincipal * OIS2[-1]
    return result

#To Calculate the Market Value of Floating Rate Note/Leg
#The market value of the floating rate is is assumed to reset to par
#at payment periods but can be recalculated as follow:

def floatingRateLeg():
    result = 0.0
    ans = 0.0
    for x in range(0,lenOfMaturity,1):
        if x == 0:
            numberOfDays = (maturities[x] - val_date).days
            ans = ans + OIS2[x] * oisImpFR[x]/100.0 * numberOfDays/360.0
        else:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            ans = ans + OIS2[x] * oisImpFR[x]/100.0 * numberOfDays/360.0
    result = notionalPrincipal * OIS2[-1] + ans * notionalPrincipal
    return result
    
#To Calculate the Market Value of Swap = Market Value of Fixed Leg = Market Value of Floating Leg
def swapMarketValue():
    return fixedRateLeg() - floatingRateLeg()
    
    
#Sample Calls
print ""
ratePrinter()
print "MARKET VALUE CALCULATED USING OIS DISCOUNTING"
print "_____________________________________________"
print ""
print ("Market Value of Fixed Rate Leg = ") + str(locale.currency(fixedRateLeg(),grouping=True))
print ""
print ("Market Value of Floating Rate Leg = ") + str(locale.currency(floatingRateLeg(),grouping=True))
print ""
print ("Market Value of Swap: (MV Fixed - MV FRN) = ") + str(locale.currency(swapMarketValue(),grouping=True))

"""
ORIGINAL RATE, OIS DISCOUNT RATE AND OIS IMPLIED FORWARD RATE
_________________________________________________________

   Period  Rate  Disc_Rate  Imp_For_Rate(%)
0       1  0.50   0.999745         0.500000
1       2  1.00   0.996943         1.501405
2       3  1.60   0.990917         2.838879
3       4  2.10   0.983056         3.679512
4       5  2.44   0.974887         3.732931
5       6  2.76   0.965445         4.388564
6       7  3.08   0.954664         5.120995
7       8  3.40   0.942524         5.742007

MARKET VALUE CALCULATED USING OIS DISCOUNTING
_____________________________________________

Market Value of Fixed Rate Leg = $104,677,378.03

Market Value of Floating Rate Leg = $100,994,615.74

Market Value of Swap: (MV Fixed - MV FRN) = $3,682,762.30

Final Result from Article:
__________________________
MV of Fixed Leg:  $104,671,244

MV of Floating Leg: $100,989,671

MV of Swap: 

Difference between Python Implementation & Article:
    
$3,682,762.30 - $3,681,573 = $1,189.29 -> Deemed immaterial/Due to Rounding Differences



"""

