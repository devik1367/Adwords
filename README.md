# Adwords

Problem: 
We are given a set of advertisers, each of whom has a daily budget B(i). When a user performs a query, an ad request is placed online and advertisers can bid for that advertisement slot. The bid of advertiser i for an ad request q is denoted as b(iq). It is assumed that the bids are small in relation to the advertisers' daily budgets , and that each advertisement slot can be allocated only to one advertiser. The advertiser is charged the bid from their budget. The aim is to maximize the amount of money recieved from the advertisers.

Formulae:
1. Optimal revenue = sum of budgets of all advertisers
2. Competitive ratio = (Mean revenue of algorithm over all possible inpout sequences) / Optimal matching
(I calculated the mean revenue over 100 random permutations of the input sequence)

Assumptions:
1. For the optimal matching (used to determine the competitive ratio), assume all advertisers' budgets are fully used up.
2. The bid values are fixed.
3. Each ad request has just one advertisement slot to display.

Dataset:
There are two files with data, bidder_dataset.csv and queries.txt. The former contains information about the advertisers and has four columns:
1. advertiser ID
2. query that the advertiser bids on
3. bid value for the query
4. total budget (for all the keywords).

The latter file contains the order of arrival of keywords that the advertisers will bid on. These arrive online and a fresh auctioning will be made for every word.

