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
https://www.cmegroup.com/market-data/cme-group-benchmark-administration/term-sofr.html#term
"""


if __name__ == '__main__':

    """
    Set the start and end dates using datetime function
    """

    start = datetime.datetime(2021, 8, 3)
    end = datetime.datetime(2022, 1, 3)
    d = pd.date_range(start, end, freq='D')
     
                    
    observedData = {
                  datetime.datetime(2021,8, 3): 0.05,
                  datetime.datetime(2021,9, 3): 0.04847,
                  datetime.datetime(2021,11, 3): 0.04777,
                  datetime.datetime(2022,1, 3): 0.04785
                }
    
    observedData = pd.DataFrame(observedData.items())
    observedData.index = observedData[0]
    observedData.index.name = 'Date'
    observedData = observedData[[1]]
    observedData.columns = ["Data"]
    
    d = pd.DataFrame(index=d)
    combinedData = pd.concat([d, observedData], axis=1, join='outer')
    combinedData = combinedData.interpolate(method='linear')
    
    
    
    

    
    fixingDate = datetime.date(2021,8,3) 
    plt.close('all')
    fig, ax = plt.subplots(1)
    ax.plot(combinedData.index,combinedData['Data'],lw=1.5, label='Interpolated Rates')
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.title('Interpolated SOFR Term Rates as of {:%d, %b %Y}'.format(fixingDate),fontweight="bold")
    plt.plot(observedData.index,observedData["Data"], 'bo', lw=0.5, label='Observed Rates')
    plt.legend(loc=0)
    plt.grid(True)
    
    plt.ylabel('SOFR Term Rates (%)')
    plt.xlabel('Maturities')
    plt.show()
        
    
    
