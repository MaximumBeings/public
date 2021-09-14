#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 13:00:14 2021

@author: oluwaseyiawoga
"""

import pandas as pd
import numpy as np
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
import pandas as pd
import numpy as np
import matplotlib
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
pd.options.display.float_format = '{:20,.3f}'.format



date_cols = ["Period"]
mts = pd.read_csv("/Users/oluwaseyiawoga/Downloads/mts3.csv",parse_dates=date_cols)


Period = []
Receipts = []
Outlays = []
Deficit_Surplus = []
mtsSubset = mts[['Period', 'Receipts', 'Outlays', 'Deficit/Surplus (-)']]
mtsSubset.columns = ['Period', 'Receipts', 'Outlays', 'Net_Flow']
for x in range(len(mtsSubset['Receipts'])):
    try: 
        toUse =mtsSubset['Receipts'][x].replace('r','')
        toUse =toUse.replace(',','')
        Receipts.append(int(toUse))
    except:
        toUse =toUse.replace('r','')
        Receipts.append(int(toUse))


for x in range(len(mtsSubset['Outlays'])):
    try: 
        toUse =mtsSubset['Outlays'][x].replace('r','')
        toUse =toUse.replace(',','')
        Outlays.append(int(toUse))
    except:
        toUse =toUse.replace(',','')
        Outlays.append(int(toUse))


for x in range(len(mtsSubset['Net_Flow'])):
    try: 
        toUse =mtsSubset['Net_Flow'][x].replace('r','')
        toUse =toUse.replace(',','')
        Deficit_Surplus.append(int(toUse))
    except:
        toUse =toUse.replace(',','')
        Deficit_Surplus.append(int(toUse))

newFinal = pd.DataFrame()
newFinal['Period'] = mtsSubset['Period'].tolist()
newFinal['Receipts'] = Receipts
newFinal['Outlays'] = Outlays
newFinal['Net_Flow'] = Deficit_Surplus

print(newFinal)





newFinal2 = newFinal[:]

#newFinal2["Net_Flow"][-60:].plot()
newFinal2['Period'] = newFinal2['Period'].dt.date
newFinal2.set_index(newFinal2['Period'], inplace=True)

newFinal2["Net_Flow"][-60:].plot(figsize=(15,12),title='Monthly Treasury Statement (MTS)\n Net Surplus/Deficit $',xlabel="Date",ylabel="Amount")

#newFinal2[-60:].plot(figsize=(15,12),title='Monthly Treasury Statement (MTS)\n Net Surplus/Deficit %',xlabel="Date",ylabel="Amount")

import copy
newFinal3 = copy.deepcopy(newFinal2[-48:])
dateToUse = newFinal3.index.tolist()        

result = []       

for x in dateToUse:
    #print(x)
    
    try:
        res = web.DataReader("^DJI", 'yahoo',x, x)["Adj Close"][0]
        result.append(res)
    except:
        result.append(None)

newFinal3["Dow_Jones"] = result


result = []       

for x in dateToUse:
    #print(x)
    
    try:
        res = web.DataReader("^GSPC", 'yahoo',x, x)["Adj Close"][0]
        result.append(res)
    except:
        result.append(None)

newFinal3["SP"] = result




result = []       

for x in dateToUse:
    #print(x)
    
    try:
        res = web.DataReader("^IXIC", 'yahoo',x, x)["Adj Close"][0]
        result.append(res)
    except:
        result.append(None)

newFinal3["Nasdaq"] = result






newFinal4 = newFinal3[['Net_Flow', 'Dow_Jones', 'SP', 'Nasdaq']]

newFinal4 = newFinal4.interpolate(method='linear')
newFinal4.dropna(inplace=True)

netFinal5 = newFinal4[['Net_Flow', 'Dow_Jones']]



netFinal5['Dow_Jones'] = netFinal5['Dow_Jones'].shift(-1)
netFinal5 = netFinal5.dropna()
netFinal5[["Net_Flow","Dow_Jones"]].pct_change().plot(figsize=(15,12),title='Correlation Between Monthly Treasury Statement (MTS)\n Net Flow & Dow Jones Index',xlabel="Date",ylabel="Amount")
netFinal5.corr() 

netFinal6 = newFinal4[['Net_Flow', 'SP']]
netFinal6['SP'] = netFinal6['SP'].shift(-1)
netFinal6 = netFinal6.dropna()
netFinal6[["Net_Flow","SP"]].pct_change().plot(figsize=(15,12),title='Correlation Between Monthly Treasury Statement (MTS)\n Net Flow & Standard & Poor Index',xlabel="Date",ylabel="Amount")
netFinal6.corr() 




netFinal7 = newFinal4[['Net_Flow', 'Nasdaq']]
netFinal7['Nasdaq'] = netFinal7['Nasdaq'].shift(-1)
netFinal7 = netFinal7.dropna()
netFinal7[["Net_Flow","Nasdaq"]].pct_change().plot(figsize=(15,12),title='Correlation Between Monthly Treasury Statement (MTS)\n Net Flow & Nasdaq',xlabel="Date",ylabel="Amount")
netFinal7.corr() 












