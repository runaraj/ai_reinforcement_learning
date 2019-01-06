import numpy as np
import json
import os

# This file contains all the useful methods used both for training and testing

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


# get movetypes (i.e. observations) from @filename and return them in a list
def get_obs(filename):
    observations = []

    with open(filename) as f:
        data = json.load(f)
    for i in range(len(data['bids'])):
        if 'agent1' not in data['bids'][i].keys():
            # bid is 'Accept'
            continue

        observation_a1 = get_movetype(data, agent=1, roundNr=i)

        if 'agent2' not in data['bids'][i].keys():
            # bid is 'Accept'
            continue

        observation_a2 = get_movetype(data, agent=2, roundNr=i)

        observations.append([observation_a1, observation_a2])

    return observations


# get movetype for @agent in @roundNr
def get_movetype(data, agent, roundNr):
    opponent = 1
    name = 'agent2'
    if agent == 1:
        opponent = 2
        name = 'agent1'

    # if the new bid is exactly the same as the new one the bid is unchanged
    try:
        prev_own_bid = data['bids'][roundNr - 1][name].split(',')
        new_own_bid = data['bids'][roundNr][name].split(',')
        equal = True
        for i in range(len(prev_own_bid)):
            if prev_own_bid[i] != new_own_bid[i]:
                equal = False
                break
        if equal:
            return _UNCHANGED
    except Exception:
        pass

    util_prev_own_bid = get_utility(data, roundNr - 1, agent)
    util_new_own_bid = get_utility(data, roundNr, agent)

    opp_util_prev_own_bid = get_utility(data, roundNr - 1, opponent)
    opp_util_new_own_bid = get_utility(data, roundNr, opponent)

    self_diff = util_new_own_bid - util_prev_own_bid

    opp_diff = opp_util_new_own_bid - opp_util_prev_own_bid

    # classification of the move
    if 0 <= abs(self_diff) < 0.01 and 0 <= abs(opp_diff) < 0.01:
        return _SILENT
    if (self_diff < 0) and (opp_diff >= 0):
        return _CONCEDE
    if (self_diff <= 0) and (opp_diff < 0):
        return _UNFORTUNATE
    if (self_diff > 0) and (opp_diff > 0):
        return _FORTUNATE
    if (self_diff > 0) and (opp_diff <= 0):
        return _SELFISH
    if (abs(self_diff) == 0) and (opp_diff > 0):
        return _NICE


# gets the utility of @agent in @roundNr for bid given by @bidder
def get_utility(data, roundNr, agent):
    profile = data['Utility1']
    bidder = 'agent1'
    if agent == 2:
        # agentName = 'agent2'
        profile = data['Utility2']
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


# Implements the filtering algorithm
def filtering(t_matrix, o_matrix, p0, observations):
    fw = np.zeros((p0.size, observations.size + 1))
    fw[:, 0] = p0

    for i in range(observations.size):
        obs = np.diag(o_matrix[observations[i], :])

        f_row_vec = np.matrix(fw[:, i])
        fw[:, i + 1] = f_row_vec * np.matrix(t_matrix) * np.matrix(obs)
        fw[:, i + 1] = fw[:, i + 1] / np.sum(fw[:, i + 1])

    return fw


# Returns observations as a list of integer representing the moves of @agent
def create_observations(filename, agent):
    obs = get_obs(filename)

    observations = []
    for i in range(len(obs)):
        a1 = obs[i][agent]
        a1 = movetype_to_number(a1)
        observations.append(a1)

    return observations


# help method that check if the new model is better than the previous one, using filtering
def better(p, old_p, t_matrix, p0, observations):

    isbetter = True

    # check the prediction for each strategy
    for strategy in ['conceder', 'hardheaded', 'random', 'tft']:
        # and for each observations sequence of that strategy moves seen so far
        for observ in observations[strategy]:

            # transform the observations in integers
            ob = []
            for k in range(len(observ)):
                m1 = movetype_to_number(observ[k])
                ob.append(m1)
            ob = np.array(ob)

            # do filtering with the new model
            o_mat_new = np.array([p['conceder'], p['hardheaded'], p['random'], p['tft']])
            fw_new = filtering(t_matrix, o_mat_new.transpose(), p0, ob)

            # do filtering with the old model
            o_mat_old = np.array([old_p['conceder'], old_p['hardheaded'], old_p['random'], old_p['tft']])
            fw_old = filtering(t_matrix, o_mat_old.transpose(), p0, ob)

            s = strategy_to_number(strategy)

            # check which result is better
            if fw_new[s, ob.size] <= fw_old[s, ob.size]:
                isbetter = False
                break
    return isbetter
