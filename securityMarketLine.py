#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 05:41:29 2018

@author: oluwaseyiawoga
"""
"""
Import Libraries & Packages
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime
import pandas_datareader.data as web
matplotlib.style.use('ggplot')
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
from dateutil.relativedelta import relativedelta
pd.options.display.float_format = '{:20,.3f}'.format
from scipy import stats


def CAPMExpectedReturn(beta, riskFreeRate, marketReturn):
    """
    Function to Calculate CAPM Expected Returns
    Args:
        param1: beta, riskFreeRate, marketReturn
    Returns:
        CAPM Expected Returns
    """

    return riskFreeRate + beta * (marketReturn - riskFreeRate)


def alpha(mutualFundExpectedReturn, beta, riskFreeRate, marketReturn):
    """
    Function to Calculate Alpha Jensen Returnss
    Args:
        param1: mutualFundExpectedReturn, beta, riskFreeRate, marketReturn
    Returns:
        Jensen Alpha
    """

    return mutualFundExpectedReturn - riskFreeRate - \
        beta * (marketReturn - riskFreeRate)


def identifyArbitrageOpportunities(returnsA, betaA, returnsF, betaF):
    """
    Function to identify Arbitrage Opportunities
    Args:
        param1: eturnsA, betaA, returnsF, betaF
    Returns:
        None:
        Prints a list of arbitrage opportunities and reasons
    """

    print("ONLY THE FIRST FOUR RETURNS & BETA WERE CONSIDERED")
    print("")
    for x in range(4):
        a = expReturnPortF[x] * 0.8 + expReturnPortA[x] * 0.2
        b = betaPortF[x] * 0.8 + betaPortA[x] * 0.2
        if a > 8.0 and b < 0.6:
            print("")
            print("The Expected Return & Beta of the Constructed Portfolio: ")
            print("Weighted 80% Portfolio F & 20% Portfolio A is :")
            print("Expected Return: " + str(a))
            print("Beta: " + str(b))
            print("Since the Return is higher than 8% and the beta is less than 0.6")
            print("Long the Constructed Portfolio and Short Portfoio E")
            print("")


"""
All the Above Functions are Called From Below
"""


if __name__ == '__main__':

    """
    QUESTION - PART 1:
        . Consider a mutual fund with a beta of 0.8 which has an expected rate of return
          of 14%.  If risk-free rate of return is rf = 5%, and you expect the rate of return on
          market portfolio to be 15%.

        . Use Python to address the following questions:
            . Would you be interested in investing in the fund? If so, what is the Alpha of the
              fund.
            . What passive portfolio comprised of a market-index portfolio and a money-market account
              would have the same beta as the fund.

        Note: show that the difference between the expected rate of return on this passive
        portfolio and that of the fund equals the alpha from question 1.
    """

    beta = 0.8
    mutualFundExpectedReturn = 0.14
    riskFreeRate = 0.05
    marketReturn = 0.15

    CAPM = CAPMExpectedReturn(beta, riskFreeRate, marketReturn)

    print("")

    print("The Capital Asset Pricing Model Expected Return is :")

    print("")

    print(round(CAPM,5))

    """
    A positive alpha of 1.0 means the fund or stock has outperformed its benchmark
    index by 1 percent. A similar negative alpha of 1.0 would indicate an underperformance
    of 1 percent. A beta of less than 1 means that the security will be less volatile than
    the market.

    In other words, Alpha measures how well an investment performed compared to its benchmark.
    In finance, Jensen's index is used to determine the required excess return of a stock,
    security or portfolio. It uses a relationship between risk and return (technically called
     “security market line”) as a benchmark.

    Alpha = r - Rf - beta * (Rm - Rf)

    r = the security's or portfolio's return
    Rf = the risk-free rate of return
    beta = systemic risk of a portfolio (the security's or portfolio's price
    volatility relative to the overall market)
    Rm = the market return.
    """

    alpha = alpha(mutualFundExpectedReturn, beta, riskFreeRate, marketReturn)

    print("")

    print("The Alpha is :")

    print("")

    print(round(alpha,5))

    """
    Yes I will invest in the fund because it has a positive alpha.  That is, it outperformed
    the market by 1%.
    """

    """
    What passive portfolio comprised of a market-index portfolio and a money-market account
    would have the same beta as the fund?

    A passive portfolio or money market fund with simiar composition and weighting as
    the fund may have same beta as the fund under consideration.
    """

    """
    QUESTION - PART II:
        . Consider the following data for a one-factor economy. All portfolios are assumed to
          be well diversified.

        Portfolio        Expected Return      Beta
        A                12%-20%              1.2-1.7
        F                6%-9%                0.0-0.9

        Note: Consider that Expected Return changes in step sizes of 1%
        (e.g. Portfolio A can have expected returns of 12%,13%,…19%,20%) and Beta change
        in step sizes of 0.1 (e.g Portfolio F can have Beta values of 0.0,0.1,0.2,….0.8,0.9)

        . Suppose that another portfolio, portfolio E, is well diversified with a beta of
          0.6 and expected return of 8%.

        . For which range of values of Expected Return and Beta would an arbitrage
          opportunity exist?

         . Develop a simple strategy in Python to exploit the most  juice out of
           the arbitrage opportunity strategy for each of the cases.

         . Plot the risk-reward profiles of these strategies (for each set of combination of
           Expected Return and Beta for Portfolio A & F) and discuss.
    """

    expReturnPortF = np.arange(6, 9 + 0.01, 1)
    betaPortF = np.arange(0.0, 0.3 + 0.01, 0.1)

    expReturnPortA = np.arange(12, 17 + 0.01, 1)
    betaPortA = np.arange(1.2, 1.70 + 0.01, 0.1)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    ax.set_title('Portfolio A - Risk Return Profile')
    ax.plot(betaPortA, expReturnPortA, 'ro', color='r')
    ax.plot(betaPortA, expReturnPortA, color='r', label='Returns Versus Beta')
    ax.vlines(1.5, 12, 15, colors='b')
    ax.hlines(15, 1.2, 1.5, colors='b')
    ax.annotate('Exp Return A',
                xy=(1.3, 15), xycoords='data',
                xytext=(0.4, 0.8), textcoords='axes fraction',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='top')
    ax.set_xlabel('Beta A')
    ax.set_ylabel('Returns')
    ax.legend(loc='best')
    plt.show()

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    ax.set_title('Portfolio F - Risk Return Profile')
    ax.plot(betaPortF, expReturnPortF, 'ro', color='r')
    ax.plot(betaPortF, expReturnPortF, color='r', label='Returns Versus Beta')
    ax.vlines(0.15, 6, 7.5, colors='b')
    ax.hlines(7.5, 0.0, 0.15, colors='b')
    ax.annotate('Exp Return F',
                xy=(0.05, 7.5), xycoords='data',
                xytext=(0.4, 0.8), textcoords='axes fraction',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='top')
    ax.set_xlabel('Beta F')
    ax.set_ylabel('Returns')
    ax.legend(loc='best')
    plt.show()

    expReturnPortF[0] * 0.5 + expReturnPortA[0] * 0.5
    betaPortA[0] * 0.5 + betaPortF[0] * 0.5

    """
    expReturnPortF[0] * 0.5 + expReturnPortA[0] * 0.5
    #9.0
    betaPortA[0] * 0.5 + betaPortF[0] * 0.5
    #0.6

    Suppose that another portfolio, portfolio E, is well diversified with a beta of
          0.6 and expected return of 8%.



    Suppose PortFolio E is my Benchmark Portfolio and at timeframe 1 (represented by index
    0 in the array)....I decided to construct a portfolio that consists of 50% of A and
    50% of F.....I get a beta of 0.6 and a return of 9%.  This is the same as the risk of
    portfolio E but higher return.  So I short E and long the newly constructed portfoliio
    and make a riskless profit.
    """

    identifyArbitrageOpportunities(
        expReturnPortA,
        betaPortA,
        expReturnPortF,
        betaPortF)

    """
    QUESTION PART 3:
        Suppose the economy can be in one of the following two states:
            1. Boom or "good" state and
            2. Recession or "bad" state.

        Each state can occur with an equal opportunity.  The annual return on the market
        and a certain security X in the two states of the economy are as follows:
            . Market: at the end of the year, the market is expected to yield a return of
              30% in the good state and a return of (-10%) in the bad state;
            . Security X: at the end of the year, the security is expected to yield
              a return of 40% in the good state and a return of (-35%) in the bad state;

        Furthermore, assume that annual risk-free rate of return is 5%.
            . Write a Python Program to calculate the beta of security X relative to the market.
            . Furthermore, calculate the alpha of security X using CAPM.
            . Draw the security market line (SML). Label the axes and all points (including
              the market portfolio, the risk-free security, and security X) in the graph clearly.
              Identify alpha in the graph.
    """

    expectedReturnMarket = np.linspace(0.3 * 0.5 + -0.1 * 0.5, 2)  # Extended
    expectedReturnSecurityX = np.linspace(
        0.4 * 0.5 + -0.35 * 0.5,
        len(expectedReturnMarket))  # Extended
    riskFreeRate = 0.05

    beta, alpha, r_value, p_value, std_err = stats.linregress(
        [expectedReturnSecurityX], [expectedReturnMarket])

    print("")
    print("Beta :" + str(beta))
    print("")
    print("Alpha :" + str(round(alpha, 5)))

    """
    Security Market Line:
        E(Ri) = Rf + Beta(ERm - Rf)

        SML: (E(Ri)- Rf) = beta*(Erm - Rf)

    The SML graphs the results from the capital asset pricing model (CAPM) formula. The x-axis represents the risk (beta), and the y-axis represents the expected return. The market risk premium is determined from the slope of the SML.

    The relationship between β and required return is plotted on the security market
    line (SML) which shows expected return as a function of β. The intercept is the
    nominal risk-free rate Rf available for the market, while the slope is E(Rm)− Rf
    (for market return Rm). The security market line can be regarded as representing
    a single-factor model of the asset price, where beta is exposure to changes in
    value of the market. The equation of the SML, giving the expected value of the
    return on asset i, is thus:
    """

    Ri = riskFreeRate + beta * (expectedReturnMarket - riskFreeRate)

    

    betas = beta * (expectedReturnMarket - riskFreeRate)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    ax.set_title('Security Market Line (SML)')
    ax.plot(betas, Ri, 'ro', color='r')
    ax.plot(betas, Ri, color='r', label='Security Market Line (SML')
    ax.vlines(0.04, 0.00, 0.09, colors='b')
    ax.hlines(0.09, 0.0, 0.04, colors='b')
    ax.annotate('Undervalued',
                xy=(0.03, 0.11), xycoords='data',
                xytext=(0.6, 0.8), textcoords='axes fraction',
                arrowprops=dict(facecolor='green', shrink=0.05),
                horizontalalignment='right', verticalalignment='top')

    ax.annotate('Overvalued',
                xy=(0.06, 0.05), xycoords='data',
                xytext=(0.7, 0.2), textcoords='axes fraction',
                arrowprops=dict(facecolor='green', shrink=0.05),
                horizontalalignment='right', verticalalignment='top')

    ax.annotate('Risk Free Rate',
                xy=(0.002, 0.053), xycoords='data',
                xytext=(0.4, 0.2), textcoords='axes fraction',
                arrowprops=dict(facecolor='blue', shrink=0.05),
                horizontalalignment='right', verticalalignment='top')

    ax.set_xlabel('Beta = beta * (expectedReturnMarket - riskFreeRate)')
    ax.set_ylabel('Returns = rF + beta * (expectedReturnMarket - rF)')
    ax.legend(loc='best')
    plt.show()
