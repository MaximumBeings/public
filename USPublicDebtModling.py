#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 15:02:31 2021

@author: oluwaseyiawoga
"""

import pandas as pd
import numpy as np
import requests
from IPython import get_ipython
import matplotlib
matplotlib.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas_datareader.data as web
import seaborn
seaborn.mpl.rcParams['figure.figsize'] = (12.0, 8.0)
np.warnings.filterwarnings('ignore')
import matplotlib
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
pd.options.display.float_format = '{:20,.3f}'.format
pd.set_option('display.max_columns', 500)
import quandl


#Fetch Data from US Treasury API
urlToUse = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?sort=-record_date&format=json&page[number]=1&page[size]=10000'
url = requests.get(urlToUse)
data = url.json()
data.keys()
#dict_keys(['data', 'meta', 'links'])
dataToUse = data['data']
debtDataDataFrame = pd.DataFrame(dataToUse)
debtDataDataFrame.keys()


#Preprocess the Downloaded JSON Data set and convert to Pandas DataFrame
"""
Index(['record_date', 'debt_held_public_amt', 'intragov_hold_amt', 'tot_pub_debt_out_amt', 'src_line_nbr', 'record_fiscal_year', 'record_fiscal_quarter', 'record_calendar_year', 'record_calendar_quarter', 'record_calendar_month', 'record_calendar_day'], dtype='object')
"""
debtDataDataFrame = debtDataDataFrame[["record_date", "tot_pub_debt_out_amt"]]
debtDataDataFrame.sort_values(by=['record_date'], ascending=True, inplace=True)
debtDataDataFrame["tot_pub_debt_out_amt"] = debtDataDataFrame["tot_pub_debt_out_amt"].astype(float)
debtDataDataFrame.set_index("record_date", inplace=True)
debtDataDataFrame[:].plot(figsize=(15,12),title='US Govt Public Debt',xlabel="Record Date",ylabel='Total Outstanding Debt')

debtDataDataFrame = debtDataDataFrame.interpolate(method='linear')
debtDataDataFrame['Period'] = debtDataDataFrame.index
debtDataDataFrame['Period'] = pd.to_datetime(debtDataDataFrame['Period'])
debtDataDataFrame.set_index("Period", inplace=True)
debtDataDataFrame.dropna(inplace=True)




#Resample to Annual
AnnualDebtData = debtDataDataFrame.resample("A").last()

dateToUse = AnnualDebtData.index.tolist()        

result = []       

for x in dateToUse:
    try:
        res = web.DataReader("^DJI", 'yahoo',x, x)["Adj Close"][0]
        result.append(res)
    except:
        result.append(None)

AnnualDebtData["Dow_Jones"] = result


result = []       

for x in dateToUse:
    try:
        res = web.DataReader("^GSPC", 'yahoo',x, x)["Adj Close"][0]
        result.append(res)
    except:
        result.append(None)

AnnualDebtData["SP"] = result


result = []       

for x in dateToUse:
    try:
        res = web.DataReader("^IXIC", 'yahoo',x, x)["Adj Close"][0]
        result.append(res)
    except:
        result.append(None)
        
        
AnnualDebtData["NASDAQ"] = result


#Fetch GDP Data from Quandl/Nasdaq Data

mydata = quandl.get("FRED/GDP")
mydata = mydata.resample("A").last()
mydata.columns = ["GDP"]
mydata['Period'] = mydata.index
mydata['Period'] = pd.to_datetime(mydata['Period'])
mydata.set_index("Period", inplace=True)

AnnualDebtData2 = AnnualDebtData.join(mydata)


#Interpolate for missing Data

AnnualDebtData2 = AnnualDebtData2.interpolate(method='linear')
AnnualDebtData2.dropna(inplace=True)


#Generate a plot of percentage change in US Debt and Market Indexes
AnnualDebtData2[:-1].pct_change()[:].plot(figsize=(15,12),title='US Govt Public Debt Versus GDP & Market Indexes (DOW, S&P & NASDAQ)\n Percentage Change\n 1993-2021 [Annual Data]\nSource:  US Treasury Data API',xlabel="Record Date",ylabel='Percentage Change (%)')


#Calculate the Cumulative Percentage Annual Changes
newFinal = pd.DataFrame()
totDebt = [0]
DowJones = [0]
SP = [0]
NASDAQ = [0]
GDP = [0]

for x in range(1, len(AnnualDebtData2)):
    totDebt.append((AnnualDebtData2["tot_pub_debt_out_amt"][x] - AnnualDebtData2["tot_pub_debt_out_amt"][0])/AnnualDebtData2["tot_pub_debt_out_amt"][0])
    DowJones.append((AnnualDebtData2["Dow_Jones"][x] - AnnualDebtData2["Dow_Jones"][0])/AnnualDebtData2["Dow_Jones"][0])
    SP.append((AnnualDebtData2["SP"][x] - AnnualDebtData2["SP"][0])/AnnualDebtData2["SP"][0])
    NASDAQ.append((AnnualDebtData2["NASDAQ"][x] - AnnualDebtData2["NASDAQ"][0])/AnnualDebtData2["NASDAQ"][0])
    GDP.append((AnnualDebtData2["GDP"][x] - AnnualDebtData2["GDP"][0])/AnnualDebtData2["GDP"][0])
    
newFinal["Debt"] = totDebt
newFinal["DowJones"] = DowJones
newFinal["SP"] = SP
newFinal["NASDAQ"] = NASDAQ
newFinal["GDP"] = GDP

#Generate a plot of percentage change in US Debt, GDP and Market Indexes
newFinal[:-1].plot(figsize=(15,12),title='US Govt Public Debt Versus GDP & Market Indexes (DOW, S&P & NASDAQ)\n Cumulative Percentage Change\n 1993-2021 [Annual Data]\nSource:  US Treasury Data API',xlabel="Record Date",ylabel='Cumulative Percentage Change (%)')

print(newFinal)

