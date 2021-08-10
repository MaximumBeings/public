#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 16:13:51 2021

@author: oluwaseyiawoga
"""

import numpy as np
np.set_printoptions(suppress=True)
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web 
plt.style.use('ggplot')
import cvxpy as cp

import matplotlib.pyplot as plt

    
sp = ["MMM",
           "ABT",
           "ABBV",
           "ACN",
           "ATVI",
           "AYI",
           "ADBE",
           "AAP",
           "AES",
           "AET",
           "AMG",
           "AFL",
           "A",
           "APD",
           "AKAM",
           "ALK",
           "ALB",
           "ALXN",
           "ALLE",
           "AGN",
           "ADS",
           "LNT",
           "ALL",
           "GOOGL",
           "GOOG",
           "MO",
           "AMZN",
           "AEE",
           "AAL",
           "AEP",
           "AXP",
           "AIG",
           "AMT",
           "AWK",
           "AMP",
           "ABC",
           "AME",
           "AMGN",
           "APH",
           "APC",
           "ADI",
           "ANTM",
           "AON",
           "APA",
           "AIV",
           "AAPL",
           "AMAT",
           "ADM",
           "ARNC",
           "AJG",
           "AIZ",
           "T",
           "ADSK",
           "ADP",
           "AN",
           "AZO",
           "AVB",
           "AVY",
           "BHGE",
           "BLL",
           "BAC",
           "BAX",
           "BBT",
           "BDX",
           "BBBY",
           "BRK-B",
           "BBY",
           "BIIB",
           "BLK",
           "HRB",
           "BA",
           "BWA",
           "BXP",
           "BSX",
           "BMY",
           "AVGO",
           "BF-B",
           "CHRW",
           "CA",
           "COG",
           "CPB",
           "COF",
           "CAH",
           "KMX",
           "CCL",
           "CAT",
           "CBOE",
           "CBS",
           "CELG",
           "CNC",
           "CNP",
           "CTL",
           "CERN",
           "CF",
           "SCHW",
           "CHTR",
           "CHK",
           "CVX",
           "CMG",
           "CB",
           "CHD",
           "CI",
           "XEC",
           "CINF",
           "CTAS",
           "CSCO",
           "C",
           "CFG",
           "CTXS",
           "CME",
           "CMS",
           "TPR",
           "KO",
           "CTSH",
           "CL",
           "CMCSA",
           "CMA",
           "CAG",
           "CXO",
           "COP",
           "ED",
           "STZ",
           "GLW",
           "COST",
           "COTY",
           "CCI",
           "CSX",
           "CMI",
           "CVS",
           "DHI",
           "DHR",
           "DRI",
           "DVA",
           "DE",
           "DLPH",
           "DAL",
           "XRAY",
           "DVN",
           "DLR",
           "DFS",
           "DISCA",
           "DISCK",
           "DG",
           "DLTR",
           "D",
           "DOV",
           "DWDP",
           "DPS",
           "DTE",
           "DUK",
           "DNB",
           "ETFC",
           "EMN",
           "ETN",
           "EBAY",
           "ECL",
           "EIX",
           "EW",
           "EA",
           "EMR",
           "ETR",
           "EVHC",
           "EOG",
           "EQT",
           "EFX",
           "EQIX",
           "EQR",
           "ESS",
           "EL",
           "ES",
           "EXC",
           "EXPE",
           "EXPD",
           "ESRX",
           "EXR",
           "XOM",
           "FFIV",
           "FB",
           "FAST",
           "FRT",
           "FDX",
           "FIS",
           "FITB",
           "FSLR",
           "FE",
           "FISV",
           "FLIR",
           "FLS",
           "FLR",
           "FMC",
           "FTI",
           "FL",
           "F",
           "FBHS",
           "BEN",
           "FCX",
           "FTR",
           "GPS",
           "GRMN",
           "GD",
           "GE",
           "GGP",
           "GIS",
           "GM",
           "GPC",
           "GILD",
           "GPN",
           "GS",
           "GT",
           "GWW",
           "HAL",
           "HBI",
           "HOG",
           "HRS",
           "HIG",
           "HAS",
           "HCA",
           "HCP",
           "HP",
           "HSIC",
           "HES",
           "HOLX",
           "HD",
           "HON",
           "HRL",
           "HST",
           "HPQ",
           "HUM",
           "HBAN",
           "IDXX",
           "ITW",
           "ILMN",
           "INCY",
           "IR",
           "INTC",
           "ICE",
           "IBM",
           "IP",
           "IPG",
           "IFF",
           "INTU",
           "ISRG",
           "IVZ",
           "IRM",
           "JBHT",
           "JEC",
           "SJM",
           "JNJ",
           "JCI",
           "JPM",
           "JNPR",
           "KSU",
           "K",
           "KEY",
           "KMB",
           "KIM",
           "KMI",
           "KLAC",
           "KSS",
           "KR",
           "LB",
           "LLL",
           "LH",
           "LRCX",
           "LEG",
           "LEN",
           "LUK",
           "LLY",
           "LNC",
           "LKQ",
           "LMT",
           "L",
           "LOW",
           "LYB",
           "MTB",
           "MAC",
           "M",
           "MNK",
           "MRO",
           "MPC",
           "MAR",
           "MMC",
           "MLM",
           "MAS",
           "MA",
           "MAT",
           "MKC",
           "MCD",
           "MCK",
           "MDT",
           "MRK",
           "MET",
           "MTD",
           "KORS",
           "MCHP",
           "MU",
           "MSFT",
           "MAA",
           "MHK",
           "TAP",
           "MDLZ",
           "MON",
           "MNST",
           "MCO",
           "MS",
           "MSI",
           "MUR",
           "MYL",
           "NDAQ",
           "NOV",
           "NAVI",
           "NTAP",
           "NFLX",
           "NWL",
           "NFX",
           "NEM",
           "NWSA",
           "NWS",
           "NEE",
           "NLSN",
           "NKE",
           "NI",
           "NBL",
           "JWN",
           "NSC",
           "NTRS",
           "NOC",
           "NRG",
           "NUE",
           "NVDA",
           "ORLY",
           "OXY",
           "OMC",
           "OKE",
           "ORCL",
           "PCAR",
           "PH",
           "PDCO",
           "PAYX",
           "PYPL",
           "PNR",
           "PBCT",
           "PEP",
           "PKI",
           "PRGO",
           "PFE",
           "PCG",
           "PM",
           "PSX",
           "PNW",
           "PXD",
           "PNC",
           "RL",
           "PPG",
           "PPL",
           "PX",
           "PCLN",
           "PFG",
           "PG",
           "PGR",
           "PLD",
           "PRU",
           "PEG",
           "PSA",
           "PHM",
           "PVH",
           "QRVO",
           "QCOM",
           "PWR",
           "DGX",
           "RRC",
           "RTN",
           "O",
           "RHT",
           "REG",
           "REGN",
           "RF",
           "RSG",
           "RAI",
           "RHI",
           "ROK",
           "COL",
           "ROP",
           "ROST",
           "RCL",
           "R",
           "SPGI",
           "CRM",
           "SCG",
           "SLB",
           "SNI",
           "STX",
           "SEE",
           "SRE",
           "SHW",
           "SIG",
           "SPG",
           "SWKS",
           "SLG",
           "SNA",
           "SO",
           "LUV",
           "SWN",
           "SWK",
           "SPLS",
           "SBUX",
           "STT",
           "SRCL",
           "SYK",
           "STI",
           "SYMC",
           "SYF",
           "SYY",
           "TROW",
           "TGT",
           "TEL",
           "TGNA",
           "TDC",
           "TSO",
           "TXN",
           "TXT",
           "BK",
           "CLX",
           "COO",
           "HSY",
           "MOS",
           "TRV",
           "DIS",
           "TMO",
           "TIF",
           "TWX",
           "TJX",
           "TMK",
           "TSS",
           "TSCO",
           "TDG",
           "RIG",
           "TRIP",
           "FOXA",
           "FOX",
           "TSN",
           "USB",
           "UDR",
           "ULTA",
           "UA",
           "UAA",
           "UNP",
           "UAL",
           "UNH",
           "UPS",
           "URI",
           "UTX",
           "UHS",
           "UNM",
           "URBN",
           "VFC",
           "VLO",
           "VAR",
           "VTR",
           "VRSN",
           "VRSK",
           "VZ",
           "VRTX",
           "VIAB",
           "V",
           "VNO",
           "VMC",
           "WMT",
           "WBA",
           "WM",
           "WAT",
           "WEC",
           "WFC",
           "HCN",
           "WDC",
           "WU",
           "WY",
           "WHR",
           "WFM",
           "WMB",
           "WLTW",
           "WYN",
           "WYNN",
           "XEL",
           "XRX",
           "XLNX",
           "XL",
           "XYL",
           "YHOO",
           "YUM",
           "ZBH",
           "ZION",
           "ZTS"]


#pip install pandas-datareader --upgrade

def stockDownloader(tickers):
    """
    Function to download stock prices from Yahoo!.
    Args:
        param1: list of tickers and data - column to download
    Returns:
        A Dataframe of stock prices for the tickers .
    """
    d = pd.date_range(start, end, freq='D')
    stockData = pd.DataFrame(index=d)
    for tick in tickers:
        try:
            result = web.DataReader(tick, 'yahoo',start, end)["Close"]
            result = pd.DataFrame(result)
            result.columns = [tick]
            stockData = pd.concat([stockData, result], axis=1, join='outer')
        except BaseException:
            pass

    return stockData

if __name__ == "__main__":
    
    start = '2021-01-01'
    end = '2021-07-27'
    final = stockDownloader(sp)
    final=final.pct_change()
    final.dropna(inplace=True)
    tickers = final.columns
    print(final.head())
    
    """
    Version to Maximize Risk-Adjusted Return
    """
    
    
    np.random.seed(1)
    n = len(final.columns)
    
    
    mu = np.array((final.mean()) *252) 
    Sigma = np.random.randn(n,n)
    Sigma = Sigma.T.dot(Sigma)
    
    
    #Portfolio optimization.
    
    w = cp.Variable(n)
    gamma = cp.Parameter(nonneg=True)
    ret = mu.T@w
    risk = cp.quad_form(w, Sigma)
    prob = cp.Problem(cp.Maximize(ret - gamma*risk),[cp.sum(w) == 1, w >= 0,ret >= 0.2])
    
    
    SAMPLES = 100
    risk_data = np.zeros(SAMPLES)
    ret_data = np.zeros(SAMPLES)
    gamma_vals = np.logspace(-2, 3, num=SAMPLES)
    for i in range(SAMPLES):
        gamma.value = gamma_vals[i]
        prob.solve()
        risk_data[i] = cp.sqrt(risk).value
        ret_data[i] = ret.value
        
    
    
    # Print Results:
    symbols = final.columns
    
    print("----------------------")
    print("Optimal Portfolio - Maximize Risk Adjusted Returns")
    print("----------------------")
    for x in range(len(symbols)):
        print('%s = %f' %(symbols[x],w.value[x]))
    print("----------------------")
    print('Exp Ret = %f' %(ret.value))
    print('Risk    = %f' %((risk.value)**0.5))
    print('Sharpe Ratio    = %f' %(ret.value/(risk.value)**0.5))
    print("----------------------")
    
    
    """
    Version to Minimize RIsk
    """
    np.random.seed(1)
    n = len(final.columns)
    
    
    mu = np.array((final.mean()) *252) 
    Sigma = np.random.randn(n,n)
    Sigma = Sigma.T.dot(Sigma)
    
    
    #Portfolio optimization.
    
    w = cp.Variable(n)
    gamma = cp.Parameter(nonneg=True)
    ret = mu.T@w
    risk = cp.quad_form(w, Sigma)
    
    prob = cp.Problem(cp.Minimize(risk), [cp.sum(w) == 1,ret >= 0.2])
    
    SAMPLES = 100
    risk_data = np.zeros(SAMPLES)
    ret_data = np.zeros(SAMPLES)
    gamma_vals = np.logspace(-2, 3, num=SAMPLES)
    for i in range(SAMPLES):
        gamma.value = gamma_vals[i]
        prob.solve()
        risk_data[i] = cp.sqrt(risk).value
        ret_data[i] = ret.value
        

    
    # Print Results:
    symbols = final.columns
    
    print("----------------------")
    print("Optimal Portfolio - Minimize Risk")
    print("----------------------")
    for x in range(len(symbols)):
        print('%s = %f' %(symbols[x],w.value[x]))
    print("----------------------")
    print('Exp Ret = %f' %(ret.value))
    print('Risk    = %f' %((risk.value)**0.5))
    print('Sharpe Ratio    = %f' %(ret.value/(risk.value)**0.5))
    print("----------------------")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
