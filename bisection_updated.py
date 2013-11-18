"""
This is a translation of the pseudocode in Dan Stefanica's
book - A Primer for the Mathematics of Financial Engineering.  
This is my second attempt at translating the Pseudocode to Python.
The program is an improved version of the earlier one because it
uses a helper function. It can be used to find the root of a function.

"""
import math

def func_calculator(x):
    return math.pow(x,4) - 5.0 * math.pow(x,2) + 4.0 - 1.0 / (1 + math.pow(math.e,(math.pow(x,3))))

def bisection(xo,x1):
    xm = (xo + x1)/2.0
    tol_int = 1e-06
    tol_app = 1e-09
    fxo = 0.0
    fx1 = 0.0
    fxm = 0.0
    fxo = func_calculator(xo)
    fx1 = func_calculator(x1)
    fxm = func_calculator(xm)
   
    while ((max(abs(fxo),abs(fx1)) > tol_app) or (x1 - xo) > tol_int):
        
        if fxm == 0:
            return xm
        elif fxo * fxm < 0:
            x1 = xm
        else:
            xo = xm
        xm = (xo + x1)/2
        fxo = func_calculator(xo)
        fx1 = func_calculator(x1)
        fxm = func_calculator(xm)
    return xm 
    
 