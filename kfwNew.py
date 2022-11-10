from __future__ import division
from math import exp, sqrt



from scipy.optimize import fsolve
import math
import sys
import copy
import colored
from colored import stylize

def factor(time):
    factor =[[]]
    temp = []
    for x in range(time):
        if x == 0:
            factor[0].append(0)
            print(factor)
        else:
            for y in range(0,x+1):
                
                if y == 0:
                    temp.append(1)
                else:
                    temp.append(y * 2)
                    x = x - 2
            #temp.reverse()
            factor.append(temp)
            temp = []
    return factor
    
multiplier = factor(3)   

multiplier = [list(reversed(x)) for x in multiplier][:]


def print_lattice2(lattice, info = []):
    """
    Helper function to print lattice in a nice way.
    Source of Lattice Printer -> Financial Engineering & Risk Management - Columbia University via Coursera
    """
    print("")
    levels = len(lattice[-1])
    start_date = len(lattice[0]) - 1
    dates = levels - start_date # (end_date + 1) == levels
    outlist = []
    col_widths = [0] * dates
    # Group level by level
    for j in range(levels):
        level = []
        for k in range(dates):
            try:
                point = "{:.16f}".format(lattice[k][levels - 1 - j])
                esc_width = 0 # Take care of the color escape sequence
                if info != [] and info[k][levels - 1 - j] > 0:
                    point = colored.fg(point, 'red')
                    esc_width += 9 # len(colored('', 'red')) == 9
                level.append(point)
                col_widths[k] = max(col_widths[k], len(point) - esc_width)
            except IndexError:
                level.append('')
        outlist.append(level)

    # Prepare separator
    separator = "|-".join(['-' * w for w in col_widths])
    # Prepare format
    formats = [ ]
    for k in range(dates):
        formats.append("%%%ds" % col_widths[k])
    pattern = "  ".join(formats)
    print(pattern % tuple(str(start_date + time) for time in range(dates)))
    print(separator)
    for line in outlist:
        print(pattern % tuple(line))


m = 0.02  #Initial Guess

a2 = 100/(1+0.04991*0.25)**2
a3 = 100/(1+0.05030*0.25)**3
a4 = 100/(1+0.05126*0.25)**4
a5 = 100/(1+0.05166*0.25)**5
a6 = 100/(1+0.05207*0.25)**6

pV = [100,100,100]

mo = [0.035]

rate2 = [[0.035]]

vol = 0.1

c = [3.5,4.0,4.5]

m = 0.02

def rateCalculator2(m,node):
    ratte = []
    #print counter_m
    for x in range(0,node+1):
        if x == node:
            ratte.append(m)
            print(ratte)
        else:
            ratte.append(m * math.exp(multiplier[node][x] * vol))

    return ratte

rateCalculator2(0.0407360494424552,1)
#
#rate3 = [[]]
 
def valueCalculator2(m,node,rate3):
    nValue = []
    nValue2 = []
    #delta = 0.25
    rate = []

    for x in range(node+1):
        if x == node:
            rate.append(m)
        else:
            rate.append(m * math.exp(multiplier[node][x]* vol))
        #print rate
    for x in range(len(rate)):
        nValue2.append(((100+c[node])/(1+rate[x])))
        nValue = copy.deepcopy(nValue2)
        ratedFinal = nValue


    rate4 = rate3[:]

    rate4.reverse()

    ratedFinal2 =[]
    y = 0
    while len(ratedFinal) > 2:

        if len(ratedFinal) <= 2:
            break
        for x in range(len(ratedFinal)-1):
            #print ratedFinal
            ratedFinal2.append(((0.5*(ratedFinal[x]+c[node]) + 0.5*(ratedFinal[x+1]+c[node])))/(1 + rate4[y][x]))
            if len(ratedFinal) <= 2:
                break
            #print y,x
        if len(ratedFinal) <= 2:
            break
        #print ratedFinal
        rate=[]
        y = y + 1
        #ratedFinal = []
        ratedFinal = ratedFinal2[:]
        ratedFinal2 = []
        print(ratedFinal)
    return ( 0.5*((ratedFinal[0]+c[node]) + (ratedFinal[1]+c[node]))/(1+rate2[0][0]) - pV[node])



rate3=[[]]
nNodes = 3
rate2 = [[0.035]]
mo = [0.035]

#def solution2(m,args=data):
#    return mo.append(fsolve(valueCalculator2,m,args=data)[0])
    


def solutionIterator(mo,nNodes,rate3,rate2):
    for x in range(1,nNodes):
        data = (x,rate3)
        mo.append(fsolve(valueCalculator2,m,args=data)[0])
        print(mo)
        rate2.append(rateCalculator2(mo[x],x))
        rate3 = rate2[1:]
        data = (x,rate3)
    return rate2
    
rate4 = solutionIterator(mo,nNodes,rate3,rate2)[:]




reversed_lists = [list(reversed(x)) for x in rate4]

#reversed_lists[1].reverse()

print("     ")

print("---------------------------------------------------")
print("KALOTAY-WILLIAMS-FABOZZI SHORT RATE MODEL AUTOMATED")
print("---------------------------------------------------")

print_lattice2(reversed_lists, info = [])

print("     ")


#        
#def 
#for x in range(len(pV)):
#    data = (mo,x,rate3)
#    mo.append(fsolve(valueCalculator2,m,args=data)[0])
#    rate2.append(rateCalculator2(mo,x))
#    rate3 = rate2[1:]
#    print rate3     
