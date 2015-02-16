#My schedule is busier now so I won't be posting as frequently as before.  I will be posting old programs I created from 
#my archives like this one which I wrote about four months ago.  In order to keep my github current, I will be posting
#codes from my archives at least once every 6-8 weeks.  These are suitable for pedagogy and I will ultimately use them to 
#write articles in the future - either to self publish or to publish in a journal. 

#See you next time!

"""
Using matrix algebra to generate discount curves from bond prices.
"""

import numpy as np

"""
Consider three bonds with the following information
Maturity    Coupon  Price
6 months    1%     100
1 year      2.5%    99
1.5 years   5.0%    98

"""

#Let us assume that we want to calculate the discount rates 
#from the observed bond details above

#Discount Rate for First Period i.e. Six Months
100/(100.1)

#0.999000999000999

#Discount Rate for second Period i.e. 1 Year
(99-(0.25*0.999001))/(100.25)

#0.985039897755611

#Discount Rate for Third Period i.e. 1.5 Years
(98-((0.5*0.999000999000999)+(0.5*0.985039897755611)))/(100.5)

0.9652535278768328


"""
So our output looks like below:
    
Maturity    Discount_Factors
6 months    0.999000999000999
1 year      0.985039897755611
1.5 years   0.9652535278768328
"""

#However we can generate the same output using matrix algebra like below
#We are going to use a Python library known as Numpy to create our matrix

M = np.matrix('100.10, 0.00, 0.00; 0.25,100.25,0.00; 0.50,0.50,100.50')

P = np.matrix('100;99;98')

inverse = np.linalg.inv(M)

discount_rate = np.dot(inverse,P)

discount_rate

"""
matrix([[ 0.999001  ],
        [ 0.9850399 ],
        [ 0.96525353]])
"""
#This is the same result we got when we solved the probelem algeraically.
