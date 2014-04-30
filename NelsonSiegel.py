"""
Topic: Nelson-Siegel Curve Smoothing Technique

Sources: Generating a Yield Curve with Nelson-Seigel Method in Excel -> https://www.youtube.com/watch?v=GsZRJmDcDbY
         Data fitting using fmin -> http://glowingpython.blogspot.it/2011/05/curve-fitting-using-fmin.html
         

Comment: Refer to the above video for an explanation of the method.  Also see https://github.com/MaximumBeings/public/blob/master/NSSandNS.txt
         for an MS Excel version of the NSS and NS method.  Though the code works very
         well, we noticed that the Excel version fitted our original data better because the solver in Excel is pretty powerful.  Nonetheless,
         this is a very good implementation of the NSS method.  We try to fit the curve by minimizing the sum of squared errors using the
         NS formula.  It is an iterative method that tries to guess the values for the NS parameters so you need to try different initial
         values.  Feed the program with a set of initial values and observe the curve plot and change the parameters to get better fits. A good
         starting set of initial values is array([0.01,0.01,0.01,1.00]) but can be changed to get a better fit.
"""



import pylab
from numpy import *
from scipy.optimize import fmin
import pandas as pd
print ""
# parametric function, x is the independent variable
# and c are the parameters.
# it's a polynomial of degree 2
fp = lambda c, x: c[0]+(c[1]+c[2])*(c[3]/x)*(1-exp(-x/c[3])-c[2]*exp(-x/c[3]))


# error function to minimize
e = lambda p, x, y: ((fp(p,x)-y)**2).sum()

# generating data with noise

x = array([1,2,3,5,7,10])  #The periods for which data are available, skip the periods with empty rate
y = array([2.05/100,1.98/100,2.23/100,2.80/100,3.24/100,3.77/100])  #Available rates only

# fitting the data with fmin
p0 = array([0.01,0.01,0.01,1.00])  # initial parameter value
p = fmin(e, p0, args=(x,y))
c = p
j=[]
for h in range(1,31,1):
    j.append(c[0]+(c[1]+c[2])*(c[3]/h)*(1-exp(-h/c[3])-c[2]*exp(-h/c[3])))


print ""
print 'Estimated Parameters: ', p
print ""
print 'Initial Parameters: ', p0


#To display interpolated data.
print ""
h = range(1,31,1)
rateTable = pd.DataFrame.from_items([('Period', h),('NS', j)])
print(rateTable.to_string())

"""
    Period        NS
0        1  0.020496
1        2  0.019812
2        3  0.022323
3        4  0.025178
4        5  0.027887
5        6  0.030338
6        7  0.032521
7        8  0.034451
8        9  0.036156
9       10  0.037662
10      11  0.038995
11      12  0.040178
12      13  0.041230
13      14  0.042170
14      15  0.043011
15      16  0.043767
16      17  0.044448
17      18  0.045065
18      19  0.045624
19      20  0.046133
20      21  0.046598
21      22  0.047024
22      23  0.047416
23      24  0.047776
24      25  0.048109
25      26  0.048418
26      27  0.048704
27      28  0.048970
28      29  0.049219
29      30  0.049451


"""

xx = array([1,2,5,10,25,30])
pylab.plot(x, y, 'ro')
pylab.plot(xx, fp(p,xx), 'b')
pylab.title('Nelson-Siegel')
pylab.show()

