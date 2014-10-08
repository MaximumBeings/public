"""
Import relevant Python libraries and packages.
"""

import datetime
import pandas as pd
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import collections
import locale
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
locale.setlocale(locale.LC_ALL,'')

"""
OBSERVED DATA:
    
Observed NIBOR Rates on the Fixing Date
=======================================

Tenor	Rate(%)	Comment
O/N	11.1250	Observed
1M	12.3266	Observed
3M	13.3355	Observed
6M	14.1147	Observed

"""
"""
PUBLIC HOLIDAYS

Source: http://www.holiday-times.com/public-holidays-nigeria/

Stock Market Holiday Schedule - 2014
****************************************************************

Description					Date
============					======
New Year's Day                    		January 1, 2014
Milad un Nabi (Birth of Prophet Mohammed)       January 13, 2014
Good Friday                    			April 18, 2014
Easter Monday					April 21, 2014
Worker's Day                    		May 01, 2014
Democracy Day					May 29, 2014
Eid al-Fitr (End of Ramadan)                	July 28, 2014
Independence Day                                October 1, 2014
Eid al-Adha (Feast of Sacrifice)		October 4, 2014
Christmas Day					December 25, 2014
Boxing Day					December 26, 2014

Stock Market Holiday Schedule - 2015
****************************************************************

Description					Date
============					======
New Year's Day                    		January 1, 2015
Milad un Nabi (Birth of Prophet Mohammed)       January 3, 2015
Good Friday                    			April 3, 2015
Easter Monday					April 06, 2015
Worker's Day                    		May 01, 2015
Democracy Day					May 29, 2015
Eid al-Fitr (End of Ramadan)                	July 18, 2014
Independence Day                                October 1, 2014
Eid al-Adha (Feast of Sacrifice)		October 23, 2014
Christmas Day					December 25, 2015
Boxing Day					December 26, 2015
"""


"""
The Program Starts Here
"""

"""
Declare Variables Here
"""
#The following variables are to be updated as necessary:

#Change this to the fixing date on which the rates were observed.

fixingDate = datetime.date(2014,9,18)

#Create a list for the observable rates using a list data structure.

rates = [11.3750, 12.5232, 13.4910, 14.3201]   

#Rates are usually set two days in advance - so we need to adjust for reset days.

resetDateAdjustment = 2   

#This is longest tenor for the observable NIBOR rates - which is 6 months.

longestTenor = 6  



#Capital markets do not open on public holidays so we have to move public holidays to the next good business day under
#the Modified Business Day rule - which is the main assumption for our methodology.
#The holiday list should cover at least the entire duration of the period for which we are interpolating.

publicHolidays = [datetime.date(2014,1,1),datetime.date(2014,1,13),datetime.date(2014,4,18),\
datetime.date(2014,4,21),datetime.date(2014,5,1),datetime.date(2014,5,29),datetime.date(2014,7,28),\
datetime.date(2014,10,1),datetime.date(2014,10,4),datetime.date(2014,12,25),datetime.date(2014,12,26),\
datetime.date(2015,1,1),datetime.date(2015,1,3),datetime.date(2015,4,3),datetime.date(2015,4,6), \
datetime.date(2015,5,1),datetime.date(2015,5,29),datetime.date(2015,7,18),datetime.date(2015,10,1),\
datetime.date(2015,10,23),datetime.date(2015,12,25),datetime.date(2015,12,26)]

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

#Determine the Reset Dates for the Observable NIBOR Rates.

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
monthlyMaturities = [1,3,6]
for x in monthlyMaturities:
    originalMaturities.append(firstResetDate + relativedelta(months=x))

#To Store The Original Information in a Pandas Dataframe - A Table Structure.

observedNIBOR = pd.DataFrame.from_items([('Fixing Date',fixingDateList ),\
('Reset Adj.', [a_i - b_i for a_i, b_i in zip(resetDateList, fixingDateList)]),\
('Reset Dates', resetDates),('Tenors',[a_i - b_i for a_i, b_i in zip(originalMaturities,\
resetDates)]) ,('Maturities', originalMaturities),('NIBOR', rates)])

#Reset Index to Start From 1 Instead of 0.  Human beings are used to counting from 
# 1 and not 0 like computers.

newIndex = []
for x in observedNIBOR.index:
    newIndex.append(x + 1)

observedNIBOR.index = newIndex

"""
To Print Original/Observable Data.
"""

print ""
print "OBSERVED NIBOR RATES, RESET DATES, TENORS &\
MATURITIES AS OF {:%d, %b %Y}".format(fixingDate)
print "____________________________________________\
_____________________________"
print ""
print(observedNIBOR.to_string())

"""
Sample Output Generated By the Codes Above - Visualizing The Original Data In This Way Helps
Us To Understand The Process Better And Provides A Basis For Comparison To The Interpolated Data:
    
OBSERVED NIBOR RATES, RESET DATES, TENORS & MATURITIES AS OF 18, Sep 2014
_________________________________________________________________________

  Fixing Date  Reset Date Adjustments Reset/Effective Dates   Tenors  Maturities    NIBOR
1  2014-09-18                  2 days            2014-09-20   1 days  2014-09-21  11.3750
2  2014-09-18                  2 days            2014-09-20  30 days  2014-10-20  12.5232
3  2014-09-18                  2 days            2014-09-20  91 days  2014-12-20  13.4910
4  2014-09-18                  2 days            2014-09-20 181 days  2015-03-20  14.3201

"""

"""
The Codes Below Are Used To Interpolate The Observable Data To Cover The
Entire Term Of The Interpolation Period.  The Interpolation Methodology Used Is Linear And It
Is Implemented Using The Pandas Library Within Python.
"""

"""
To determine the length of the interpolation period in days.
"""

longestNumberOfDays = (lastResetDate - firstResetDate).days    

"""
The Following Programs Are Used To Create Intermediate Data Containers Used In Our Calculation. 
The Data Structures Here Cover The Entire Interpolation Period.
"""

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


#Interpolate Using Linear Methodology.

InterpolatedRatesDF = CombDF.interpolate(method='linear')   

InterpolatedRatesDic = dict(zip(InterpolatedRatesDF[0], InterpolatedRatesDF[1]))
 
"""
This section is used to adjust for weekends and holidays.  The assumptions made in this section are as follows:
(a) If the maturity date for a tenor falls on a Saturday move the maturity to the next good business day as long as the
updated maturity and the original maturity are in the same month.  Saturdays are moved foward by 2 days i.e. next Monday.

(b) If the maturity date for a tenor falls on a Sunday move the maturity to the next good business day as long as the
updated maturity and the original maturity are in the same month.  Sundays are moved foward by 1 day i.e. next Monday.

(c) If the maturity date for a tenor falls on a Public holiday (and holiday does not fall on a weekend) move the maturity 
to the next good business day as long as the updated maturity and the original maturity are in the same month.  
Holidays are moved foward by 1 day.

(d) if the maturity does not fall on a weekend or public holiday no further adjustments are necessary.

(e) If the second to the longest tenor or the longest tenor falls on a weekend or a public holiday no further 
adjustment is necessary.  Of course, this can be implemented in a slightly different way, but this is a simplifying
assumption we made for these rare ``corner cases''.

"""


"""
To adjust for public holidays
"""
publicHolidayDict={}
for k in InterpolatedRatesDic.iterkeys():
    
    if k in publicHolidays and (k.isoweekday() not in [6,7]) and not \
    (k + timedelta(days=1)) > lastResetDate:
        publicHolidayDict[k] = InterpolatedRatesDic[k + timedelta(days=1)]
    
    elif k in publicHolidays and (k.isoweekday() not in [6,7]) and \
    k.month != (k + timedelta(days=1)).month and not (k + timedelta(days=1)) > lastResetDate:
        
        if (InterpolatedRatesDic[k] - timedelta(days=1)) not in publicHolidays:
            publicHolidayDict[k] = InterpolatedRatesDic[k - timedelta(days=1)]
            
        elif (InterpolatedRatesDic[k] - timedelta(days=1)) in publicHolidays \
        and (InterpolatedRatesDic[k] - timedelta(days=2)) not in publicHolidays:
            publicHolidayDict[k] = InterpolatedRatesDic[k - timedelta(days=2)]
    else:
        publicHolidayDict[k] = InterpolatedRatesDic[k]

finalDict = {}
for k in publicHolidayDict.iterkeys():
    
    if k.isoweekday() == 6 and k.month == (k + timedelta(days=2)).month \
    and not (k + timedelta(days=1)) > lastResetDate:
        finalDict[k] = publicHolidayDict[k + timedelta(days=2)]
    
    elif k.isoweekday() == 6 and k.month != (k + timedelta(days=2)).month \
    and not (k + timedelta(days=1)) > lastResetDate:
        if (k - timedelta(days=1)) not in publicHolidays:
            finalDict[k] = publicHolidayDict[k - timedelta(days=1)]
        elif (k - timedelta(days=1)) in publicHolidays and \
        (k - timedelta(days=2)) not in publicHolidays:
            finalDict[k] = publicHolidayDict[k - timedelta(days=2)]
            
    elif k.isoweekday() == 7 and k.month == (k + timedelta(days=1)).month \
    and not (k + timedelta(days=1)) > lastResetDate:
        finalDict[k] = publicHolidayDict[k + timedelta(days=1)]
    
    elif k.isoweekday() == 7 and k.month != (k + timedelta(days=1)).month \
    and not (k + timedelta(days=1)) > lastResetDate:
        if (k - timedelta(days=2)) not in publicHolidays:
            finalDict[k] = publicHolidayDict[k - timedelta(days=2)]
        elif (k - timedelta(days=2)) in publicHolidays and \
        (k - timedelta(days=3)) not in publicHolidays:
            finalDict[k] = publicHolidayDict[k - timedelta(days=3)]
    
    else:
        finalDict[k] = publicHolidayDict[k]


#Dictionaries Are Unordered Lists So We Need To Sort Them By Dates Since This Is A Timeseries.

od = collections.OrderedDict(sorted(finalDict.items()))

#To Store the Interpolated Information In A Pandas Dataframe - A Table Structure.

interpolatedNIBOR = pd.DataFrame.from_items([('Fixing Date',fixingDateList ),\
('Reset Adj.',[a_i - b_i for a_i, b_i in zip(newResetDateList, \
fixingDateList)]),('Reset Dates', newResetDateList), ('Tenors',[a_i - b_i \
for a_i, b_i in zip(elongatedMaturities, newResetDateList)]) ,('Maturities', od.keys()),\
('NIBOR', od.values())])


#Reset Index to Start from 1 instead of 0. Humans beings are used to counting from 1 not 0.

newIndex = []
for x in interpolatedNIBOR.index:
    newIndex.append(x + 1)

interpolatedNIBOR.index = newIndex


"""
Display The Interpolated LIBOR Rates Generated From The Codes Above.
"""

print ""
print "INTERPOLATED NIBOR RATES, RESET DATES, TENORS &\
MATURITIES AS OF {:%d, %b %Y}".format(fixingDate)
print "___________________________________\
___________________________________________"
print ""
print(interpolatedNIBOR.to_string())

"""
Sample Output Generated Are Displayed Below:
    
INTERPOLATED NIBOR RATES, RESET DATES, TENORS & MATURITIES AS OF 18, Sep 2014
______________________________________________________________________________

    Fixing Date  Reset Date Adjustments Reset/Effective Dates   Tenors  Maturities      NIBOR
1    2014-09-18                  2 days            2014-09-20   1 days  2014-09-21  11.414593
2    2014-09-18                  2 days            2014-09-20   2 days  2014-09-22  11.414593
3    2014-09-18                  2 days            2014-09-20   3 days  2014-09-23  11.454186
4    2014-09-18                  2 days            2014-09-20   4 days  2014-09-24  11.493779
5    2014-09-18                  2 days            2014-09-20   5 days  2014-09-25  11.533372
6    2014-09-18                  2 days            2014-09-20   6 days  2014-09-26  11.572966
7    2014-09-18                  2 days            2014-09-20   7 days  2014-09-27  11.691745
8    2014-09-18                  2 days            2014-09-20   8 days  2014-09-28  11.691745
9    2014-09-18                  2 days            2014-09-20   9 days  2014-09-29  11.691745
10   2014-09-18                  2 days            2014-09-20  10 days  2014-09-30  11.731338
11   2014-09-18                  2 days            2014-09-20  11 days  2014-10-01  11.810524
12   2014-09-18                  2 days            2014-09-20  12 days  2014-10-02  11.810524
13   2014-09-18                  2 days            2014-09-20  13 days  2014-10-03  11.850117
14   2014-09-18                  2 days            2014-09-20  14 days  2014-10-04  11.968897
15   2014-09-18                  2 days            2014-09-20  15 days  2014-10-05  11.968897
16   2014-09-18                  2 days            2014-09-20  16 days  2014-10-06  11.968897
17   2014-09-18                  2 days            2014-09-20  17 days  2014-10-07  12.008490
18   2014-09-18                  2 days            2014-09-20  18 days  2014-10-08  12.048083
19   2014-09-18                  2 days            2014-09-20  19 days  2014-10-09  12.087676
20   2014-09-18                  2 days            2014-09-20  20 days  2014-10-10  12.127269
21   2014-09-18                  2 days            2014-09-20  21 days  2014-10-11  12.246048
22   2014-09-18                  2 days            2014-09-20  22 days  2014-10-12  12.246048
23   2014-09-18                  2 days            2014-09-20  23 days  2014-10-13  12.246048
24   2014-09-18                  2 days            2014-09-20  24 days  2014-10-14  12.285641
25   2014-09-18                  2 days            2014-09-20  25 days  2014-10-15  12.325234
26   2014-09-18                  2 days            2014-09-20  26 days  2014-10-16  12.364828
27   2014-09-18                  2 days            2014-09-20  27 days  2014-10-17  12.404421
28   2014-09-18                  2 days            2014-09-20  28 days  2014-10-18  12.523200
29   2014-09-18                  2 days            2014-09-20  29 days  2014-10-19  12.523200
30   2014-09-18                  2 days            2014-09-20  30 days  2014-10-20  12.523200
31   2014-09-18                  2 days            2014-09-20  31 days  2014-10-21  12.539066
32   2014-09-18                  2 days            2014-09-20  32 days  2014-10-22  12.554931
33   2014-09-18                  2 days            2014-09-20  33 days  2014-10-23  12.570797
34   2014-09-18                  2 days            2014-09-20  34 days  2014-10-24  12.586662
35   2014-09-18                  2 days            2014-09-20  35 days  2014-10-25  12.634259
36   2014-09-18                  2 days            2014-09-20  36 days  2014-10-26  12.634259
37   2014-09-18                  2 days            2014-09-20  37 days  2014-10-27  12.634259
.............................................................................................
.............................................................................................
.............................................................................................
124  2014-09-18                  2 days            2014-09-20 124 days  2015-01-22  13.795003
125  2014-09-18                  2 days            2014-09-20 125 days  2015-01-23  13.804216
126  2014-09-18                  2 days            2014-09-20 126 days  2015-01-24  13.831852
127  2014-09-18                  2 days            2014-09-20 127 days  2015-01-25  13.831852
128  2014-09-18                  2 days            2014-09-20 128 days  2015-01-26  13.831852
129  2014-09-18                  2 days            2014-09-20 129 days  2015-01-27  13.841064
130  2014-09-18                  2 days            2014-09-20 130 days  2015-01-28  13.850277
131  2014-09-18                  2 days            2014-09-20 131 days  2015-01-29  13.859489
132  2014-09-18                  2 days            2014-09-20 132 days  2015-01-30  13.868701
133  2014-09-18                  2 days            2014-09-20 133 days  2015-01-31  13.877913
134  2014-09-18                  2 days            2014-09-20 134 days  2015-02-01  13.896338
135  2014-09-18                  2 days            2014-09-20 135 days  2015-02-02  13.896338
136  2014-09-18                  2 days            2014-09-20 136 days  2015-02-03  13.905550
137  2014-09-18                  2 days            2014-09-20 137 days  2015-02-04  13.914762
138  2014-09-18                  2 days            2014-09-20 138 days  2015-02-05  13.923974
139  2014-09-18                  2 days            2014-09-20 139 days  2015-02-06  13.933187
140  2014-09-18                  2 days            2014-09-20 140 days  2015-02-07  13.960823
141  2014-09-18                  2 days            2014-09-20 141 days  2015-02-08  13.960823
142  2014-09-18                  2 days            2014-09-20 142 days  2015-02-09  13.960823
143  2014-09-18                  2 days            2014-09-20 143 days  2015-02-10  13.970036
144  2014-09-18                  2 days            2014-09-20 144 days  2015-02-11  13.979248
145  2014-09-18                  2 days            2014-09-20 145 days  2015-02-12  13.988460
146  2014-09-18                  2 days            2014-09-20 146 days  2015-02-13  13.997672
147  2014-09-18                  2 days            2014-09-20 147 days  2015-02-14  14.025309
148  2014-09-18                  2 days            2014-09-20 148 days  2015-02-15  14.025309
149  2014-09-18                  2 days            2014-09-20 149 days  2015-02-16  14.025309
150  2014-09-18                  2 days            2014-09-20 150 days  2015-02-17  14.034521
151  2014-09-18                  2 days            2014-09-20 151 days  2015-02-18  14.043733
152  2014-09-18                  2 days            2014-09-20 152 days  2015-02-19  14.052946
153  2014-09-18                  2 days            2014-09-20 153 days  2015-02-20  14.062158
154  2014-09-18                  2 days            2014-09-20 154 days  2015-02-21  14.089794
155  2014-09-18                  2 days            2014-09-20 155 days  2015-02-22  14.089794
156  2014-09-18                  2 days            2014-09-20 156 days  2015-02-23  14.089794
157  2014-09-18                  2 days            2014-09-20 157 days  2015-02-24  14.099007
158  2014-09-18                  2 days            2014-09-20 158 days  2015-02-25  14.108219
159  2014-09-18                  2 days            2014-09-20 159 days  2015-02-26  14.117431
160  2014-09-18                  2 days            2014-09-20 160 days  2015-02-27  14.126643
161  2014-09-18                  2 days            2014-09-20 161 days  2015-02-28  14.135856
162  2014-09-18                  2 days            2014-09-20 162 days  2015-03-01  14.154280
163  2014-09-18                  2 days            2014-09-20 163 days  2015-03-02  14.154280
164  2014-09-18                  2 days            2014-09-20 164 days  2015-03-03  14.163492
165  2014-09-18                  2 days            2014-09-20 165 days  2015-03-04  14.172704
166  2014-09-18                  2 days            2014-09-20 166 days  2015-03-05  14.181917
167  2014-09-18                  2 days            2014-09-20 167 days  2015-03-06  14.191129
168  2014-09-18                  2 days            2014-09-20 168 days  2015-03-07  14.218766
169  2014-09-18                  2 days            2014-09-20 169 days  2015-03-08  14.218766
170  2014-09-18                  2 days            2014-09-20 170 days  2015-03-09  14.218766
171  2014-09-18                  2 days            2014-09-20 171 days  2015-03-10  14.227978
172  2014-09-18                  2 days            2014-09-20 172 days  2015-03-11  14.237190
173  2014-09-18                  2 days            2014-09-20 173 days  2015-03-12  14.246402
174  2014-09-18                  2 days            2014-09-20 174 days  2015-03-13  14.255614
175  2014-09-18                  2 days            2014-09-20 175 days  2015-03-14  14.283251
176  2014-09-18                  2 days            2014-09-20 176 days  2015-03-15  14.283251
177  2014-09-18                  2 days            2014-09-20 177 days  2015-03-16  14.283251
178  2014-09-18                  2 days            2014-09-20 178 days  2015-03-17  14.292463
179  2014-09-18                  2 days            2014-09-20 179 days  2015-03-18  14.301676
180  2014-09-18                  2 days            2014-09-20 180 days  2015-03-19  14.310888
181  2014-09-18                  2 days            2014-09-20 181 days  2015-03-20  14.320100

"""

"""
Plot The Timeseries Chart Of The Interpolated NIBOR Rates And Fit the Observed Rate
"""

plt.close('all')
fig, ax = plt.subplots(1)
ax.plot(interpolatedNIBOR['Maturities'],interpolatedNIBOR['NIBOR'],\
lw=1.5,label='Interpolated Rates')
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.title('Interpolated NIBOR Rates as of {:%d, %b %Y}'.format(fixingDate), fontweight="bold")
plt.plot(observedNIBOR['Maturities'],observedNIBOR['NIBOR'], 'ro', \
lw=1.5,label='Observed Rates')
plt.grid(True)
plt.legend(loc=0)
plt.ylabel('NIBOR Rates (%)')
plt.xlabel('Maturities')
plt.show()
