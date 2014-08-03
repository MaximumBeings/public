#Download libor and Ois Data from any of the sites online and delete any extraneous data
# and also delete entries with N/A - because rates are not available for some days
#we could have deleted the N/As in R but that was just my thought process when I downloaded 
#the data.  For the libor rates - rename the date column - Date and the rates column libor.
#save the file as a csv and call it liborrates.  For the ois data also delete all descriptive
#data if any and rename the Date column Date and the rates column ois and save the file as
#oisrates in csv format.  OIS rates are the overnight Fed Fund Rates in the US of A.
#set your working directory in R to the folder where you saved the files

#Read data from csv files after downloading
libor <- read.csv("liborrates.csv", header=TRUE)
ois <- read.csv("oisrates.csv", header = TRUE)
#Check the structure of our data
str(libor)
str(ois)
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
combined <- merge(libor,ois, by="Date")
#Check the structure of the first few records using head(dataframe)
head(combined)
#Rename column
names(combined)[2]<-paste("libor")  
names(combined)[3]<-paste("ois")
#Check again that everything is properly renamed
head(combined)
#Now calculate libor OIS spread in basis points
combined$liborOISSpread = ((combined$libor - combined$ois)/100)/0.0001
#Check again that everything is properly renamed
head(combined)
#Lets check the highest libor - ois spread using summary function
summary(combined)
#Or better yet get the actual date when the largest spread occurred
combined$Date[which.max(combined$liborOISSpread)]
#And lets get the highest spread
combined$liborOISSpread[which.max(combined$liborOISSpread)]
#Now lets plot the data from 1/1/2006 using ggplot
#First lets subset our data to plot only from 1/1/2006
tsdata<-combined[combined$Date>"2006-01-01",]
#check that our data was properly subsetted
head(tsdata)
#Load the ggplot ploting library
#If package is not available - download using install.packages("ggplot2")
library(ggplot2)
#plot the timeseries
ggplot( data = tsdata, aes( Date, liborOISSpread )) + geom_line() + xlab("Year") + ylab("Basis Points") + ggtitle(" LIBOR - OIS SPREAD BETWEEN 2006 AND 2014") +  theme(plot.title = element_text(lineheight=.8, face="bold"))




