# Kaavya Antony
# Imitation Game
# Spring 2019 


# EGOISTS = 1, HOOLIGANS = 0
import random
import matplotlib.pyplot as plt
import numpy as np
import statistics as st
from scipy import stats
import matplotlib.mlab as mlab
import math

DEBUG = False

def compareArrays(array1, array2):
    if len(array1) != len(array2):
        return False

    else:
        for i in range(len(array1)):
            if array1[i] != array2[i]:
                return False
        return True

def game(N, C):
    allRounds = []
    commCurrent = createInitialCommunity(N)
    payoffs = calculatePayoffs(commCurrent, C)
    allRounds.append(commCurrent)

    if DEBUG:
        print("Community 0: ", commCurrent)

    # for j in range(3):
    for j in range(2):
        payoffs = calculatePayoffs(commCurrent, C)
        commCurrent = createNextCommunity(commCurrent, payoffs)
        allRounds.append(commCurrent)
        if DEBUG:
            print("Community", j + 1, ": ", commCurrent)

    i = 3
    i = 2
    while not(compareArrays(allRounds[i], allRounds[(i-2)])):
        payoffs = calculatePayoffs(commCurrent, C)
        commCurrent = createNextCommunity(commCurrent, payoffs)
        allRounds.append(commCurrent)
        if DEBUG:
            print("Community", i + 1, ": ", commCurrent)
        i += 1
    if DEBUG:
        print("Community", i + 1, ": ", commCurrent)
        print("start check")
        print(i, ": ", allRounds[i%len(allRounds)])
        print(i - 2, ": ", allRounds[(i-2)%len(allRounds)])
        print("end check")
        print("Simulation Over in ", i, "rounds")

    # output = (N - sum(commCurrent))/N
    # return sum(commCurrent)
    if compareArrays(allRounds[i], allRounds[(i-1)]):
        #print("not blinking")
        blink = False
        num = sum(allRounds[i])

    else: #if compareArrays(allRounds[i], allRounds[(i-2)]):
        blink = True
        num = (sum(allRounds[i]) + sum(allRounds[(i-1)])) / 2

    print(allRounds)
    print(len(allRounds))
    return allRounds[i], allRounds[(i-1)], allRounds[(i-2)], blink, num, i


''' This method creates a neighborhood of size N with an even distribution of Altruists and Egoists'''
def createInitialCommunity(N):
    community = []
    for i in range(N):
        prob = random.randrange(0, 2)
        if prob == 1:
            # add an egoist to the community 
            community.append(1)
        else:
            # add a hooligan to the community 
            community.append(0)
    if DEBUG:
        print("Simulation Begin")
    return community


''' This method calculates the payoffs for each agent at each round so they can decide what their next move is'''
def calculatePayoffs(community, C):
    payoffs = []
    N = len(community)
    for i in range(len(community)):
        leftNeighbor = community[(i-1) % N]
        rightNeighbor = community[(i+1) % N]
        damage = 0
        if leftNeighbor == 0:
            damage += 1
        elif rightNeighbor == 0:
            damage += 1
        # if the agent is an Egoist
        if community[i] == 1:
            payoff = leftNeighbor + rightNeighbor - damage
        # if the agent is a Hooligan
        else:
            payoff = leftNeighbor + rightNeighbor - damage + C
        payoffs.append(payoff)
    return payoffs


''' This method creates a neighborhood of size N based on the payoffs of each agent's neighbors'''
def createNextCommunity(community, payoffs):
    community2 = []
    N = len(community)
    for i in range(len(payoffs)):
        totalE = []
        totalH = []
        i = i % N
        # leftNeighbor = (i-1) % N
        # rightNeighbor = (i+1) % N
        for j in range((i-1)%N, (i+2)%N):
            if community[j] == 1:
                totalE.append(payoffs[j])
            else:
                totalH.append(payoffs[j])
        if totalH == []:
            community2.append(1)
        elif totalE == []:
            community2.append(0)
        elif st.mean(totalE) > st.mean(totalH):
            # agent decides to be an Egoist 
            community2.append(1)
        else:
            community2.append(0)
    return community2

def percentHool(N):
    popSize = []
    percentHool = []
    for i in range(100):
      popSize.append(i)
      percentHool.append(game(N, 1/4))

    plt.scatter(popSize, percentHool)
    plt.title("% Hooligans for Population Size " + str(N))
    plt.xlabel("Number of Simulation")
    plt.ylabel("% Hooligans")
    plt.show()

def percentHoolC(N):
    costs = [.1, .2, .3, .4, .5, .6, .7, .8, .9]
    avgPercentHool = []
    for j in costs: 
        percentHool = []
        for i in range(100):
          percentHool.append(game(N, j)) 

        avgPercentHool.append(st.mean(percentHool))

    plt.scatter(costs, avgPercentHool)
    plt.title("% Hooligans for Population Size " + str(N))
    plt.xlabel("Enjoyment Cost of Being a Hooligan ")
    plt.ylabel("% Hooligans")
    plt.show()

def Egoists60(N):
    threshold = N * .6
    simCount = 1000
    results = []
    numGame = []
    for i in range(simCount):
        numGame.append(i)
        comm1, comm2, comm3, blink, num, i = game2(N, 1/4)
        num = math.ceil(num)
        results.append(num)
        # if num > 47:
        #     print("num = ", num)
        #     print("blinking = ", blink)
        #     print("Comm 3", comm1)
        #     print("Comm 2", comm2)
        #     print("Comm 1", comm3)

            # print("Comm 3", comm2, "sum = ", sum(comm2))

    plt.scatter(numGame, results)
    plt.axhline(y=threshold, color='r', linestyle='-')
    plt.title("Prop 1 Verification")
    plt.xlabel("Number of Simulation")
    plt.ylabel("Percent of Egoism in Final Stable State")
    plt.show()

def main():
    #Egoists60(101)
    game(21, 1/4)

main()

