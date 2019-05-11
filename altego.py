# Kaavya Antony
# Imitation Game
# Spring 2019 

import random
import matplotlib.pyplot as plt
import numpy as np
import statistics as st
import math
from scipy import stats

''' This method compares all the items in two arrays and returns True if they
are equivalent arrays '''
def compareArrays(array1, array2):
    if len(array1) != len(array2):
        return False

    else:
        for i in range(len(array1)):
            if array1[i] != array2[i]:
                return False
        return True

''' This method runs the simulation until a stable state has been reached. '''
def game(N, C):
    # this array will hold all the communities throughout the simulation
    allRounds = []
    # create initial community with uniform distribution of Altuists and Egoists
    commCurrent = createInitialCommunity(N)
    # calculate the payoffs of each agent in the community
    payoffs = calculatePayoffs(commCurrent, C)
    # add the community to the array of all communities
    allRounds.append(commCurrent)

    # run the simulation until we have a stable state (blinking or not)
    for j in range(2):
        payoffs = calculatePayoffs(commCurrent, C)
        commCurrent = createNextCommunity(commCurrent, payoffs)
        allRounds.append(commCurrent)

    i = 2
    
    while not(compareArrays(allRounds[i], allRounds[(i-2)])):
        payoffs = calculatePayoffs(commCurrent, C)
        commCurrent = createNextCommunity(commCurrent, payoffs)
        allRounds.append(commCurrent)
        i += 1

    if compareArrays(allRounds[i], allRounds[(i-1)]):
        blink = False
        num = sum(allRounds[i])

    else: 
        blink = True
        num = (sum(allRounds[i]) + sum(allRounds[(i-1)])) / 2

    return allRounds[i], allRounds[(i-1)], allRounds[(i-2)], blink, num, i

''' This method will create the initial community with uniform distribution of
both Altruists and Egoists '''
def createInitialCommunity(N):
    community = []
    for i in range(N):
        prob = random.randrange(0, 2)
        if prob == 1:
            community.append(1)
        else:
            community.append(0)

    return community

''' This method will calculate the payoffs of each agent based on their neighbors'''
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

''' This method will calculate the next community based off the payoffs'''
def createNextCommunity(community, payoffs):
    community2 = []
    N = len(community)
    for i in range(len(payoffs)):
        totalA = []
        totalE = []
        x = [(i-1)%N, i, (i+1)%N]
        for j in x:
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

''' This method will generate a graph of 1000 simulation to verify that the %
of Altruists in the final state is at least 60%'''
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
    average = st.mean(results)
    plt.scatter(numGame, results)
    plt.axhline(y=threshold, color='r', linestyle='-')
    plt.axhline(y=average, color='purple', linestyle='-')
    plt.title("Prop 1 Verification")
    plt.xlabel("Number of Simulation")
    plt.ylabel("Percent of Altruism in Final Stable State")
    plt.show()

''' This method creates a line of best fit'''
def bestFit(X, Y):
    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in X]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar

    print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

    return a, b

''' This method will generate a graph of rounds until stable state is reached
as a function of N'''
def roundsTilStable():
    simCount = 100
    results = []
    x = []
    for j in range(10, 220, 10):
        popSize = []
        res = []
        for i in range(simCount):
            popSize.append(i)
            comm1, comm2, comm3, blink, num, i = game(j, 1/4)
            res.append(i)
        results.append(st.mean(res))
        x.append(j)

    a, b = bestFit(x, results)
    yfit = [a + b * xi for xi in x]

    x = np.array(x)
    results = np.array(results)
    z= np.polyfit(x, results, 2)
    z = z.tolist()
    a = z[0]
    b = z[1]
    c = z[2]
    best_fit = a*(x**2) + b*x + c

    plt.plot(x.tolist(), results.tolist(), 'bo', x, best_fit, 'g', x, yfit, 'r')
    plt.title("Rounds Until Stable State as a Function of N")
    plt.xlabel("N")
    plt.ylabel("Rounds Til Final Stable State")
    plt.show()

''' This method will generate a graph of % of simulations that converge to all Egoism
as a function of N'''
def allEgoism():
    simCount = 100
    results = []
    x = []
    for j in range(2, 200, 10):
        popSize = []
        res = []
        for i in range(simCount):
            popSize.append(i)
            comm1, comm2, comm3, blink, num, i = game(j, 1/4)
            if sum(comm1) == 0:
                res.append(1)
                # x.append(j)
        results.append(sum(res)/simCount)
        x.append(j)
        
    x = np.array(x)
    results = np.array(results)
    z= np.polyfit(x, results, 2)
    z = z.tolist()
    a = z[0]
    b = z[1]
    c = z[2]
    best_fit = a*(x**2) + b*x + c

    plt.plot(x.tolist(), results.tolist(), 'bo', x, best_fit, 'g',)
    plt.title("Percent of Simulations that Converge to All Egoism")
    plt.xlabel("N")
    plt.ylabel("Percent of Egoism")
    plt.show()        

def main():
    #Altruists60(101)
    #roundsTilStable()
    #allEgoism()
    game(101, 1/4)
    
main()

