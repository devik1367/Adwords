#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 15:52:44 2020

@author: devikrishnan
"""
import sys
import pandas as pd
import random
import math
import copy
from collections import defaultdict

def read_dataset():
    #my adwords.py file was in the adwords directory. Please change the file path accordingly if needed when testing.
    #read bidder_dataset
    bidder_df = pd.read_csv(r'bidder_dataset.csv', engine = "python")
    
    #read queries
    with open(r'queries.txt') as file:
        queries = file.read().splitlines()
     
    #create list of bidder id's
    bidders = sorted(list(set(bidder_df["Advertiser"].tolist())))
    
    #create dictionary of interested advertisers per query
    bidderDict = defaultdict(list) 
    budgetDict = dict()
    for i in range(len(bidders)):
        for index, row in bidder_df.iterrows():
            if row["Advertiser"] == i:
                if not pd.isna(row["Budget"]):
                    b = row["Budget"]
                    budget = b
                    budgetDict[row["Advertiser"]] = budget
                else:
                    budget = b
                bidderDict[row["Keyword"]].append([row["Advertiser"], row["Bid Value"]])
    
    #print(bidderDict["lucius review"])          
    #output in the form (bidder ID, bid value)
    #[[0, 0.2], [5, 0.3], [16, 0.4], [52, 0.2], [82, 0.8], [96, 0.9]]    
    return bidderDict, queries, budgetDict
            


#function to check whether all the advertisers' budgets are fully spent
def isBudgetSpent(bidderList, budgetDict):
    bidders_ids = [q[0] for q in bidderList]
    temp = [budgetDict[i] for i in bidders_ids]
    #return true if all the budget values are 0
    if (any(temp)) == False:
        return True
    else:
        return False



#Greedy algorithm
def greedy(bidderDict, queries, budgetDict):
    revenue = 0
    for q in queries:
        #get interested bidders and make sure all bidders have enough in their budget left to bid
        q_bidders = [b for b in bidderDict[q] if b[1] > budgetDict[b[0]]]
        #if all the interested bidders have spent their full budget, continue
        if isBudgetSpent(q_bidders, budgetDict) == True:
            continue
        #sort bidders in ascending order of bid value
        sorted_bidders = sorted(q_bidders, key = lambda x:x[1])
        #the bidder with the highest bid value is the winner
        winner = sorted_bidders[-1][0]
        highestBid = sorted_bidders[-1][1]            
        #reduce highest bidder's budget by the bid amount
        budgetDict[winner] -= highestBid
        #add the bid amount to the revenue
        revenue += highestBid
    return revenue

    

#Balance algorithm
def balance(bidderDict, queries, budgetDict):
    revenue = 0
    for q in queries:
        #get interested bidders
        q_bidders = [b for b in bidderDict[q] if b[1] > budgetDict[b[0]]]
        highestUnspentBudget = 0
        winner = 0
        #if all the interested bidders have spent their full budget, continue
        if isBudgetSpent(q_bidders, budgetDict) == True:
            continue
        #iterate through interested bidders to find the bidder with the highest unsoent budget
        for b in q_bidders:
            budget = budgetDict[b[0]]
            #check if budget of bidder is greater than the current highest unspent budget and also if the bid amount is within bidder's budget
            if budget > highestUnspentBudget and b[1] <= budget:
                highestUnspentBudget = budget
                #the bidder with the highest unspent budget is the winner!
                winner = b[0]
                highestBid = b[1]
        #reduce highest bidder's budget by the bid amount
        budgetDict[winner] -= highestBid
        #add the bid amount to the revenue
        revenue += highestBid
    return revenue



#MSVV algorithm
def msvv(bidderDict, s_queries, budgetDict):
    originalBudgetDict = copy.deepcopy(budgetDict)
    revenue = 0
    for q in queries:
        #get interested bidders
        q_bidders = bidderDict[q]
        highestWeightedBid = 0
        winner = 0
        #if all the interested bidders have spent their full budget, continue
        if isBudgetSpent(q_bidders, budgetDict) == True:
            continue
        #iterate through interested bidders to find the bidder with the highest unsoent budget
        for b in q_bidders:
            bidValue = b[1]
            #check if the bid amount is greater than the current highest and also if the bid amount is within the advertiser's budget
            xu = (originalBudgetDict[b[0]] - budgetDict[b[0]]) / originalBudgetDict[b[0]]
            if bidValue * (1 - math.exp(xu - 1)) > highestWeightedBid and b[1] <= budgetDict[b[0]]:
                highestWeightedBid = bidValue * (1 - math.exp(xu - 1))
                highestBid = bidValue
                #the bidder with the highest bid is the winner!
                winner = b[0]
        #reduce highest bidder's budget by the bid amount
        budgetDict[winner] -= highestBid
        #add the bid amount to the revenue
        revenue += highestBid
    return revenue



if __name__ == '__main__':
    random.seed(0)
    bidderDict, queries, budgetDict = read_dataset()
    budgetlist = budgetDict.values()
    s_revenue = 0
    if sys.argv[1] == 'greedy':
        #calculate revenue for given keyword list
        revenue = greedy(bidderDict, queries, budgetDict)
        #calculate average revenue over 100 permutations of the query list
        for i in range(100):
            bidderDict, queries, budgetDict = read_dataset()
            s_queries = queries
            random.shuffle(s_queries)
            s_revenue += greedy(bidderDict, s_queries, budgetDict)
        meanRevenue = s_revenue/100
        print("Greedy algorithm results:")
    elif sys.argv[1] == 'balance':
        #calculate revenue for given keyword list
        revenue = balance(bidderDict, queries, budgetDict)
        #calculate average revenue over 100 permutations of the query list
        for i in range(100):
            bidderDict, queries, budgetDict = read_dataset()
            s_queries = queries
            random.shuffle(s_queries)
            s_revenue += balance(bidderDict, s_queries, budgetDict)
        meanRevenue = s_revenue/100
        print("Balance algorithm results: ")
    elif sys.argv[1] == 'msvv':
        #calculate revenue for given keyword list
        revenue = msvv(bidderDict, queries, budgetDict)
        #calculate average revenue over 100 permutations of the query list
        for i in range(100):
            bidderDict, queries, budgetDict = read_dataset()
            s_queries = queries
            random.shuffle(s_queries)
            s_revenue += msvv(bidderDict, s_queries, budgetDict)
        meanRevenue = s_revenue/100
        print("MSVV algorithm results: ")
    else:
        print("Invalid argument.")
    
    #calculate the revenue generated from an optimal matching
    optimalMatching = sum(budgetlist)
    
    #calculate competitive ratio
    cratio = meanRevenue/optimalMatching
    
    print("Revenue: " + str(round(revenue, 2)))
    #print("Average revenue: " + str(round(meanRevenue, 2)))
    #print("Optimal matching: " + str(round(optimalMatching, 2)))
    print("Competitive ratio: " + str(round(cratio, 2)))



"""
My code takes about 10 minutes to run. 

My outputs were as follows:

Greedy algorithm results:
Revenue: 16731.4
Competitive ratio: 0.94

Balance algorithm results:
Revenue: 12320.2
Competitive ratio: 0.69

MSVV algorithm results:
Revenue: 17671.0
Competitive ratio: 0.99
"""

