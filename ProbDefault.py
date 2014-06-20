"""
Topic: Representing Historical Default Probabilities in Python's Pandas

Source: Introduction to Credit Risk - TU Delt via Edx

Discussion: Refer to week 4 lectures on Default Probabilities in the above course. These ratings are usually provided
by one of the three rating oligopolies (they control 90% of the market according to the class slides). Some bonds are 
rated while others are not rated so we will consider how to evaluate the credit risk for an unrated company 
using Altman-Z score (the z score falls into the category of models known as discrimant models).  Most companies 
use a variation of the model but not the original one.

This is just an attempt to replicate the class lectures on PD in Pandas Data Frame.

See you next time!!!
"""

import pandas as pd
transition_matrix = {'AAA' : [90.81, 0.70,0.09,0.02,0.03,0.00,0.00],
                     'AA'  : [8.33,90.65,2.27,0.33,0.14,0.11,0.00],
                     'A': [0.68,7.79,91.05,5.85,0.67,0.24,0.22],
                     'BBB': [0.06, 0.64,5.52,86.90,7.73,0.43,1.30],
                     'BB': [0.12,0.06,0.74,5.30,80.53,6.48,2.38],
                     'B': [0.00,0.14,0.26,1.10,8.84,83.46,11.24],
                     'CCC': [0.00,0.02,0.01,0.32,1.00,4.07,64.86],
                    'DF' :[0.00,0.00,0.06,0.18,1.06,5.20,19.79]}
print ""
print "Historical Probability of Default (PD) - Transition Matrix"
a = pd.DataFrame(transition_matrix, index=['AAA','AA','A','BBB','BB','B','CCC'], columns=['AAA', 'AA','A','BBB','BB','B','CCC','DF'])
print ""
print a

"""
Historical Probability of Default (PD) - Transition Matrix

       AAA     AA      A    BBB     BB      B    CCC     DF
AAA  90.81   8.33   0.68   0.06   0.12   0.00   0.00   0.00
AA    0.70  90.65   7.79   0.64   0.06   0.14   0.02   0.00
A     0.09   2.27  91.05   5.52   0.74   0.26   0.01   0.06
BBB   0.02   0.33   5.85  86.90   5.30   1.10   0.32   0.18
BB    0.03   0.14   0.67   7.73  80.53   8.84   1.00   1.06
B     0.00   0.11   0.24   0.43   6.48  83.46   4.07   5.20
CCC   0.00   0.00   0.22   1.30   2.38  11.24  64.86  19.79

"""

#Examples
#a is the name of our transition matrix for historical default probabilities
print ""
print "The probability that a bond rated AAA row_index will transition to CCC column_index is a['CCC']['AAA'] "
print
print str(round(a['CCC']['AAA'],3)) + "%"

#>>> The probability that a bond rated AAA row_index will transition to CCC column_index is a['CCC']['AAA'] 
#0.0%


print ""
print "The probability that a bond rated CCC row_index will transition to DF column_index"
print "within one year is a['DF']['CCC'] "
print
print str(round(a['DF']['CCC'],3)) + "%"

#>>>The probability that a bond rated CCC row_index will transition to DF column_index
#>>> within one year is a['DF']['CCC'] 
#19.79%

cum_matrix = {1 : [0.00,0.18,5.20,19.79],
                     2  : [0.00,0.44,11.00,26.92],
                     3:[0.07,0.72,15.95,31.63],
                     4: [0.15,1.27,19.40,35.97],
                     5: [0.24,1.78,21.88,40.15],
                     7: [0.66,2.99,25.14,42.64],
                     10: [1.40,4.34,29.02,45.10],
                    15 :[1.40,4.70,30.65,45.10]}
print ""
print "Cummulative Default Probability -  This is only a subset of matrix for illustration only"
b = pd.DataFrame(cum_matrix, index=['AAA','BBB','B','CCC',], columns=[1,2,3,4,5,7,10,15])
print ""
print b

"""
Cummulative Default Probability -  This is only a subset of matrix for illustration only

        1      2      3      4      5      7      10     15
AAA   0.00   0.00   0.07   0.15   0.24   0.66   1.40   1.40
BBB   0.18   0.44   0.72   1.27   1.78   2.99   4.34   4.70
B     5.20  11.00  15.95  19.40  21.88  25.14  29.02  30.65
CCC  19.79  26.92  31.63  35.97  40.15  42.64  45.10  45.10

"""

print
print "What is the probability a CCC bond default by end of the second year - b[2]['CCC']?"
print str(round(b[2]['CCC'],3)) + "%"

print
print "What is the probability a CCC bond default during the second year given that it does not default during the first year -b[2]['CCC']- b[1]['CCC']?"
print str(round(b[2]['CCC']- b[1]['CCC'],3)) + "%"

print
print "What is the probability a CCC bond default by end of the second year - b[2]['CCC']?"
print "We first compute the probability of not defaulting by end of year 1 - 100 - b[1]['CCC']"
x = 100 - b[1]['CCC']

print "The unconditional probability of defaulting during the second year is - b[2]['CCC']- b[1]['CCC']"
y = b[2]['CCC']- b[1]['CCC']

print "Hence the conditional probability is y/x"
print str(round(y/x,4)*100) + "%"
#>>>result
#>>>8.89%





