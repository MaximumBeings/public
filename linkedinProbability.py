#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 14:12:40 2022

@author: oluwaseyiawoga
"""
import random 
import pandas as pd
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
"""
A,B and C play a table tennis tournament. The winner of the tournament will be the first person to win two games in a row. 
In any game, whoever is not playing acts as refree, and each player has equal chance of winning the game. The first game of the
tournament is played between A and B, with C as refree. Thereafter, if the tournament is still undecided at then end of any game, 
the winner and referee of that game play the next game. The tournament is recorded by listing in order the winners of each game, so
that, for example, ACC records a three-game tournament won by C, the first game having been won by A. Determine which of the following
sequences of letters could be the record of a complete tournament, giving brief reasons for your answers:
    
(a) ACB
(b) ABB
(c) ACBB

Find the probability that the tournament is still undecided after 5 games have been played.
Find also the probabilities that each of A, B and C wins in 5 or fewer ganes.
Show the probability that A wins eventually is 5/14, and find the corresponding probabilities for B and C
"""


player_1 = "A"
player_1 = "B"
player_1 = "C"

gameChances = [0,1]

winnersWithinATournament = []

def returnWinnersLosers(winnersWithinATournament):
    res = []
    for x in range(1,len(winnersWithinATournament)):
        if winnersWithinATournament[x-1] == winnersWithinATournament[x]:
            a = winnersWithinATournament[x-1]
            b = winnersWithinATournament[x]
            res.append(a)
            res.append(b)
            return res
    return ""


def playATournament( playersInthisTournament, noOFGAMESPerTourn):
    winnersWithinATournament = []
    for x in range(noOFGAMESPerTourn):
        winner = random.choice(playersInthisTournament)
        winnersWithinATournament.append(winner)
        if(returnWinnersLosers(winnersWithinATournament) != ""):
            return winnersWithinATournament
    return winnersWithinATournament

def playAGameUntilAWinnerEmerge( noOFGAMESPerTourn=3):
    count = 0
    allPlayers = ["A","B","C"]
    tournamentNotDecided = True
    gamePlayRecorded = ""
    allResults = ""
    temp = []
    while tournamentNotDecided:
        if count == 0:
            playersInthisTournament = [allPlayers[0], allPlayers[1]]
            referee = allPlayers[2]
            # print(f"Referee {referee}")
            # print(f"Players {playersInthisTournament}")
            temp = playATournament(playersInthisTournament, noOFGAMESPerTourn)
            allResults = allResults + "".join(temp)
            if returnWinnersLosers(temp) != "":
                gamePlayRecorded=gamePlayRecorded + "".join(temp)
                
                return (gamePlayRecorded,allResults)
        elif count > 0:
            playersInthisTournament = [referee, temp[-1]]
            referee = [x for x in allPlayers if x not in playersInthisTournament][0]
            # print(f"Referee {referee}")
            # print(f"Players {playersInthisTournament}")
            temp = playATournament(playersInthisTournament, noOFGAMESPerTourn)
            allResults = allResults + "-" + "".join(temp)
            if returnWinnersLosers(temp[:]) != "":
                gamePlayRecorded=gamePlayRecorded + "".join(temp)
                return (gamePlayRecorded,allResults)
      
        tournamentNotDecided = True
        count = count + 1
    
    
    
globalGamePlay = []     
v = 10000        
while v > 0:           
    globalGamePlay.append(playAGameUntilAWinnerEmerge())
    v = v - 1
            
results = list(set(globalGamePlay))


results = pd.DataFrame(results)
results.columns = ["Winning Tournament", "All Tournaments"]
print(results)

def probGameNotDecidedAfterFiveGames(noOFGAMESPerTourn=3):
    count = 0
    allPlayers = ["A","B","C"]
    tournamentNotDecided = True
    gamePlayRecorded = ""
    allResults = ""
    temp = []
    while tournamentNotDecided:
        if count == 0:
            playersInthisTournament = [allPlayers[0], allPlayers[1]]
            referee = allPlayers[2]
            # print(f"Referee {referee}")
            # print(f"Players {playersInthisTournament}")
            temp = playATournament(playersInthisTournament, noOFGAMESPerTourn)
            allResults = allResults + "".join(temp)
            if returnWinnersLosers(temp) != "":
                gamePlayRecorded=gamePlayRecorded + "".join(temp)
                
                return allResults
        elif count > 0:
            playersInthisTournament = [referee, temp[-1]]
            referee = [x for x in allPlayers if x not in playersInthisTournament][0]
            # print(f"Referee {referee}")
            # print(f"Players {playersInthisTournament}")
            temp = playATournament(playersInthisTournament, noOFGAMESPerTourn)
            allResults = allResults + "".join(temp)
            if returnWinnersLosers(temp[:]) != "":
                gamePlayRecorded=gamePlayRecorded + "".join(temp)
                return allResults
      
        tournamentNotDecided = True
        count = count + 1
    
    
    
probaGameUndecidedAfterFiveGames = []     
v = 1000000
numberOfSimulation = 1000000
winningAfterFiveGames  = 0    
while v > 0:           
    res = probGameNotDecidedAfterFiveGames(noOFGAMESPerTourn=3)
    if len(res) > 5:
        #print(res)
        winningAfterFiveGames = winningAfterFiveGames + 1 
    probaGameUndecidedAfterFiveGames.append(playAGameUntilAWinnerEmerge())
    v = v - 1
            
results = winningAfterFiveGames/numberOfSimulation
print(f"Probability of No Win After Five (5) Games: {results}")



"""
Find also the probabilities that each of A, B and C wins in 5 or fewer games.
"""

def aParticularPlayerWinsInFiveOrLessGames(playersName):
    probaGameUndecidedAfterFiveGames = []     
    v = 1000000
    numberOfSimulation = 1000000
    temp = 0
    while v > 0:           
        res = probGameNotDecidedAfterFiveGames(noOFGAMESPerTourn=3)
        if len(res) <= 5:
            if res[-1] == playersName:
                temp = temp + 1 
        probaGameUndecidedAfterFiveGames.append(res)
        v = v - 1
    result = temp/numberOfSimulation
    #print(probaGameUndecidedAfterFiveGames)
    return result
    
    
                
results = aParticularPlayerWinsInFiveOrLessGames("A")
player = "A"
print(f"Probability of Player {player} Winning in Five or Fewer (5) Games: {results}")
"""
Probability of Player A Winning in Five or Fewer (5) Games: 0.406195
"""

results = aParticularPlayerWinsInFiveOrLessGames("B")
player = "B"
print(f"Probability of Player {player} Winning in Five or Fewer (5) Games: {results}")
"""
Probability of Player B Winning in Five or Fewer (5) Games: 0.406195
"""

results = aParticularPlayerWinsInFiveOrLessGames("C")
player = "C"
print(f"Probability of Player {player} Winning in Five or Fewer (5) Games: {results}")
"""
Probability of Player C Winning in Five or Fewer (5) Games: 0.062149
"""

"""
Show the probability that A wins eventually is 5/14, and find the corresponding probabilities for B and C
"""

def aParticularPlayerWins(playersName):
    probaGameUndecidedAfterFiveGames = []     
    v = 1000000
    numberOfSimulation = 1000000
    temp = 0
    while v > 0:           
        res = probGameNotDecidedAfterFiveGames(noOFGAMESPerTourn=3)
        if res[-1] == playersName:
            temp = temp + 1 
        probaGameUndecidedAfterFiveGames.append(res)
        v = v - 1
    result = temp/numberOfSimulation
    #print(probaGameUndecidedAfterFiveGames)
    return result
          
#print(aParticularPlayerWins("C"))
    

                
results = aParticularPlayerWins("A")
player = "A"
print(f"Probability of Player {player} Wins: {results}")
"""
PProbability of Player A Wins: 0.444409
"""

results = aParticularPlayerWins("B")
player = "B"
print(f"Probability of Player {player} Wins: {results}")
"""
Probability of Player B Wins: 0.444556
"""

results = aParticularPlayerWins("C")
player = "C"
print(f"Probability of Player {player} Wins: {results}")
"""
Probability of Player C Wins: 0.111002
"""





