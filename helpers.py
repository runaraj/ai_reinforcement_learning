import json
import os
from pprint import pprint
import numpy
import math

_CONCEDE = 'concede'
_SILENT = 'silent'
_SELFISH = 'selfish'
_FORTUNATE = 'fortunate'
_UNFORTUNATE = 'unfortunate'
_NICE = 'nice'

'''
NOT USED/FINISHED
'''

# get movetype for @agent in @roundNr
def get_movetype(data, agent, roundNr):
    opponent = 1
    if agent == 1:
        opponent = 2

    util_prev_own_bid = get_utility(data, roundNr-1, agent, agent)
    util_new_own_bid = get_utility(data, roundNr, agent, agent)

    opp_util_prev_own_bid = get_utility(data, roundNr-1, opponent, agent)
    opp_util_new_own_bid = get_utility(data, roundNr, opponent, agent)

    self_diff = util_new_own_bid - util_prev_own_bid
    opp_diff = opp_util_new_own_bid - opp_util_prev_own_bid

    if (abs(self_diff)==0.0):
        if opp_diff > 0.08:
            return _NICE
        return _SILENT
    else:
        # Self utility is worse
        if self_diff < 0:
            if opp_diff < 0:
                return _UNFORTUNATE
            else:
                return _CONCEDE
        else:
            # self is better
            if opp_diff < 0:
                return _SELFISH
            else:
                return _FORTUNATE

# gets the utility of @agent in @roundNr for bid given by @bidder
def get_utility(data, roundNr, agent, bidder):
    # agentName = 'agent1'
    profile = data['Utility1']
    bidder = 'agent1'
    if agent == 2:
        # agentName = 'agent2'
        profile = data['Utility2']
    if bidder == 2:
        bidder = 'agent2'
    try:
        bid = data['bids'][roundNr][bidder].split(',')
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



# There are no state transitions
def prob_of_state(prevState, state):
    if prevState == state:
        return 1
    return 0