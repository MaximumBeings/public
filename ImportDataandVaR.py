"""
#TOPIC: Importing Data into Python & Calculating VaR Using Historical Loss Distribution

#SOURCE: Introduction to Credit Risk Management - TU Delft via Edx

#DISCUSSION: This is just a conversion of the class sample on calculation of VaR for historical
#            loss distribution from R to Python.  I am converting some the course codes (in R) and other manual examples
#            to Python just for the sake of doing so. Auditing the class to refresh and while away time.
#
#Question: Calculate the VaR at 95% confidence interval for a loss distirbution consisting of 1504 records.

#The first and last five records in the data are listed below: (To get the complete file, register for the course free of charge
#on edx - this is just to help us visualize what the data looks like).

# So next time we will post the python code to calculate Expected Shortfall even though this was done manually in 
#the course, we can implement it in python just because we can.

    
    losses;
1;-1.1981768206
2;1.0061948139
3;0.5014854404
4;3.0888666123
5;-1.0104259483
6;8.310673145
..........
..........
..........
1501;20.01
1502;30.01
1503;-2.56
1504;8.27

R Implementation is pretty straightfoward as given in the class
> data <- read.csv("losses3.csv")
#then the VaR at 95% confidence level is calculated as follow:

> quantile(data,0.95)
> 6.679614

"""


#PYTHON IMPLEMENTATION:  To illustrate how to import data into python and calculate VaR

import ast
import csv
import numpy as np
with open('losses3.csv') as f:  #replace with the location of file on your computer
    data=[]
    reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)  #indicate that the delimiter is a ';'
    reader.next()  #Skip the header "losses" on the first row
    for line in reader:   #read the file line by line and get the second column
        a=ast.literal_eval(line[1])
        data.append(a)  # append to a list
    

print np.percentile(data,95)  # calculate the VaR of the loss distribution at 95% confidence interval

#result ->  6.6796142564  -> same as the one in the R code above.


