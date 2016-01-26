"""
Topic:  Multi-Curve Modeling Using Trees

Source: Multi-Curve Modeling Using Trees by John Hull & Alan White.

Background: Model the above as an extension of our previous work on the Hull-White
Model available - https://github.com/MaximumBeings/public/blob/master/HW_FirstStage.py

Inputs:

Percentage interest rates for the examples. The OIS Rates are expressed with continous compounding while all forward and forward spread rates
are expressed with annual compounding.  The OIS zero rates and LIBOR forward rates for maturities other than those given are determined using linear 
interpolation.  The rates in the final two columns are rounded values calculated from the given OIS zero rates and LIBOR forard rates.

Table 1:
Maturity(Years)         OIS Zero Rate       Forward_12_Month_LIBOR_Rate         Forward_12_Month_Rate       Forward Spread: 12_Month_LIBOR_less_12_Month_OIS
0                       3.000               3.300                               3.149                       0.151
0.5                     3.050               3.410                               3.252                       0.158
1.0                     3.100               3.520                               3.355                       0.165
1.5                     3.150               3.630                               3.458                       0.172
2.0                     3.200               3.740                               3.562                       0.178
2.5                     3.250               3.850                               3.666                       0.184
3.0                     3.300               3.960                               3.769                       0.191
4.0                     3.400               4.180                               3.977                       0.203
4.0                     3.500               4.400                               4.185                       0.215
7.0                     3.700


Table 2:
Reversion Rates, Volatilities, and Correlation for the Examples:
    
OIS reversion rate, ar :                0.22
OIS Volatility         :                0.25
Spread reversion rate, as:              0.10
Spread volatility, &s  :                0.20
Correlation between OISand spread, p:   0.05


Table 3:
Adjustments to probabilities to reflect correlation in a three-dimensional trinomial tree.
(e = p/36 where p is the correlation)

Probability         Change when p > 0               Change when p < 0
puu                 +5e                             +e
pum                 -4e                             +4e
pud                 -e                              -5e
pmu                 -4e                             +4e
pmm                 +8e                             -8e
pmd                 -4e                             +4e
pdu                 -e                              -5e
pdm                 -4e                             +4e
pdd                 +5e                             +e


See you next time!!!



        
"""
