"""
This is a translation of the pseudocode in Dan Stefanica's
book - A Primer for the Mathematics of Financial Engineering.
This is my first attempt at translating the Pseudocode to Python.
The program uses a helper function to calculate the root of a function.

"""

import math

#To calculate the root of the original function - this function can be changed to a new one.


def func_calculator(x):
    return math.pow(x,4) - 5.0 * math.pow(x,2) + 4.0 - 1.0 / (1 + math.pow(math.e,(math.pow(x,3))))

#To calculate the root of the first derivative of the function.

def func_prime_calculator(x):
    return 4 * math.pow(x,3) - 10 * x + (3 * math.pow(x,2) * math.pow(math.e,(math.pow(x,3))))/math.pow((1 + math.pow(math.e,(math.pow(x,3)))),2)
    

#This is the implementation of the Newton-Raphson method

def newton(x):  #xo is the initial guess  #Sample call newton(0.1)
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
    
    
    
    
