"""
Source - ISDA Linear Interpolation Example
Software - Canopy Express By Enthought 
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


"""
OBSERVED DATA:
    
Observed LIBOR Rates on the Fixing Date (2014/09/17)
====================================================

Tenor	Rate(%)	    Comment
O/N	-0.04714    Observed
1 Week  -0.04643    Observed
1M	0.00071     Observed
2M      0.03214     Observed
3M	0.05000	    Observed
6M	0.14286	    Observed
12M     0.30071     Observed

"""

"""
PUBLIC HOLIDAYS

Stock Market Holiday Schedule - 2014
****************************************************************
Description					Date
============					======
New Year's Day                    		January 1, 2014
Martin Luther King Jr. Day             		January 20, 2014
Washington's Birthday (Presidents' Day)         February 17, 2014
Good Friday                    			April 18, 2014
Memorial Day                    		May 26, 2014
Independence Day                		July 4, 2014
Labor Day                    			September 1, 2014
Thanksgiving Day				November 27, 2014
Christmas Day					December 25, 2014

Stock Market Holiday Schedule - 2015
********************************************************************
Description 					Date
===========					======
New Year's Day					January 1, 2015
Martin Luther King Jr. Day			January 19, 2015
Washington's Birthday (President's Day)		February 16, 2015
Good Friday					April 3, 2015
Memorial Day					May 25, 2015
Independence Day				July 3, 2015
Labor Day					September 7, 2015
Thanksgiving Day				November 26, 2015
Christmas Day					December 25, 2015


"""


"""
The Program Starts Here
"""

"""
Declare Variables Here
"""
#The following variables are to be updated as necessary:

fixingDate = datetime.date(2014,9,17)  #Change this to the fixing date on which the rates were observed

resetDateAdjustment = 2  #Rates are usually set two days in advance - so we need to adjust for reset days.

longestTenor = 12  #This is longest tenor for the observable LIBOR rates - which is 12 months

rates = [-0.04714,-0.04643,0.00071,0.03214,0.05000,0.14286,0.30071]  #Create a list for the observable rates using a list data structure.

#Capital markets do not open on public holidays so we have to move public holidays to the next good business day under
#the Modified Business Day rule - which is the main assumption for our methodology.
#The holiday list should cover at least the entire duration of the period for which we are interpolating.

publicHolidays = [datetime.date(2014,1,1),datetime.date(2014,1,20), \
datetime.date(2014,2,17),datetime.date(2014,4,18),datetime.date(2014,5,26), \
datetime.date(2014,7,4),datetime.date(2014,9,1),datetime.date(2014,11,27), \
datetime.date(2014,12,25), datetime.date(2015,1,1),datetime.date(2015,1,19), \
datetime.date(2015,2,16),datetime.date(2015,4,3),datetime.date(2015,5,26),\
datetime.date(2015,7,3),datetime.date(2014,9,7),datetime.date(2015,11,26),\
datetime.date(2015,12,25), ]


"""
Declare and initialize intermediate variables. These variables and declarations should not be changed.
"""
#This variable does not need to change and is used to track the number of observable rates.

lengthOfObservedData = len(rates)

#Determine the First Reset Date.  Interbank Offered Rates Are Usually Fixed 2 Days Prior to Reset Date
#However, this Depends on the Convention in a Particular Market. The Number of Days of Reset Date Adjustment
#Was Stored In The Variable Named "resetDateAdjustment" Above. 

firstResetDate = fixingDate + timedelta(days=resetDateAdjustment)

#Determine the Longest Reset Date for the Observable LIBOR Rates
#In the Case of LIBOR - this is 12 Months Unless it Changes in the Future
#This information is Stored In the Variable Named longestTenor


lastResetDate = firstResetDate + relativedelta(months=longestTenor)

"""
This Section is Used to Programatically Display the Observable Rates, Tenors and Maturities.
"""
#Determine the Reset Dates for the Observable LIBOR Rates.

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

observedLIBOR = pd.DataFrame.from_items([('Fixing Date',fixingDateList ),\
('Reset Adj.',[a_i - b_i for a_i, b_i in zip(resetDateList, fixingDateList)]),\
('Reset Dates', resetDates),('Tenors',[a_i - b_i for a_i, b_i in \
zip(originalMaturities, resetDates)]) ,('Maturities', \
originalMaturities),('LIBOR', rates)])


#Reset Index to Start From 1 Instead of 0.

newIndex = []
for x in observedLIBOR.index:
    newIndex.append(x + 1)

observedLIBOR.index = newIndex

#To Print Original/Observable Data.

print ""
print "OBSERVED LIBOR RATES, RESET DATES, TENORS & \
MATURITIES AS OF {:%d, %b %Y}".format(fixingDate)
print "_______________________________________\
__________________________________"
print ""
print(observedLIBOR.to_string())

"""
Sample Output Generated by the Codes Above - Visualizing The Original 
Data in this Way Helps In Understanding The Process Better and 
Provides A Basis For Comparison To The Interpolated Data:
    
OBSERVED LIBOR RATES, RESET DATES, TENORS & MATURITIES AS OF 17, Sep 2014
_________________________________________________________________________

  Fixing Date  Reset Date Adjustments Reset/Effective Dates   Tenors  Maturities    LIBOR
1  2014-09-17                  2 days            2014-09-19   1 days  2014-09-20 -0.04714
2  2014-09-17                  2 days            2014-09-19   7 days  2014-09-26 -0.04643
3  2014-09-17                  2 days            2014-09-19  30 days  2014-10-19  0.00071
4  2014-09-17                  2 days            2014-09-19  61 days  2014-11-19  0.03214
5  2014-09-17                  2 days            2014-09-19  91 days  2014-12-19  0.05000
6  2014-09-17                  2 days            2014-09-19 181 days  2015-03-19  0.14286
7  2014-09-17                  2 days            2014-09-19 365 days  2015-09-19  0.30071

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
for k in InterpolatedRatesDic.iterkeys():
    
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
for k in publicHolidayDict.iterkeys():
    
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


#To Store the Interpolated Information In A Pandas Dataframe - A Table Structure.

interpolatedLIBOR = pd.DataFrame.from_items([('Fixing Date',fixingDateList ),\
('Reset Adj.', [a_i - b_i for a_i, b_i in zip(newResetDateList, fixingDateList)]),\
('Reset Dates', newResetDateList), ('Tenors',[a_i - b_i for a_i, b_i in \
zip(elongatedMaturities, newResetDateList)]) ,('Maturities', od.keys()),('LIBOR', od.values())])

#Reset Index to Start from 1 instead of 0. Human beings are not used to counting 
#from zero but from one.

newIndex = []
for x in interpolatedLIBOR.index:
    newIndex.append(x + 1)

interpolatedLIBOR.index = newIndex


"""
Display The Interpolated LIBOR Rates Generated From The Codes Above.
"""
print ""
print "INTERPOLATED LIBOR RATES, RESET DATES, TENORS & \
MATURITIES as of {:%d, %b %Y}".format(fixingDate)
print "_______________________________________________\
_______________________________"
print ""
print(interpolatedLIBOR.to_string())


"""
Sample Output Generated Are Displayed Below:
    
INTERPOLATED LIBOR RATES, RESET DATES, TENORS & MATURITIES AS OF 17, Sep 2014
______________________________________________________________________________

    Fixing Date  Reset Date Adjustments Reset/Effective Dates   Tenors  Maturities     LIBOR
1    2014-09-17                  2 days            2014-09-19   1 days  2014-09-20 -0.046903
2    2014-09-17                  2 days            2014-09-19   2 days  2014-09-21 -0.046903
3    2014-09-17                  2 days            2014-09-19   3 days  2014-09-22 -0.046903
4    2014-09-17                  2 days            2014-09-19   4 days  2014-09-23 -0.046785
5    2014-09-17                  2 days            2014-09-19   5 days  2014-09-24 -0.046667
6    2014-09-17                  2 days            2014-09-19   6 days  2014-09-25 -0.046548
7    2014-09-17                  2 days            2014-09-19   7 days  2014-09-26 -0.046430
8    2014-09-17                  2 days            2014-09-19   8 days  2014-09-27 -0.040281
9    2014-09-17                  2 days            2014-09-19   9 days  2014-09-28 -0.040281
10   2014-09-17                  2 days            2014-09-19  10 days  2014-09-29 -0.040281
11   2014-09-17                  2 days            2014-09-19  11 days  2014-09-30 -0.038232
12   2014-09-17                  2 days            2014-09-19  12 days  2014-10-01 -0.036182
13   2014-09-17                  2 days            2014-09-19  13 days  2014-10-02 -0.034133
14   2014-09-17                  2 days            2014-09-19  14 days  2014-10-03 -0.032083
15   2014-09-17                  2 days            2014-09-19  15 days  2014-10-04 -0.025934
16   2014-09-17                  2 days            2014-09-19  16 days  2014-10-05 -0.025934
17   2014-09-17                  2 days            2014-09-19  17 days  2014-10-06 -0.025934
18   2014-09-17                  2 days            2014-09-19  18 days  2014-10-07 -0.023885
19   2014-09-17                  2 days            2014-09-19  19 days  2014-10-08 -0.021835
20   2014-09-17                  2 days            2014-09-19  20 days  2014-10-09 -0.019786
21   2014-09-17                  2 days            2014-09-19  21 days  2014-10-10 -0.017736
22   2014-09-17                  2 days            2014-09-19  22 days  2014-10-11 -0.011587
23   2014-09-17                  2 days            2014-09-19  23 days  2014-10-12 -0.011587
24   2014-09-17                  2 days            2014-09-19  24 days  2014-10-13 -0.011587
25   2014-09-17                  2 days            2014-09-19  25 days  2014-10-14 -0.009538
26   2014-09-17                  2 days            2014-09-19  26 days  2014-10-15 -0.007488
27   2014-09-17                  2 days            2014-09-19  27 days  2014-10-16 -0.005439
............................................................................................
............................................................................................
............................................................................................
344  2014-09-17                  2 days            2014-09-19 344 days  2015-08-29  0.284410
345  2014-09-17                  2 days            2014-09-19 345 days  2015-08-30  0.284410
346  2014-09-17                  2 days            2014-09-19 346 days  2015-08-31  0.284410
347  2014-09-17                  2 days            2014-09-19 347 days  2015-09-01  0.285268
348  2014-09-17                  2 days            2014-09-19 348 days  2015-09-02  0.286126
349  2014-09-17                  2 days            2014-09-19 349 days  2015-09-03  0.286984
350  2014-09-17                  2 days            2014-09-19 350 days  2015-09-04  0.287842
351  2014-09-17                  2 days            2014-09-19 351 days  2015-09-05  0.290415
352  2014-09-17                  2 days            2014-09-19 352 days  2015-09-06  0.290415
353  2014-09-17                  2 days            2014-09-19 353 days  2015-09-07  0.290415
354  2014-09-17                  2 days            2014-09-19 354 days  2015-09-08  0.291273
355  2014-09-17                  2 days            2014-09-19 355 days  2015-09-09  0.292131
356  2014-09-17                  2 days            2014-09-19 356 days  2015-09-10  0.292989
357  2014-09-17                  2 days            2014-09-19 357 days  2015-09-11  0.293847
358  2014-09-17                  2 days            2014-09-19 358 days  2015-09-12  0.296421
359  2014-09-17                  2 days            2014-09-19 359 days  2015-09-13  0.296421
360  2014-09-17                  2 days            2014-09-19 360 days  2015-09-14  0.296421
361  2014-09-17                  2 days            2014-09-19 361 days  2015-09-15  0.297278
362  2014-09-17                  2 days            2014-09-19 362 days  2015-09-16  0.298136
363  2014-09-17                  2 days            2014-09-19 363 days  2015-09-17  0.298994
364  2014-09-17                  2 days            2014-09-19 364 days  2015-09-18  0.299852
365  2014-09-17                  2 days            2014-09-19 365 days  2015-09-19  0.300710

"""

"""
Plot the Timeseries of the Interpolated LIBOR Rates 
and Fit the Observed Rate - Vidsualization.
"""

plt.close('all')
fig, ax = plt.subplots(1)
ax.plot(interpolatedLIBOR['Maturities'],interpolatedLIBOR['LIBOR'],lw=1.5, label='Interpolated Rates')
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.title('Interpolated LIBOR Rates as of {:%d, %b %Y}'.format(fixingDate),fontweight="bold")
plt.plot(observedLIBOR['Maturities'],observedLIBOR['LIBOR'], 'ro', lw=0.5, label='Observed Rates')
plt.legend(loc=0)
plt.grid(True)

plt.ylabel('LIBOR Rates (%)')
plt.xlabel('Maturities')
plt.show()
