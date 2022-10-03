"""
Source - ISDA Linear Interpolation Example
Software - Anaconda (Spyder)
Ameribor Rates
"""



"""
Import relevant Python libraries and packages.
"""

import datetime
import pandas as pd
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import locale
import collections
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
locale.setlocale(locale.LC_ALL,'')
from matplotlib import pyplot as plt
plt.style.use('ggplot')


"""
OBSERVED DATA:
    
Observed AMERIBOR Rates on the Fixing Date (2022/10/2)
====================================================

Tenor	    Rate(%)	          Comment
O/N	        3.22436           Observed
1 Week      3.21676           Observed
1M	        3.21260           Observed
2M          3.69293           Observed
3M	        4.04693	          Observed
6M	        4.27399	          Observed
12M         3.99702           Observed

"""

"""
PUBLIC HOLIDAYS

Stock Market Holiday Schedule - 2022
****************************************************************
Description					                     Date
============					                 ======
New Year's Day                    		         January 1, 2022
Martin Luther King Jr. Day             		     January 17, 2022
Washington's Birthday (Presidents' Day)          February 21, 2022
Good Friday                    			         April 15, 2022
Memorial Day                    		         May 30, 2022
Juneteenth                                       June 20, 2022
Independence Day                		         July 4, 2022
Labor Day                    			         September 5, 2022
Thanksgiving Day				                 November 24, 2022
Christmas Day					                 December 25, 2022

Stock Market Holiday Schedule - 2023
********************************************************************
Description 					                 Date
===========					                     ======
New Year's Day					                 January 1, 2023
Martin Luther King Jr. Day			             January 16, 2023
Washington's Birthday (President's Day)		     February 20, 2023
Good Friday					                     April 7, 2023
Memorial Day					                 May 29, 2023
Juneteenth                                       June 19, 2023
Independence Day				                 July 4, 2023
Labor Day					                     September 4, 2023
Thanksgiving Day				                 November 23, 2023
Christmas Day					                 December 25, 2023


"""




"""
The Program Starts Here
"""

"""
Declare Variables Here
"""
#The following variables are to be updated as necessary:

fixingDate = datetime.date(2022,10,3)  #Change this to the fixing date on which the rates were observed

resetDateAdjustment = 2  #Rates are usually set two days in advance - so we need to adjust for reset days.

longestTenor = 12  #This is longest tenor for the observable AMERIBOR rates - which is 12 months

rates = [3.22436/100,3.21676/100,3.21260/100,3.69293/100,4.04693/100,4.27399/100,3.99707/100]  #Create a list for the observable rates using a list data structure.

#Capital markets do not open on public holidays so we have to move public holidays to the next good business day under
#the Modified Business Day rule - which is the main assumption for our methodology.
#The holiday list should cover at least the entire duration of the period for which we are interpolating.
publicHolidays = [datetime.date(2022,1,1),datetime.date(2022,1,17), \
datetime.date(2022,2,21),datetime.date(2022,4,15),datetime.date(2022,5,30),datetime.date(2022,6,20), \
datetime.date(2022,7,4),datetime.date(2022,9,5),datetime.date(2022,11,24), \
datetime.date(2022,12,25), datetime.date(2023,1,1),datetime.date(2023,1,16), \
datetime.date(2023,2,20),datetime.date(2022,4,7),datetime.date(2023,5,29),datetime.date(2023,6,19),\
datetime.date(2023,7,4),datetime.date(2023,9,4),datetime.date(2023,11,23),\
datetime.date(2023,12,25), ]



"""
Declare and initialize intermediate variables. These variables and declarations should not be changed.
"""
#This variable does not need to change and is used to track the number of observable rates.

lengthOfObservedData = len(rates)

#Determine the First Reset Date.  Interbank Offered Rates Are Usually Fixed 2 Days Prior to Reset Date
#However, this Depends on the Convention in a Particular Market. The Number of Days of Reset Date Adjustment
#Was Stored In The Variable Named "resetDateAdjustment" Above. 

firstResetDate = fixingDate + timedelta(days=resetDateAdjustment)

#Determine the Longest Reset Date for the Observable AMERIBOR Rates
#In the Case of AMERIBOR - this is 12 Months Unless it Changes in the Future
#This information is Stored In the Variable Named longestTenor


lastResetDate = firstResetDate + relativedelta(months=longestTenor)

"""
This Section is Used to Programatically Display the Observable Rates, Tenors and Maturities.
"""
#Determine the Reset Dates for the Observable AMERIBOR Rates.

resetDates = []
for x in range(lengthOfObservedData):
    resetDates.append(firstResetDate)

#The Following Programs are Used to Create Intermediate Data Containers to Use in Our Calculation.

fixingDateList = []
for x in range(lengthOfObservedData):
    fixingDateList.append(fixingDate)
    
resetDateList = []
for x in range(lengthOfObservedData):
    resetDateList.append(firstResetDate)
    
originalMaturities = []
originalMaturities.append(firstResetDate + timedelta(days=1))
originalMaturities.append(firstResetDate + timedelta(days=7))
monthlyMaturities = [1,2,3,6,12]
for x in monthlyMaturities:
    originalMaturities.append(firstResetDate + relativedelta(months=x))

#To Store the Original Information In A Pandas Dataframe - A Table Structure.

observedAMERIBOR = pd.DataFrame()

                                        
observedAMERIBOR['Fixing Date'] = fixingDateList
observedAMERIBOR['Reset Adj.']  = [a_i - b_i for a_i, b_i in zip(resetDateList, fixingDateList)]                      
observedAMERIBOR['Reset Dates'] =resetDates
observedAMERIBOR['Tenors'] = [a_i - b_i for a_i, b_i in zip(originalMaturities, resetDates)]
observedAMERIBOR['Maturities'] = originalMaturities
observedAMERIBOR['AMERIBOR'] = rates

#Reset Index to Start From 1 Instead of 0.

newIndex = []
for x in observedAMERIBOR.index:
    newIndex.append(x + 1)

observedAMERIBOR.index = newIndex

#To Print Original/Observable Data.

print("")
print("OBSERVED AMERIBOR RATES, RESET DATES, TENORS & \
MATURITIES AS OF {:%d, %b %Y}".format(fixingDate))
print("_______________________________________\
__________________________________")
print("")
print(observedAMERIBOR.to_string())

"""
Sample Output Generated by the Codes Above - Visualizing The Original 
Data in this Way Helps In Understanding The Process Better and 
Provides A Basis For Comparison To The Interpolated Data:
    
OBSERVED AMERIBOR RATES, RESET DATES, TENORS & MATURITIES AS OF 03, Oct 2022
_________________________________________________________________________

  Fixing Date Reset Adj. Reset Dates   Tenors  Maturities  AMERIBOR
1  2022-10-03     2 days  2022-10-05   1 days  2022-10-06  0.032244
2  2022-10-03     2 days  2022-10-05   7 days  2022-10-12  0.032168
3  2022-10-03     2 days  2022-10-05  31 days  2022-11-05  0.032126
4  2022-10-03     2 days  2022-10-05  61 days  2022-12-05  0.036929
5  2022-10-03     2 days  2022-10-05  92 days  2023-01-05  0.040469
6  2022-10-03     2 days  2022-10-05 182 days  2023-04-05  0.042740
7  2022-10-03     2 days  2022-10-05 365 days  2023-10-05  0.039971

"""

"""
The Codes Below Are Used To Interpolate The Observable Data To Cover The
Entire Term Of The Interpolation Period.  The Interpolation Methodology Used Is Linear And It
Is Implemented Using The Pandas Library Within Python.
"""

longestNumberOfDays = (lastResetDate - firstResetDate).days  #To determine the length of the interpolation period in days.

#The Following Programs Are Used To Create Intermediate Data Containers Used In Our Calculation.
#The Data Structures Here Cover The Entire Interpolation Period.

fixingDateList = []
for x in range(longestNumberOfDays):
    fixingDateList.append(fixingDate)
    
newResetDateList = []
for x in range(longestNumberOfDays):
    newResetDateList.append(firstResetDate)
    
elongatedMaturities = []
for x in range(1,longestNumberOfDays+1):
    elongatedMaturities.append(firstResetDate + timedelta(days=x))
    
elongatedTenor = [(a_i - b_i).days for a_i, b_i in zip(elongatedMaturities, newResetDateList)]

observedRateDictionary = {key:value for key, value in zip(originalMaturities,rates)}

obsRateDF = pd.DataFrame(observedRateDictionary.items())

elongatedRateDF = pd.DataFrame(elongatedMaturities)

CombDF = pd.merge(elongatedRateDF, obsRateDF, on=0, how='outer')

InterpolatedRatesDF = CombDF.interpolate(method='linear')  #Interpolate Using Linear Methodology.


InterpolatedRatesDic = dict(zip(InterpolatedRatesDF[0], InterpolatedRatesDF[1]))

#Dictionaries Are Unordered Lists So We Need To Sort Them By Dates Since This Is A Timeseries.

InterpolatedRatesDic = collections.OrderedDict(sorted(InterpolatedRatesDic.items())) 

"""
This section is used to adjust for weekends and holidays.  The assumptions made in this section are as follows:
    
(a) If the maturity date for a tenor falls on a Saturday move the maturity to the next good business day as long as the
updated maturity and the original maturity are in the same month.  Saturdays are moved foward by 2 days i.e. next Monday.
If the next good business day falls in a different month, roll back the maturity date to the previous good business day
or the day before as long as those dates do not fall on a public holiday.


(b) If the maturity date for a tenor falls on a Sunday move the maturity to the next good business day as long as the
updated maturity and the original maturity are in the same month.  Sundays are moved foward by 1 day i.e. next Monday.
If the next good business day falls in a different month, roll back the maturity date to the previous good business day
or the day before as long as those dates do not fall on a public holiday.

(c) If the maturity date for a tenor falls on a Public holiday (and holiday does not fall on a weekend) move the maturity 
to the next good business day as long as the updated maturity and the original maturity are in the same month.  
Holidays are moved foward by 1 day.


(d) if the maturity does not fall on a weekend or public holiday no further adjustments are necessary.

(e) If the second to the longest tenor or the longest tenor falls on a weekend or a public holiday no further 
adjustment is necessary.  Of course, this can be implemented in a slightly different way, but this is a simplifying
assumption we made for these rare ``corner cases''.
"""

publicHolidayDict={}
for k in InterpolatedRatesDic.keys():
    
    if k in publicHolidays and (k.isoweekday() not in [6,7]) and not \
    (k + timedelta(days=1)) > lastResetDate:
        publicHolidayDict[k] = InterpolatedRatesDic[k + timedelta(days=1)]
    
    elif k in publicHolidays and (k.isoweekday() not in [6,7]) and \
    k.month != (k + timedelta(days=1)).month and not (k + timedelta(days=1))\
    > lastResetDate:
        
        if (InterpolatedRatesDic[k] - timedelta(days=1)) not in publicHolidays:
            publicHolidayDict[k] = InterpolatedRatesDic[k - timedelta(days=1)]
            
        elif (InterpolatedRatesDic[k] - timedelta(days=1)) in publicHolidays \
        and (InterpolatedRatesDic[k] - timedelta(days=2)) not in publicHolidays:
            publicHolidayDict[k] = InterpolatedRatesDic[k - timedelta(days=2)]
    else:
        publicHolidayDict[k] = InterpolatedRatesDic[k]

finalDict = {}
for k in publicHolidayDict.keys():
    
    if k.isoweekday() == 6 and k.month == (k + timedelta(days=2)).month and not (k + timedelta(days=1)) > lastResetDate:
        finalDict[k] = publicHolidayDict[k + timedelta(days=2)]
    
    elif k.isoweekday() == 6 and k.month != (k + timedelta(days=2)).month and not (k + timedelta(days=1)) > lastResetDate:
        if (k - timedelta(days=1)) not in publicHolidays:
            finalDict[k] = publicHolidayDict[k - timedelta(days=1)]
        elif (k - timedelta(days=1)) in publicHolidays and (k - timedelta(days=2)) not in publicHolidays:
            finalDict[k] = publicHolidayDict[k - timedelta(days=2)]
            
    elif k.isoweekday() == 7 and k.month == (k + timedelta(days=1)).month and not (k + timedelta(days=1)) > lastResetDate:
        finalDict[k] = publicHolidayDict[k + timedelta(days=1)]
    
    elif k.isoweekday() == 7 and k.month != (k + timedelta(days=1)).month and not (k + timedelta(days=1)) > lastResetDate:
        if (k - timedelta(days=2)) not in publicHolidays:
            finalDict[k] = publicHolidayDict[k - timedelta(days=2)]
        elif (k - timedelta(days=2)) in publicHolidays and (k - timedelta(days=3)) not in publicHolidays:
            finalDict[k] = publicHolidayDict[k - timedelta(days=3)]
    
    else:
        finalDict[k] = publicHolidayDict[k]


#Dictionaries are unordered list but since this is a timeseries we want to order by dates

od = collections.OrderedDict(sorted(finalDict.items()))

interpolatedAMERIBOR = pd.DataFrame()
#To Store the Interpolated Information In A Pandas Dataframe - A Table Structure.


#Reset Index to Start from 1 instead of 0. Human beings are not used to counting 
#from zero but from one.
interpolatedAMERIBOR["Fixing Date"] = fixingDateList
interpolatedAMERIBOR["Reset Adj."] = [a_i - b_i for a_i, b_i in zip(newResetDateList, fixingDateList)]
interpolatedAMERIBOR["Reset Dates"] = newResetDateList
interpolatedAMERIBOR["Tenors"] = [a_i - b_i for a_i, b_i in zip(elongatedMaturities, newResetDateList)]
interpolatedAMERIBOR["Maturities"] = od.keys()
interpolatedAMERIBOR["AMERIBOR"]=od.values()


newIndex = []
for x in interpolatedAMERIBOR.index:
    newIndex.append(x + 1)

interpolatedAMERIBOR.index = newIndex


"""
Display The Interpolated AMERIBOR Rates Generated From The Codes Above.
"""
print("")
print("INTERPOLATED AMERIBOR RATES, RESET DATES, TENORS & \
MATURITIES as of {:%d, %b %Y}".format(fixingDate))
print("_______________________________________________\
_______________________________")
print("")
print(interpolatedAMERIBOR.to_string())


"""
Sample Output Generated Are Displayed Below:
    
INTERPOLATED AMERIBOR RATES, RESET DATES, TENORS & MATURITIES as of 03, Oct 2022
______________________________________________________________________________

    Fixing Date Reset Adj. Reset Dates   Tenors  Maturities  AMERIBOR
1    2022-10-03     2 days  2022-10-05   1 days  2022-10-06  0.032244
2    2022-10-03     2 days  2022-10-05   2 days  2022-10-07  0.032231
3    2022-10-03     2 days  2022-10-05   3 days  2022-10-08  0.032193
4    2022-10-03     2 days  2022-10-05   4 days  2022-10-09  0.032193
5    2022-10-03     2 days  2022-10-05   5 days  2022-10-10  0.032193
6    2022-10-03     2 days  2022-10-05   6 days  2022-10-11  0.032180
7    2022-10-03     2 days  2022-10-05   7 days  2022-10-12  0.032168
8    2022-10-03     2 days  2022-10-05   8 days  2022-10-13  0.032166
9    2022-10-03     2 days  2022-10-05   9 days  2022-10-14  0.032164
10   2022-10-03     2 days  2022-10-05  10 days  2022-10-15  0.032159
11   2022-10-03     2 days  2022-10-05  11 days  2022-10-16  0.032159
12   2022-10-03     2 days  2022-10-05  12 days  2022-10-17  0.032159
13   2022-10-03     2 days  2022-10-05  13 days  2022-10-18  0.032157
14   2022-10-03     2 days  2022-10-05  14 days  2022-10-19  0.032155
15   2022-10-03     2 days  2022-10-05  15 days  2022-10-20  0.032154
16   2022-10-03     2 days  2022-10-05  16 days  2022-10-21  0.032152
17   2022-10-03     2 days  2022-10-05  17 days  2022-10-22  0.032147
18   2022-10-03     2 days  2022-10-05  18 days  2022-10-23  0.032147
19   2022-10-03     2 days  2022-10-05  19 days  2022-10-24  0.032147
20   2022-10-03     2 days  2022-10-05  20 days  2022-10-25  0.032145
21   2022-10-03     2 days  2022-10-05  21 days  2022-10-26  0.032143
22   2022-10-03     2 days  2022-10-05  22 days  2022-10-27  0.032142
23   2022-10-03     2 days  2022-10-05  23 days  2022-10-28  0.032140
24   2022-10-03     2 days  2022-10-05  24 days  2022-10-29  0.032135
25   2022-10-03     2 days  2022-10-05  25 days  2022-10-30  0.032135
26   2022-10-03     2 days  2022-10-05  26 days  2022-10-31  0.032135
27   2022-10-03     2 days  2022-10-05  27 days  2022-11-01  0.032133
28   2022-10-03     2 days  2022-10-05  28 days  2022-11-02  0.032131
29   2022-10-03     2 days  2022-10-05  29 days  2022-11-03  0.032129
30   2022-10-03     2 days  2022-10-05  30 days  2022-11-04  0.032128
31   2022-10-03     2 days  2022-10-05  31 days  2022-11-05  0.032446
32   2022-10-03     2 days  2022-10-05  32 days  2022-11-06  0.032446
33   2022-10-03     2 days  2022-10-05  33 days  2022-11-07  0.032446
34   2022-10-03     2 days  2022-10-05  34 days  2022-11-08  0.032606
35   2022-10-03     2 days  2022-10-05  35 days  2022-11-09  0.032766
36   2022-10-03     2 days  2022-10-05  36 days  2022-11-10  0.032927
37   2022-10-03     2 days  2022-10-05  37 days  2022-11-11  0.033087
38   2022-10-03     2 days  2022-10-05  38 days  2022-11-12  0.033567
.....................................................................
.....................................................................
.....................................................................
337  2022-10-03     2 days  2022-10-05 337 days  2023-09-07  0.040394
338  2022-10-03     2 days  2022-10-05 338 days  2023-09-08  0.040379
339  2022-10-03     2 days  2022-10-05 339 days  2023-09-09  0.040334
340  2022-10-03     2 days  2022-10-05 340 days  2023-09-10  0.040334
341  2022-10-03     2 days  2022-10-05 341 days  2023-09-11  0.040334
342  2022-10-03     2 days  2022-10-05 342 days  2023-09-12  0.040319
343  2022-10-03     2 days  2022-10-05 343 days  2023-09-13  0.040304
344  2022-10-03     2 days  2022-10-05 344 days  2023-09-14  0.040288
345  2022-10-03     2 days  2022-10-05 345 days  2023-09-15  0.040273
346  2022-10-03     2 days  2022-10-05 346 days  2023-09-16  0.040228
347  2022-10-03     2 days  2022-10-05 347 days  2023-09-17  0.040228
348  2022-10-03     2 days  2022-10-05 348 days  2023-09-18  0.040228
349  2022-10-03     2 days  2022-10-05 349 days  2023-09-19  0.040213
350  2022-10-03     2 days  2022-10-05 350 days  2023-09-20  0.040198
351  2022-10-03     2 days  2022-10-05 351 days  2023-09-21  0.040183
352  2022-10-03     2 days  2022-10-05 352 days  2023-09-22  0.040167
353  2022-10-03     2 days  2022-10-05 353 days  2023-09-23  0.040122
354  2022-10-03     2 days  2022-10-05 354 days  2023-09-24  0.040122
355  2022-10-03     2 days  2022-10-05 355 days  2023-09-25  0.040122
356  2022-10-03     2 days  2022-10-05 356 days  2023-09-26  0.040107
357  2022-10-03     2 days  2022-10-05 357 days  2023-09-27  0.040092
358  2022-10-03     2 days  2022-10-05 358 days  2023-09-28  0.040077
359  2022-10-03     2 days  2022-10-05 359 days  2023-09-29  0.040061
360  2022-10-03     2 days  2022-10-05 360 days  2023-09-30  0.040061
361  2022-10-03     2 days  2022-10-05 361 days  2023-10-01  0.040016
362  2022-10-03     2 days  2022-10-05 362 days  2023-10-02  0.040016
363  2022-10-03     2 days  2022-10-05 363 days  2023-10-03  0.040001
364  2022-10-03     2 days  2022-10-05 364 days  2023-10-04  0.039986
365  2022-10-03     2 days  2022-10-05 365 days  2023-10-05  0.039971
"""

"""
Plot the Timeseries of the Interpolated AMERIBOR Rates 
and Fit the Observed Rate - Vidsualization.
"""

plt.close('all')
fig, ax = plt.subplots(1)
ax.plot(interpolatedAMERIBOR['Maturities'],interpolatedAMERIBOR['AMERIBOR'],lw=1.5, label='Interpolated Rates')
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.title('Interpolated AMERIBOR Rates as of {:%d, %b %Y}'.format(fixingDate),fontweight="bold")
plt.plot(observedAMERIBOR['Maturities'],observedAMERIBOR['AMERIBOR'], 'ro', lw=0.5, label='Observed Rates')
plt.legend(loc=0)
plt.grid(True)

plt.ylabel('AMERIBOR Rates (%)')
plt.xlabel('Maturities')
plt.show()
