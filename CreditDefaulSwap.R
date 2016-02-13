
#NOTE: Will provide more context around this later.  Essentially, this calculates the harzard rate for a simple CDS
#structure.  Actually, I have like 16 models from two years ago all written in R.  One of my buddies took a graduate level Credit
#Risk Management class like two years ago and shared all his handouts.  I was a little bit less busy then so I used those
#materials to build models in R.  In the coming days or weeks, I will be releasing them one at a time.  Eventually, I will rebuild
#the models in Python and make them more elegant.  There is one on basis swap, logistic regression, multivariable linear regression.
#Bootstrapping, interest rate swap, bootstrapping credit spreads etc etc.  So keep it locked and see you soon!!!!

#We will also cover other CDS examples...mostly plain vanilla type.  

#CDS CALCULATION

spread = 150/10000  #Note that you have to convert by divind by 10000 - This example also assumes constant spread
rRecRate = 40/100
harzardRate = 0.015 #Initial Guess
Notional = 1000000
time = c(1,2,3,4,5)
spot = c(0.01,0.01,0.01,0.01,0.01)  #Flat 1% Spot Rate - Unrealistic in practice
DF = c()

for(x in 1:length(time)) DF[x] = 1/(1+spot[x]/2)**(2*time[x])
print(DF)

FeeLeg <- function(r)
{
  PS = c()  #Probability of Survival
  PD = c()  #Probability of Default
  feeIfNoDefault = c()
  accrualOnDefault = c()
  
  for(x in 1:length(time))
  {
    if(x == 1)
    {
      PS[x] = 1 - r
    }
    
    else
    {
      PS[x] = PS[x-1] * (1-r)
    }
  }
  
  for(x in 1:length(time))
  {
    if(x == 1)
    {
      PD[x] = 1 - PS[x]
    }
    
    else
    {
      PD[x] = PS[x-1] - PS[x]
    }
  }
  
  for(x in 1:length(time))
  {

    
    feeIfNoDefault[x] = spread*DF[x]*PS[x]*Notional
    
    }
  
  for(x in 1:length(time))
  {
    if(x == 1)
    {
      accrualOnDefault[x] = 0.5*(1-PS[x])*spread*Notional*DF[x]
    }
    
    else
    {
      accrualOnDefault[x] = 0.5*(PS[x-1]-PS[x])*spread*Notional*DF[x]
    }
  }
  
  
  return(sum(feeIfNoDefault) + sum(accrualOnDefault))
  
}


contingentLeg <- function(r)
{
  PS = c()  #Probability of Survival
  ContLeg = c()
  for(x in 1:length(time))
  {
    if(x == 1)
    {
      PS[x] = 1 - r
    }
    
    else
    {
      PS[x] = PS[x-1] * (1-r)
    }
    
    
  }
  
  for(x in 1:length(time))
  {
    if(x == 1)
    {
      ContLeg[x] = (1 - rRecRate)*Notional*DF[x]*(1-PS[x])
    }
    
    else
    {
      ContLeg[x] = (1 - rRecRate)*Notional*DF[x]*(PS[x-1]-PS[x])
    }
    
    
  }
  
  return(sum(ContLeg))
}
  

bisection <- function(a, b, tol = 1.e-10) {
  while(b-a > tol) {
    c <- (a+b)/2   
    ifelse(FeeLeg(c) > contingentLeg(c), a <- c, b<-c)
  }
  (a+b)/2  
}



bisection(-1,1)
#0.02469136  
  
