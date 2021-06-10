#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:00:09 2017

@author: oluwaseyiawoga
"""

import datetime
import pylab
import pandas as pd
pd.set_option('display.precision', 10)
import matplotlib
matplotlib.style.use('ggplot')
import pandas_datareader.data as web
import statsmodels.api as sm
import warnings
warnings.simplefilter('ignore')
import seaborn
seaborn.mpl.rcParams['figure.figsize'] = (10.0, 6.0)
seaborn.mpl.rcParams['savefig.dpi'] = 90


"""
QUESTION - Equilibrium Foreign Exchange in Python:
    . Explain how macroeconomic factors influence FX evolution
    . Calculate the equilibrium foreign exchange using cointegration
      (use one macroeconomic factor in the analysis)
    . Calculate the equilibrium foreign exchange using cointegration
      (use two or more macroeconomic factors in the analysis)
    . Discuss your final results
    . FXRATENGA618NUPN - Exchange Rate to U.S. Dollar for Nigeria
    . DDOI11NGA156NWDB - Remittance Inflows to GDP for Nigeria
    . PLXCPPNGA670NRUG - Price Level of Exports for Nigeria
    . PLMCPPNGA670NRUG - Price Level of Imports for Nigeria
    . RGDPNANGA666NRUG - Real GDP at Constant National Prices for Nigeria
    . DCOILWTICO - Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma
    
    
Discussion
Many macroeconomic variables affect the FX of country. For instance, in an oil 
exporting country or an economy that is dependent on the exportation of agricultural 
produce or cash crops, the prices of these commodities influence the balance in the 
foreign reserves of the countries in question and by extension the foreign exchange 
rate. During periods of rising prices, the FX of commodities exporting countries, 
stabilizes and even appreciates but during periods of falling prices, FX rate 
depreciates because usually foreign reserve balances are depleted and this sends 
a negative feedback loop to the market. Other factors that influences FX includes 
remittances, economic growth, interest rate, national debt and foreign direct investments.
In this study we used both single and multiple variable regression anaylsis to model 
the equilibrium FX of Nigeria. As shown in the screenshots above, for the single variable 
regression, the FX equilibrium is defined by the equation below:
    
Equilibrium FX = -2.7148 + 1.7832 * Oil Price For the Multiple regression the Equilibrium FX is model as follows:
    
Equilibrium FX = 72.1979 - 0.5772 * Remittances - 72.8220 * Exports - 244.7055 * Import + 0.0005 * Real GDP - 0.8167 * Oil Price

As mentioned earlier, this analysis is significantly limited by the quality of the data used. 
Also, the analysis could have been implemented using VAR, VECM etc.

References
1. WQU Econometric Class Notes and Materials. 2. Youtube Videos .
3. Investopedia

"""


"""
All the Above Functions are Called From Below
"""


if __name__ == '__main__':

    """
    Set the start and end dates using datetime function
    """
    start = datetime.datetime(1970, 1, 1)
    end = datetime.datetime.today()

    """
    Download House Price Index from FRED
    """

    data = web.DataReader(["FXRATENGA618NUPN",
                           "DDOI11NGA156NWDB",
                           "PLXCPPNGA670NRUG",
                           "PLMCPPNGA670NRUG",
                           "RGDPNANGA666NRUG",
                           "POILWTIUSDM"],
                          "fred",
                          start,
                          end)
    data.dropna(how='any', axis=0, inplace=True)
    data.columns = [
        'Exchange Rate',
        'Remittances',
        'Exports',
        'Imports',
        'Real GDP',
        'Oil Price']
    
    data.head()
    
    data["Imports"] = -1 * data["Imports"]

    #logData = np.log(data)

    """
    Implement a single variable regression
    Dependent Variable = data['Exchange Rate']
    Independent Variable = data['Oil Price']
    """

    y1 = data['Exchange Rate']
    x1 = data['Oil Price']

    x1 = sm.add_constant(x1)

    model = sm.OLS(y1, x1,)

    results = model.fit()

    equilibrium_fx = results.fittedvalues

    print("")

    print(equilibrium_fx)

    print("")

    print(results.summary())

    """
    Plot FX & Equilibrium FX
    """
    pylab.plot(equilibrium_fx, label="Equilibrium Exchange Rates")
    pylab.plot(y1)
    pylab.title("Single Variable Regression \n FX & Equilibrium FX")
    pylab.legend(loc='best')
    pylab.xlabel("Date")
    pylab.ylabel("Prices")
    pylab.show()

    """
    Implement a Multiple variable regression
    """

    y1 = data['Exchange Rate']
    X = data[['Remittances', 'Exports', 'Imports', 'Real GDP', 'Oil Price']]
    X = sm.add_constant(X)
    model = sm.OLS(y1, X,)

    results = model.fit()

    equilibrium_fx = results.fittedvalues

    print("")

    print(equilibrium_fx)

    print("")

    print(results.summary())

    """
    Plot FX & Equilibrium FX
    """
    pylab.plot(equilibrium_fx, label="Equilibrium Exchange Rates")
    pylab.plot(y1)
    pylab.title("Multiple Regression \n FX & Equilibrium FX")
    pylab.legend(loc='best')
    pylab.xlabel("Date")
    pylab.ylabel("Prices")
    pylab.show()
