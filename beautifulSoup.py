#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 21:01:49 2019

@author: oluwaseyiawoga
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

type_ = 'losers'

urlToUse = f'https://finance.yahoo.com/{type_}?offset=0&count=100'

def getUrlIntoSoup(urlToUse):
    url = requests.get(urlToUse).content
    soup = BeautifulSoup(url,'lxml')
    results = soup.find('div', attrs={"id":"scr-res-table"})
    return results

results = getUrlIntoSoup(urlToUse)


def getSymbols(results):
    a = results.findAll('a')
    sym = []
    for x in range(len(a)):
        sym.append(a[x].get('href').split("=",1)[1])
    return sym

sym = getSymbols(results)
    

def getCompanyNames(results):    
    a = results.findAll('a')
    title=[]
    for x in a:
        soup = BeautifulSoup(str(x), 'html5lib')
        title.append(soup.find('a').attrs['title'])
    return title

title = getCompanyNames(results)


def getMetrics(results):
    c=results.findAll('span')
    result = []
    c = c[10:]
    
    w = []
    for x in range(len(c)):
        q=BeautifulSoup(str(c[x]),   'html5lib')
        if q.find('span').text == 'N/A':
            pass
        else:
            b = q.find('span')
            a = b.attrs
            if "class" in [*a] and b['class'][0] == "Trsdu(0.3s)":
                w.append(c[x])
        
    chunks = [w[x:x+5] for x in range(0, len(w), 5)]
    result = []
    
    for x in range(0,len(chunks)):
        temp = []
        print(x)
        price = BeautifulSoup(str(chunks[x][0]),'html5lib')
        change = BeautifulSoup(str(chunks[x][1]),'html5lib')
        changePct = BeautifulSoup(str(chunks[x][2]),'html5lib')
        Volume = BeautifulSoup(str(chunks[x][3]),'html5lib')
        Mkt_Value = BeautifulSoup(str(chunks[x][4]),'html5lib')
        
        
        priceSoup = price.find('span').text
        changeSoup = change.find('span').text
        changePctSoup = changePct.find('span').text
        volumesoup = Volume.find('span').text
        try:
            Mkt_ValueSoup = Mkt_Value.find('span').text
        except:
            Mkt_ValueSoup = "N/A"
       
        temp.append(priceSoup)
        temp.append(changeSoup)
        temp.append(changePctSoup)
        temp.append(volumesoup)
        temp.append(Mkt_ValueSoup)
        #temp.append(x)
        result.append(temp)
    return result
   

result =  getMetrics(results)

def getFinalDF(result):
    moversYahoo = pd.DataFrame()
    moversYahoo["Symbol"] = sym
    moversYahoo["Company"] = title
    moversYahoo = pd.concat([moversYahoo, pd.DataFrame(result, columns=['Price','Change','ChangePct','Volume','Mkt_Value'])], axis=1)
    return moversYahoo[['Symbol', 'Price', 'Change', 'ChangePct', 'Volume','Mkt_Value']]

finalDF = getFinalDF(result)
print()
print(f"Yahoo! Finance {type_.title()} - BeautifulSoup Webscraping")
print()
print(finalDF)

#finalDF["Change"]= finalDF["Change"].astype(float)
#finalDF['ChangePct'] = finalDF['ChangePct'].str.replace('%', '')
#finalDF['ChangePct'] = finalDF['ChangePct'].astype(float)
#finalDF['Volume'] = finalDF['Volume'].str.replace('M', '')
#finalDF['Volume'] = finalDF['Volume'].str.replace(',', '')
#finalDF['Volume'] = finalDF['Volume'].astype(float) 
