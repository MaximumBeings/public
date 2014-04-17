"""
Topic: Using Secant for solving nonlinear problems. So far, we have discussed
the bisection and newton-raphson method for solving nonlinear problems.  However,
in order to use the newton method, we have to be able to calculate f'(x) (f prime).
However, in certain instances, it is not possible to calculate the f'(x), so we can
use the secant method to solve such problems.

Source: A Primer for the Mathematics of Financial Engineering - Dan Stefanica
        Introduction to Computational Thinking and Data Science - John Guttag

Software: Canopy Free by Enthought
          mpmath library (open source)

Discussion: So now we have discussed the three methods of solving numerical problems,
namely bisection, newton and secant there are more advanced ones but for our purpose 
these are mostly sufficient.  
"""

import mpmath
import math
mpmath.dps = 30; mpmath.pretty = True

def helper(x):
    return x**4 - 5*x**2 + 4 - 1.0/(1 + math.e**(x**3))
    
def secant(x0):
    xnew = x0
    xold = x0 - 1
    xoldest = 0.0
    tol_consec = 10**-6
    tol_approx = 10**-9
    while (helper(xnew) > tol_approx) or (abs(xnew - xold) >  tol_consec):
        xoldest = xold
        xold = xnew
        xnew = xold - (helper(xold) * (xold - xoldest)/(helper(xold) - helper(xoldest)))
    return xnew

##Sample call >>> secant(-3)  >>> -2.074304402865879

"""
According to John Guttag in his edx python class, in order to have reasonable assurance in our model,
we must have confidence in three things namely:
    
    (a) Conceptual model - We must have an assurance that our underlying theory is reasonable/sound.
    (b) Implementation - We must be confident that the model was properly implemented using our tool of choice.
    (c) And that we have tested the model with sufficient samples to be confident that the model will work for different
    scenarios.

This is a rather simplistic model but lets just pretend it is complex and of significance to our business, one way to develop
a greater assurance in the model is to test against other implementations, hence we used to the mpmath library to solve the same
function and obtained similar results.  Also, python has a unit testing functionality that we can use to ensure that the result is 
within a certain boundary.  For instance, if we pass an initial guess of -1 to our secant method like so secant(-1) we get 0.9507482560164136
which is different from the result above, so we can use unit test to test that the result generated gives us zero when we sub into the original
funtion.  We are not going to do that but just be aware that you can do so.  We will be using these techniques to solve real problems in the
future....everything we discuss are not end in themselves but rather means to solving business problems.  

"""

###Alternative secant method using the mpmath open source library
def f(x):
    return x**4 - 5*x**2 + 4 - 1.0/(1 + math.e**(x**3))

###Sample call >>> print mpmath.findroot(f,-3, solver='secant')  >>>-2.07430440286585

"""
Future Discussions:  So everybody is talking about analytics and big data and how it is going to change the world.
Well yes, analytics is great but great for certain types of problems and not for others. So in the near future, we will be chiming in into the
discussion and will be discussing the strengths and limitations of analytics.  It is used heavily in medicine, aviation, accounting, risk, algorithmic trading
finance, statistics and in all walks of life and not just in certain fields and not quite a new phenomenon.  
"""

    
