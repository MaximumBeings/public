"""
This is a translation of the pseudocode in Dan Stefanica's
book - A Primer for the Mathematics of Financial Engineering.

This module uses the sympy python library to calculate the 
first derivative of an expression instead of doing it manually
or manually via wolfram alpha.  Recall that we built a zero curve
generator for a bond portfolio using calculus as documented in the above book.
But we calculated the derivatives of our expressions manually. In 
order to make the code we built more dynamic
and extend it to generate the curve for the longer ends of the yield
curve (say 30 years) we need to find a way to calculate the derivatives
within python or programmatically.  

The sympy library is a full feature Computer Algebra System (CAS) that allows
us to do just that.  This module is therefore an illustration to show how to use
sympy to calculate derivatives and it is used in combination with the newton method
to find the root of a function. In the near future, we will re-write our bond
zero curve generator using sympy and further extend the code to generate the curves 
for 10 years, 15 years and 30 years.  Of course, we don't have to use calculus
as documented in the book because there are algebraic formulae for bootstrapping
the zero-curve but our plan is to survey different methods of bootstrapping without
necessarily emphasizing whether one method is better than the other.

See you next time!!!

"""

import math
from sympy import *

#*******************************************************************************
#Suppose we want to find the root of the expression below:
# x**4 - 5.0 * x**2 + 4.0 - 1.0 / (1 + math.e**x**3) we will approach it like so.
# set x as a symbol
#pass the expression into a variable called "expression"
#Example
#>>> x = symbols('x')
#>>> expression = x**4 - 5.0 * x**2 + 4.0 - 1.0 / (1 + math.e**x**3)
#To resolve expression at the point x = 2 we do as follows:
#>>> expression.subs(x,2)
#>>> -0.000335350130466478
#To find the derivative of the variable "expression" we do as follows:
#>>> j = diff(expression,x)  #differentiate expression with respect to x
#>>> print j
#>>> 3.0*2.71828182845905**(x**3)*x**2/(2.71828182845905**(x**3) + 1)**2 + 4*x**3 - 10.0*x
#>>> j.subs(x,2)
#>>> 12.0040228520491
#Using the above illustration we can now combine with our newton-ralphson
#method to find the root of a function.  The function passed to the variable
#"expression" can be changed to any function.

#*********************************************************************

x = symbols('x')
expression = x**4 - 5.0 * x**2 + 4.0 - 1.0 / (1 + math.e**x**3)

#To calculate the root of the original function - this function can be changed to a new one.


def func_calculator(x0):
    return expression.subs(x,x0)

#To calculate the root of the first derivative of the function.

def func_prime_calculator(x0):
    j = diff(expression,x)
    return j.subs(x,x0)

#This is the implementation of the Newton-Raphson method

def newton(x): #xo is the initial guess #Sample call newton(0.1) >>> 2.00002793524508

    epsilon = 10e-9
    maxIterationCount = 1000000
    x0 = x
    x1 = 0.0
    i = 0
    try:
        while (i < maxIterationCount):
            fValue = func_calculator(x0)
            fDerivative = func_prime_calculator(x0)

            x1 = x0 - fValue/fDerivative
            if abs(x1 - x0) <= epsilon:
                return x1
            x0 = x1
            ++i
    except (OverflowError,RuntimeError, TypeError, NameError):
        print""
        print "No Solution Was Found!!!."
