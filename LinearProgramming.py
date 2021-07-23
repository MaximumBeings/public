#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 08:30:31 2018

@author: oluwaseyiawoga
"""

"""
Import Libraries & Packages
"""

import pulp as pp

"""
    QUESTION - Problem 1:
        
    (a) A company is investing in two securities, x1 and x2.  The risk management division
        of the company indicated the following constraints to the investment strategy:

    (b) Short selling is not allowed.
    
    (c) The company must not buy more than 400 units of x1
    
    (d) The total volume must not exceed 800 for every unit of x1 and x2 invested
    
    (e) The total volume must not exceed 1,000 for every 2 units of x1 invested and 
        1 unit of x2 invested.
        
    (f) The total number of units is maximized considering that, for each 3 units of 
        x1 security, 2 units of x2 security must be bought.
        
    (g) The company requests the following from you:
        
        . Indicate the objective function.
        . Write the optimization problem.
        . Find x1 and x2 values that maximize the objective function 
          and explain the algorithm.
          
    (h) Use the pulp modeler for Python.
    
    SOLUTION:
        
        Objective Function:
            
            Maximize 3x1 + 2x2
            
        Subject to:
            
            Constraints:
                 
                x1 <= 400
                x1 + x2 <= 800
                2x1 + x2 <= 1000
                
            Non-Negativity Constraints:
                
                x1,x2 >= 0

"""


"""
Main Function
"""


if __name__ == '__main__':
    
    """
    Set up the Linear Variable Model
    """

    prob = pp.LpProblem("Securities", pp.LpMaximize)
    
    x1 = pp.LpVariable("stock1", 0, None, pp.LpInteger)
    
    x2 = pp.LpVariable("stock2", 0, None, pp.LpInteger)
    
    """
    The objective function is added to 'prob' first - "Maximization Objective".
    """
    
    
    prob += 3*x1 + 2*x2 
    
    """
    Add the constraints as specified in the Home Work
    """
    
    prob += x1 <= 400.00 
    prob += x1 + x2 <= 800.00
    prob += 2*x1 + x2 <= 1000.00
    
    """
    The problem data is written to an .lp file
    """
    
    prob.writeLP("securitiesModel.lp")
    
    
    """
    The problem is solved using PuLP's choice of Solver.
    """
    
    prob.solve()
    
    """
    The status of the solution is printed to the screen
    """
    print("")
    print("Status:", pp.LpStatus[prob.status])
    
    
    """
    Each of the variables is printed with it's resolved optimum value
    """
    
    for v in prob.variables():
        print(v.name, "=", v.varValue)
        
    """
    The optimised objective function value is printed to the screen
    """
    print("")
    print("Total Maximized Objective: ", pp.value(prob.objective))
    






