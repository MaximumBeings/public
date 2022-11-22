from __future__ import division
from scipy.optimize import fsolve
import math
import copy

def factor(time):
    """
    Helper Function
    """
    factor =[[]]
    temp = []
    for x in range(time):
        if x == 0:
            factor[0].append(0)
        else:
            for y in range(0,x+1):
                
                if y == 0:
                    temp.append(1)
                else:
                    temp.append(y * 2)
                    x = x - 2
            factor.append(temp)
            temp = []
    return factor
    
multiplier = factor(5)   

multiplier = [list(reversed(x)) for x in multiplier][:]


def print_lattice(lattice, info = []):
    """
    Lattice Printer.
    """
    print ("")
    levels = len(lattice[-1])
    start_date = len(lattice[0]) - 1
    dates = levels - start_date 
    outlist = []
    col_widths = [0] * dates
    for j in range(levels):
        level = []
        for k in range(dates):
            try:
                point = "{:.16f}".format(lattice[k][levels - 1 - j])
                esc_width = 0 
                if info != [] and info[k][levels - 1 - j] > 0:
                    point = (point, 'red')
                    esc_width += 9 
                level.append(point)
                col_widths[k] = max(col_widths[k], len(point) - esc_width)
            except IndexError:
                level.append('')
        outlist.append(level)
    separator = "|-".join(['-' * w for w in col_widths])
    formats = [ ]
    for k in range(dates):
        formats.append("%%%ds" % col_widths[k])
    pattern = "  ".join(formats)
    print (pattern % tuple(str(start_date + time) for time in range(dates)))
    print (separator)
    for line in outlist:
        print (pattern % tuple(line))

        
#print_lattice(multiplier, info = [])


m_guess = 0.2  #Initial guess for the second node.


ObservedRate = [0.1,0.11,0.12,0.125,0.13]
vol = [0.20,0.19,0.18,0.1622,0.14365]

zCBond_0 = 100/(1+ObservedRate[0])**1  
zCBond_1 = 100/(1+ObservedRate[1])**2  
zCBond_2 = 100/(1+ObservedRate[2])**3
zCBond_3 = 100/(1+ObservedRate[3])**4
zCBond_4 = 100/(1+ObservedRate[4])**5

pV = [zCBond_0, zCBond_1, zCBond_2, zCBond_3, zCBond_4]

temp_rate_tracker = [[0.1]]



def bdtOne(guess):
    ru = guess * math.exp(2 * 0.19)
    rd = guess 
    N1 = (100)/(1+ru)
    N2 = (100)/(1+rd)
    return (0.5*((N1/(1+ObservedRate[0])) + (N2/(1+ObservedRate[0])))-zCBond_1)
    
g = fsolve(bdtOne,m_guess)[0]

ru = g * math.exp(2 * vol[1])
rd = g

m = [0.1,0.1]   #Guess list data structure for node 2 and above.

final_rate_tracker=[[]]
nNodes = 5
temp_rate_tracker = [[ObservedRate[0]],[ru,rd]]
mo = [[0.1],[rd,1]]
m = [0.1,0.1]
final_rate_tracker = temp_rate_tracker[1:]


def rateCalculator(m,node):
    rate = []
    for x in range(0,node+1):
        if x == node:
            rate.append(m[0])
        else:
            rate.append(m[0] * math.exp(multiplier[node][x] * m[1]))
    return rate


def valueCalculator(m,node,final_rate_tracker):
    nValue = []
    nValue2 = []
    rate = []
    final_rate_tracker = final_rate_tracker[:]
    final_rate_tracker.reverse()

    for x in range(node+1):
        if x == node:
            rate.append(float(m[0]))
        else:
            rate.append(m[0] * math.exp(multiplier[node][x]* m[1]))
    for x in range(len(rate)):
        nValue2.append(((100)/(1+rate[x])))
        nValue = copy.deepcopy(nValue2)

    nValue2 = []

    y = 0
    while len(nValue) > 2:

        if len(nValue) <= 2:
            break
        
        for x in range(len(nValue)-1):
            nValue2.append((0.5*((nValue[x]) + (nValue[x+1])))/(1 + final_rate_tracker[y][x]))
        if y == 0:
            yu = math.sqrt(100/nValue2[0]) - 1
            yd = math.sqrt(100/nValue2[1]) - 1
            if len(nValue) <= 2:
                break
        if len(nValue) <= 2:
            break
        rate=[]
        y = y + 1
        nValue = nValue2[:]
        nValue2 = []
    out = [ ( 0.5*((nValue[0]) + (nValue[1]))/(1+temp_rate_tracker[0][0]) - pV[node])]
    out.append((0.5 * math.log(yu/yd) - vol[node]))
    return out

def solutionIterator(mo,nNodes,final_rate_tracker,temp_rate_tracker):
    
    for x in range(2,nNodes):
        data = (x,final_rate_tracker)
        mo.append(fsolve(valueCalculator,m,args=data))
        temp_rate_tracker.append(rateCalculator(mo[x],x))
        final_rate_tracker = temp_rate_tracker[1:]
        data = (x,final_rate_tracker)
    return temp_rate_tracker
    
final_rate_tracker = solutionIterator(mo,nNodes,final_rate_tracker,temp_rate_tracker)[:]

reversed_lists = [list(reversed(x)) for x in final_rate_tracker]

final_Rate = [[100 * y for y in x] for x in reversed_lists]

print ("     ")

print ("----------------------------------------------------------------------------")
print ("BLACK-DERMAN-TOY SHORT RATE MODEL AUTOMATED - VERSION THAT MATCHES JOHN HULL")
print ("----------------------------------------------------------------------------")

print_lattice(final_Rate, info = [])

print ("     ")
