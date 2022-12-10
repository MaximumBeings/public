#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:54:16 2022

@author: oluwaseyiawoga


"""

from datetime import date
from dateutil.relativedelta import relativedelta

from numpy import array
import numpy as np
from scipy.optimize import fsolve
import pandas as pd
pd.options.display.float_format = "{:,.2f}".format
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



"""
FAS 91 - Case 1 - Amortization Based on Contractual Payment Terms

On January 1, 19X7, A Company originates a 10-year $100,000 loan with a 10 percent
stated interest rate. The contract specifies equal annual payments of $16,275 through
December 31, 19Y6. The contract also specifies that no penalty will be charged
for prepayments of the loan. A Company charges a 3 percent ($3,000) nonrefundable
fee to the borrower and incurs $1,000 in direct loan origination costs (attorney fees,
appraisal, title insurance, wages and payroll-related fringe benefits of employees
performing origination activities, outside broker's fees'). The carrying amount of 
the loan is computed as follows:
    
    Loan Principal                      100,000
    Origination fees                    (3,000)
    Direct loan origination costs        1,000
    Carrying amount of loan             $98,000
    
A Company accounts for this loan using contractual payments to apply the interest
method of amortization. In calculating the effective rate to apply the interest 
method, the discount rate necessary to equate 10 annual payments of $16,275 to the
initial carrying amount of $98,000 is approximately 10.4736 percent. 
"""

contractualPayments = [16275.00]*10
netLoanAmount = 98000
noOfYears = 10
yearlyContractualPayments = 16275
statedAnnualInterest = 0.1
payments = 16275.00

principal =100000
netOrigninationFees = 2000


def npvOfContractualPayments(unknownRate):
    result  = 0
    for x in range(0,noOfYears):
        result = result  + contractualPayments[x]/(1+unknownRate)**(x+1)
    return result
        

unknownRate=0.2
def optimizationFunc(unknownRate):
    a = netLoanAmount
    b = npvOfContractualPayments(unknownRate)
    return b - a

solutions = fsolve(optimizationFunc, [20/100], xtol=1.49012e-16,)
effectiveInterestRate = solutions[0]

def generateAmprtizationTable():
    statedInterest = []
    interestIncome = []
    amortization = []
    remPrinBal = []
    amortizationToDate = 0.0
    unamortizedNetFees = []
    carryingAmount = []
    for x in range(0,10):
        if x == 0:
            statedInterestThisYear = principal * statedAnnualInterest
            statedInterest.append(statedInterestThisYear)
            interestIncomeThisYear = netLoanAmount * effectiveInterestRate
            interestIncome.append(interestIncomeThisYear)
            yearlyAmort = interestIncomeThisYear-statedInterestThisYear
            amortization.append(yearlyAmort)
            amortizationToDate = amortizationToDate + yearlyAmort
            remainingPrinThisYear = principal - (yearlyContractualPayments-statedInterestThisYear)
            remPrinBal.append(max(0,remainingPrinThisYear))
            unamortFeesThisYear = netOrigninationFees - amortizationToDate
            unamortizedNetFees.append(unamortFeesThisYear)
            carryAmountThisYear = remainingPrinThisYear - unamortFeesThisYear
            carryingAmount.append(carryAmountThisYear)
            
        elif x >= 1:
            statedInterestThisYear = remPrinBal[x-1] * statedAnnualInterest
            statedInterest.append(statedInterestThisYear)
            interestIncomeThisYear = carryingAmount[x-1] * effectiveInterestRate
            interestIncome.append(interestIncomeThisYear)

            yearlyAmort = interestIncomeThisYear-statedInterestThisYear
            amortization.append(yearlyAmort)
            amortizationToDate = amortizationToDate + yearlyAmort
            remainingPrinThisYear = remPrinBal[x-1] - (yearlyContractualPayments-statedInterestThisYear)
            remPrinBal.append(max(0,remainingPrinThisYear))
            unamortFeesThisYear = netOrigninationFees - amortizationToDate
            unamortizedNetFees.append(max(unamortFeesThisYear,0))
            carryAmountThisYear = remPrinBal[x] - unamortFeesThisYear
            carryingAmount.append(carryAmountThisYear)
    
    print()
    print("FAS 91 -> Amortization Case Study 1")
    print()
    print(f"Principal: {principal}")
    print(f"Origination Fees: {netOrigninationFees}")
    print(f"Net Loan Amount: {netLoanAmount}")
    print(f"Contractual Payments: {payments}")
    print(f"Effective Interest Rate -> Calculated {effectiveInterestRate}")
    print(f"Number of Years: {noOfYears}")
    print()
    
    finalTable = pd.DataFrame()
    finalTable["Years"] = [x for x in range(1,11)]
    finalTable["Cashflows"] = contractualPayments
    finalTable["Stated_Interest"] = statedInterest
    finalTable["Amortization"] = amortization
    finalTable["Int_Income"] = interestIncome
    finalTable["Prin_Balance"] = remPrinBal
    finalTable["UnamortNetFees"] = unamortizedNetFees
    finalTable["CarryingAmount"] = carryingAmount
    print(finalTable.to_string(index=False))


generateAmprtizationTable()

