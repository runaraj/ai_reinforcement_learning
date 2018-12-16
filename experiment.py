import json
import os
from pprint import pprint
import numpy
import math
'''
NOT USED/FINISHED
'''
fileDir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(fileDir, 'training_logs/conceder_conceder.json')

with open(filename) as f:
    data = json.load(f)
# pprint(data['issues'])

issues = data['issues'].keys()

profile1 = data['Utility1']
profile2 = data['Utility2']


bid0 = data['bids'][0]
bid0Agent1 = bid0['agent1']
bid0Agent1 = bid0Agent1.split(',')



# Get utility for a bid 
i=0
util = 0.0
for k in data['issues'].keys():
    bidVal = bid0Agent1[i]
    issueWeight = profile1[k]['weight']
    issueValueWeight = profile1[k][bidVal]
    # print(issueWeight)
    # print(issueValueWeight)
    util += (issueWeight*issueValueWeight)
    i += 1
# "agent1": "Apples,Milk,None,None",


# gets the utility of @agent in @roundNr for its own bid
def getSelfBidUtil(logData, roundNr, agent):
    agentName = 'agent1'
    profile = data['Utility1']
    if agent == 2:
        agentName = 'agent2'
        profile = data['Utility2']
    bid = data['bids'][roundNr][agentName].split(',')
    util = 0.0
    i=0
    for k in data['issues'].keys():
        bidVal = bid[i]
        issueWeight = profile[k]['weight']
        issueValueWeight = profile[k][bidVal]
        util += (issueWeight*issueValueWeight)
        i += 1
    return util

# gets the utility of @agent in @roundNr for received bid
def getOppsBidUtil(logData, roundNr, agent):
    profile = data['Utility1']
    opponent = 'agent2'
    if agent == 2:
        profile = data['Utility2']
        opponent = 'agent1'
    bid = data['bids'][roundNr][opponent].split(',')
    util = 0.0
    i=0
    for k in data['issues'].keys():
        bidVal = bid[i]
        issueWeight = profile[k]['weight']
        issueValueWeight = profile[k][bidVal]
        util += (issueWeight*issueValueWeight)
        i += 1
    return util

# print(getSelfBidUtil(data, 0, 1))
# print(getSelfBidUtil(data, 1, 1))
# print(getOppsBidUtil(data, 0, 1))


# Compares the bid given by @agent in @roundNr with the bid
# given in @roundNr -1 and returns the type of move it is
def getMoveType(logData, roundNr, agent):
    self_old_util = getSelfBidUtil(logData, roundNr-1, agent)
    self_new_util = getSelfBidUtil(logData, roundNr, agent)
    # print(self_new_util)
    opp_old_util = getOppsBidUtil(logData, roundNr-1, agent)
    opp_new_util = getOppsBidUtil(logData, roundNr, agent)

    self_diff = self_new_util-self_old_util
    opp_diff = opp_new_util-opp_old_util

    if abs(self_diff) < 0.001:
        return "SILENT||NICE"
    else:
        # Self utility is worse
        if self_diff < 0:
            if opp_diff < 0:
                return 'UNFORTUNATE'
            else:
                return 'CONCEDING'
        else:
            # self is better
            if opp_diff < 0:
                return 'SELFISH'
            else:
                return 'FORTUNATE'

# print(getMoveType(data, 1, 1))
# print(getMoveType(data, 2, 1))
# print(getMoveType(data, 3, 1))
for i in range(1,20):
    print(getMoveType(data, i, 1))

# i = 0
# for k,v in data.items():
#     if i==0:
#         print(k,v)
#     i += 1