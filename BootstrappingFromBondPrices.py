"""
Topic: Boostrapping Spot Rates from Bond Prices Algebraically - A simple Example.

Source: Extraction of Nelson-Siegel Factors from Bond Prices by Bc. Robert Berec (google it).

Discussion: Just a simple example of how to bootstrap zero rates from bond prices
algebraically.  See pages 7-8 in the above article for more background information.
We are just building different modules that we will use later for more expansive problems.
Later we will examine more difficult problems and use some of the libraries we have built so
far.  See you next time.

In the near future we will examine Vasicek model, Cox-Ingersoll-Ross and Diebold-Li. We will also
examine tree based interest rate models such as Hull-White, Black-Karanski, Black-Derman-Toy etc and
use python to solve some examples.  This is just to help us build some intuition and for pedagogical reasons,
most companies have their own systems and you should always use those to value your securities as they are more
defensible.  However, in some esoteric cases you may have to build your own models internally.


BOND DATA:
Bond        Time to Maturity(years)     Coupon      Price
1           1                           0%          $90.7
2           2                           3%          $97.4
3           3                           5%          $99.6

"""

import math
bonds = [[1,0,90.7],[2,3,97.4],[3,5,99.6]]
r = []
for x in range(len(bonds)):
    if bonds[x][1] == 0:
        r_ = -1 * (math.log(bonds[x][2]/100.00))/1.0
        r.append(r_)
    ans=0.0
    if bonds[x][1] > 0:
        numyears = bonds[x][0]
        
        
        for y in range(1,numyears):
            ans = ans + bonds[x][1]*math.exp(-1*r[y-1]*y)
        r_=0.0
        r_ =r_ +  -1*(math.log((bonds[x][2] - ans)/(100+bonds[x][1]))/(bonds[x][0]))
        r.append(r_)

print r
#result >>> [0.09761282886700041, 0.04211838276616048, 0.04965128359284274]

        
"""
Result: 

Bond        Time to Maturity(years)     Spot Rates      
1           1                           9.76%          
2           2                           4.21%          
3           3                           4.97%          

"""
