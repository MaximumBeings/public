#Download libor and Ois Data from any of the sites online and delete any extraneous data
# and also delete entries with N/A - because rates are not available for some days
#we could have deleted the N/As in R but that was just my thought process when I downloaded 
#the data.  For the libor rates - rename the date column - Date and the rates column libor.
#save the file as a csv and call it liborrates.  For the ois data also delete all descriptive
#data if any and rename the Date column Date and the rates column ois and save the file as
#oisrates in csv format.  OIS rates are the overnight Fed Fund Rates in the US of A.
#set your working directory in R to the folder where you saved the files

#Read data from csv files after downloading

#Sources:  Analytical Edge - MITx on Edx
#          Federal Reserve Bank Online Data Repositories - libor and Fed Funds Rate
#          RStudio
#          ggplot2 package

  libor <- read.csv("liborrates.csv", header=TRUE)
  ois <- read.csv("oisrates.csv", header = TRUE)

#check the imported data like so:

  head(libor)
# Date   rate
# 1 1/2/1986 8.0000
# 2 1/3/1986 8.0625
# 3 1/6/1986 8.1250
# 4 1/7/1986 8.1250
# 5 1/8/1986 8.0000
# 6 1/9/1986 8.1875

  head(ois)
  
# Date rate
# 1 7/1/1954 1.13
# 2 7/2/1954 1.25
# 3 7/3/1954 1.25
# 4 7/4/1954 1.25
# 5 7/5/1954 0.88
# 6 7/6/1954 0.25

#Check the structure of our data

  str(libor)
  str(ois)

#Once we check the structure of the imported data you will realize that the date fields
#were imported as Factors instead of date class so we use the commande below to convert the column to date

#convert the date field to Date class from factors

  libor$Date <- as.Date(libor$Date, '%m/%d/%Y')
  ois$Date <- as.Date(ois$Date,'%m/%d/%Y')
  
#Check structure of our data again
  str(libor)
  str(ois)
  
#To understand our data better at the highlevel lets use the summary function
#to view the data

  summary(libor)
  summary(ois)
  
#Now lets merge the dataframes in one using Date as the common field
#the merge command will combine the two data using the Date field as the primary keys
#only the dates that are present in the two tables are combined and others are discarded
#this is exactly what we want

  combined <- merge(libor,ois, by="Date")
  
#Check the structure of the first few records using head(dataframe)
  head(combined)
  
# Date rate.x rate.y
# 1 1986-01-02 8.0000   8.76
# 2 1986-01-03 8.0625   8.34
# 3 1986-01-06 8.1250   8.00
# 4 1986-01-07 8.1250   7.82
# 5 1986-01-08 8.0000   7.79
# 6 1986-01-09 8.1875   7.93
  
#Rename column - we need to rename the combined data using meaningful column names
#rate.x is the libor rate and rate.y is the ois rates
#R starts indexing at 1 instead of 0 like in other programming languages

  names(combined)[2]<-paste("libor")  
  names(combined)[3]<-paste("ois")
  
#Check again that everything is properly renamed
  
  head(combined)

# Date  libor  ois
# 1 1986-01-02 8.0000 8.76
# 2 1986-01-03 8.0625 8.34
# 3 1986-01-06 8.1250 8.00
# 4 1986-01-07 8.1250 7.82
# 5 1986-01-08 8.0000 7.79
# 6 1986-01-09 8.1875 7.93
  
#Now calculate libor OIS spread in basis points and create a new column to hold the data
  
  combined$liborOISSpread = ((combined$libor - combined$ois)/100)/0.0001

#Check again that everything is properly renamed and calculated

  head(combined)

# Date  libor  ois liborOISSpread
# 1 1986-01-02 8.0000 8.76         -76.00
# 2 1986-01-03 8.0625 8.34         -27.75
# 3 1986-01-06 8.1250 8.00          12.50
# 4 1986-01-07 8.1250 7.82          30.50
# 5 1986-01-08 8.0000 7.79          21.00
# 6 1986-01-09 8.1875 7.93          25.75

#Lets check the highest libor - ois spread using summary function
  
  summary(combined)
# Date                libor              ois         liborOISSpread   
# Min.   :1986-01-02   Min.   : 0.2228   Min.   : 0.040   Min.   :-943.56  
# 1st Qu.:1993-02-18   1st Qu.: 1.4294   1st Qu.: 1.250   1st Qu.:  12.00  
# Median :2000-04-10   Median : 4.9141   Median : 4.535   Median :  21.50  
# Mean   :2000-04-11   Mean   : 4.1945   Mean   : 3.927   Mean   :  26.75  
# 3rd Qu.:2007-06-05   3rd Qu.: 6.0625   3rd Qu.: 5.772   3rd Qu.:  37.00  
# Max.   :2014-07-25   Max.   :10.6250   Max.   :16.170   Max.   : 402.88 
  
#Or better yet get the actual date when the largest spread occurred

  combined$Date[which.max(combined$liborOISSpread)]
#"2008-10-10"
  
#And lets get the highest spread

  combined$liborOISSpread[which.max(combined$liborOISSpread)]
#402.875
  
#Now lets plot the data from 1/1/2006 using ggplot
#First lets subset our data to plot only from 1/1/2006

  tsdata<-combined[combined$Date>"2006-01-01",]
  
#check that our data was properly subsetted
  head(tsdata)

# Date   libor  ois liborOISSpread
# 5057 2006-01-03 4.54438 4.34         20.438
# 5058 2006-01-04 4.54063 4.22         32.063
# 5059 2006-01-05 4.55000 4.24         31.000
# 5060 2006-01-06 4.55000 4.22         33.000
# 5061 2006-01-09 4.56000 4.25         31.000
# 5062 2006-01-10 4.56850 4.24         32.850
  
#Load the ggplot ploting library
#If package is not available - download using install.packages("ggplot2")

  library(ggplot2)
  
#plot the timeseries
  ggplot( data = tsdata, aes( Date, liborOISSpread )) + geom_line() + xlab("Year") + ylab("Basis Points") + ggtitle(" LIBOR - OIS SPREAD BETWEEN 2006 AND 2014") +  theme(plot.title = element_text(lineheight=.8, face="bold"))




