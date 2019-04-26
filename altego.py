# Kaavya Antony
# Imitation Game
# Spring 2019 

import random
import matplotlib.pyplot as plt
import numpy as np
import statistics as st
import math
from scipy import stats

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
    # commPrev = [0]
    commCurrent = createInitialCommunity(N)
    #commCurrent = [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1]
    # if sum(commCurrent) == 0:
    #     print("TRUE")
    # else:
    #     print("FALSE")

    # commNext = [0]
    payoffs = calculatePayoffs(commCurrent, C)
    # allRounds.append(commPrev)
    allRounds.append(commCurrent)
    # allRounds.append(commNext)

    #print("Community 0: ", commCurrent)

    for j in range(2):
        payoffs = calculatePayoffs(commCurrent, C)
        commCurrent = createNextCommunity(commCurrent, payoffs)
        allRounds.append(commCurrent)
        #print("Community", j + 1, ": ", commCurrent)

    i = 2
    
    while not(compareArrays(allRounds[i], allRounds[(i-2)])): # or compareArrays(allRounds[i], allRounds[(i-1)])):

        # print("start check")
        # print(i, ": ", allRounds[i])
        # print(i - 2, ": ", allRounds[i-2])
        # print("end check")
        payoffs = calculatePayoffs(commCurrent, C)
        commCurrent = createNextCommunity(commCurrent, payoffs)
        allRounds.append(commCurrent)
        #print("Community", i + 1, ": ", commCurrent)
        #print("Payoffs", i + 1, ": ", payoffs)
        i += 1
    # if DEBUG:
    #     print("Community", i + 1, ": ", commCurrent)
    #     print("start check")
    #     print(i, ": ", allRounds[i%len(allRounds)])
    #     print(i - 2, ": ", allRounds[(i-2)%len(allRounds)])
    #     print("end check")
    #     print("Simulation Over in ", i, "rounds")

    if compareArrays(allRounds[i], allRounds[(i-1)]):
        #print("not blinking")
        blink = False
        num = sum(allRounds[i])

    else: #if compareArrays(allRounds[i], allRounds[(i-2)]):
        blink = True
        num = (sum(allRounds[i]) + sum(allRounds[(i-1)])) / 2

    return allRounds[i], allRounds[(i-1)], allRounds[(i-2)], blink, num, i

''' This method creates a neighborhood of size N with an even distribution of Altruists and Egoists'''
def createInitialCommunity(N):
    community = []
    for i in range(N):
        prob = random.randrange(0, 2)
        if prob == 1:
            community.append(1)
        #print("A", end=" ")
        else:
            community.append(0)
        #print("E", end=" ")
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
        # if the agent is an Altruist
        if community[i] == 1:
            payoff = leftNeighbor + rightNeighbor - C
        # if the agent is an Egoist
        else:
            payoff = leftNeighbor + rightNeighbor
        payoffs.append(payoff)
    return payoffs


''' This method creates a neighborhood of size N based on the payoffs of each agent's neighbors'''
def createNextCommunity(community, payoffs):
    community2 = []
    N = len(community)
    for i in range(len(payoffs)):
        totalA = []
        totalE = []
        i = i % N
        # leftNeighbor = (i-1) % N
        # rightNeighbor = (i+1) % N
        for j in range((i-1)%N, (i+2)%N):
            if community[j] == 1:
                totalA.append(payoffs[j])
            else:
                totalE.append(payoffs[j])
        if totalE == []:
            community2.append(1)
        elif totalA == []:
            community2.append(0)
        elif st.mean(totalE) > st.mean(totalA):
            # agent decides to be an Egoist 
            community2.append(0)
        else:
            community2.append(1)
    return community2


# def majorityEgoists(N):
#     threshold = N * .6

#     simCount = 1000
#     results = []
#     numGame = []
#     for i in range(simCount):
# 	    numGame.append(i)
# 	    num = game(N, 1/4)[0]
# 	    if num >= threshold:
#             # at least 60% of population is Altruistic 
# 		    results.append(1)
# 	    else:
# 		    results.append(0)

#     res = stats.relfreq(results, numbins=2)

#     x = res.lowerlimit + np.linspace(0, res.binsize*res.frequency.size, res.frequency.size)

#     # fig = plt.figure(figsize=(5, 4))
#     # ax = fig.add_subplot(1, 1, 1)
#     # ax.bar(x, res.frequency, width=res.binsize)
#     # ax.set_title('Relative Frequency Histogram for Size 100')
#     # ax.set_xlim([x.min(), x.max()])
#     # print("Majority Egoist: ", round(res.frequency[0]*100, 2), "% of ", simCount, "simulations for population size", N)
#     # print("Majority Altruist: ", round(res.frequency[1]*100, 2), "% of ", simCount, "simulations for population size", N)
#     return res.frequency[0]*100


# def numRounds(N):
#     simCount = 1000
#     threshold = N * .6
#     rounds = []
#     numGame = []
#     for i in range(simCount):
#         numGame.append(i)
#         e, r = game(N, 1 / 4)
#         rounds.append(r)
#         if e >= threshold:
#             majorityEgoists.append(1)
#         else:
#             majorityEgoists.append(0)

#     return st.mean(rounds), majorityEgoists


def Altruists60(N):
    threshold = N * .6
    simCount = 1000
    results = []
    numGame = []
    for i in range(simCount):
        numGame.append(i)
        comm1, comm2, comm3, blink, num, i = game(N, 1/4)
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
    plt.ylabel("Percent of Altruism in Final Stable State")
    plt.show()

def numRounds(N):
    simCount = 1000
    results = []
    numGame = []
    for i in range(simCount):
        numGame.append(i)
        num = game(N, 1/4)[5]
        results.append(num)

    avg = st.mean(results)
    return avg
    # plt.scatter(numGame, results)
    # # plt.axhline(y=threshold, color='r', linestyle='-')
    # plt.title("Rounds of Simulation Until Stable State for N = "+ str(N))
    # plt.axhline(y=avg, color='r', linestyle='-')
    # plt.xlabel("Number of Simulation")
    # plt.ylabel("Number of Rounds til Stable State")
    # plt.show()

def main():
    Altruists60(101)
    #game(101, 1/4)
    # averages = []
    # popSize = []
    # for i in range(10, 120, 10):
    #     popSize.append(i)
    #     avg = numRounds(i)
    #     averages.append(avg)

    # slope, intercept, r_value, p_value, std_err = stats.linregress(popSize,averages)
    # print(slope)
    # line = slope*popSize+intercept

    # plt.plot(popSize,averages,'o', popSize, line)

    # plt.scatter(popSize, averages)
    # # plt.axhline(y=threshold, color='r', linestyle='-')
    # plt.title("Rounds Until Stable State as a function of N")
    # plt.xlabel("N")
    # plt.ylabel("Number of Rounds til Stable State")
    # plt.show()

    #print(sum([1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]))
    #print(sum([1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1]))
    #print(sum([1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1]))
main()

