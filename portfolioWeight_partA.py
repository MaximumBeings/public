#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 08:30:31 2018

@author: oluwaseyiawoga
"""

"""
Import Libraries & Packages
"""

import scipy

"""
    QUESTION - Problem 1:
        
    (a) A company is investing in two securities, x1 and x2.  
        Fictitious Portfolio - (Source: Investopedia):
        Stock A is worth $50,000 and has a standard deviation of 20%. 
        Stock B is worth $100,000 and has a standard deviation of 10%. 
        The correlation between the two stocks is 0.85. 
    
        The capital market division
        of the company indicated the following constraints to the investment strategy:

    (b) Short selling is not allowed. Specifically, the portfolio must consist of at least
        10% of either stock A or B.
    
    (c) The company wants to minimize the portfolio standard deviation
        
    (d) The company requests the following from you:
        
        . Indicate the objective function.
        . Write the optimization problem.
        . Find w1 and w2 values that minimizes the objective function 
          and explain the algorithm.
          
    (e) Use the pulp modeler for Python.
    
    (f) Using optimization techniques calculate the weight that minimizes portfolio variance 
    
    SOLUTION:
        
    Objective Function:
        
        Maximize w1**2 * 0.2**2 + w2**2 * 0.1**2 + 2 * w1 * w2 * 0.85 * 0.2 * 0.1
        
    Subject to:
        
        Constraints:
             
        w1 + w2 == 1
            
        Non-Negativity Constraints:
            
            w1,w2 >= 0
            w1 >= 0.1
            w2 >= 0.1

"""


"""
Main Function
"""



if __name__ == '__main__':
    
    def con(w):
        return w[0] + w[1] - 1
    
    def portfolioVariance(x):
        return x[0]**2 * 0.2**2 + x[1]**2 * 0.1**2 + 2 * x[0] * x[1] * 0.85 * 0.2 * 0.1
    
    def optimizer(x):
        """
        Function optimize for the best buy and sell percentage.
            param1: An array of buy and sell percentages Guess
            e.g. [0.2,0.1]
        Returns:
            An optimal array of buy and sell percentages
        """
    
        return 1 * (portfolioVariance(x))
    
    cons = {'type':'eq', 'fun': con}
    guess = [0.2, 0.1]
    
    optimizedResult = scipy.optimize.minimize(optimizer, guess,constraints=cons,bounds=[(0.1,1),(0.1,1)])
    print("")
    print(optimizedResult)
