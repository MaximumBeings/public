# USD_SOFR.py
# -------------------------------------------------------------------------
# Import Libraries & Packages
# These packages are used by all modules.
# ------------------------------------------------------------------------- 
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
import locale
locale.setlocale(locale.LC_ALL, '')
pd.set_option('display.precision',10)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
matplotlib.style.use('ggplot')
from scipy.interpolate import interp1d
from scipy import arange, array, exp
import numpy as np
from scipy import interpolate
from copy import deepcopy

# -------------------------------------------------------------------------
# Store the Observed Deposit Rates in List Data Structures.
# ------------------------------------------------------------------------- 

val_date = datetime.date(2022, 12, 22)

dayCountBase = 365.0

dEPOSIT_dATES = [datetime.date(2022, 12, 23),datetime.date(2023,1,22),\
               datetime.date(2023,3,22),datetime.date(2023,5,22)]
               
dEPOSIT_rATES = [4.3000,4.32336,4.45107,4.71758]

#---------------------------------------------------------------------------
# Calculate the discount rate for deposit rates
#-----------------------------------------------------------------------------

def discountDEPOST():
    dEPOSIT_dISCOUNT = []
    result = 0.0
    for x in range(len(dEPOSIT_dATES)):
        numberOfDays = (dEPOSIT_dATES[x] - val_date).days
        result = 1/(1+ (dEPOSIT_rATES[x]/100.0 * numberOfDays/dayCountBase))
        dEPOSIT_dISCOUNT.append(result)
        result=0.0
    return dEPOSIT_dISCOUNT
    
dEPOSIT_dISCOUNT = discountDEPOST()

# -------------------------------------------------------------------------
# Create a Pandas dataframe to combine all the above lists into a table.
# ------------------------------------------------------------------------- 

DEPOSIT = {'Maturities' : pd.Series(dEPOSIT_dATES),\
'Rates' : pd.Series(dEPOSIT_rATES), 'Discounts' : pd.Series(dEPOSIT_dISCOUNT)}

DEPOSIT_df = pd.DataFrame(DEPOSIT,columns=['Maturities', 'Rates','Discounts'])

# -------------------------------------------------------------------------
# Preview the discount rates.
# ------------------------------------------------------------------------- 
print()
print(DEPOSIT_df.to_string(index = False))

"""
 Maturities    Rates     Discounts
 2022-12-23  4.30000  0.9998822057
 2023-01-22  4.32336  0.9963415387
 2023-03-22  4.45107  0.9891439071
 2023-05-22  4.71758  0.9808570409
"""

# -------------------------------------------------------------------------
# Store the observed futures rates in list data structures.
# ------------------------------------------------------------------------- 
fUTURES_sTART_dATES = [datetime.date(2023,8,22),datetime.date(2023,11,22),\
               datetime.date(2024,2,22),datetime.date(2024,5,22),\
               datetime.date(2024,8,22),datetime.date(2024,11,22)]
              
fUTURES_eND_dATES = [datetime.date(2023,11,22),\
               datetime.date(2024,2,22),datetime.date(2024,5,22),\
               datetime.date(2024,8,22),datetime.date(2024,11,22), datetime.date(2025,2,22) ]
               
fUTURES_pRICES = [95.18242,95.08242,94.98242,94.88242,94.78242,94.68242]

# -------------------------------------------------------------------------
# The first step is to convert futures prices into futures interest rate
# ------------------------------------------------------------------------- 

def futureInterestRate(fUTURES_pRICES):
    fInterestRate = []
    for x in range(len(fUTURES_pRICES)):
        fInterestRate.append((fUTURES_pRICES[x] - 100.0)/(-1))
    return fInterestRate
    
fInterestRate = deepcopy(futureInterestRate(fUTURES_pRICES))

def fUTURES_dISCOUNT():
    futuresDiscount=deepcopy(dEPOSIT_dISCOUNT)
    for x in range(0,len(fInterestRate)):
        numberOfDays = (fUTURES_eND_dATES[x] - fUTURES_sTART_dATES[x]).days
        if x == 0:
            P = deepcopy(dEPOSIT_dISCOUNT)[-1]
            result = P / (1  + fInterestRate[x]/100.0* numberOfDays/365.0)
            futuresDiscount.append(result)
        elif x > 0:
            P = futuresDiscount[-1]
            result = P/(1+ fInterestRate[x]/100.0 * numberOfDays/365.0)
            futuresDiscount.append(result)
    return futuresDiscount[len(dEPOSIT_dISCOUNT):]
    
fUTURE_dISCOUNT_rATES = deepcopy(fUTURES_dISCOUNT())

# -------------------------------------------------------------------------
# Create a Pandas dataframe to combine all the above lists into a table.
# ------------------------------------------------------------------------- 

FUTURE = {'Maturities' : pd.Series(fUTURES_eND_dATES),\
'Rates' : pd.Series(fInterestRate), 'Discounts' : pd.Series(fUTURE_dISCOUNT_rATES)}

FUTURE_df = pd.DataFrame(FUTURE,columns=['Maturities', 'Rates','Discounts'])

# -------------------------------------------------------------------------
# Preview the futures discount rates.
# ------------------------------------------------------------------------- 
print()
print(FUTURE_df.to_string(index = False))

"""
  Maturities    Rates     Discounts
 2023-11-22  4.81758  0.9690894446
 2024-02-22  4.91758  0.9572246488
 2024-05-22  5.01758  0.9455264863
 2024-08-22  5.11758  0.9334853599
 2024-11-22  5.21758  0.9213682975
 2025-02-22  5.31758  0.9091823310
"""

# -------------------------------------------------------------------------
# Combine deposit & future instruments discount curves and preview the data
# ------------------------------------------------------------------------- 
print()
middleLevelCurves=DEPOSIT_df.append(FUTURE_df,ignore_index = True)
print(middleLevelCurves.to_string(index = False))

"""
 Maturities    Rates     Discounts
 2022-12-23  4.30000  0.9998822057
 2023-01-22  4.32336  0.9963415387
 2023-03-22  4.45107  0.9891439071
 2023-05-22  4.71758  0.9808570409
 2023-11-22  4.81758  0.9690894446
 2024-02-22  4.91758  0.9572246488
 2024-05-22  5.01758  0.9455264863
 2024-08-22  5.11758  0.9334853599
 2024-11-22  5.21758  0.9213682975
 2025-02-22  5.31758  0.9091823310
"""

# -------------------------------------------------------------------------
# Store the Observed SOFR Swap Fixed Rates in a list data structure.
#  Use SFR from 3 years.
# This is because the deposit and future instruments already covered our
# rates for the up to 2 years.  So we will only use SFRs from two years
# onward.
# ------------------------------------------------------------------------- 


sFR_dATES = [datetime.date(2025,12,22),datetime.date(2027,12,22),datetime.date(2032,12,22),\
            datetime.date(2042,12,22),datetime.date(2052,12,22)]
               
sFR_rATES = [5.41758,5.61758,5.91758,6.11758,6.517581]
# -------------------------------------------------------------------------
# Create a Pandas Dataframe to store the SFR data and preview the data.
# ------------------------------------------------------------------------- 

SFR = {'Maturities' : pd.Series(sFR_dATES),\
'Rates' : pd.Series(sFR_rATES)}

SFR_df = pd.DataFrame(SFR,columns=['Maturities', 'Rates'])

print()
print(SFR_df.to_string(index = False))

"""
 Maturities     Rates
 2025-12-22  5.417580
 2027-12-22  5.617580
 2032-12-22  5.917580
 2042-12-22  6.117580
 2052-12-22  6.517581
"""

# -------------------------------------------------------------------------
# In order to build the discount curves for using swap instruments, we need
# to make an assumption about the tenor of swap instruments.  We assume that
# our swap instruments have cashflows that are payable or receiveable every
# three months.  However, swap fixed rates are only observable for certain 
# dates. So we need to interpolate to ensure that rates are available at least
# on a quarterly basis. We do not need to do that for the deposit and futures
# instruments because we were able to observe data for those instruments at
# least on a quarterly or shorter basis.  In order to do this, we first create
# a list containing dates on a three-month basis from the maturity of the first
# SFR we are using to the maturity of the last one. We then merge the data
# with the dataframe of the ones we were able to observe and interpolate.
# Preview a subset of the interpolated data.
# ------------------------------------------------------------------------- 

start = datetime.date(2022,12,22)
end = datetime.date(2052,12,22)


#Get the range of months to cover
months = (end.year - start.year)*12 + end.month - start.month

#The frequency of periods
period = 3 # in months
months = int(months/period)


def maturities(x,compounding):
    maturities = []
    for y in range(1,months+1):
        maturities.append((x)+relativedelta(months=compounding*y))
    return maturities
    
maturities2 = maturities(start,period)

df = {'Maturities': pd.Series(maturities2)}
lONG_SFR_dATES = pd.DataFrame(df,columns=['Maturities'])

nEW_SFR= pd.merge(lONG_SFR_dATES, SFR_df, on='Maturities', how='outer')

nEW_SFR = nEW_SFR.sort_values(by=['Maturities'], ascending=True)

nEW_SFR = nEW_SFR.reset_index(drop=True)

nEW_SFR = nEW_SFR.interpolate(method='linear')
nEW_SFR.dropna(inplace=True)
print()
print(nEW_SFR.to_string(index = False))

"""
 Maturities        Rates
 2025-12-22  5.417580000
 2026-03-22  5.442580000
 2026-06-22  5.467580000
 2026-09-22  5.492580000
 2026-12-22  5.517580000
 2027-03-22  5.542580000
 2027-06-22  5.567580000
 2027-09-22  5.592580000
 2027-12-22  5.617580000
 2028-03-22  5.632580000
 2028-06-22  5.647580000
 2028-09-22  5.662580000
 2028-12-22  5.677580000
 2029-03-22  5.692580000
 2029-06-22  5.707580000
 2029-09-22  5.722580000
 2029-12-22  5.737580000
 2030-03-22  5.752580000
 2030-06-22  5.767580000
 2030-09-22  5.782580000
 2030-12-22  5.797580000
 2031-03-22  5.812580000
 2031-06-22  5.827580000
 2031-09-22  5.842580000
 2031-12-22  5.857580000
 2032-03-22  5.872580000
 2032-06-22  5.887580000
 2032-09-22  5.902580000
 2032-12-22  5.917580000
 2033-03-22  5.922580000
 2033-06-22  5.927580000
 2033-09-22  5.932580000
 2033-12-22  5.937580000
 2034-03-22  5.942580000
 2034-06-22  5.947580000
 2034-09-22  5.952580000
 2034-12-22  5.957580000
 2035-03-22  5.962580000
 2035-06-22  5.967580000
 2035-09-22  5.972580000
 2035-12-22  5.977580000
 2036-03-22  5.982580000
 2036-06-22  5.987580000
 2036-09-22  5.992580000
 2036-12-22  5.997580000
 2037-03-22  6.002580000
 2037-06-22  6.007580000
 2037-09-22  6.012580000
 2037-12-22  6.017580000
 2038-03-22  6.022580000
 2038-06-22  6.027580000
 2038-09-22  6.032580000
 2038-12-22  6.037580000
 2039-03-22  6.042580000
 2039-06-22  6.047580000
 2039-09-22  6.052580000
 2039-12-22  6.057580000
 2040-03-22  6.062580000
 2040-06-22  6.067580000
 2040-09-22  6.072580000
 2040-12-22  6.077580000
 2041-03-22  6.082580000
 2041-06-22  6.087580000
 2041-09-22  6.092580000
 2041-12-22  6.097580000
 2042-03-22  6.102580000
 2042-06-22  6.107580000
 2042-09-22  6.112580000
 2042-12-22  6.117580000
 2043-03-22  6.127580025
 2043-06-22  6.137580050
 2043-09-22  6.147580075
 2043-12-22  6.157580100
 2044-03-22  6.167580125
 2044-06-22  6.177580150
 2044-09-22  6.187580175
 2044-12-22  6.197580200
 2045-03-22  6.207580225
 2045-06-22  6.217580250
 2045-09-22  6.227580275
 2045-12-22  6.237580300
 2046-03-22  6.247580325
 2046-06-22  6.257580350
 2046-09-22  6.267580375
 2046-12-22  6.277580400
 2047-03-22  6.287580425
 2047-06-22  6.297580450
 2047-09-22  6.307580475
 2047-12-22  6.317580500
 2048-03-22  6.327580525
 2048-06-22  6.337580550
 2048-09-22  6.347580575
 2048-12-22  6.357580600
 2049-03-22  6.367580625
 2049-06-22  6.377580650
 2049-09-22  6.387580675
 2049-12-22  6.397580700
 2050-03-22  6.407580725
 2050-06-22  6.417580750
 2050-09-22  6.427580775
 2050-12-22  6.437580800
 2051-03-22  6.447580825
 2051-06-22  6.457580850
 2051-09-22  6.467580875
 2051-12-22  6.477580900
 2052-03-22  6.487580925
 2052-06-22  6.497580950
 2052-09-22  6.507580975
 2052-12-22  6.517581000
"""




# -------------------------------------------------------------------------
# Create temporary files to store dates and rates for the different section
# of the yield curve. These should store the observed data for deposit and 
#futures and interpolated for swap.  This is a temporary file only.
# This section also creates other temporary files.
# ------------------------------------------------------------------------- 

sWAP_eND_dATES = nEW_SFR['Maturities'].tolist()



maturities = dEPOSIT_dATES + fUTURES_eND_dATES+sWAP_eND_dATES

sWAP_rATES = nEW_SFR['Rates'].tolist()



rATES= dEPOSIT_rATES + fInterestRate + sWAP_rATES

SFRStartingIndex = len(dEPOSIT_rATES + fInterestRate)

discountSOFR = middleLevelCurves['Discounts'].tolist()

futuresLastDate = datetime.date(2022,12,22)

# -------------------------------------------------------------------------
# The programs below are used in generating the discount factors for the 
# long end of the yield curve using the SFRs.
# ------------------------------------------------------------------------- 
#Helper function used in calculating Disc Factors for SFR

def discountSFRhelper(SOFRlist,n):
    final = 0.0
    ans = 0.0
    for x in range(n):
        if x == 0:
            numberOfDays = (maturities[x] - val_date).days
            ans = numberOfDays/365.0 * SOFRlist[x]
            final = final + ans

        elif x > 0:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            ans = numberOfDays/365.0 * SOFRlist[x]
            final = final + ans

    return deepcopy(final)
    
#discountSFRhelper(SOFR,10)
    
#Function to calculate Discount Factors for Swap Fixed Rate
def swapRateCalculatorDiscCalc():
    numberOfDays2=0.0
    SOFR= []
    SOFR = deepcopy(discountSOFR)[:]
    SFRRate = deepcopy(rATES)
    for x in range(SFRStartingIndex,len(maturities)):
        final = 0.0
        ans = 0.0
        tttt = 0.0
        numberOfDays2 = (maturities[x] - maturities[x-1]).days
        tttt = discountSFRhelper(SOFR,x)
        print(x, tttt)
        print(x )
        print(x, numberOfDays2)
        k = SFRRate[x]/100.0
        print(k)
        ans = (1 -  (k * tttt))
        print(x, ans)
        b = (1 + (SFRRate[x]/100.0) * numberOfDays2/365.0)
        print(x, b)
       
        final=ans/b
        print(x, final)
     
        SOFR.append(ans/b)
        final = 0.0
    return SOFR
    

Discount = deepcopy(swapRateCalculatorDiscCalc())

Disc = {'Maturities' : pd.Series(maturities),\
'Discounts' : pd.Series(Discount)}

Discount_df = pd.DataFrame(Disc,columns=['Maturities','Discounts'])

# -------------------------------------------------------------------------
# Preview a subset of the discount factors generated using the SFRs.
# ------------------------------------------------------------------------- 

print('')
print(Discount_df.to_string(index = False))

"""
 
 Maturities     Discounts
 2022-12-23  0.9998822057
 2023-01-22  0.9963415387
 2023-03-22  0.9891439071
 2023-05-22  0.9808570409
 2023-11-22  0.9690894446
 2024-02-22  0.9572246488
 2024-05-22  0.9455264863
 2024-08-22  0.9334853599
 2024-11-22  0.9213682975
 2025-02-22  0.9091823310
 2025-12-22  0.8497444876
 2026-03-22  0.8378076879
 2026-06-22  0.8256836797
 2026-09-22  0.8136225902
 2026-12-22  0.8017453398
 2027-03-22  0.7900497317
 2027-06-22  0.7781822382
 2027-09-22  0.7663829988
 2027-12-22  0.7547678017
 2028-03-22  0.7436697275
 2028-06-22  0.7325591237
 2028-09-22  0.7215502538
 2028-12-22  0.7107519113
 2029-03-22  0.7001599324
 2029-06-22  0.6894512475
 2029-09-22  0.6788434363
 2029-12-22  0.6684398235
 2030-03-22  0.6582362958
 2030-06-22  0.6479259395
 2030-09-22  0.6377154106
 2030-12-22  0.6277026796
 2031-03-22  0.6178836904
 2031-06-22  0.6079673505
 2031-09-22  0.5981496191
 2031-12-22  0.5885232320
 2032-03-22  0.5789923700
 2032-06-22  0.5694661771
 2032-09-22  0.5600372049
 2032-12-22  0.5507930637
 2033-03-22  0.5424911748
 2033-06-22  0.5341247101
 2033-09-22  0.5258682444
 2033-12-22  0.5178034540
 2034-03-22  0.5099254931
 2034-06-22  0.5019877723
 2034-09-22  0.4941549209
 2034-12-22  0.4865039122
 2035-03-22  0.4790301302
 2035-06-22  0.4715011459
 2035-09-22  0.4640721150
 2035-12-22  0.4568155327
 2036-03-22  0.4496543734
 2036-06-22  0.4425159733
 2036-09-22  0.4354728036
 2036-12-22  0.4285930848
 2037-03-22  0.4218726331
 2037-06-22  0.4151053784
 2037-09-22  0.4084288436
 2037-12-22  0.4019071925
 2038-03-22  0.3955364437
 2038-06-22  0.3891227469
 2038-09-22  0.3827954511
 2038-12-22  0.3766148601
 2039-03-22  0.3705771866
 2039-06-22  0.3645002086
 2039-09-22  0.3585054973
 2039-12-22  0.3526496849
 2040-03-22  0.3468724036
 2040-06-22  0.3411168353
 2040-09-22  0.3354395667
 2040-12-22  0.3298937291
 2041-03-22  0.3244758997
 2041-06-22  0.3190254670
 2041-09-22  0.3136495491
 2041-12-22  0.3083979586
 2042-03-22  0.3032674427
 2042-06-22  0.2981073930
 2042-09-22  0.2930182383
 2042-12-22  0.2880466364
 2043-03-22  0.2826128249
 2043-06-22  0.2771544731
 2043-09-22  0.2717656509
 2043-12-22  0.2664899670
 2044-03-22  0.2612810903
 2044-06-22  0.2560957049
 2044-09-22  0.2509772375
 2044-12-22  0.2459661619
 2045-03-22  0.2410597525
 2045-06-22  0.2361364847
 2045-09-22  0.2312775828
 2045-12-22  0.2265205237
 2046-03-22  0.2218626962
 2046-06-22  0.2171915310
 2046-09-22  0.2125822333
 2046-12-22  0.2080694109
 2047-03-22  0.2036505642
 2047-06-22  0.1992217010
 2047-09-22  0.1948522626
 2047-12-22  0.1905741112
 2048-03-22  0.1863530470
 2048-06-22  0.1821573565
 2048-09-22  0.1780186991
 2048-12-22  0.1739663071
 2049-03-22  0.1699978972
 2049-06-22  0.1660255525
 2049-09-22  0.1621079130
 2049-12-22  0.1582717032
 2050-03-22  0.1545147442
 2050-06-22  0.1507566212
 2050-09-22  0.1470509343
 2050-12-22  0.1434220137
 2051-03-22  0.1398677823
 2051-06-22  0.1363149900
 2051-09-22  0.1328124241
 2051-12-22  0.1293821309
 2052-03-22  0.1260000891
 2052-06-22  0.1226442940
 2052-09-22  0.1193365717
 2052-12-22  0.1160967870

"""

# -------------------------------------------------------------------------
# Calculate the implied forward rates for the entire duration of 
# term structure of interest rate and preview the data.  The implied forward
# rate calculate here is the method used in the pre-crisis era.
# ------------------------------------------------------------------------- 

def impliedForwardRate():
    fRate = []
    result = 0.0
    for x in range(0,len(maturities),1):
        if x == 0:
            fRate.append(rATES[0]/100.0)
        elif x > 0:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            result = ((Discount[x-1]/Discount[x]) - 1) * (1/(numberOfDays/365.0))
            
            fRate.append(result)
            result = 0.0
    return fRate
    
fRate = deepcopy(impliedForwardRate())
fRate = [x * 100 for x in fRate]
Discount_df['Forward'] = pd.Series(fRate)
Discount_df['Rates'] = pd.Series(rATES)

Discount_df = Discount_df[['Maturities','Rates','Discounts','Forward']]


Discount_df2=Discount_df.drop(Discount_df['Forward'].idxmax())
Discount_df2=Discount_df2.drop(Discount_df2['Forward'].idxmin())
print()
print(Discount_df2.to_string(index = False))


maturitiesK= Discount_df2['Maturities'].tolist()
rATESK= Discount_df2['Rates'].tolist()



"""
 Maturities        Rates     Discounts        Forward
 2022-12-23  4.300000000  0.9998822057   4.3000000000
 2023-01-22  4.323360000  0.9963415387   4.3236293076
 2023-03-22  4.451070000  0.9891439071   4.5016423075
 2023-05-22  4.717580000  0.9808570409   5.0553082486
 2024-02-22  4.917580000  0.9572246488   4.9175800000
 2024-05-22  5.017580000  0.9455264863   5.0175800000
 2024-08-22  5.117580000  0.9334853599   5.1175800000
 2024-11-22  5.217580000  0.9213682975   5.2175800000
 2025-02-22  5.317580000  0.9091823310   5.3175800000
 2025-12-22  5.417580000  0.8497444876   8.4260672871
 2026-03-22  5.442580000  0.8378076879   5.7782179834
 2026-06-22  5.467580000  0.8256836797   5.8255583721
 2026-09-22  5.492580000  0.8136225902   5.8812356191
 2026-12-22  5.517580000  0.8017453398   5.9419766208
 2027-03-22  5.542580000  0.7900497317   6.0036965392
 2027-06-22  5.567580000  0.7781822382   6.0503810383
 2027-09-22  5.592580000  0.7663829988   6.1081991476
 2027-12-22  5.617580000  0.7547678017   6.1725510841
 2028-03-22  5.632580000  0.7436697275   5.9857557316
 2028-06-22  5.647580000  0.7325591237   6.0172771860
 2028-09-22  5.662580000  0.7215502538   6.0531466057
 2028-12-22  5.677580000  0.7107519113   6.0938328026
 2029-03-22  5.692580000  0.7001599324   6.1352209564
 2029-06-22  5.707580000  0.6894512475   6.1622258790
 2029-09-22  5.722580000  0.6788434363   6.1995647064
 2029-12-22  5.737580000  0.6684398235   6.2427125388
 2030-03-22  5.752580000  0.6582362958   6.2866441131
 2030-06-22  5.767580000  0.6479259395   6.3132551797
 2030-09-22  5.782580000  0.6377154106   6.3522322093
 2030-12-22  5.797580000  0.6277026796   6.3980854586
 2031-03-22  5.812580000  0.6178836904   6.4448142841
 2031-06-22  5.827580000  0.6079673505   6.4710712867
 2031-09-22  5.842580000  0.5981496191   6.5118794363
 2031-12-22  5.857580000  0.5885232320   6.5607151944
 2032-03-22  5.872580000  0.5789923700   6.6025365029
 2032-06-22  5.887580000  0.5694661771   6.6367655400
 2032-09-22  5.902580000  0.5600372049   6.6796316213
 2032-12-22  5.917580000  0.5507930637   6.7317748280
 2033-03-22  5.922580000  0.5424911748   6.2063261632
 2033-06-22  5.927580000  0.5341247101   6.2144736340
 2033-09-22  5.932580000  0.5258682444   6.2290565496
 2033-12-22  5.937580000  0.5178034540   6.2471165757
 2034-03-22  5.942580000  0.5099254931   6.2655247701
 2034-06-22  5.947580000  0.5019877723   6.2734684567
 2034-09-22  5.952580000  0.4941549209   6.2887133708
 2034-12-22  5.957580000  0.4865039122   6.3078858808
 2035-03-22  5.962580000  0.4790301302   6.3274387659
 2035-06-22  5.967580000  0.4715011459   6.3351759150
 2035-09-22  5.972580000  0.4640721150   6.3511405624
 2035-12-22  5.977580000  0.4568155327   6.3715153851
 2036-03-22  5.982580000  0.4496543734   6.3878687979
 2036-06-22  5.987580000  0.4425159733   6.3999557272
 2036-09-22  5.992580000  0.4354728036   6.4167062018
 2036-12-22  5.997580000  0.4285930848   6.4383858460
 2037-03-22  6.002580000  0.4218726331   6.4605198612
 2037-06-22  6.007580000  0.4151053784   6.4678389605
 2037-09-22  6.012580000  0.4084288436   6.4854444900
 2037-12-22  6.017580000  0.4019071925   6.5085351509
 2038-03-22  6.022580000  0.3955364437   6.5321226741
 2038-06-22  6.027580000  0.3891227469   6.5392335206
 2038-09-22  6.032580000  0.3827954511   6.5577733808
 2038-12-22  6.037580000  0.3766148601   6.5823962501
 2039-03-22  6.042580000  0.3705771866   6.6075627999
 2039-06-22  6.047580000  0.3645002086   6.6144680879
 2039-09-22  6.052580000  0.3585054973   6.6340308533
 2039-12-22  6.057580000  0.3526496849   6.6603205040
 2040-03-22  6.062580000  0.3468724036   6.6804426349
 2040-06-22  6.067580000  0.3411168353   6.6940675421
 2040-09-22  6.072580000  0.3354395667   6.7147553822
 2040-12-22  6.077580000  0.3298937291   6.7428664099
 2041-03-22  6.082580000  0.3244758997   6.7716302775
 2041-06-22  6.087580000  0.3190254670   6.7781420478
 2041-09-22  6.092580000  0.3136495491   6.8000639028
 2041-12-22  6.097580000  0.3083979586   6.8301593367
 2042-03-22  6.102580000  0.3032674427   6.8609712783
 2042-06-22  6.107580000  0.2981073930   6.8673023770
 2042-09-22  6.112580000  0.2930182383   6.8905841117
 2042-12-22  6.117580000  0.2880466364   6.9228514880
 2043-03-22  6.127580025  0.2826128249   7.7976376759
 2043-06-22  6.137580050  0.2771544731   7.8134829296
 2043-09-22  6.147580075  0.2717656509   7.8669126311
 2043-12-22  6.157580100  0.2664899670   7.9405280310
 2044-03-22  6.167580125  0.2612810903   7.9962721325
 2044-06-22  6.177580150  0.2560957049   8.0331112765
 2044-09-22  6.187580175  0.2509772375   8.0911572482
 2044-12-22  6.197580200  0.2459661619   8.1715993895
 2045-03-22  6.207580225  0.2410597525   8.2544745161
 2045-06-22  6.217580250  0.2361364847   8.2717118927
 2045-09-22  6.227580275  0.2312775828   8.3350772059
 2045-12-22  6.237580300  0.2265205237   8.4233037531
 2046-03-22  6.247580325  0.2218626962   8.5143103601
 2046-06-22  6.257580350  0.2171915310   8.5327177179
 2046-09-22  6.267580375  0.2125822333   8.6022650802
 2046-12-22  6.277580400  0.2080694109   8.6994436539
 2047-03-22  6.287580425  0.2036505642   8.7998177159
 2047-06-22  6.297580450  0.1992217010   8.8198389975
 2047-09-22  6.307580475  0.1948522626   8.8966233398
 2047-12-22  6.317580500  0.1905741112   9.0041707331
 2048-03-22  6.327580525  0.1863530470   9.0852509786
 2048-06-22  6.337580550  0.1821573565   9.1382234016
 2048-09-22  6.347580575  0.1780186991   9.2235665184
 2048-12-22  6.357580600  0.1739663071   9.3432459564
 2049-03-22  6.367580625  0.1699978972   9.4672386236
 2049-06-22  6.377580650  0.1660255525   9.4924219808
 2049-09-22  6.387580675  0.1621079130   9.5879396393
 2049-12-22  6.397580700  0.1582717032   9.7218865408
 2050-03-22  6.407580725  0.1545147442   9.8609074370
 2050-06-22  6.417580750  0.1507566212   9.8900761552
 2050-09-22  6.427580775  0.1470509343   9.9978351698
 2050-12-22  6.437580800  0.1434220137  10.1487631732
 2051-03-22  6.447580825  0.1398677823  10.3057206928
 2051-06-22  6.457580850  0.1363149900  10.3402548466
 2051-09-22  6.467580875  0.1328124241  10.4629135676
 2051-12-22  6.477580900  0.1293821309  10.6342881346
 2052-03-22  6.487580925  0.1260000891  10.7661292008
 2052-06-22  6.497580950  0.1226442940  10.8555824519
 2052-09-22  6.507580975  0.1193365717  10.9966529820
"""

# -------------------------------------------------------------------------
# Plot the timeseries of the interpolated SONIA Rates 
# and fit the observed rate - Visualization.
# -------------------------------------------------------------------------

plt.close('all')
fig, ax = plt.subplots(1)
ax.plot(Discount_df2['Maturities'],Discount_df2['Forward'],'r',lw=1.5, \
label='Forward Rates')
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.title('Observed/Forward/Discount SOFR SWAP Rates (%) [0-30 Years] \n \
Linear Interpolation\n \
Data Source: Assumed')
plt.plot(Discount_df['Maturities'],Discount_df['Rates'], 'g', lw=1.5, \
label='Observed/Interpolated Rates')
plt.plot(Discount_df2['Maturities'],Discount_df2['Discounts'], 'b', lw=1.5, \
label='Discount Rates')
plt.legend(loc=0)
plt.grid(True)

plt.ylabel('Rates (%)')
plt.xlabel('Maturities')
plt.show()

