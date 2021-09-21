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
urlToUse = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?sort=-record_date&format=json&page[number]=1&page[size]=10000'
url = requests.get(urlToUse)
data = url.json()
data.keys()
#dict_keys(['data', 'meta', 'links'])
dataToUse = data['data']
ratesDataDataFrame = pd.DataFrame(dataToUse)
ratesDataDataFrame.keys()

ratesSubset  = ratesDataDataFrame[['record_date','avg_interest_rate_amt','security_desc']]
treasuryBonds = ratesSubset.loc[ratesSubset['security_desc'] == 'Treasury Bonds']
treasuryBonds
treasuryBonds['record_date'] = pd.to_datetime(treasuryBonds['record_date'])
treasuryBonds.set_index("record_date", inplace=True)



import datetime
start = datetime.datetime(2001, 1, 1)
end = datetime.datetime(2021, 12, 31)


caseSchiler = web.DataReader('CSUSHPINSA', 'fred', start, end)
caseSchiler = caseSchiler.resample("A").last()

#finalDataFrame = pd.concat([treasuryBonds, caseSchiler], axis=1, sort=False, join='inner')
finalDataFrame = treasuryBonds.join(caseSchiler)
finalDataFrame = finalDataFrame[["avg_interest_rate_amt","CSUSHPINSA"]]
finalDataFrame["avg_interest_rate_amt"] = finalDataFrame["avg_interest_rate_amt"].astype(float)
finalDataFrame.sort_index(inplace=True)
finalDataFrame.dropna(inplace=True)

finalDataFrame[:].pct_change().plot(figsize=(15,12),title='Treasury Bond Rates Versus \n Case Schiller House Price Index - National',xlabel="Record Date",ylabel='Annual Percentage Change (%)')


#Calculate the Cumulative Percentage Annual Changes
newFinal = pd.DataFrame(index=finalDataFrame.index)
totRate = [0]
totCaseSchiller = [0]

for x in range(1, len(finalDataFrame)):
    totRate.append((finalDataFrame["avg_interest_rate_amt"][x] - finalDataFrame["avg_interest_rate_amt"][0])/finalDataFrame["avg_interest_rate_amt"][0])
    totCaseSchiller.append((finalDataFrame["CSUSHPINSA"][x] - finalDataFrame["CSUSHPINSA"][0])/finalDataFrame["CSUSHPINSA"][0])

    
newFinal["TreasuryBondRates"] = totRate
newFinal["CaseSchiller"] = totCaseSchiller


#Generate a plot of percentage change in US Debt, GDP and Market Indexes
newFinal[:].plot(figsize=(15,12),title='Treasury Bond Rates Versus \n Case Schiller House Price Index - National\nMonthly Rates\nCumulative Percentage Changes',xlabel="Record Date",ylabel='Cumulative Percentage Change (%)')

print(newFinal)

