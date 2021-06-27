#Case Study Questions:

#None


#import libraries and packages - do this once.

#install.packages("PerformanceAnalytics")
#install.packages("quantmod")
#install.packages("dygraphs")

#Load libraries and packages - do this once per session.

library(PerformanceAnalytics)
library(quantmod)
library(dygraphs)

# Function to calculate daily returns on a stock 
daily_stock_returns <- function(ticker, start_year) {
  # Download the data from Yahoo finance
  symbol <- getSymbols(ticker, src = 'yahoo', auto.assign = FALSE, warnings = FALSE) 
  # Tranform it to monthly returns using the periodReturn function from quantmod
  data <- periodReturn(symbol, period = 'daily', subset=paste(start_year, "::", sep = ""), 
                       type = 'log')
  
  # Let's rename the column of returns to something intuitive because the column name is what
  # will eventually be displayed on the time series graph.
  colnames(data) <- as.character(ticker)
  
  # We want to be able to work with the xts objects that result from this function 
  # so let's explicitly put them to the global environment with an easy to use 
  # name, the stock ticker.
  assign(ticker, data, .GlobalEnv)
}



# Calculate daily returns of the DJIA index and the downloaded stocks over the period under study
# Choose the starting year and assign it to the 'year' variable.
year <- 2016

# Use the function the daily returns on DJIA and the 30 component stocks, and pass in the 'year' value
daily_stock_returns('DJIA', year)
daily_stock_returns('AAPL', year)
daily_stock_returns('AXP', year)
daily_stock_returns('BA', year)
daily_stock_returns('CAT', year)
daily_stock_returns('CSCO', year)
daily_stock_returns('CVX', year)
daily_stock_returns('KO', year)
daily_stock_returns('DD', year)
daily_stock_returns('XOM', year)
daily_stock_returns('GE', year)
daily_stock_returns('GS', year)
daily_stock_returns('HD', year)
daily_stock_returns('IBM', year)
daily_stock_returns('INTC', year)
daily_stock_returns('JNJ', year)
daily_stock_returns('JPM', year)
daily_stock_returns('MCD', year)
daily_stock_returns('MMM', year)
daily_stock_returns('MSFT', year)
daily_stock_returns('NKE', year)
daily_stock_returns('MRK', year)
daily_stock_returns('PFE', year)
daily_stock_returns('PG', year)
daily_stock_returns('TRV', year)
daily_stock_returns('UNH', year)
daily_stock_returns('AAPL', year)
daily_stock_returns('V', year)
daily_stock_returns('VZ', year)
daily_stock_returns('WMT', year)
daily_stock_returns('DIS', year)

# Merge the monthly return xts objects into 1 xts object.
merged_returns <- merge.xts(DJIA, AAPL, AXP, BA, CAT, CSCO, MRK, CVX, KO, DD, XOM, GE, GS, HD, IBM, INTC, JNJ, JPM, MCD, MMM, MSFT, NKE, PFE, PG, TRV, UNH, AAPL, V,VZ,WMT,DIS)

#Preview the monthly returns for DJIA and the 30 Compoenent stock tickers
head(merged_returns)


#ASSUME DJIA is explanatory variale and individual stock is the response variable

#First Approach To Calculatung Linear Regression

r2s <- apply(merged_returns, 2, function(x) summary(lm(x ~ DJIA )))

r2s

#Second Approach To Calculatung Linear Redression

intercepts <- c()

beta <- c()

tracker <- c()

for (x in 2:31)
{
 
x <- coef(lm( merged_returns[,x] ~ merged_returns$DJIA))
intercepts <- cbind(intercepts, x[1] )
beta <- cbind(beta, x[2] )
tracker <- cbind(tracker, x)
}
  
tracker
intercepts
beta

plot(intercepts,beta,xlab = "Alpha", ylab = "Beta",
     main = "Alpha Versus Beta - DOW JONES & COMPONENT STOCKS")


#Third Approach To Calculatung Linear Redression

myRegressor<-function(index) {coef(lm(merged_returns[,index]~merged_returns$DJIA))}

result <- lapply(2:31,FUN=myRegressor)

result


#ASSUME DJIA is response variale and individual stock is the explanatory variable

#First Approach To Calculatung Linear Regression

r2s <- apply(merged_returns, 2, function(x) summary(lm(DJIA~x )))

r2s

#Second Approach To Calculatung Linear Redression

intercepts <- c()

beta <- c()

tracker <- c()

for (x in 2:31)
{
  
  x <- coef(lm( merged_returns$DJIA~merged_returns[,x]))
  intercepts <- cbind(intercepts, x[1] )
  beta <- cbind(beta, x[2] )
  tracker <- cbind(tracker, x)
}

tracker
intercepts
beta

plot(intercepts,beta,xlab = "Alpha", ylab = "Beta",
     main = "Alpha Versus Beta - DOW JONES & COMPONENT STOCKS")


#Third Approach To Calculatung Linear Redression

myRegressor<-function(index) {coef(lm(merged_returns$DJIA~merged_returns[,index]))}

result <- lapply(2:31,FUN=myRegressor)

result



