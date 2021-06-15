#Case Study Questions:

"
Using R Programming Language to Perform Statistical & Stock Data Analysis

(a) Download stock data (from 2016) for five (5) tickers using any of the stock data API of your choosing (e.g. Yahoo! Finance, Alpaca, IEX, Polygon etc)

(b) Create a function to calculate the monthly returns of these tickers and create a data frame of stock returns.  How are the monthly returns of the tickers distributed? Are the stock returns normally distributed? Plot Histograms of the returns to examine their probability distributions.

(c) Create an equally weighted portfolio of three stocks from the five tickers above and construct a portfolio from the equally weighted stocks. Calculate the cumulative return of the portfolio and the constituent stocks. Plot the cumulative returns on a chart. Also calculate the standard deviation or variance of the portfolio so created.

(d) Create four different portfolios using any three of the above tickers (randomly selected without repeat in each portfolio). Each of the four portfolio will consist of three tickers. 

(e) Calculate the cumulative return for each of the portfolio. Plot the cumulative returns on a chart. Also calculate the standard deviation or variance of the portfolio so created. How are the monthly returns of the portfolios distributed? Are the portfolio returns normally distributed? Plot Histograms of the returns to examine their probability distributions. Calculate the standard deviation or variance of the portfolio so created.  Do you see a wide variance in the possible portfolio returns and its cumulative outcome? Given that you chose similar stocks from the same industry, what accounts for the variance of returns among different portfolios (if any)?

"



#import libraries and packages

#install.packages("PerformanceAnalytics")
#install.packages("quantmod")
#install.packages("dygraphs")

#Load libraries and packages

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


# Choose the starting year and assign it to the 'year' variable.
year <- 2016

# Use the function the monthly returns on 5 stocks, and pass in the 'year' value
# Let's choose MSFT, AAPL, ORCL, EBAY, CSCO; after you run these functions, have 
# a look at the global environment and make sure your three xts objects are there
monthly_stock_returns('MSFT', year)
monthly_stock_returns('AAPL', year)
monthly_stock_returns('ORCL', year)
monthly_stock_returns('FB', year)
monthly_stock_returns('CSCO', year)

# Merge the monthly return xts objects into 1 xts object.
merged_returns <- merge.xts(MSFT,AAPL, ORCL, FB, CSCO)



#Preview the monthly returns for 5 stock tickers
head(merged_returns)
# 
# MSFT         AAPL         ORCL          FB        CSCO
# 2016-01-29 -0.007054384 -0.119626225 -0.006040600  0.06965507 -0.13247994
# 2016-02-29 -0.079498273  0.074422617  0.012860979 -0.04829123  0.09573039
# 2016-03-31  0.082036345  0.146617768  0.106420340  0.06499437  0.08385511
# 2016-04-29 -0.102086684 -0.005721389 -0.026001192  0.03004373 -0.03502856
# 2016-05-31  0.060872314  0.035957752  0.008493681  0.01040659  0.05519615
# 2016-06-30 -0.035138530 -0.010066257  0.017996270 -0.03887399 -0.01246978


# Plot the merged returns returns using dygraph to examine their probability distributions
dygraph(merged_returns, main = "Microsoft vs Yahoo vs Oracle vs Facebook vs Cisco") %>% 
  dyAxis("y", label = "%") %>% 
  dyOptions(colors = RColorBrewer::brewer.pal(6, "Set2")) 

#Plot Histograms of the returns to examine their probability distributions
hist(merged_returns$MSFT, # histogram
     col = "peachpuff", # column color
     border = "black", 
     right = FALSE,
     prob = TRUE, # show densities instead of frequencies
     xlim = c(-0.2,0.2),
     ylim = c(0,10),
     xlab = "Returns",
     ylab = "Frequency",
     main = "Histogram of MSFT")
lines(density(merged_returns$MSFT), # density plot
      lwd = 2, # thickness of line
      col = "black")

#Plot Histograms of the returns to examine their probability distributions
hist(merged_returns$AAPL, # histogram
     col = "peachpuff", # column color
     border = "black",
     right = FALSE,
     prob = TRUE, # show densities instead of frequencies
     xlim = c(-0.20,0.20),
     ylim = c(0,8),
     xlab = "Returns",
     ylab = "Frequency",
     main = "Histogram of AAPL")
lines(density(merged_returns$AAPL), # density plot
      lwd = 2, # thickness of line
      col = "black")

#Plot Histograms of the returns to examine their probability distributions
hist(merged_returns$ORCL, # histogram
     col = "peachpuff", # column color
     border = "black", 
     right = FALSE,
     prob = TRUE, # show densities instead of frequencies
     xlim = c(-0.12,0.15),
     ylim = c(0,12),
     xlab = "Returns",
     ylab = "Frequency",
     main = "Histogram of ORCL")
lines(density(merged_returns$ORCL), # density plot
      lwd = 2, # thickness of line
      col = "black")



# Subset Three .
subSetThree <- subset(merged_returns, select=c('MSFT','FB','ORCL'))

#Calculate Cummmulative Returns
subSetCumReturns <- cumsum(subSetThree)

#Preview the subsetted data
head(subSetCumReturns)

# MSFT        AAPL         ORCL
# 2016-01-29 -0.007054384 -0.11962622 -0.006040600
# 2016-02-29 -0.086552657 -0.04520361  0.006820379
# 2016-03-31 -0.004516312  0.10141416  0.113240719
# 2016-04-29 -0.106602996  0.09569277  0.087239526
# 2016-05-31 -0.045730682  0.13165052  0.095733207
# 2016-06-30 -0.080869212  0.12158427  0.113729477

# We have the 3 monthly returns saved in 1 object.
# Now, let's choose the respective weights of those 3.
# Here we'll allocate 25% to Google, 25% to JP Morgan and 50% to Amazon.
w <- c(1/3.0, 1/3.0, 1/3.0)

# Now use the built in PerformanceAnalytics function Return.portfolio
# to calculate the monthly returns on the portfolio, supplying the vector of weights 'w'.
portfolio_monthly_returns <- Return.portfolio(subSetThree, weights = w)

#Cummulative of Portfolio Returns and Normal Portfolio Reurns
PortCumReturns <- cumsum(portfolio_monthly_returns)

PortRetversCumsumReturns <- cbind(portfolio_monthly_returns,PortCumReturns)

names(PortRetversCumsumReturns)[1]<-paste("Portfolio Returns")
names(PortRetversCumsumReturns)[2]<-paste("Cumm Portfolio Returns")

#Preview
head(PortRetversCumsumReturns)
# Portfolio Returns Cumm Portfolio Returns
# 2016-01-29     -0.0442404030            -0.04424040
# 2016-02-29     -0.0002212724            -0.04446168
# 2016-03-31      0.1119094464             0.06744777
# 2016-04-29     -0.0427082080             0.02473956
# 2016-05-31      0.0334436052             0.05818317
# 2016-06-30     -0.0078197785             0.05036339

var(PortRetversCumsumReturns)
# Portfolio Returns Cumm Portfolio Returns
# Portfolio Returns            0.001796588            0.001145249
# Cumm Portfolio Returns       0.001145249            0.005508981




#Combine cummulative  returns and portfolio returns
complete <- cbind(subSetCumReturns,portfolio_monthly_returns)

names(complete)[4]<-paste("PORTFOLIO")

#Preview monthly portfolio returns and cummulative returns for three stocks
head(complete)

# MSFT        AAPL         ORCL     PORTFOLIO
# 2016-01-29 -0.007054384 -0.11962622 -0.006040600 -0.0442404030
# 2016-02-29 -0.086552657 -0.04520361  0.006820379 -0.0002212724
# 2016-03-31 -0.004516312  0.10141416  0.113240719  0.1119094464
# 2016-04-29 -0.106602996  0.09569277  0.087239526 -0.0427082080
# 2016-05-31 -0.045730682  0.13165052  0.095733207  0.0334436052
# 2016-06-30 -0.080869212  0.12158427  0.113729477 -0.0078197785

# Plot the combine returns using dygraph
dygraph(complete, main = "Microsoft vs Yahoo vs Oracle vs Portfolio") %>% 
  dyAxis("y", label = "%") %>% 
  dyOptions(colors = RColorBrewer::brewer.pal(6, "Set2")) 


#Plot the returns using plot and add the mean, sd and median for the portfolio return

myColors <- c("red", "darkgreen", "goldenrod", "darkblue", "black", "purple","orange")

plot(x = complete[,"MSFT"], xlab = "Maturity", ylab = "Returns",
     main = "MSFT vs. FB vs. ORCL vs. PORTFOLIO", ylim = c(-0.15, 0.4), major.ticks= "years",
     minor.ticks = FALSE, col = "red")
lines(x = complete[,"FB"], col = "darkgreen")
lines(x = complete[,"ORCL"], col = "goldenrod")
lines(x = complete[,"PORTFOLIO"], col = "darkblue")
abline(h = mean(complete$PORTFOLIO), col="black")
abline(h = median(complete$PORTFOLIO), col="purple")
abline(h = sd(complete$PORTFOLIO), col="orange")
legend(x = 'topleft', legend = c("MSFT", "FB", "ORCL", "PORTFOLIO", "Portfolio Mean", "Portfolio Median","Portfolio Std Dev"),
       lty = 1, col = myColors)

#Calculate Portfolio Variance
var(complete)

# MSFT        AAPL         ORCL    PORTFOLIO
# MSFT      0.0075921556 0.007795267 0.0014339251 0.0008525509
# AAPL      0.0077952671 0.015772477 0.0043905310 0.0016845044
# ORCL      0.0014339251 0.004390531 0.0021894188 0.0009757441
# PORTFOLIO 0.0008525509 0.001684504 0.0009757441 0.0017965879

#Mean, Standard Deviation & Median of the returns

mean(complete$MSFT)
sd(complete$MSFT)
median(complete$MSFT)

mean(complete$AAPL)
sd(complete$AAPL)
median(complete$AAPL)

mean(complete$ORCL)
sd(complete$ORCL)
median(complete$ORCL)

mean(complete$PORTFOLIO)
sd(complete$PORTFOLIO)
median(complete$PORTFOLIO)

#PART 2


portfolio_list <- c('MSFT', 'ORCL', 'FB', 'CSCO')
portfolio_1 <- sample(portfolio_list,3)
portfolio_2 <- sample(portfolio_list,3)
portfolio_3 <- sample(portfolio_list,3)
portfolio_4 <- sample(portfolio_list,3)

portfolio_1
portfolio_2
portfolio_3
portfolio_4

w <- c(1/3.0, 1/3.0, 1/3.0)



subSetPort_1 <- subset(merged_returns, select=c(portfolio_1))
portfolio_monthly_returns <- Return.portfolio(subSetPort_1, weights = w)
names(portfolio_monthly_returns)[1]<-paste("PORTFOLIO_1")

subSetPort_2 <- subset(merged_returns, select=c(portfolio_2))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_2, weights = w)))
names(portfolio_monthly_returns)[2]<-paste("PORTFOLIO_2")

subSetPort_3 <- subset(merged_returns, select=c(portfolio_3))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_3, weights = w)))
names(portfolio_monthly_returns)[3]<-paste("PORTFOLIO_3")

subSetPort_4 <- subset(merged_returns, select=c(portfolio_4))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_4, weights = w)))
names(portfolio_monthly_returns)[4]<-paste("PORTFOLIO_4")

PortCumReturns <- cumsum(portfolio_monthly_returns)

# Plot the combine returns using dygraph
dygraph(PortCumReturns, main = "Four Portfolio Returns") %>% 
  dyAxis("y", label = "%") %>% 
  dyOptions(colors = RColorBrewer::brewer.pal(6, "Set2")) 

meanPortfolio1 <- mean(portfolio_monthly_returns$PORTFOLIO_1)
medianPortfolio1 <- median(portfolio_monthly_returns$PORTFOLIO_1)
sdPortfolio1 <- sd(portfolio_monthly_returns$PORTFOLIO_1)

meanPortfolio1
medianPortfolio1
sdPortfolio1

meanPortfolio2 <- mean(portfolio_monthly_returns$PORTFOLIO_2)
medianPortfolio2 <- median(portfolio_monthly_returns$PORTFOLIO_2)
sdPortfolio2 <- sd(portfolio_monthly_returns$PORTFOLIO_2)

meanPortfolio2
medianPortfolio2
sdPortfolio2

meanPortfolio3 <- mean(portfolio_monthly_returns$PORTFOLIO_3)
medianPortfolio3 <- median(portfolio_monthly_returns$PORTFOLIO_3)
sdPortfolio3 <- sd(portfolio_monthly_returns$PORTFOLIO_3)

meanPortfolio3
medianPortfolio3
sdPortfolio3

meanPortfolio4 <- mean(portfolio_monthly_returns$PORTFOLIO_4)
medianPortfolio4 <- median(portfolio_monthly_returns$PORTFOLIO_4)
sdPortfolio4 <- sd(portfolio_monthly_returns$PORTFOLIO_4)

meanPortfolio4
medianPortfolio4
sdPortfolio4


myColors <- c("red", "darkgreen", "goldenrod", "darkblue", "black", "purple","orange")

plot(x = portfolio_monthly_returns[,"PORTFOLIO_1"], xlab = "Maturity", ylab = "Returns",
     main = "PORTFOLIO_1 vs. PORTFOLIO_2 vs. PORTFOLIO_3 vs. PORTFOLIO_4", ylim = c(-0.15, 0.4), major.ticks= "years",
     minor.ticks = FALSE, col = "red")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_2"], col = "darkgreen")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_3"], col = "goldenrod")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_4"], col = "darkblue")
abline(h = mean(portfolio_monthly_returns$PORTFOLIO_1), col="black")
abline(h = median(portfolio_monthly_returns$PORTFOLIO_1), col="purple")
abline(h = sd(portfolio_monthly_returns$PORTFOLIO_1), col="orange")
legend(x = 'topleft', legend = c("PORTFOLIO_1", "PORTFOLIO_2", "PORTFOLIO_3", "PORTFOLIO_4", "PORTFOLIO_1_Mean", "PORTFOLIO_2_Median","PORTFOLIO_1_Std_Dev"),
       lty = 1, col = myColors)

#Calculate Portfolio Variance
var(portfolio_monthly_returns)

#            PORTFOLIO_1 PORTFOLIO_2 PORTFOLIO_3 PORTFOLIO_4
# PORTFOLIO_1 0.001385384 0.001037869 0.001496239 0.001148900
# PORTFOLIO_2 0.001037869 0.001456972 0.001283481 0.001702640
# PORTFOLIO_3 0.001496239 0.001283481 0.001986732 0.001785415
# PORTFOLIO_4 0.001148900 0.001702640 0.001785415 0.002351801

#Calculate Portfolio Variance
sd(portfolio_monthly_returns)^2
#

#ANOTHER APPROACH FOR PORTFOLIO VARIANCE
w <- c(1/4.0, 1/4.0, 1/4.0, 1/4.0)

portfolio_Variance <- Return.portfolio(portfolio_monthly_returns, weights = w)
names(portfolio_Variance)[1]<-paste("Total_Portfolio_Return")

var(portfolio_Variance$Total_Portfolio_Return)

#                                   Total_Portfolio_Return
# Total_Portfolio_Return            0.001509272





#From class forum - using combination functions

Symbols<-c('MSFT', 'AAPL','ORCL', 'FB', 'CSCO')
chooseStocks<-function(Symbols){
  for (i in 1:10)
  { 
    ticker<-combn(Symbols, 2, FUN=NULL, simplify=FALSE)
    print(ticker[[i]])
  }
}
chooseStocks(Symbols)

# [1] "MSFT" "AAPL" "ORCL"
# [1] "MSFT" "AAPL" "FB"  
# [1] "MSFT" "AAPL" "CSCO"
# [1] "MSFT" "ORCL" "FB"  
# [1] "MSFT" "ORCL" "CSCO"
# [1] "MSFT" "FB"   "CSCO"
# [1] "AAPL" "ORCL" "FB"  
# [1] "AAPL" "ORCL" "CSCO"
# [1] "AAPL" "FB"   "CSCO"
# [1] "ORCL" "FB"   "CSCO"

portfolio_1 <- c("MSFT","AAPL", "ORCL")
portfolio_2 <- c("MSFT" ,"AAPL", "FB" )
portfolio_3 <- c("MSFT", "AAPL" ,"CSCO")
portfolio_4 <- c("MSFT" ,"ORCL", "FB"  )
portfolio_5 <- c("MSFT" ,"ORCL" ,"CSCO")
portfolio_6 <- c("MSFT", "FB"  , "CSCO")
portfolio_7 <- c("AAPL" ,"ORCL" ,"FB"  )
portfolio_8 <- c("AAPL" ,"ORCL" ,"CSCO")
portfolio_9 <- c("AAPL", "FB"  , "CSCO")
portfolio_10 <- c("ORCL" ,"FB"  , "CSCO")

w <- c(1/3.0, 1/3.0, 1/3.0)

subSetPort_1 <- subset(merged_returns, select=c(portfolio_1))
portfolio_monthly_returns <- Return.portfolio(subSetPort_1, weights = w)
names(portfolio_monthly_returns)[1]<-paste("PORTFOLIO_1")

subSetPort_2 <- subset(merged_returns, select=c(portfolio_2))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_2, weights = w)))
names(portfolio_monthly_returns)[2]<-paste("PORTFOLIO_2")

subSetPort_3 <- subset(merged_returns, select=c(portfolio_3))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_3, weights = w)))
names(portfolio_monthly_returns)[3]<-paste("PORTFOLIO_3")

subSetPort_4 <- subset(merged_returns, select=c(portfolio_4))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_4, weights = w)))
names(portfolio_monthly_returns)[4]<-paste("PORTFOLIO_4")

subSetPort_5 <- subset(merged_returns, select=c(portfolio_5))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_5, weights = w)))
names(portfolio_monthly_returns)[5]<-paste("PORTFOLIO_5")

subSetPort_6 <- subset(merged_returns, select=c(portfolio_6))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_6, weights = w)))
names(portfolio_monthly_returns)[6]<-paste("PORTFOLIO_6")

subSetPort_7 <- subset(merged_returns, select=c(portfolio_7))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_7, weights = w)))
names(portfolio_monthly_returns)[7]<-paste("PORTFOLIO_7")

subSetPort_8 <- subset(merged_returns, select=c(portfolio_8))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_8, weights = w)))
names(portfolio_monthly_returns)[8]<-paste("PORTFOLIO_8")

subSetPort_9 <- subset(merged_returns, select=c(portfolio_9))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_9, weights = w)))
names(portfolio_monthly_returns)[9]<-paste("PORTFOLIO_9")

subSetPort_10 <- subset(merged_returns, select=c(portfolio_10))
portfolio_monthly_returns <- cbind(portfolio_monthly_returns,(Return.portfolio(subSetPort_10, weights = w)))
names(portfolio_monthly_returns)[10]<-paste("PORTFOLIO_10")

meanPortfolio1 <- mean(portfolio_monthly_returns$PORTFOLIO_1)
medianPortfolio1 <- median(portfolio_monthly_returns$PORTFOLIO_1)
sdPortfolio1 <- sd(portfolio_monthly_returns$PORTFOLIO_1)

meanPortfolio1
medianPortfolio1
sdPortfolio1

meanPortfolio2 <- mean(portfolio_monthly_returns$PORTFOLIO_2)
medianPortfolio2 <- median(portfolio_monthly_returns$PORTFOLIO_2)
sdPortfolio2 <- sd(portfolio_monthly_returns$PORTFOLIO_2)

meanPortfolio2
medianPortfolio2
sdPortfolio2

meanPortfolio3 <- mean(portfolio_monthly_returns$PORTFOLIO_3)
medianPortfolio3 <- median(portfolio_monthly_returns$PORTFOLIO_3)
sdPortfolio3 <- sd(portfolio_monthly_returns$PORTFOLIO_3)

meanPortfolio3
medianPortfolio3
sdPortfolio3

meanPortfolio4 <- mean(portfolio_monthly_returns$PORTFOLIO_4)
medianPortfolio4 <- median(portfolio_monthly_returns$PORTFOLIO_4)
sdPortfolio4 <- sd(portfolio_monthly_returns$PORTFOLIO_4)

meanPortfolio4
medianPortfolio4
sdPortfolio4

meanPortfolio5 <- mean(portfolio_monthly_returns$PORTFOLIO_5)
medianPortfolio5 <- median(portfolio_monthly_returns$PORTFOLIO_5)
sdPortfolio5 <- sd(portfolio_monthly_returns$PORTFOLIO_5)

meanPortfolio5
medianPortfolio5
sdPortfolio5

meanPortfolio6 <- mean(portfolio_monthly_returns$PORTFOLIO_6)
medianPortfolio6 <- median(portfolio_monthly_returns$PORTFOLIO_6)
sdPortfolio6 <- sd(portfolio_monthly_returns$PORTFOLIO_6)

meanPortfolio6
medianPortfolio6
sdPortfolio6

meanPortfolio7 <- mean(portfolio_monthly_returns$PORTFOLIO_7)
medianPortfolio7 <- median(portfolio_monthly_returns$PORTFOLIO_7)
sdPortfolio7 <- sd(portfolio_monthly_returns$PORTFOLIO_7)

meanPortfolio7
medianPortfolio7
sdPortfolio7

meanPortfolio8 <- mean(portfolio_monthly_returns$PORTFOLIO_8)
medianPortfolio8 <- median(portfolio_monthly_returns$PORTFOLIO_8)
sdPortfolio8 <- sd(portfolio_monthly_returns$PORTFOLIO_8)

meanPortfolio8
medianPortfolio8
sdPortfolio8

meanPortfolio9 <- mean(portfolio_monthly_returns$PORTFOLIO_9)
medianPortfolio9 <- median(portfolio_monthly_returns$PORTFOLIO_9)
sdPortfolio9 <- sd(portfolio_monthly_returns$PORTFOLIO_9)

meanPortfolio9
medianPortfolio9
sdPortfolio9

meanPortfolio10 <- mean(portfolio_monthly_returns$PORTFOLIO_10)
medianPortfolio10 <- median(portfolio_monthly_returns$PORTFOLIO_10)
sdPortfolio10 <- sd(portfolio_monthly_returns$PORTFOLIO_10)

meanPortfolio10
medianPortfolio10
sdPortfolio10


myColors <- c("red", "darkgreen", "goldenrod", "darkblue", "black", "purple","orange","yellow","green","blue","black","purple")

plot(x = portfolio_monthly_returns[,"PORTFOLIO_1"], xlab = "Maturity", ylab = "Returns",
     main = "10 Portfolios", ylim = c(-0.15, 0.4), major.ticks= "years",
     minor.ticks = FALSE, col = "red")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_2"], col = "darkgreen")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_3"], col = "goldenrod")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_4"], col = "darkblue")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_5"], col = "darkgreen")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_6"], col = "goldenrod")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_7"], col = "darkblue")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_8"], col = "darkgreen")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_9"], col = "goldenrod")
lines(x = portfolio_monthly_returns[,"PORTFOLIO_10"], col = "darkblue")
abline(h = mean(portfolio_monthly_returns$PORTFOLIO_1), col="black")
abline(h = median(portfolio_monthly_returns$PORTFOLIO_1), col="purple")
abline(h = sd(portfolio_monthly_returns$PORTFOLIO_1), col="orange")


#ANOTHER APPROACH FOR PORTFOLIO VARIANCE
w <- c(1/10.0, 1/10.0, 1/10.0, 1/10.0,1/10.0, 1/10.0, 1/10.0, 1/10.0,1/10.0, 1/10.0)

portfolio_Variance <- Return.portfolio(portfolio_monthly_returns, weights = w)
names(portfolio_Variance)[1]<-paste("Total_Portfolio_Return")

var(portfolio_Variance$Total_Portfolio_Return)

# Total_Portfolio_Return
# Total_Portfolio_Return            0.001554363
