import numpy as np
import json
import os
from pprint import pprint

# name variables
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


# get movetypes from @filename and return them in a list
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
    name = 'agent2'
    if agent == 1:
        opponent = 2
        name = 'agent1'

    # if the new bid as exactly the same as the new one the bid is unchanged
    try:
        prev_own_bid = data['bids'][roundNr - 1][name].split(',')
        new_own_bid = data['bids'][roundNr][name].split(',')
        equal = True
        for i in range(len(prev_own_bid)):
            if (prev_own_bid[i] != new_own_bid[i]):
                equal = False
                break
        if equal:
            return _UNCHANGED
    except Exception:
        pass

    util_prev_own_bid = get_utility(data, roundNr - 1, agent, agent)
    util_new_own_bid = get_utility(data, roundNr, agent, agent)

    opp_util_prev_own_bid = get_utility(data, roundNr - 1, opponent, agent)
    opp_util_new_own_bid = get_utility(data, roundNr, opponent, agent)

    self_diff = util_new_own_bid - util_prev_own_bid
    opp_diff = opp_util_new_own_bid - opp_util_prev_own_bid
    # if both utilities change by very little it is a silent move
    if 0 < abs(self_diff) < 0.05 and 0 < abs(opp_diff) < 0.05:
        return _SILENT
    if abs(self_diff) == 0.0:
        # If our utility is the same and opponent is worse it is a selfish move
        if opp_diff < 0:
            return _SELFISH
        else:
            # If our utility is the same and opponent is better it is a concession
            # We don't have nice moves
            return _NICE
    # self is worse
    elif self_diff < 0:
        # If our and opponent's utility is worse it is unfortunate
        if opp_diff <= 0:
            return _UNFORTUNATE
        else:
            # If ours is worse and opponent is better it is a concession
            return _CONCEDE
    # self is better
    else:
        # If ours is better and opponent is worse it is selfish
        if opp_diff <= 0:
            return _SELFISH
        else:
            # If ours and opponent is better it is fortunate
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
        i = 0
        for k in data['issues'].keys():
            bidVal = bid[i]
            issueWeight = profile[k]['weight']
            issueValueWeight = profile[k][bidVal]
            util += (issueWeight * issueValueWeight)
            i += 1
        return util
    except Exception:
        return 0.0


# Convert string movetype @m to number
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
    if m == _NICE:
        return 4
    if m == _SILENT:
        return 5
    if m == _UNCHANGED:
        return 6


# Convert number @n to strategy string
def number_to_strategy(n):
    if n == 0:
        return _CONCEDER
    if n == 1:
        return _HARDHEADED
    if n == 2:
        return _TFT
    if n == 3:
        return _RANDOM


# Convert strategy string @s to number
def strategy_to_number(s):
    if s == _CONCEDER:
        return 0
    if s == _HARDHEADED:
        return 1
    if s == _TFT:
        return 2
    if s == _RANDOM:
        return 3


# Get strategy name from string @s. E.g. input 'Conceder1' will return 'Conceder'
def get_strat_name(s):
    if _CONCEDER in s:
        return _CONCEDER
    if _HARDHEADED in s:
        return _HARDHEADED
    if _TFT in s:
        return _TFT
    if _RANDOM in s:
        return _RANDOM


# Returns normalized version of input array @arr
def normalize(arr):
    s = sum(arr)
    out = []
    for i in range(len(arr)):
        out.append(round(arr[i] / s, 3))
    return out


# Takes two lists of equal length as arguments
# Adds the two lists element by element and returns the normalized result
def combine_and_normalize(list1, list2):
    if len(list1) != len(list2):
        print("LISTS MUST BE SAME LENGTH")
        return
    out = []
    for i in range(len(list1)):
        out.append(list1[i] + list2[i])
    out = normalize(out)
    return out


def filtering(t_matrix, o_matrix, p0, observations):
    fw = np.zeros((p0.size, observations.size + 1))
    fw[:, 0] = p0

    for i in range(observations.size):
        #print('fw is \n', fw)

        obs = np.diag(o_matrix[observations[i], :])

        f_row_vec = np.matrix(fw[:, i])
        fw[:, i + 1] = f_row_vec * np.matrix(t_matrix) * np.matrix(obs)
        fw[:, i + 1] = fw[:, i + 1] / np.sum(fw[:, i + 1])

    return fw


def create_observations(filename, agent):
    obs = []
    # name = filename.split('.')[0].split('_')
    with open(filename) as f:
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
        obs.append([observation_a1, observation_a2])
    #print(obs)
    observations = []
    for i in range(len(obs)):
        a1 = obs[i][agent]
        # print(a1)
        a1 = movetype_to_number(a1)
        observations.append(a1)
    #print(observations)
    return observations
