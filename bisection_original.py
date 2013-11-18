"""
This is a translation of the pseudocode in Dan Stefanica's
book - A Primer for the Mathematics of Financial Engineering.  
This is my first attempt at translating the Pseudocode to Python.
The program can be improved by using a helper function to calculate
the value of the function which I will do in an updated version. It can 
be used to find the root of a function.

"""

import math

def bisection(xo,x1):
    xm = (xo + x1)/2.0
    tol_int = 1e-06
    tol_app = 1e-09
    fxo = 0.0
    fx1 = 0.0
    fxm = 0.0
    fxo = xo**4.0 - 5.0 * xo**2.0 + 4.0 - 1.0 / (1 + math.e**xo**3)
    fx1 = x1**4.0 - 5.0 * x1**2.0 + 4.0 - 1.0 / (1 + math.e**xo**3)
    fxm = xm**4.0 - 5.0 * xm**2.0 + 4.0 - 1.0 / (1 + math.e**xm**3)
   
    while ((max(abs(fxo),abs(fx1)) > tol_app) or (x1 - xo) > tol_int):
        if fxm == 0:
            return xm
        elif fxo * fxm < 0:
            x1 = xm
        else:
            xo = xm
        xm = (xo + x1)/2
        fxo = xo**4.0 - 5.0 * xo**2.0 + 4.0 - 1.0 / (1 + math.e**xo**3)
        fx1 = x1**4.0 - 5.0 * x1**2.0 + 4.0 - 1.0 / (1 + math.e**xo**3)
        fxm = xm**4.0 - 5.0 * xm**2.0 + 4.0 - 1.0 / (1 + math.e**xm**3)
    return xm 
    
 