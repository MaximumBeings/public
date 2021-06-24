"
Using R Programming Language to Test Hypothesis of Two Sample Populations (Part 4 of 6)

(1) Pick two separate corporations from www.nasdaq.com, and download the opening stock prices for the stocks from 2016. Calculate daily returns of the DJIA index and the downloaded stocks over the period under study.

(2) Determine a claim (prior to analyzing the descriptive statistics) based on two population means/samples.  (For example - CLAIM: There are no differences in the prices of Adobe and Amzn Stocks during the period under study:  Use alpha=0.05).

(3) Plot the stock returns in a simple graph without using any library.

(4) Conduct the hypothesis testing based on the claim in item 2 above. Outline all the specifics in 
A Word document describing your conclusion. Note any possible reasons for the results. This might include some research on the corporations chosen in item 1. Follow the following steps to conduct your hypothesis:

(a) Write down a shortened version of the claim
(b) Come up with null and alternate hypothesis (Ho always has the equals part on it)
(c) Determine if claim matches Ho or H1
(d) Find p-value using R
(e) If p-value is less than alpha, Reject Ho.  If p-value is greater then alpha Accept Ho. 
"
#import libraries and packages - do this once.

#install.packages("PerformanceAnalytics")
#install.packages("quantmod")
#install.packages("dygraphs")

# Import data directly into R from Yahoo Finance
# for ADOBE Composite (ADBE Ticker)
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

# Use the function the daily returns to calculate the daily returns of the two stocks,
daily_stock_returns('AMZN', year)
daily_stock_returns('AMZN', year)

# 2. Determine a claim (prior to analyzing the descriptive statistics) 
# based on two population means/samples.


# Merge the monthly return xts objects into 1 xts object.
merged_returns <- merge.xts(AMZN, AAPL)

#Preview the monthly returns for DJIA and the 30 Compoenent stock tickers
head(merged_returns)
# CLAIM: There is no difference in the prices of Adobe and Amzn Stocks:  Use alpha=0.05

merged_returns <- merged_returns[complete.cases(merged_returns), ] 
tail(merged_returns)

#Get Descriptive Statistics of the Stocks

summary(merged_returns$AMZN )
summary(merged_returns$AAPL )


#Plot the stock price in a simple graph without using any library
#For the last one year using line plot

plot(merged_returns$AAPL, type = "l", col = "red", xlab = "Date", ylab = "Price",
     main = "APPLE (AAPL)")

plot(merged_returns$AMZN, type = "l", col = "red", xlab = "Date", ylab = "Price",
     main = "AMAZON (AMZN)")



hist(merged_returns$AMZN, # histogram
     col = "peachpuff", # column color
     border = "black", 
     right = FALSE,
     prob = TRUE, # show densities instead of frequencies
     xlim = c(-0.06,0.06),
     ylim = c(0,65),
     xlab = "Returns",
     ylab = "Frequency",
     main = "Histogram of Amazon Returns")
lines(density(merged_returns$AMZN), # density plot
      lwd = 2, # thickness of line
      col = "black")

abline(v = mean(merged_returns$AMZN),
       col = "royalblue",
       lwd = 2)

abline(v = median(merged_returns$AMZN),
       col = "red",
       lwd = 2)

abline(v = sd(merged_returns$AMZN),
       col = "green",
       lwd = 2)

legend(x = "topright", # location of legend within plot area
       c("Density plot", "Mean", "Median","Standard Deviation"),
       col = c("gray", "royalblue", "red","green"),
       lwd = c(2, 2, 2))


hist(merged_returns$AAPL, # histogram
     col = "peachpuff", # column color
     border = "black", 
     right = FALSE,
     prob = TRUE, # show densities instead of frequencies
     xlim = c(-0.06,0.06),
     ylim = c(0,65),
     xlab = "Returns",
     ylab = "Frequency",
     main = "Histogram of Apple Returns")
lines(density(merged_returns$AAPL), # density plot
      lwd = 2, # thickness of line
      col = "black")

abline(v = mean(merged_returns$AAPL),
       col = "royalblue",
       lwd = 2)

abline(v = median(merged_returns$AAPL),
       col = "red",
       lwd = 2)

abline(v = sd(merged_returns$AAPL),
       col = "green",
       lwd = 2)

legend(x = "topright", # location of legend within plot area
       c("Density plot", "Mean", "Median","Standard Deviation"),
       col = c("gray", "royalblue", "red","green"),
       lwd = c(2, 2, 2))



amzn_sample <- merged_returns$AMZN[sample(nrow(AMZN), 30), ]

aapl_sample <- merged_returns$AAPL[sample(nrow(AAPL), 30), ]

summary(adbe_sample)
summary(amzn_sample)


write.csv(aapl_sample, file = "aapl_sample_Returns.csv")

write.csv(amzn_sample, file = "amzn_sample_Returns.csv")

# Conduct the hypothesis test based on the claim from item 2. Outline all the specifics in 
# the Word document describing your conclusion. Note any possible reasons for the results. 
# This might include some research on the corporations chosen in item 1.

# #Steps (P-Value technology)
# 1. Write down a shortened version of the claim
# 2. Come up with null and alternate hypothesis (Ho always has the equals part on it)
# 3. See if claim matches Ho or H1
# 4. Find p-value using technology
# 5. If p-value is less than alpha, Reject Ho.  If p-value
# is greater then alpha , Accept Ho.  Determine the claim based on step 3
# 


# CLAIM
# U1 > U2
# Ho: U1 = U2
# H1: U1 > U2

#Claiim matches Ho.

#In R "Two Tails

alpha = 0.05
n1 = length(aapl_sample)
xbar1 = mean(aapl_sample)
s1 = sd(aapl_sample)
alpha

n2 = length(amzn_sample)
xbar2 = mean(amzn_sample)
s2 = sd(amzn_sample)

# n is the smaller of n1 and n2
n = min(n1,n2)

ts = ((xbar1-xbar2)-(0-0))/sqrt(s1^2/n1+s2^2/n2)

p_value =  pt(ts,df=n-1,lower.tail=FALSE)

format(p_value,scientific=FALSE)



# p-value is less than alpha so we fail to accept claim Ho
# 
# Accept H1
#   
# Since claim matches H1, reject claim

