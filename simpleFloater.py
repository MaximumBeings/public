"""
Title: Simple Floater 

Source: Google it

Discussion: To be used in an upcoming article.  See you next time.
"""
import datetime
from dateutil.relativedelta import relativedelta

#Set Variables:
iSSUESPREAD = 0.0030 #30 basis points
vALUATIONDATE = datetime.date(2010, 8, 15)
mATURITYDATE = datetime.date(2014, 9, 15)
nEXTCOUPONDATE = datetime.date(2010, 9, 15)
lASTCOUPONDATE = nEXTCOUPONDATE - relativedelta(months=3)
d = (nEXTCOUPONDATE - lASTCOUPONDATE).days  #92
f = (nEXTCOUPONDATE - vALUATIONDATE).days  #31
pAYMENTFREQUENCY = 4   #Quarterly
n = ((mATURITYDATE - nEXTCOUPONDATE).days)/(365/pAYMENTFREQUENCY)
lIBORLAST = 0.0698    #6.98%
dISCOUNTMARGIN = 0.0015 #15 Basis Point or 0.15%
zEROSWAPRATE = 0.0840 #8.40% - Swap Rate to Maturity from Valuation Date
lIBORVALUATIONDATE = 0.0705  #7.05%
 
#Calculations:
 
i = (zEROSWAPRATE + dISCOUNTMARGIN)/pAYMENTFREQUENCY

v = 1/(1 + i) 

An = (1 - v**n)/i

P = ((((lIBORLAST + iSSUESPREAD) * d/365)  + ((iSSUESPREAD - dISCOUNTMARGIN)/pAYMENTFREQUENCY * An) + 1)\
/(1 + (lIBORVALUATIONDATE + dISCOUNTMARGIN) * f/365)) * 100.

print "The Price of the FRN is: ", P
