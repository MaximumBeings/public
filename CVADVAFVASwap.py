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
