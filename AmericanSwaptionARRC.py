"""
Author: Oluwaseyi Awoga
IDE: CS50 IDE on Cloud 9/AWS
Topic: ARRC Swaption - LIBOR-SOFR Transition - American Swaptions
Sources:
1. Martin Haugh - Term Structure Lattice Models, Financial Engineering Department, Columbia University (2016).
2. John Hull (2010). Options, Futures & Other Derivatives - Technical Note 23. Toronto, Canada.
3. Fisher Black, Emmanuel Derman & William Toy (1990). A One-Factor Model of Interest Rates
and Its Application to Treasury Bond Options. FA Journal, New York..
4. Gerald W. Buetow, Bernd Hanke & Frank Fabozzi (2002). Impact of Different Interest Rate Models
on Bond Measures, Institutional Investors Inc, New York.
5. Frank Fabozzi (2014). Bond Market Analysis & Strategies. Pearson, India.
6. Andrew Kalotay, George Williams & Frank Fabozzi (1993). A Model for Valuing Bonds and Em- bedded Options. FA Journal, NY.
7. Martin Haugh & Garud Iyenger (2014). Financial Engineering & Risk Management, Columbia University via Coursera. New York, NY.
8. Donald J. Smith (2015). Understanding CVA,DVA,FVA: Examples of Interest Rate Swap Valuation. SSRN, USA.

Location: Milky-Way Galaxy
"""

from __future__ import division
from scipy.optimize import fsolve
import math
import copy
import warnings
warnings.filterwarnings('ignore')


"""
Declare Variables
"""

"""
Period      LIBOR       SOFR        VOL
1           0.0730      0.0664      0.005
2           0.0762      0.0693      0.005
3           0.0810      0.0736      0.005
4           0.0845      0.0768      0.005
5           0.0920      0.0836      0.005
6           0.0964      0.0876      0.005
7           0.1012      0.0920      0.005
8           0.1045      0.0950      0.005
9           0.1075      0.0977      0.005
10          0.1122      0.1020      0.005

Source: LIBOR & VOLATILITY - Term Structure Lattice Models by Martin Haugh (2016)
        SOFR - Assumed
"""

LIBOR = [0.073, 0.0762, 0.081, 0.0845, 0.092, 0.0964, 0.1012, 0.1045, 0.1075, 0.1122]
SOFR = [0.0664, 0.0693, 0.0736, 0.0768, 0.0836, 0.0876, 0.092, 0.095, 0.0977, 0.102]  #Assumed
vol = [0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005]


fixedRate = 0.1165	        #First payment of underlying swap at t=3 (based on t=2 spot rate) and final payment at t=10
optionExpiration = 	2	    #This is fixed but could easily be made variable
swapMaturity = 10	        #Note that the values at a node are the discounted values of the nodes 1 period ahead.
                            #We therefore start from t=9 even though final payoff occurs at t=10
optionStrike = 0.0000	    #(Strike is commonly 0)
Principal	 = 1
q  = 0.5
q_ = 0.5

"""
Create Helper Functions
"""


def factor(time, freq=1):
    """
    Helper Function
    """
    factor =[[]]
    temp = []
    for x in range(time):
        if x == 0:
            factor[0].append(0)
        else:
            for y in range(0,x+1):

                if y == 0:
                    temp.append(0)
                else:
                    temp.append(y*freq)
                    x = x - freq
            factor.append(temp)
            temp = []
    multiplier = [list(reversed(x)) for x in factor][:]
    return multiplier

def print_lattice(lattice, info = []):
    """
    Lattice Printer.
    """
    print ("")
    levels = len(lattice[-1])
    start_date = len(lattice[0]) - 1
    dates = levels - start_date
    outlist = []
    col_widths = [0] * dates
    for j in range(levels):
        level = []
        for k in range(dates):
            try:
                point = "{:.5f}".format(lattice[k][levels - 1 - j])
                esc_width = 0
                if info != [] and info[k][levels - 1 - j] > 0:
                    point = (point, 'red')
                    esc_width += 9
                level.append(point)
                col_widths[k] = max(col_widths[k], len(point) - esc_width)
            except IndexError:
                level.append('')
        outlist.append(level)
    separator = "|-".join(['-' * w for w in col_widths])
    formats = [ ]
    for k in range(dates):
        formats.append("%%%ds" % col_widths[k])
    pattern = "  ".join(formats)
    print (pattern % tuple(str(start_date + time) for time in range(dates)))
    print (separator)
    for line in outlist:
        print (pattern % tuple(line))


def zeroCouponBondPrices(LIBOR,freq=1):
    """
    Helper Function to Calculate Zero Coupon Bond Prices
    Args:
        param1: (a) LIBOR or SOFR rates
    Returns:
        A list of Zero Coupon Bond Prices
    """
    result = []
    for x in range(0,len(LIBOR)):
        temp = 100.00/((1 + LIBOR[x])/freq)**((x+1)*freq)
        result.append(temp)
    return result

def zeroCouponBondLIBOR(LIBOR):
    """
    Helper Function to Calculate Zero Coupon Bond Prices - Used in Optimization Function
    Args:
        param1: (a) LIBOR or SOFR Rate
    Returns:
        A list of Zero Coupon Bond Prices based on LIBOR
    """
    result = []
    for x in range(0,len(LIBOR)):
        temp = 100.00/((1 + LIBOR[x])/1)**((x+1)*1)
        result.append(temp)
    return result

def zeroCouponBondSOFR(SOFR,spread):
    """
    Helper Function to Calculate Zero Coupon Bond Prices - Used in Optimization Function
    Args:
        param1: (a) SOFR and SOFR Spread
    Returns:
        A list of Zero Coupon Bond Prices based on SOFR and SOFR Spread
    """
    result = []
    for x in range(0,len(SOFR)):
        temp = 100.00/((1 + SOFR[x]+spread[x])/1)**((x+1)*1)
        result.append(temp)
    return result

def optimizationfunc(spread):
    """
    Helper Function Used to Generate the Spreads to apply to each individual SOFR Rates
    So that the Swaption Price Calculated Using SOFR + Spread matches the Swaption Price
    Calculated Using LIBOR
    Args:
        param1: (a) SOFR Spread
    Returns:
        A list of Spreads Per Period to appy to each SOFR Rate
    """

    pV2 = zeroCouponBondLIBOR(LIBOR)
    return [100.00/(1+SOFR[0]+spread[0])**1 - pV2[0] , \
    100.00/(1+SOFR[1]+spread[1])**2 - pV2[1] , \
    100.00/(1+SOFR[2]+spread[2])**3 - pV2[2] , \
    100.00/(1+SOFR[3]+spread[3])**4 - pV2[3] , \
    100.00/(1+SOFR[4]+spread[4])**5 - pV2[4] , \
    100.00/(1+SOFR[5]+spread[5])**6 - pV2[5] , \
    100.00/(1+SOFR[6]+spread[6])**7 - pV2[6] , \
    100.00/(1+SOFR[7]+spread[7])**8 - pV2[7] , \
    100.00/(1+SOFR[8]+spread[8])**9 - pV2[8] , \
    100.00/(1+SOFR[9]+spread[9])**10 - pV2[9]]


def bdtOne(guess):
    """
    Helper Function for Interest Rate Tree
    """
    ru = guess * math.exp(1 * vol[1])
    rd = guess
    N1 = (100.00)/(1+ru)
    N2 = (100.00)/(1+rd)
    return (0.5*((N1/(1+LIBOR[0])) + (N2/(1+LIBOR[0])))-pV[1])


def rateCalculator(m,node):
    """
    Helper Function for Interest Rate Tree
    """
    rate = []
    for x in range(0,node+1):
        if x == node:
            rate.append(m[0])
        else:
            rate.append(m[0] * math.exp(multiplier[node][x] * m[1]))
    return rate


def valueCalculator(m,node,final_rate_tracker):
    """
    Helper Function for Interest Rate Tree
    """
    nValue = []
    nValue2 = []
    rate = []
    final_rate_tracker = final_rate_tracker[:]
    final_rate_tracker.reverse()

    for x in range(node+1):
        if x == node:
            rate.append(float(m[0]))
        else:
            rate.append(m[0] * math.exp(multiplier[node][x]* m[1]))
    for x in range(len(rate)):
        nValue2.append(((100.00)/(1+rate[x])))
        nValue = copy.deepcopy(nValue2)

    nValue2 = []

    y = 0
    while len(nValue) > 2:

        if len(nValue) <= 2:
            break

        for x in range(len(nValue)-1):
            nValue2.append((0.5*((nValue[x]) + (nValue[x+1])))/(1 + final_rate_tracker[y][x]))
        if y == 0:
            yu = math.sqrt(100.00/nValue2[0]) - 1
            yd = math.sqrt(100.00/nValue2[1]) - 1
            if len(nValue) <= 2:
                break
        if len(nValue) <= 2:
            break
        rate=[]
        y = y + 1
        nValue = nValue2[:]
        nValue2 = []
    out = [ ( 0.5*((nValue[0]) + (nValue[1]))/(1+temp_rate_tracker[0][0]) - pV[node])]
    out.append((0.5 * math.log(yu/yd) - vol[node]))
    return out

def solutionIterator(mo,nNodes,final_rate_tracker,temp_rate_tracker):
    """
    Main Helper Function for Interest Rate Tree
    """
    for x in range(2,nNodes):
        data = (x,final_rate_tracker)
        mo.append(fsolve(valueCalculator,m,args=data,xtol=1.49012e-10,factor=1000))
        temp_rate_tracker.append(rateCalculator(mo[x],x))
        final_rate_tracker = temp_rate_tracker[1:]
        data = (x,final_rate_tracker)
    return temp_rate_tracker


def swaptionPrices(interestRateTree):
    """
    Function to generate Swaption Prices at Each Node
    Args:
        param1: (a) Interest Rate Tree - e.g. BDT
    Returns:
        A Swaption Pricing Tree
    """
    length = len(interestRateTree)
    final = [0] * length
    temp = []
    for x in range(length-1, -1,-1):
        if x == length-1:
            for y in range(len(interestRateTree[x])):
                temp.append((interestRateTree[x][y] - fixedRate)/(1+interestRateTree[x][y]))
            final[x] = temp
            temp = []
        elif x < length-1 and x != optionExpiration :
            for y in range(len(interestRateTree[x])):
                a = (interestRateTree[x][y] - fixedRate)/(1+interestRateTree[x][y])
                b = ((q * final[x+1][y] + q_ * final[x+1][y+1])/(1+interestRateTree[x][y]) )
                temp.append((a+b))
            final[x] = temp
            temp = []
        if x < length-1 and x == optionExpiration:
            for y in range(len(interestRateTree[x])):
                a = (interestRateTree[x][y] - fixedRate)/(1+interestRateTree[x][y])
                b = ((q * final[x+1][y] + q_ * final[x+1][y+1])/(1+interestRateTree[x][y]) )
                w = a+b
                ans = max(0.00,w)
                temp.append(ans)
            final[x] = temp
            temp = []
        elif x < length-1 and x < optionExpiration :
            for y in range(len(interestRateTree[x])):
                b = ((q * final[x+1][y] + q_ * final[x+1][y+1])/(1+interestRateTree[x][y]) )
                temp.append((b))
            final[x] = temp
            temp = []
    return final

"""
Main Function & Function Calls
"""

if __name__ == '__main__':

    def swaptionWithoutSpread(LIBOR=LIBOR,pRinter = False):
        """
        Main Function to Call all the Helper Functions and print the Trees and Swaption Prices
        """
        global pV
        pV = []
        global temp_rate_tracker
        global m, nNodes, multiplier, m_guess
        nNodes = len(LIBOR)
        m = [0.1,0.1]   #Guess list data structure for node 2 and above.
        multiplier = factor(nNodes)
        m_guess = 0.2  #Initial guess for the second node.
        spread =spread=[0.0] * len(LIBOR)
        pV = zeroCouponBondPrices(LIBOR)
        final_rate_tracker=[[]]
        temp_rate_tracker = [[LIBOR[0]]]
        g = fsolve(bdtOne,m_guess,xtol=1.49012e-10)[0]
        ru = g * math.exp(1 * vol[1])
        rd = g
        temp_rate_tracker.append([ru,rd])
        mo = [[LIBOR[0]],[rd,1]]
        final_rate_tracker = temp_rate_tracker[1:]
        final_rate_tracker = solutionIterator(mo,nNodes,final_rate_tracker,temp_rate_tracker)[:]
        reversed_lists = [list(reversed(x)) for x in final_rate_tracker]
        final_Rate = [[100.00 * y for y in x] for x in reversed_lists]
        if pRinter == True:
            print ("     ")
            print ("----------------------------------------------------------------------------------------------")
            print ("BLACK-DERMAN-TOY SHORT RATE MODEL INTEREST RATE TREE")
            print ("----------------------------------------------------------------------------------------------")
            print_lattice(final_Rate, info = [])
            print ("     ")
        else:
            pass
        interestRateTree =  reversed_lists[:]
        final = swaptionPrices(interestRateTree)
        if pRinter == True:
            print ("     ")
            print ("----------------------------------------------------------------------------------------")
            print ("SWAPTION PRICING TREE")
            print ("----------------------------------------------------------------------------------------")
            print_lattice(final, info = [])
            print ("     ")
        else:
            pass
        return final[0][0]

    sofrSpread= fsolve(optimizationfunc,  x0=[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01])

    """
    Spread Required on SOFR to Equate the Swaption Price calculated using LIBOR:

    0.0066
    0.0069
    0.0074
    0.0077
    0.0084
    0.0088
    0.0092
    0.0095
    0.0098
    0.0102
    """

    """
    Add the spreads calculated to the SOFR rates to get the spread adjusted rates
    """

    newSOFR = [sofrSpread[x] + SOFR[x] for x in range(len(SOFR))]
    """
    SOFR Plus Spreads:

    0.0730
    0.0762
    0.0810
    0.0845
    0.0920
    0.0964
    0.1012
    0.1045
    0.1075
    0.1122
    """
    print()
    print("The Interest Rate (BDT) and Swaption Tree Generated Using LIBOR is shown below")
    print()
    LIBORSwaptionPrice = swaptionWithoutSpread(LIBOR=LIBOR,pRinter = True)
    print()
    print("The LIBOR Based Price of the Swaption is: " + str(round(LIBORSwaptionPrice,10)))
    print()

    print()
    print("The Interest Rate (BDT) and Swaption Tree Generated Using SOFR is shown below")
    print()
    SOFRPlusSPreadPrice = swaptionWithoutSpread(LIBOR=SOFR,pRinter = True)
    print()
    print("The SOFR Based Price of the Swaption is: " + str(round(SOFRPlusSPreadPrice,10)))
    print()

    print()
    print("The Interest Rate (BDT) and Swaption Tree Generated Using SOFR Plus Spread Adjustments is shown below")
    print()
    SOFRPlusSPreadPrice = swaptionWithoutSpread(LIBOR=newSOFR,pRinter = True)
    print()
    print("The SOFR Plus Spread Based Price of the Swaption is: " + str(round(SOFRPlusSPreadPrice,10)))
    print()









