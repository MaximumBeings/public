#Case Study Questions:

# 1. What factors account for the tracking error of the constructed portfolios?

# The size or number of stocks relative to the number of stocks in the index is a big factor
# Differences in the weightings of the assets versus the index
#The management fees, custodial fees, brokerage costs and other expenses affecting the portfolio that don't affect the benchmark
#The volatility of the benchmark


# 2. What is the relationship between tracking error and portfolio sample size?
# There is an inverse relationship between tracking errors and sample size as depicted in the graph.


# 3. What might be the most optimal way to decrease tracking error without having to 
#construct a full portfolio matching the entire index

# Use the same weighting as the index
#Use exchange traded notes
#mimic the component stocks of the index as much as possible



# Download data for last 3 years for the DJIA (Dow Jones Industrial Average) and each of the 30 
# component stocks. You could either manually download them from Yahoo! Finance into CSV files 
# or use an R method to fetch the data directly from Yahoo.


#import libraries and packages - do this once.

#install.packages("PerformanceAnalytics")
#install.packages("quantmod")
#install.packages("dygraphs")

#Load libraries and packages - do this once per session.

library(PerformanceAnalytics)
library(quantmod)
library(dygraphs)

# Function to calculate monthly returns on a stock 
monthly_stock_returns <- function(ticker, start_year) {
  # Download the data from Yahoo finance
  symbol <- getSymbols(ticker, src = 'yahoo', auto.assign = FALSE, warnings = FALSE) 
  # Tranform it to monthly returns using the periodReturn function from quantmod
  data <- periodReturn(symbol, period = 'monthly', subset=paste(start_year, "::", sep = ""), 
                       type = 'log')
  
  # Let's rename the column of returns to something intuitive because the column name is what
  # will eventually be displayed on the time series graph.
  colnames(data) <- as.character(ticker)
  
  # We want to be able to work with the xts objects that result from this function 
  # so let's explicitly put them to the global environment with an easy to use 
  # name, the stock ticker.
  assign(ticker, data, .GlobalEnv)
}



# Calculate Monthly returns of the DJIA index and the downloaded stocks over the period under study
# Choose the starting year and assign it to the 'year' variable.
year <- 2014

# Use the function the monthly returns on DJIA and the 30 component stocks, and pass in the 'year' value
# Let's choose MSFT, YHOO, ORCL, EBAY, CSCO; after you run these functions, have 
# a look at the global environment and make sure your three xts objects are there
monthly_stock_returns('DJIA', year)
monthly_stock_returns('AAPL', year)
monthly_stock_returns('AXP', year)
monthly_stock_returns('BA', year)
monthly_stock_returns('CAT', year)
monthly_stock_returns('CSCO', year)
monthly_stock_returns('CVX', year)
monthly_stock_returns('KO', year)
monthly_stock_returns('DD', year)
monthly_stock_returns('XOM', year)
monthly_stock_returns('GE', year)
monthly_stock_returns('GS', year)
monthly_stock_returns('HD', year)
monthly_stock_returns('IBM', year)
monthly_stock_returns('INTC', year)
monthly_stock_returns('JNJ', year)
monthly_stock_returns('JPM', year)
monthly_stock_returns('MCD', year)
monthly_stock_returns('MMM', year)
monthly_stock_returns('MSFT', year)
monthly_stock_returns('NKE', year)
monthly_stock_returns('PFE', year)
monthly_stock_returns('PG', year)
monthly_stock_returns('TRV', year)
monthly_stock_returns('UNH', year)
monthly_stock_returns('AAPL', year)
monthly_stock_returns('V', year)
monthly_stock_returns('VZ', year)
monthly_stock_returns('WMT', year)
monthly_stock_returns('DIS', year)

# Merge the monthly return xts objects into 1 xts object.
merged_returns <- merge.xts(DJIA, AAPL, AXP, BA, CAT, CSCO, CVX, KO, DD, XOM, GE, GS, HD, IBM, INTC, JNJ, JPM, MCD, MMM, MSFT, NKE, PFE, PG, TRV, UNH, AAPL, V,VZ,WMT,DIS)

#Preview the monthly returns for DJIA and the 30 Compoenent stock tickers
head(merged_returns)

merged_returns <- merged_returns[complete.cases(merged_returns), ] 
tail(merged_returns)

# DJIA        AAPL         AXP          BA         CAT         CSCO         CVX           KO
# 2014-01-31 -0.054408255 -0.11394922 -0.06500161 -0.08585980  0.03356753 -0.023456195 -0.11240371 -0.088266562
# 2014-02-28  0.038908685  0.04995000  0.07104521  0.02880045  0.03206474 -0.005033230  0.03260780  0.009997479
# 2014-03-31  0.008294911  0.01975642 -0.01378876 -0.02696598  0.02444862  0.028043494  0.03056934  0.011969932
# 2014-04-30  0.007456771  0.09476128 -0.02930446  0.02774140  0.05891237  0.030312050  0.05409815  0.053631504
# 2014-05-30  0.008188528  0.07019541  0.04550050  0.04715746 -0.03053745  0.063293694 -0.02198950  0.002937554
# 2014-06-30  0.006524614 -1.91862392  0.03616859 -0.06112842  0.06109054  0.009298591  0.06128073  0.034830012
# DD         XOM           GE            GS           HD         IBM         INTC
# 2014-01-31 -0.062887857 -0.09357249 -0.109213089 -7.701972e-02 -0.069001524 -0.05981200 -0.056252373
# 2014-02-28  0.087967065  0.04363047  0.013438938  1.409711e-02  0.065229578  0.04693416  0.008924968
# 2014-03-31  0.007179226  0.01454012  0.016355505 -1.574353e-02 -0.035992990  0.03876992  0.041532527
# 2014-04-30  0.003273325  0.04728757  0.037897678 -2.490319e-02  0.004790793  0.02046552  0.033527026
# 2014-05-30  0.029131827 -0.01852822 -0.003725712 -6.262866e-05  0.009014722 -0.06361938  0.023330034
# 2014-06-30 -0.057455549  0.00149099 -0.019220489  4.663949e-02  0.009057646 -0.01690272  0.123137149
# JNJ          JPM           MCD          MMM        MSFT          NKE           PFE
# 2014-01-31 -0.034658529 -0.054827486 -0.0299185604 -0.089912990  0.01142870 -0.076477958 -0.0075372798
# 2014-02-28  0.040428585  0.026031047  0.0103529765  0.049759192  0.01234424  0.072145136  0.0547249308
# 2014-03-31  0.064219591  0.066220036  0.0298189293  0.006879039  0.06761720 -0.058376218  0.0003113187
# 2014-04-30  0.030676001 -0.081113929  0.0336022594  0.024969392 -0.01449835 -0.012397189 -0.0264999103
# 2014-05-30  0.001676923 -0.007350997  0.0004931019  0.024571660  0.01327772  0.052861725 -0.0541916198
# 2014-06-30  0.030670144  0.036226225 -0.0068259849  0.004828744  0.01839360  0.008286969  0.0016860905
# PG          TRV         UNH          AAPL           V            VZ           WMT
# 2014-01-31 -0.06063999 -0.107891782 -0.04093272  0.001931297 -0.03309973 -0.0230557559 -0.0523037893
# 2014-02-28  0.02627664  0.031010201  0.06675829  0.025970989  0.04763349 -0.0092050439  0.0002677333
# 2014-03-31  0.02436381  0.014916839  0.05929152 -0.001539391 -0.04563943 -0.0002102365  0.0228952373
# 2014-04-30  0.02390558  0.062406448 -0.08857595  0.012671905 -0.06334710 -0.0178159537  0.0420197466
# 2014-05-30 -0.02155100  0.031193042  0.05936955 -0.017992393  0.05856407  0.0668363085 -0.0375811361
# 2014-06-30 -0.02760879  0.006612684  0.02627494 -0.006647445 -0.01936421 -0.0208319599 -0.0223928882
# DIS
# 2014-01-31 -0.050880055
# 2014-02-28  0.106998028
# 2014-03-31 -0.009199443
# 2014-04-30 -0.009158887
# 2014-05-30  0.057193499
# 2014-06-30  0.020383575


#3 - Calculate mean and standard deviation of monthly returns for the DJIA index
meanDJIA <- mean(merged_returns$DJIA)
meanDJIA

sdDJIA <- sd(merged_returns$DJIA)
sdDJIA

# Choose an equal weighted portfolio consisting of any 5 random stocks from the DJIA, 
# calculate the mean monthly returns and its standard deviation. Do the same for portfolios 
# of 10,15, 20 and 25 random stocks from the DJIA universe

# Subset Five .
subSetfive <- subset(merged_returns, select=c('AAPL','AXP','BA','CAT','CSCO'))

head(subSetfive)

# AAPL         AXP          BA         CAT         CSCO
# 2014-01-31 -0.11394922 -0.06500161 -0.08585980  0.03356753 -0.023456195
# 2014-02-28  0.04995000  0.07104521  0.02880045  0.03206474 -0.005033230
# 2014-03-31  0.01975642 -0.01378876 -0.02696598  0.02444862  0.028043494
# 2014-04-30  0.09476128 -0.02930446  0.02774140  0.05891237  0.030312050
# 2014-05-30  0.07019541  0.04550050  0.04715746 -0.03053745  0.063293694
# 2014-06-30 -1.91862392  0.03616859 -0.06112842  0.06109054  0.009298591




#Weight for sub portfoliio of five returns
w <- c(1/5.0, 1/5.0, 1/5.0, 1/5.0, 1/5.0)

portfolio_subSetfive <- Return.portfolio(subSetfive, weights = w)

portfolio_subSetfive <- cbind(subSetfive,portfolio_subSetfive)

names(portfolio_subSetfive)[6]<-paste("Port_Returns_5")

head(portfolio_subSetfive)

#             AAPL         AXP          BA         CAT         CSCO         Port_Returns_5
# 2014-01-31 -0.11394922 -0.06500161 -0.08585980  0.03356753 -0.023456195   -0.050939858
# 2014-02-28  0.04995000  0.07104521  0.02880045  0.03206474 -0.005033230    0.034821597
# 2014-03-31  0.01975642 -0.01378876 -0.02696598  0.02444862  0.028043494    0.006626145
# 2014-04-30  0.09476128 -0.02930446  0.02774140  0.05891237  0.030312050    0.036616954
# 2014-05-30  0.07019541  0.04550050  0.04715746 -0.03053745  0.063293694    0.037212088
# 2014-06-30 -1.91862392  0.03616859 -0.06112842  0.06109054  0.009298591   -0.390944821


#Standard Deviation of portfolio of 5 component stocks

sdsubSetfive <- sd(portfolio_subSetfive$Port_Returns_5)
sdsubSetfive

# SUBSET TEN .
subSetten <- subset(merged_returns, select=c('AAPL','AXP','BA','CAT','CSCO','CVX', 'KO', 'DD', 'XOM', 'GE'))

head(subSetten)

# AAPL         AXP          BA         CAT         CSCO         CVX           KO           DD         XOM           GE
# 2014-01-31 -0.11394922 -0.06500161 -0.08585980  0.03356753 -0.023456195 -0.11240371 -0.088266562 -0.062887857 -0.09357249 -0.109213089
# 2014-02-28  0.04995000  0.07104521  0.02880045  0.03206474 -0.005033230  0.03260780  0.009997479  0.087967065  0.04363047  0.013438938
# 2014-03-31  0.01975642 -0.01378876 -0.02696598  0.02444862  0.028043494  0.03056934  0.011969932  0.007179226  0.01454012  0.016355505
# 2014-04-30  0.09476128 -0.02930446  0.02774140  0.05891237  0.030312050  0.05409815  0.053631504  0.003273325  0.04728757  0.037897678
# 2014-05-30  0.07019541  0.04550050  0.04715746 -0.03053745  0.063293694 -0.02198950  0.002937554  0.029131827 -0.01852822 -0.003725712
# 2014-06-30 -1.91862392  0.03616859 -0.06112842  0.06109054  0.009298591  0.06128073  0.034830012 -0.057455549  0.00149099 -0.019220489
# 

#Weight for sub portfoliio of ten returns
w <- c(1/10.0, 1/10.0, 1/10.0, 1/10.0, 1/10.0,1/10.0, 1/10.0, 1/10.0, 1/10.0, 1/10.0)

portfolio_subSetten <- Return.portfolio(subSetten, weights = w)

portfolio_subSetten <- cbind(subSetten,portfolio_subSetten)

names(portfolio_subSetten)[11]<-paste("Port_Returns_10")

head(portfolio_subSetten)

#                  AAPL         AXP          BA         CAT         CSCO         CVX           KO           DD         XOM           GE Port_Returns_10
# 2014-01-31 -0.11394922 -0.06500161 -0.08585980  0.03356753 -0.023456195 -0.11240371 -0.088266562 -0.062887857 -0.09357249 -0.109213089     -0.07210430
# 2014-02-28  0.04995000  0.07104521  0.02880045  0.03206474 -0.005033230  0.03260780  0.009997479  0.087967065  0.04363047  0.013438938      0.03634575
# 2014-03-31  0.01975642 -0.01378876 -0.02696598  0.02444862  0.028043494  0.03056934  0.011969932  0.007179226  0.01454012  0.016355505      0.01117048
# 2014-04-30  0.09476128 -0.02930446  0.02774140  0.05891237  0.030312050  0.05409815  0.053631504  0.003273325  0.04728757  0.037897678      0.03759847
# 2014-05-30  0.07019541  0.04550050  0.04715746 -0.03053745  0.063293694 -0.02198950  0.002937554  0.029131827 -0.01852822 -0.003725712      0.01779220
# 2014-06-30 -1.91862392  0.03616859 -0.06112842  0.06109054  0.009298591  0.06128073  0.034830012 -0.057455549  0.00149099 -0.019220489     -0.20075382

#Standard Deviation of portfolio of 10 component stocks

sdsubSetten <- sd(portfolio_subSetten$Port_Returns_10)
sdsubSetten


# SUBSET FIFTEEN .
subSetfifteen <- subset(merged_returns, select=c('AAPL','AXP','BA','CAT','CSCO','CVX', 'KO', 'DD', 'XOM', 'GE','GS', 'HD', 'IBM', 'INTC', 'JNJ'))

head(subSetfifteen)

# AAPL         AXP          BA         CAT         CSCO         CVX           KO           DD         XOM           GE            GS           HD         IBM         INTC          JNJ
# 2014-01-31 -0.11394922 -0.06500161 -0.08585980  0.03356753 -0.023456195 -0.11240371 -0.088266562 -0.062887857 -0.09357249 -0.109213089 -7.701972e-02 -0.069001524 -0.05981200 -0.056252373 -0.034658529
# 2014-02-28  0.04995000  0.07104521  0.02880045  0.03206474 -0.005033230  0.03260780  0.009997479  0.087967065  0.04363047  0.013438938  1.409711e-02  0.065229578  0.04693416  0.008924968  0.040428585
# 2014-03-31  0.01975642 -0.01378876 -0.02696598  0.02444862  0.028043494  0.03056934  0.011969932  0.007179226  0.01454012  0.016355505 -1.574353e-02 -0.035992990  0.03876992  0.041532527  0.064219591
# 2014-04-30  0.09476128 -0.02930446  0.02774140  0.05891237  0.030312050  0.05409815  0.053631504  0.003273325  0.04728757  0.037897678 -2.490319e-02  0.004790793  0.02046552  0.033527026  0.030676001
# 2014-05-30  0.07019541  0.04550050  0.04715746 -0.03053745  0.063293694 -0.02198950  0.002937554  0.029131827 -0.01852822 -0.003725712 -6.262866e-05  0.009014722 -0.06361938  0.023330034  0.001676923
# 2014-06-30 -1.91862392  0.03616859 -0.06112842  0.06109054  0.009298591  0.06128073  0.034830012 -0.057455549  0.00149099 -0.019220489  4.663949e-02  0.009057646 -0.01690272  0.123137149  0.030670144


#Weight for sub portfoliio of fifteen returns
w <- c(1/15.0, 1/15.0, 1/15.0, 1/15.0, 1/15.0,1/15.0, 1/15.0, 1/15.0, 1/15.0, 1/15.0,1/15.0, 1/15.0, 1/15.0, 1/15.0, 1/15.0)

portfolio_subSetfifteen <- Return.portfolio(subSetfifteen, weights = w)

portfolio_subSetfifteen <- cbind(subSetfifteen,portfolio_subSetfifteen)

names(portfolio_subSetfifteen)[16]<-paste("Port_Returns_15")

head(portfolio_subSetfifteen)

#               AAPL         AXP          BA         CAT         CSCO         CVX           KO           DD         XOM           GE            GS           HD         IBM         INTC          JNJ       Port_Returns_15
# 2014-01-31 -0.11394922 -0.06500161 -0.08585980  0.03356753 -0.023456195 -0.11240371 -0.088266562 -0.062887857 -0.09357249 -0.109213089 -7.701972e-02 -0.069001524 -0.05981200 -0.056252373 -0.034658529    -0.067852475
# 2014-02-28  0.04995000  0.07104521  0.02880045  0.03206474 -0.005033230  0.03260780  0.009997479  0.087967065  0.04363047  0.013438938  1.409711e-02  0.065229578  0.04693416  0.008924968  0.040428585     0.035943372
# 2014-03-31  0.01975642 -0.01378876 -0.02696598  0.02444862  0.028043494  0.03056934  0.011969932  0.007179226  0.01454012  0.016355505 -1.574353e-02 -0.035992990  0.03876992  0.041532527  0.064219591     0.013751994
# 2014-04-30  0.09476128 -0.02930446  0.02774140  0.05891237  0.030312050  0.05409815  0.053631504  0.003273325  0.04728757  0.037897678 -2.490319e-02  0.004790793  0.02046552  0.033527026  0.030676001     0.029569297
# 2014-05-30  0.07019541  0.04550050  0.04715746 -0.03053745  0.063293694 -0.02198950  0.002937554  0.029131827 -0.01852822 -0.003725712 -6.262866e-05  0.009014722 -0.06361938  0.023330034  0.001676923     0.009755947
# 2014-06-30 -1.91862392  0.03616859 -0.06112842  0.06109054  0.009298591  0.06128073  0.034830012 -0.057455549  0.00149099 -0.019220489  4.663949e-02  0.009057646 -0.01690272  0.123137149  0.030670144    -0.122125494


#Standard Deviation of portfolio of 15 component stocks

sdportfolio_subSetfifteen <- sd(portfolio_subSetfifteen$Port_Returns_15)
sdportfolio_subSetfifteen


# SUBSET TWENTY .
subSettwenty <- subset(merged_returns, select=c('AAPL','AXP','BA','CAT','CSCO','CVX', 'KO', 'DD', 'XOM', 'GE','GS', 'HD', 'IBM', 'INTC', 'JNJ','JPM', 'MCD', 'MMM', 'MSFT', 'NKE'))

head(subSettwenty)

#Weight for sub portfoliio of twenty returns
w <- c(1/20.0, 1/20.0, 1/20.0, 1/20.0, 1/20.0,1/20.0, 1/20.0, 1/20.0, 1/20.0, 1/20.0,1/20.0, 1/20.0, 1/20.0, 1/20.0, 1/20.0,1/20.0, 1/20.0, 1/20.0, 1/20.0, 1/20.0)

portfolio_subSettwenty <- Return.portfolio(subSettwenty, weights = w)

portfolio_subSettwenty <- cbind(subSettwenty,portfolio_subSettwenty)

names(portfolio_subSettwenty)[21]<-paste("Port_Returns_20")

head(portfolio_subSettwenty)


#Standard Deviation of portfolio of 20 component stocks

sdportfolio_subSettwenty <- sd(portfolio_subSettwenty$Port_Returns_20)
sdportfolio_subSettwenty


# SUBSET TWENTY-FIVE .
subSettwentyFive <- subset(merged_returns, select=c('AAPL','AXP','BA','CAT','CSCO','CVX', 'KO', 'DD', 'XOM', 'GE','GS', 'HD', 'IBM', 'INTC', 'JNJ','JPM', 'MCD', 'MMM', 'MSFT', 'NKE','PFE', 'PG', 'TRV', 'UNH', 'AAPL'))

head(subSettwentyFive)

#Weight for sub portfoliio of twenty five returns
w <- c(1/25.0, 1/25.0, 1/25.0, 1/25.0, 1/25.0,1/25.0, 1/25.0, 1/25.0, 1/25.0, 1/25.0,1/25.0, 1/25.0, 1/25.0, 1/25.0, 1/25.0,1/25.0, 1/25.0, 1/25.0, 1/25.0, 1/25.0,1/25.0, 1/25.0, 1/25.0, 1/25.0, 1/25.0)

portfolio_subSettwentyFive <- Return.portfolio(subSettwentyFive, weights = w)

portfolio_subSettwentyFive <- cbind(subSettwentyFive,portfolio_subSettwentyFive)

names(portfolio_subSettwentyFive)[26]<-paste("Port_Returns_25")

head(portfolio_subSettwentyFive)


#Standard Deviation of portfolio of 20 component stocks

sdportfolio_subSettwentyFive <- sd(portfolio_subSettwentyFive$Port_Returns_25)
sdportfolio_subSettwentyFive

# Calculate tracking errors for each of the portfolios i.e. the margin by which the mean and standard deviation of the portfolio returns diverge from those of DJIA

TrackingError5 = sqrt(sum(merged_returns$DJIA - portfolio_subSetfive$Port_Returns_5)^2 / (length(merged_returns$DJIA) - 1)) * sqrt(12)

TrackingError10 = sqrt(sum(merged_returns$DJIA - portfolio_subSetten$Port_Returns_10)^2 / (length(merged_returns$DJIA) - 1)) * sqrt(12)

TrackingError15 = sqrt(sum(merged_returns$DJIA - portfolio_subSetfifteen$Port_Returns_15)^2 / (length(merged_returns$DJIA) - 1)) * sqrt(12)

TrackingError20 = sqrt(sum(merged_returns$DJIA - portfolio_subSettwenty$Port_Returns_20)^2 / (length(merged_returns$DJIA) - 1)) * sqrt(12)

TrackingError25 = sqrt(sum(merged_returns$DJIA - portfolio_subSettwentyFive$Port_Returns_25)^2 / (length(merged_returns$DJIA) - 1)) * sqrt(12)



# Graphically represent the tracking error for returns and risk (standard deviation of returns used as 
#a proxy for risk) on y-axis against the sample size of portfolio on the x-axis

sample_size <- c(5, 10, 15, 20, 25)
trackErrors <- c(TrackingError5, TrackingError10, TrackingError15, TrackingError20, TrackingError25)
stdDevs <- c(sdsubSetfive, sdsubSetten, sdportfolio_subSetfifteen, sdportfolio_subSettwenty,sdportfolio_subSettwentyFive )

sample_size
trackErrors
stdDevs
myColors <- c("red", "darkgreen")

plot(x = sample_size, y = trackErrors * 100, type = "l", col = "red",ylim = c(-0.005*100, 0.125*100), xlab = "Sample Size", ylab = "TE/SD",
     main = "Tracking Errors/Standard Deviaition \n For 5,10,15,20 and 25 Sample Sizes")

lines(x = sample_size,y = stdDevs * 100, col = "blue")
legend(x = 'topright', legend = c("Tracking Error", "Standard Deviation"),
       lty = 1, col = myColors)


