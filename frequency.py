import numpy as np
import json
import os
from pprint import pprint

_CONCEDE = 'concede'
_SILENT = 'silent'
_SELFISH = 'selfish'
_FORTUNATE = 'fortunate'
_UNFORTUNATE = 'unfortunate'
_NICE = 'nice'
_UNCHANGED = 'unchanged'

_CONCEDER = 'conceder'
_HARDHEADED = 'hardheaded'
_RANDOM = 'random'
_TFT = 'tft'

fileDir = os.path.dirname(os.path.realpath('__file__'))
folderPath = os.path.join(fileDir, 'training_logs/')
training_folder = os.path.join(fileDir, 'training_logs')


EVIDENCE_GIVEN_STATE = {}

def get_obs(filename):
    OBSERVATIONS = []
    # name = filename.split('.')[0].split('_')
    with open(folderPath + filename) as f:
        data = json.load(f)
    for i in range(len(data['bids'])):
        if not 'agent1' in data['bids'][i].keys():
            # OBSERVATIONS.append(['ACCEPT', 'None'])
            continue
            # break
        observation_a1 = get_movetype(data, agent=1, roundNr=i)
        if not 'agent2' in data['bids'][i].keys():
            # OBSERVATIONS.append([observation_a1, 'ACCEPT'])
            continue
            # break
        observation_a2 = get_movetype(data, agent=2, roundNr=i)
        # observation_a1 = movetype_to_number(observation_a1)
        # observation_a2 = movetype_to_number(observation_a2)
        OBSERVATIONS.append([observation_a1, observation_a2])
    return OBSERVATIONS


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

    if abs(self_diff)==0.0:
        if abs(opp_diff)==0.0:
            return _UNCHANGED
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

def movetype_to_number(m):
    # print(m)
    if m == _CONCEDE:
        return 0
    if m == _SELFISH:
        return 1
    if m == _FORTUNATE:
        return 2
    if m == _UNFORTUNATE:
        return 3
    if m == _SILENT:
        return 4
    if m == _NICE:
        return 5
    if m==_UNCHANGED:
        return 6

def number_to_strategy(n):
    if n==0:
        return _CONCEDER
    if n==1:
        return _HARDHEADED
    if n==2:
        return _TFT
    if n==3:
        return _RANDOM

def strategy_to_number(s):
    if s == _CONCEDER:
        return 0
    if s == _HARDHEADED:
        return 1
    if s == _TFT:
        return 2
    if s == _RANDOM:
        return 3


def get_strat_name(s):
    if _CONCEDER in s:
        return _CONCEDER
    if _HARDHEADED in s:
        return _HARDHEADED
    if _TFT in s:
        return _TFT
    if _RANDOM in s:
        return _RANDOM

def normalize(arr):
    s = sum(arr)
    out = []
    for i in range(len(arr)):
        out.append(round(arr[i]/s,3))
    return out


def test(fileName, evGivenS):
    obs = get_obs(fileName)
    # agent 1
    a1 = [0,0,0,0]
    a2 = [0,0,0,0]
    for i in range(len(obs)):
        a1_move = movetype_to_number(obs[i][0])
        a2_move = movetype_to_number(obs[i][1])
        for k in evGivenS.keys():
            a1_prob = evGivenS[k][a1_move]
            a2_prob = evGivenS[k][a2_move]
            strat_number = strategy_to_number(k)
            # print(a1_prob)
            a1[strat_number] += a1_prob
            a2[strat_number] += a2_prob
    a1 = normalize(a1)
    a2 = normalize(a2)
    print(a1)
    print(a2)

FILE_TO_LEAVE_OUT = 0

def main():
    freqs = {
        _CONCEDER: [0,0,0,0,0,0,0],
        _HARDHEADED: [0,0,0,0,0,0,0],
        _TFT: [0,0,0,0,0,0,0],
        _RANDOM: [0,0,0,0,0,0,0]
    }
    fileNames = os.listdir(training_folder)
    testFileName = ""
    if FILE_TO_LEAVE_OUT != -1:
        testFileName = fileNames[FILE_TO_LEAVE_OUT]
        del fileNames[FILE_TO_LEAVE_OUT]
    for name in fileNames:
        strategy_names = name.split('.')[0].split('_')
        strat1 = get_strat_name(strategy_names[0])
        strat2 = get_strat_name(strategy_names[1])
        obs = get_obs(name)
        # print(obs)
        for i in range(len(obs)):
            a1 = obs[i][0]
            a2 = obs[i][1]
            a1 = movetype_to_number(a1)
            a2 = movetype_to_number(a2)
            freqs[strat1][a1] += 1
            freqs[strat2][a2] += 1
    pprint(freqs)
    for k in freqs.keys():
        freqs[k] = normalize(freqs[k])
    pprint(freqs)
    print(testFileName)
    if testFileName != "":
        test(testFileName, freqs)

main()
            