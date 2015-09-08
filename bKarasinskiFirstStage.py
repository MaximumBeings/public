
"""
This is the rough prototype for the "FIRST STAGE" of the Black Karasinski Trinomial Interest Rate Tree.  The second and final stage will be 
implemented shortly and will be published in an article.  You have to wait for the article to get a good/better feel for the implementation.  
See you next time!!!

Source: Options, Futures and Other Derivatives - John Hull Fifth Edition
        Short Rate Model Implementation & Extension - Chapter 6 by Ser-Huang Poon (Via Google Search)
"""


import sys
import math 



def initialTimeStep(years):
    initialVector = [[0]]
    timeStep = range(years)
    vectorSize = 2
    y = vectorSize
    
    for x in range(len(timeStep)):
        tracker = []
        for i in range(y+1):
            tracker.append(1)
        initialVector.append(tracker[:])
        y = y + 2
        tracker = []
    return initialVector[:]
    
print initialTimeStep(2)

"""
[[0], [1, 1, 1], [1, 1, 1, 1, 1]]

"""

j = initialTimeStep(2)

    

def interMediateTimeStep(initialTimeStep):
    interMediateTimeStep = [[0]]
    collector = []
    for x in range(1,len(initialTimeStep)):
        for y in range(len(initialTimeStep[x])):
            collector.append(x)
            x = x - 1
        interMediateTimeStep.append(collector)
        collector = []
    return interMediateTimeStep
    
g = interMediateTimeStep(j)
    


"""
[[0], [1, 0, -1], [2, 1, 0, -1, -2]]

"""
"""
Construct the binomial tree for the BK Model with the following parameters:
    
a = 0.22
vol = 0.25
deltaT = 0.5

The yield curve is r(0,0.5) = 0.034303, r(0,1) = 0.03824 and r(0,1.5) = 0.04183

"""
vol = 0.25
a = 0.22
deltaT = 0.5   
deltaR = vol * math.sqrt(3 * deltaT)
M = -a * deltaT
jMax = int(math.ceil(-0.184/M))
jMin = -jMax    
    
def firstStage(interMediateTimeStep):
    firstStage = [[0.0000]]
    collector = []
    for x in range(1,len(j)):
        for y in range(len(g[x])):
            collector.append(g[x][y] * deltaR)
        firstStage.append(collector)
        collector = []
    return firstStage

initialRate = firstStage(g)   
           
test = [list(reversed(x)) for x in initialRate]

print_lattice2(test, info = [])

"""
#Function to print lattice not included

                 0                    1                    2
------------------|--------------------|--------------------|
                                          0.6123724356957945    
                                          0.3061862178478972    
                     0.3061862178478972   0.0000000000000000    
                     0.0000000000000000  -0.3061862178478972    
0.0000000000000000  -0.3061862178478972  -0.6123724356957945 



"""
#Define the Probabilities.....

def pAU(j,M):
    return (1.0/6.0 + ((j**2 * M**2) + (j * M))/2.0 )
    
def pAM(j,M):
    return ((2.0/3.0) - (j**2 * M**2))
    
def pAD(j,M):
    return ((1.0/6.0) + ((j**2 * M**2) - (j * M))/2.0 )
    

def pBU(j,M):
    return (1.0/6.0 + ((j**2 * M ** 2) - (j * M))/2.0 )
    
def pBM(j,M):
    return ((-1.0/3.0) - (j**2*M**2) + 2*j*M)
    
def pBD(j,M):
    return (7.0/6.0 + ((j**2 * M ** 2) - (3 * j * M))/2.0 )
    

def pCU(j,M):
    return (7.0/6.0 + ((j**2 * M ** 2) + (3 * j * M))/2.0 )
    
def pCM(j,M):
    return ((-1.0/3.0) - (j**2*M**2) - 2*j*M)
    
def pCD(j,M):
    return (1.0/6.0 + ((j**2 * M ** 2) + (j * M))/2.0 )


def firstStageFinal(firstStage):
    collector = []
    collector2 = []
    collectorFinal =[]
    for x in range(len(firstStage)):
        for y in range(len(firstStage[x])):
            if firstStage[x][y] == jMax:
                collector2 = [pCU(firstStage[x][y],M),pCM(firstStage[x][y],M),pCD(firstStage[x][y],M)]
            elif firstStage[x][y] == jMin:
                collector2 = [pBU(firstStage[x][y],M),pBM(firstStage[x][y],M),pBD(firstStage[x][y],M)]
            else:
                collector2 = [pAU(firstStage[x][y],M),pAM(firstStage[x][y],M),pAD(firstStage[x][y],M)]
            collector.append(collector2)
        collectorFinal.append(collector)
        collector2 = []
        collector = []
    return collectorFinal
        
        
         
Probb = firstStageFinal(g)

    
"""
The output from the above call look like so:
    
[[[0.16666666666666666, 0.6666666666666666, 0.16666666666666666]],
 [[0.11771666666666666, 0.6545666666666666, 0.22771666666666665],
  [0.16666666666666666, 0.6666666666666666, 0.16666666666666666],
  [0.22771666666666665, 0.6545666666666666, 0.11771666666666666]],
 [[0.8608666666666667, 0.05826666666666669, 0.08086666666666666],
  [0.11771666666666666, 0.6545666666666666, 0.22771666666666665],
  [0.16666666666666666, 0.6666666666666666, 0.16666666666666666],
  [0.22771666666666665, 0.6545666666666666, 0.11771666666666666],
  [0.08086666666666666, 0.05826666666666669, 0.8608666666666667]]]



""" 

"""
The table below is the output from all the codes above - Manual populated but will be implemented in Pandas later.
This is just the first stage of the three building exercise.  We will implement the second stage later in a couple
of week or sooner if time permits.


Node            A           B           C           D           E           F           G           H           I
j               0           1           0           -1          2           1           0           -1          -2
j*deltaR        0.00000     0.3062      0.0000      -0.3062     0.6124      0.3062      0.00000     -0.3062    -0.6124
Pu              0.16666     0.6546      0.16666     0.2277      0.8068      0.1177      0.1666      0.2277     0.0808
Pm              0.66666     0.6566      0.66666     0.6546      0.0582      0.6546      0.6546      0.6546     0.0582
Pd              0.16666     0.2277      0.16666     0.1177      0.0086      0.2277      0.1667      0.1177     0.8608

"""

"""
Second Stage of BK Complted:  - Final Codes Not Released.....Will be featured in an upcoming article
Final Results.  Just needs some polishing ....Stay tuned.
                 0                   1                   2
------------------|-------------------|-------------------|
                                        0.0880315826933609    
                                        0.0648132090847867    
                    0.0564170272896411  0.0477186930343022    
                    0.0415370083530419  0.0351328640728645    
0.0343030000000000  0.0305816017930718  0.0258665537439405

or shown to 5 decimal places as in the book

      0        1        2 
-------|--------|--------|
                  0.08803    
                  0.06481    
         0.05642  0.04772    
         0.04154  0.03513    
0.03430  0.03058  0.02587  


OUTSTANDING:
(a) Regular Binomial Tree (Pending but prototyped via HL,BDT and KFW)
(b) Ho Lee (Done)
(c) BDT (Prototyped)
(d) KFW (Prototyped)
(e) HW (Done)
(f) BK (Done)


"""
