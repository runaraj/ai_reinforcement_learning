import json
import os
from pprint import pprint
import numpy
import math

# Compares the bid given by @agent in @roundNr with the bid
# given in @roundNr -1 and returns the type of move it is
def getMoveType(data, roundNr, agent):
    self_old_util = getSelfBidUtil(data, roundNr-1, agent)
    self_new_util = getSelfBidUtil(data, roundNr, agent)
    # print(self_new_util)
    opp_old_util = getOppsBidUtil(data, roundNr-1, agent)
    opp_new_util = getOppsBidUtil(data, roundNr, agent)

    self_diff = self_new_util-self_old_util
    opp_diff = opp_new_util-opp_old_util

    if abs(self_diff) < 0.001:
        return "SILENT"
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


def getLastXMoveTypes(data, roundNr, agent, x):
    if x>roundNr:
        x = roundNr-1
    lastXMoveTypes = []
    print('roundNr: ' + str(roundNr))
    print(x)
    for i in range(roundNr, roundNr-x, -1):
        t = getMoveType(data, i, agent)
        lastXMoveTypes.append(t)
    return lastXMoveTypes

# gets the utility of @agent in @roundNr for its own bid
def getSelfBidUtil(data, roundNr, agent):
    agentName = 'agent1'
    profile = data['Utility1']
    if agent == 2:
        agentName = 'agent2'
        profile = data['Utility2']
    try:
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
    except Exception:
        return 0.0
    
    

# gets the utility of @agent in @roundNr for received bid
def getOppsBidUtil(data, roundNr, agent):
    profile = data['Utility1']
    opponent = 'agent2'
    if agent == 2:
        profile = data['Utility2']
        opponent = 'agent1'
    try:
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
    except Exception:
        return 0.0