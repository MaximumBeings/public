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

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import datetime


#Fetch Data from US Treasury API
urlToUse = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?sort=-record_date&format=json&page[number]=1&page[size]=10000'
url = requests.get(urlToUse)
data = url.json()
data.keys()
#dict_keys(['data', 'meta', 'links'])
dataToUse = data['data']
ratesDataDataFrame = pd.DataFrame(dataToUse)
ratesDataDataFrame.keys()


desc = ratesDataDataFrame['security_desc']
rates = ratesDataDataFrame['avg_interest_rate_amt']





#descriptions = list(set(ratesDataDataFrame['security_desc'].tolist()))



ratesSubset  = ratesDataDataFrame[['record_date','avg_interest_rate_amt','security_desc']]


GovernmentAccountSerieInflationSecurities = ratesSubset[ratesSubset['security_desc'].isin(['Government Account Series Inflation Securities'])]
GovernmentAccountSerieInflationSecurities
GovernmentAccountSerieInflationSecurities['record_date'] = pd.to_datetime(GovernmentAccountSerieInflationSecurities['record_date'])
GovernmentAccountSerieInflationSecurities.set_index("record_date", inplace=True)






UnitedStatesSavingsInflationSecurities = ratesSubset[ratesSubset['security_desc'].isin(['United States Savings Inflation Securities'])]
UnitedStatesSavingsInflationSecurities
UnitedStatesSavingsInflationSecurities['record_date'] = pd.to_datetime(UnitedStatesSavingsInflationSecurities['record_date'])
UnitedStatesSavingsInflationSecurities.set_index("record_date", inplace=True)







TreasuryInflationProtectedSecurities = ratesSubset[ratesSubset['security_desc'].isin(['Treasury Inflation-Protected Securities (TIPS)', 'Treasury Inflation-Protected Securities(TIPS)', 'Treasury Inflation Protected Securities (TIPS)'])]
TreasuryInflationProtectedSecurities
TreasuryInflationProtectedSecurities['record_date'] = pd.to_datetime(TreasuryInflationProtectedSecurities['record_date'])
TreasuryInflationProtectedSecurities.set_index("record_date", inplace=True)


TreasuryInflationIndexedBonds = ratesSubset[ratesSubset['security_desc'].isin(['Treasury Inflation-Indexed Bonds'])]
TreasuryInflationIndexedBonds
TreasuryInflationIndexedBonds['record_date'] = pd.to_datetime(TreasuryInflationIndexedBonds['record_date'])
TreasuryInflationIndexedBonds.set_index("record_date", inplace=True)



#Combined the tables


GovernmentAccountSerieInflationSecurities = GovernmentAccountSerieInflationSecurities[["avg_interest_rate_amt"]]
GovernmentAccountSerieInflationSecurities['avg_interest_rate_amt'] = GovernmentAccountSerieInflationSecurities['avg_interest_rate_amt'].astype(float)

GovernmentAccountSerieInflationSecurities.columns = ["GovernmentAccountSerieInflationSecurities"]

UnitedStatesSavingsInflationSecurities = UnitedStatesSavingsInflationSecurities[["avg_interest_rate_amt"]]
UnitedStatesSavingsInflationSecurities['avg_interest_rate_amt'] = UnitedStatesSavingsInflationSecurities['avg_interest_rate_amt'].astype(float)
UnitedStatesSavingsInflationSecurities.columns = ["UnitedStatesSavingsInflationSecurities"]

TreasuryInflationProtectedSecurities = TreasuryInflationProtectedSecurities[["avg_interest_rate_amt"]]
TreasuryInflationProtectedSecurities['avg_interest_rate_amt'] = TreasuryInflationProtectedSecurities['avg_interest_rate_amt'].astype(float)
TreasuryInflationProtectedSecurities.columns = ["TreasuryInflationProtectedSecurities"]

finalDataFrame = UnitedStatesSavingsInflationSecurities.join(TreasuryInflationProtectedSecurities)

finalDataFrame = finalDataFrame.join(GovernmentAccountSerieInflationSecurities)


finalDataFrame.dropna(inplace=True)
finalDataFrame.sort_index(inplace=True)

print(finalDataFrame)


start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2021, 12, 31)


CPIAllItems = web.DataReader('CPALTT01USM657N', 'fred', start, end)
CPIAllItems = CPIAllItems.resample("M").last()
CPIAllItems.columns = ['Inflation']




finalDataFrame = finalDataFrame.join(CPIAllItems)



newFinal = finalDataFrame[["UnitedStatesSavingsInflationSecurities","Inflation"]]
newFinal = finalDataFrame[:]
newFinal[:].plot(figsize=(15,12),title='United States Treasury Inflation Linked Securities Versus \n Consumer Price Index: Total All Items for the United States \nMonthly Rates\nCumulative ',xlabel="Record Date",ylabel='Change in Rates')

newFinal.corr()

