#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 18:06:28 2021

@author: oluwaseyiawoga
"""

"""
Import Libraries & Packages
"""
import pandas as pd
import datetime
import locale
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
locale.setlocale(locale.LC_ALL,'')

"""
SOFR Term Rates
https://www.cmegroup.com/market-data/cme-group-benchmark-administration/term-sofr.html#term

CME Clearing’s SOFR OIS Curve
https://www.cmegroup.com/trading/interest-rates/cleared-otc-sofr-swaps.html
"""


if __name__ == '__main__':

    """
    Set the start and end dates using datetime function
    """

    start = datetime.datetime(2021, 8, 4)
    end = datetime.datetime(2051, 8, 4)
    d = pd.date_range(start, end, freq='D')
     
                    
    observedData = {
                  datetime.datetime(2021,8, 4): 0.05,
                  datetime.datetime(2021,9, 5): 0.04812,
                  datetime.datetime(2021,11, 5): 0.04762,
                  datetime.datetime(2022,1, 5): 0.04714,
                  datetime.datetime(2022,8, 5): 0.0540,
                  datetime.datetime(2023,8, 5): 0.1592,
                  datetime.datetime(2024,8, 5): 0.3212,
                  datetime.datetime(2026,8, 5): 0.5957,
                  datetime.datetime(2031,8, 5): 1.0094,
                  datetime.datetime(2041,8, 5): 1.3038,
                  datetime.datetime(2051,8, 5): 1.3528
                }
    
    observedData = pd.DataFrame(observedData.items())
    observedData.index = observedData[0]
    observedData.index.name = 'Date'
    observedData = observedData[[1]]
    observedData.columns = ["Data"]
    
    
    
    d = pd.DataFrame(index=d)
    combinedData = pd.concat([d, observedData], axis=1, join='outer')
    #combinedData = combinedData.interpolate(method='spline', order=3)
    combinedData = combinedData.interpolate(method='linear')
    
    Description = ["SOFR", "SOFR Term", "SOFR Term", "SOFR Term", \
                   "SOFR OIS Curve",\
                   "SOFR OIS Curve",\
                   "SOFR OIS Curve",\
                   "SOFR OIS Curve",\
                   "SOFR OIS Curve",\
                   "SOFR OIS Curve",\
                   "SOFR OIS Curve"]
        
    observedData["Description"] = Description
    
    observedData = observedData[["Description", "Data"]]
    print("Observed Data")
    print(observedData)
    
    
    fixingDate = datetime.date(2021,8,5) 
    plt.close('all')
    fig, ax = plt.subplots(1)
    ax.plot(combinedData.index,combinedData['Data'],lw=1.5, label='Interpolated Rates')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.title('Observed & Interpolated SOFR, \n SOFR Term & SOFR OIS Curve \n for 30 years as of {:%d, %b %Y}'.format(fixingDate),fontweight="bold")
    plt.plot(observedData.index,observedData["Data"], 'bo', lw=0.5, label='Observed Rates')
    plt.legend(loc=0)
    plt.grid(True)
    
    plt.ylabel('SOFR Rates (%)')
    plt.xlabel('Maturities')
    plt.show()
        
    
    
