"

Paramters:

St = 10
r = 0.15
sigma = 0.20
T = 1
N = 100
n = 100
fixedEpsilon = 0.15

Problem Statement:

(a) Starting with the initial stock price St as specified, and considering 100 Steps, 
calculate the expected value of the stock price at the end of every successive Δt interval of time.

(b) Plot the entire movement of prices over the T period under observation

(c) Perform 5 trials of 100 steps each to plot the probable movement of stock prices over a 1 
 year period. Plot each trajectory of prices as a separate line.
 
 Implementation:
 The R code at the Github link below shows how one may implement the above.

 Github:
 https://tinyurl.com/uu86e8aw
 
 References:
 (a) WQU Statistics Class Lectures & Notes (circa 2017)
 
 
"
#1. Consider following values for the purpose of this project:

St = 10
r = 0.15
sigma = 0.20
T = 1
N = 100
n = 100
fixedEpsilon = 0.15

#2. Starting with the initial stock price St as specified, and considering 100 Steps, 
#calculate the expected value of the stock price at the end of every successive Δt interval of time

mySimFixedEpsilon <- function(St, r, sigma,T,N,fixedEpsilon, n) {
  
  temp <- c() 
  
  for (x in 1:100 )
    
    if (x == 1) {
      
      temp[x] = St
      
    }
  
  else
    
  {
    temp[x] = temp[x-1] *exp((r - 0.5 * sigma ^ 2) * (T/n) + sigma * fixedEpsilon * sqrt(T/n))
    
  }
  
  return(temp)
}

FixedSimulations <- mySimFixedEpsilon(St, r, sigma,T,N,fixedEpsilon, n)

FixedSimulations

#3. Plot the entire movement of prices over the T period under observation

plot(FixedSimulations, type = "l", col = "red", xlab = "Time", ylab = "Stock Price",
     main = "Fixed Simulations (e = 0.15)")


#4. Instead of considering a fixed ε as in the previous steps, randomly assign values 
#to ε from a standard normal distribution.

mySimRandomEpsilon <- function(St, r, sigma,T,N, n) {
  
  temp <- c() 
  randomNumber = rnorm(100,0,1)
  
  for (x in 1:100 )
    
    if (x == 1) {
      
      temp[x] = St
      
    }
  
  else
    
  {
    temp[x] = temp[x-1] *exp((r - 0.5 * sigma ^ 2) * (T/n) + sigma * randomNumber[x] * sqrt(T/n))
    
  }
  
  return(temp)
}

RandomSimulations = mySimRandomEpsilon(St, r, sigma,T,N, n)


plot(RandomSimulations, type = "l", col = "red", xlab = "Time", ylab = "Stock Price",
     main = "Random Simulations (rnorm(100,0,1))")

#5. Perform 5 trials of 100 steps each to plot the probable movement of stock prices over a 1 
#year period. Plot each trajectory of prices as a separate line.

FiveTrials <- function(numberOfTrials){
  
  for (x in 1:numberOfTrials){
    
    if (x == 1){
      temp <- list(mySimRandomEpsilon(St, r, sigma,T,N, n))
    }
    else
    {
      interMediate <-  mySimRandomEpsilon(St, r, sigma,T,N, n)
      temp <- append(temp,list(interMediate))
    }
  }
  
  return(temp)
}


FinalSimulation <- FiveTrials(5)

plot(unlist(FinalSimulation[1]), type = "l", col = "red", xlab = "Time",ylim = c(0,60),ylab = "Stock Price",
     main = "Five Random Trials")
lines(unlist(FinalSimulation[2]), #Line Plot
      lwd = 2, # thickness of line
      col = "black")
lines(unlist(FinalSimulation[3]), #Line Plot
      lwd = 2, # thickness of line
      col = "green")
lines(unlist(FinalSimulation[4]), #Line Plot
      lwd = 2, # thickness of line
      col = "blue")
lines(unlist(FinalSimulation[5]), #Line Plot
      lwd = 2, # thickness of line
      col = "purple")


lapply(c(5,10,15,20), FiveTrials)



#Variances of Five Different Trials
varTrial1 = var(unlist(FinalSimulation[1]))
varTrial2 = var(unlist(FinalSimulation[2]))
varTrial3 = var(unlist(FinalSimulation[3]))
varTrial4 = var(unlist(FinalSimulation[4]))
varTrial5 = var(unlist(FinalSimulation[5]))

varTrial1
varTrial2
varTrial3
varTrial4
varTrial5

#Another Approach

trial1 <- unlist(FinalSimulation[1])[100]
trial2 <- unlist(FinalSimulation[2])[100]
trial3 <- unlist(FinalSimulation[3])[100]
trial4 <- unlist(FinalSimulation[4])[100]
trial5 <- unlist(FinalSimulation[5])[100]

lastNumbers <- c(trial1,trial2,trial3,trial4,trial5)
var(lastNumbers)


delta_t=1/12
S2<-rep(0,500) ### I create S2 by initializing with 500 repetitions of 0
dim(S2) <- c(100,5)  ### Set the object up as a 100 x 5 array
S2[1,1:5] = 10 ### Initialized the first element of each of the 5 arrays as 10 i.e. each of my trial has first element as 10
### This allows for repeatability. Without a seed, the problem will generate a new set of random numbers every time
### Now see below for how I use element "t" to generate element "t+1", and subsequently elemeent "t+1" to generate "t+2" etc. 
for (i in 1:5){
  for (j in 1:99){
    S2[j+1,i]=S2[j, i]*exp((r-0.5*sigma**2)*delta_t + sigma*rnorm(1)*sqrt(delta_t))
  }
}
plot.ts(S2[,1:5], plot.type = "single", main = "Simulated Stock Prices", col=c("red", "green","black","blue","chocolate"), ylab="Stock Price", xlab="Timestep")
