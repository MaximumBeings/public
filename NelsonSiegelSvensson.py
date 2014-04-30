"""
Topic: Nelson-Siegel-Svensson Curve Smoothing Technique

Sources: Generating a Yield Curve with Nelson-Seigel-Svensson Method in Excel -> https://www.youtube.com/watch?v=uQnA9j_FvAg
         Data fitting using fmin -> http://glowingpython.blogspot.it/2011/05/curve-fitting-using-fmin.html
         

Comment: Refer to the above video for an explanation of the method.  Also see https://github.com/MaximumBeings/public/blob/master/NSSandNS.txt
         for an MS Excel version of the NSS and NS method. We will upload the code for the NS version shortly.  Though the code works very
         well, we noticed that the Excel version fitted our original data better because the solver in Excel is pretty powerful.  Nonetheless,
         this is a very good implementation of the NSS method.  We try to fit the curve by minimizing the sum of squared errors using the
         NSS formula.  It is an iterative method that tries to guess the values for the NSS parameters so you need to try different initial
         values.  Feed the program with a set of initial values and observe the curve plot and change the parameters to get better fits. A good
         starting set of initial values is array([0.01,0.01,0.01,0.01,0.01,1.00,1.00]) but can be changed to get better fit.
"""



import pylab
from numpy import *
from scipy.optimize import fmin
import pandas as pd
print ""
# parametric function, x is the independent variable
# and c are the parameters.
# it's a polynomial of degree 2
fp = lambda c, x: (c[0])+ (c[1]*((1- exp(-x/c[4]))/(x/c[4])))+ (c[2]*((((1-exp(-x/c[4]))/(x/c[4])))- (exp(-x/c[4]))))+ (c[3]*((((1-exp(-x/c[5]))/(x/c[5])))- (exp(-x/c[5]))))
real_p = array([0.02,0.01,0.01,0.01,1.00,1.00])

# error function to minimize
e = lambda p, x, y: ((fp(p,x)-y)**2).sum()

# generating data with noise

x = array([1,2,5,10,25])  #The periods for which data are available, skip the periods with empty rate
y = array([0.39/100,0.61/100,1.66/100,2.58/100,3.32/100])  #Available rates only

# fitting the data with fmin
p0 = array([0.01,0.01,0.01,0.01,0.01,1.00,1.00])  # initial parameter value
p = fmin(e, p0, args=(x,y))
c = p
j=[]
for h in range(1,31,1):
    j.append((c[0])+ (c[1]*((1- exp(-h/c[4]))/(h/c[4])))+ (c[2]*((((1-exp(-h/c[4]))/(h/c[4])))- (exp(-h/c[4]))))+ (c[3]*((((1-exp(-h/c[5]))/(h/c[5])))- (exp(-h/c[5])))))


print ""
print 'Estimated Parameters: ', p
print ""
print 'Initial Parameters: ', p0


#To display interpolated data.
print ""
h = range(1,31,1)
rateTable = pd.DataFrame.from_items([('Period', h),('NSS', j)])
print(rateTable.to_string())

"""
    Period       NSS
0        1  0.003884
1        2  0.006163
2        3  0.009368
3        4  0.013020
4        5  0.016380
5        6  0.019214
6        7  0.021526
7        8  0.023395
8        9  0.024912
9       10  0.026154
10      11  0.027183
11      12  0.028047
12      13  0.028780
13      14  0.029410
14      15  0.029957
15      16  0.030435
16      17  0.030857
17      18  0.031233
18      19  0.031568
19      20  0.031871
20      21  0.032144
21      22  0.032393
22      23  0.032620
23      24  0.032828
24      25  0.033019
25      26  0.033196
26      27  0.033360
27      28  0.033512
28      29  0.033653
29      30  0.033785

"""

xx = array([1,2,5,10,25,30])
pylab.plot(x, y, 'ro')
pylab.plot(xx, fp(p,xx), 'b')
pylab.title('Nelson-Siegel-Svensson')
pylab.show()

