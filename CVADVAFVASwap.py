"""
Topic: Understanding CVA, DVA and FVA:  Examples of Interest Rate Swap Valuation.

Source: Understanding CVA, DVA and FVA:  Examples of Interest Rate Swap Valuation by Donald Smith.

Background: We are going to use this topic to discuss the application of one of the interest rate models
we built in the past.  Check it out here - https://github.com/MaximumBeings/public/blob/master/KWFPython.py
This article uses the binomial interest rate tree developed by Kalotay-Fabozzi-William to value interest rate
swap and calculate CVA, DVA and FVA.  The article is accessible once you know how to build the tree.  The article uses
Par bonds to build the tree.  As we shall see, the par rate is a transformation of the spot rate and the forward rate. 
I am thinking of extendiing the model discussed in the article to use Hull-White, Ho-Lee, Black-Derman-Toy and Black Karansiski
so we may need to transform the input a little.  We Will cross the river when we get there.

The article is accessible once you know how to build the tree which we have already done before in the link shown above.
We just have to replicate using the same par bonds used in the article.

Dates       Coupon_Rates    Prices      Discount_Factors
1           1.00%           100.00      0.990099
2           2.00%           100.00      0.960978
3           2.50%           100.00      0.928023
4           2.80%           100.00      0.894344
5           3.00%           100.00      0.860968

OTHER POSSIBLE EXTENSIONS: Develop the model discussed in the paper using the paper by John Hull in Multi-Curve Modeling Using Trees
to build the tree.

Previous Models On The KFW Tree:
https://github.com/MaximumBeings/public/blob/master/KFW.R  (Prototype R Version)
https://github.com/MaximumBeings/public/blob/master/KWFPython.py  (Prototype & Automated Version in Python)

Programming language of choice = Python.



See you soon!!!
"""

"""
This is the tree in the article built using R.  I did this in 2014 if memory serves me right
but it is prototype in R.  But since Python is our programming language of choice we will implement
in Python.  This is just for heads up only.  Python and R are different but are eerily close in some respect.
So this can be easily translated to Python.  We weill also use this to test the automated version of our model.

See you next time!!

# ##################################################################################################
# 
#     FINAL BINOMIAL FORWARD RATE TREE - POPULATED MANUALLY FROM CALCULATION BELOW
#
# Year 0        Year 1             Year 2            Year 3        Year 4
# 
#                                                                  0.08084137
#                                                   0.06518412
#                                  0.05111153                      0.05418959           
#               0.3632577                           0.04369422
# 0.01                             0.03426108                      0.03632437
#               0.2434989                           0.02928911
#                                  0.02296589                      0.02434895
#                                                   0.01963308
#                                                                  0.01632159
#################################################################################################
                                                   
           
#Implemented using Numerical Methods (Uniroot for Finding roots in R).  Not the most elegant code
#Source - An Introduction to the Valuation of Debt Securities
# and Interest Rate Derivatives in a World of CVA and DVA By Don Smith

#Conclusion - Same results as those in referenced article
#Comments - It can be reproduced in Excel using Solver



#Par Bonds Details

# Year   Coupon Rate   Price
# 0      0.01          100.00
# 1      0.02          100.00
# 2      0.025         100.00
# 3      0.028         100.00
# 4      0.030         100.00



r = 2.000/100    #Initial Guess for the forward rate 
vol = 0.2    #Assumed Constant Volatility 20%
factor = exp(2*vol*sqrt(1))  #Proportionality Factor

#Probability Weights at each node - Lets Assume we know these numbers - Simplifying Assumption
#We Start from 50/50 and work our way up the nodes.


#STEPS - 
#Calculate the binomial forward rates in Year 1 
#We assume that the rate on the last node i.e. N2 in this case is r
#In order to maintain proportionality we assume that all rates one node up is scaled by the factor
#We also maintain the probability weights of 50/50 at every node
#Our goal is to find r such that the final value of the bond is 100.00 which is the par value
#Repeat for every node

kalotayYear1 <- function(r)
{
  N1 = 102/(1+(r*factor))    #FV value of bond is 102 at maturity
  N2 = 102/(1+r)
  ans = (2+(0.5*N1 + 0.5*N2))/1.01
  return(ans - 100)
  
  
}

#Use a root finding algorithm in R to find the value of R
uniroot(kalotayYear1,c(0,1),tol = 1e-20)$root 

ndRate = 0.02434989 * 100   #2.434989
nuRate = ndRate * 1.491825  #3.632577


kalotayYear2 <- function(r)
{
  N1 = 102.5/(1+(r*factor))    #FV value of bond is 102.5 at maturity
  N2 = 102.5/(1+(r))
  N3 = 102.5/(1+r/factor)
  ans1 = (2.5+(0.5*N1 + 0.5*N2))/(1.03632577)
  ans2 = (2.5+(0.5*N2 + 0.5*N3))/(1.02434989)
  fAns = (2.5+(0.5*ans1 + 0.5*ans2))/1.01
  return(fAns - 100)
  
  
}

#Use a root finding algorithm in R to find the value of R
uniroot(kalotayYear2,c(0,1),tol = 1e-30)$root 
#0.03426108
#So for Year 2 with 3 nodes
Node1 = 0.03426108 * factor
Node2 = 0.03426108
Node3 = 0.03426108/factor

# Node1 = 0.05111153
# Node2 = 0.03426108
# Node3 = 0.02296589


kalotayYear3 <- function(r)
{
  N1 = 102.8/(1+(r*factor*factor*factor))    #FV value of bond is 102.8 at maturity
  N2 = 102.8/(1+r*factor*factor)
  N3 = 102.8/(1+r*factor)
  N4 = 102.8/(1+r)
  
  ans1 = (2.8+(0.5*N1 + 0.5*N2))/(1.05111153)
  ans2 = (2.8+(0.5*N2 + 0.5*N3))/(1.03426108)
  ans3 = (2.8+(0.5*N3 + 0.5*N4))/(1.02296589)
  
  xans1 = (2.8+(0.5*ans1 + 0.5*ans2))/(1.03632577)
  xans2 = (2.8+(0.5*ans2 + 0.5*ans3))/(1.02434989)
  
  fAns = (2.8+(0.5*xans1 + 0.5*xans2))/1.01
  return(fAns - 100)

}

#Use a root finding algorithm in R to find the value of R
uniroot(kalotayYear3,c(0,1),tol = 1e-20)$root 
#0.01963308

#Year3 has four nodes and the forward rates for the four nodes are as follows
Node1 = 0.01963308*factor*factor*factor
Node2 = 0.01963308*factor*factor
Node3 = 0.01963308*factor
Node4 = 0.01963308


# Node1 = 0.06518412
# Node2 = 0.04369422
# Node3 = 0.02928911
# Node4 = 0.01963308


kalotayYear4 <- function(r)
{
  N1 = 103/(1+(r*factor*factor))    #FV value of bond is 102.5 at maturity
  N2 = 103/(1+(r*factor))
  N3 = 103/(1+r)
  N4 = 103/(1+r/factor)
  N5 = 103/(1+r/factor/factor
            )
  ans1 = (3.0+(0.5*N1 + 0.5*N2))/(1.06518412)
  ans2 = (3.0+(0.5*N2 + 0.5*N3))/(1.04369422)
  ans3 = (3.0+(0.5*N3 + 0.5*N4))/(1.02928911)
  ans4 = (3.0+(0.5*N4 + 0.5*N5))/(1.01963308)
  
  xans1 = (3.0+(0.5*ans1 + 0.5*ans2))/(1.05111153)
  xans2 = (3.0+(0.5*ans2 + 0.5*ans3))/(1.03426108)
  xans3 = (3.0+(0.5*ans3 + 0.5*ans4))/(1.02296589)
  
  yans1 = (3.0+(0.5*xans1 + 0.5*xans2))/(1.03632577)
  yans2 = (3.0+(0.5*xans2 + 0.5*xans3))/(1.02434989)
  
  fAns = (3.0+(0.5*yans1 + 0.5*yans2))/1.01
  return(fAns - 100)
  
  
}

#Use a root finding algorithm in R to find the value of R
uniroot(kalotayYear4,c(0,1),tol = 1e-30)$root 
#0.03632437



#Year4 has five nodes and the forward rates for the four nodes are as follows:
Node1 = 0.03632437*factor*factor
Node2 = 0.03632437*factor
Node3 = 0.03632437
Node4 = 0.03632437/factor
Node5 = 0.03632437/factor/factor

# Node1 = 0.08084137
# Node2 = 0.05418959
# Node3 = 0.03632437
# Node4 = 0.02434895
# Node5 = 0.01632159

"""
