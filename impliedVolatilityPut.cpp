//Implied Volatility of a Put Option Using C++.  We developed the program for the calculation of the Implied Volatility
//of a call option in Python but for a change we decided to do this one in C++.  C++ makes things difficult by an order
//of magnitude and for these types of programs, there is is no noticeable difference in the speed and efficiency of
//of the programs.  So Python is more user friendly ....however, for legacy reasons most Finance related programs
//were developed in C++ so it is good to have a working knowledge of the program.  Also, many finance related books
//were written in a combination of English Language and C++.  However, if you have a prototype written in Python it is
//easy to translate to C++.  See you next time!!

#include <iostream>
#include <cmath>
#include <string>
using namespace std;

const double PI = 3.1415926;

double cumm_dens_function(double t);

double blackScholesImpVol(double t,double S,double K,double T,double a,double r,double q);

double vegaImpVol(double t,double S,double K,double T,double a,double r,double q);

double impliedVolPut(double t,double S,double K,double T,double r,double q, double P);


double cumm_dens_function(double t)
{
    double z = abs(t);

    double y = 1.0/(1.0 + 0.2316419*z);

    double a1 = 0.319381530;

    double a2 = -0.356563782;

    double a3 = 1.781477937;

    double a4 = -1.821255978;

    double a5 = 1.330274429;


    double cdf = 1 - exp(-1*(pow(-t,2.0)/2.0))*(a1*y + a2*(pow(y,2.0)) + a3*(pow(y,3.0)) + a4*(pow(y,4.0)) + a5*(pow(y,5.0)))/sqrt(2*PI);


    double result ;

    if (t > 0.0)
    {
     result = cdf;

    }
    else
    {
      result = 1 - cdf;
    }

    return result;

}

double blackScholesImpVol(double t,double S,double K,double T,double a,double r,double q)
{
    double d1, d2, result;

    //t = Beginning Time
    //S = Spot Price
    //K = Strike
    //T = Maturity
    //a = volatility
    //r = Constant Interest Rate
    //q = Continous Dividend Rate of the Underlying Asset

    d1 = (log(S/K) + (r - q + pow(a,2)/2.0)*(T-t))/(a*sqrt(T-t));

    d2 = d1 - (a*sqrt(T-t));

    result = K*exp(-r*(T-t))*cumm_dens_function(-d2) - S*exp(-q*(T-t))*cumm_dens_function(-d1);

    return result;
}

double vegaImpVol(double t,double S,double K,double T,double a,double r,double q)
{
    double d1, result;

    //t = Beginning Time
    //S = Spot Price
    //K = Strike
    //T = Maturity
    //a = volatility
    //r = Constant Interest Rate
    //q = Continous Dividend Rate of the Underlying Asset

    d1 = (log(S/K) + (r - q + pow(a,2)/2.0)*(T-t))/(a*sqrt(T-t));

    result = S * exp(-q* (T-t)) * sqrt(T-t) * (1.0/sqrt(2.0*PI)) * exp(pow(-d1,2)/2.0);

    return result;
}

double impliedVolPut(double t,double S,double K,double T,double r,double q,double P)

{
    //t = Beginning Time
    //S = Spot Price
    //T = Strike
    //a = Volatility Is Assumed to Start at 0.25
    //r = Constant Interest Rate
    //q = Continous Dividend Rate of the Underlying Asset
    //P = Put Price

    double epsilon, xnew, xold;

    int maxIterationCount, i;

    epsilon = 10e-9;

    maxIterationCount = 100000;

    xnew = 0.25;

    xold = xnew - 1;

    i = 0;

    double f_BS_xnew = 0.0;

    double vega_BS_xnew = 0.0;

    while (i < maxIterationCount)
    {
        f_BS_xnew = blackScholesImpVol(t,S,K,T,xnew,r,q);

        vega_BS_xnew = vegaImpVol(t,S,K,T,xnew,r,q);

        xold = xnew;

        xnew = xnew - (f_BS_xnew - P)/vega_BS_xnew;

        if (abs(xnew - xold) <= epsilon) break;

        ++i;
    }

    return xnew;
    }

int main()
{
        cout << endl;

        cout << "The Implied Volatility of a Put Option with the Given Input Parameters is: " << impliedVolPut(0,25.0,20.0,1.0,0.05,0.00,7.0) << endl;

        return 0;
}

//The result returned by calling this module is 1.17522 which is the same result you get if you use RQuantLib to the 
//calculation like so:
//library(RQuantLib)
//EuropeanOptionImpliedVolatility(type="put", value=7.0, underlying=25.0, strike=20, dividendYield=0.00, riskFreeRate=0.05,maturity=1.0, volatility=0.25)
// Result: 1.175224
