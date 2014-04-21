from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd
import pylab

"""
Discussion:  Recall the article on Interest Rate Swap Valuation available at http://tinyurl.com/mnan8ok,
we assumed that the Swap Fixed Rate was already interpolated. The aim of this post is 
to examine different interpolation techniques namely linear, cubic spline, zero, quadratic
and nearest using a simple example and explain how to fit a curve.  Subsequently, we will
apply the knowledge to interpolate the swap rate over a 30 year period. The gist is that
certain rates are available at commonly quoted intervals.  However, in order to value a security
or bootstrap the zero rate we need to interpolate between the available rates for periods for which 
there are no quoted rates.


SOURCE: 
(a) Boston University School of Management Research Paper Series (No.2012-­‐11)
Valuing Interest Rate Swaps Using OIS Discounting By Donald J. Smith
Electronic copy available at: http://ssrn.com/abstract=2036979

(b) Introduction to Computational Thinking and Data Science - John Guttag

Software: Canopy Free by Enthought
          scipy (Scientific Python) library (open source)


    
Consider the example from the above post:

Time         Description     Rate
3-month      LIBOR           0.50%
6-month      LIBOR           1.00%
9-month      LIBOR           1.60%
12-month     LIBOR           2.10%
24-month     SFR             3.40%

As you can see, rates are missing for the 15th, 18th, and 21st months and we need
those rates because cashflow payments are due on a quarterly basis which is every 3 months.
So we need to interpolate those rates.  Fortunately, there is an open source python library -
Scipy that can be used to perform different types of interpolation as enumerated above.
"""
#store available data for maturities and rates in list
x = [3, 6, 9,12,24]
y = [0.50/100,1/100.0,1.60/100,2.10/100,3.40/100]

#Use scipy 1 dimensional interpolation function to interpolate
f = interp1d(x,y, kind='linear')  #the kind can be changed to slinear, quadratic, zero, cubic, nearest

#interpolate with piecewise constant function (p=0) #kind='nearest'
#interpolate with piecewise linear function(p=1) #kind='linear'
#interpolate with piecewise constant function (p=2) - kind='quadratic'
#interpolate with cubic  = cubic spline


#Create a list for the missing dates 
xint = [15,18,21]

#Use the interpolation function we created above to find the rates for the missing dates
yint = f(xint)

#Expand our original rates to include both missing and available information
y = y + list(yint)
y.sort()

##Expand our original maturities to include both missing and available information
x = x + xint
x.sort()
    
#TO DISPLAY INTERPOLATED DATA
print ""
rateTable = pd.DataFrame.from_items([('Period', x),('Rate', y)])
print(rateTable.to_string())

"""
Result of Python Code:
#      Period     Rate (Interpolated)
0       3         0.00500
1       6         0.01000
2       9         0.01600
3      12         0.02100
4      15         0.02425
5      18         0.02750
6      21         0.03075
7      24         0.03400

Interpolated Rates from Source (Original article):
    
Time         Description   Rate
3-month      LIBOR         0.50%
6-month      LIBOR         1.00%
9-month      LIBOR         1.60%
12-month     LIBOR         2.10%
15-month     SFR           2.44%
18-month     SFR           2.76%
21-month     SFR           3.08%
24-month     SFR           3.40%
"""

##Fit the curve by plotting original information over the interpolated one.
##If you run the code and change kind on line 34 above from linear to cubic
##you will realize that only slinear and linear interpolation techniques
#fitted the original data very well.
##very well.

#Orignal Data to benchmark interpolated data - curve fitting
x = [3, 6, 9,12,24]
y = [0.50/100,1/100.0,1.60/100,2.10/100,3.40/100]
x.sort()
y.sort()

pylab.plot(x, y, 'b--')
pylab.plot(xint, yint, '--ro')
pylab.title('Linear Interpolation of Interest Rates') 
pylab.show()

"""
CONCLUSION: This technique will be used to discuss interpolation & curve fitting techniques for 
long dated securities (30 years) shortly.  Subsequently, we will use the techniques to bootstrap zero rates
and value securities - see you next time!!!
"""
