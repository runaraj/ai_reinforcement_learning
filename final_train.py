import util as u
import os
from pprint import pprint
import json
import numpy as np


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
fileNames = os.listdir(training_folder)

# Pre probabilities of how the different agents may act. Based on pre knowledge
# concede - self - fortun - unfortun - nice - silent - unchange
_PRE = {
    _CONCEDER: [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
    _HARDHEADED: [0.01, 0.04, 0.05, 0.05, 0.05, 0.6, 0.2],
    _RANDOM: [0.2, 0.2, 0.15, 0.15, 0.1, 0.05, 0.15],
    _TFT: [0.2, 0.2, 0.15, 0.1, 0.1, 0.15, 0.1]
}

# list of observations from negotiation traces, for each strategy
observations = {
    _CONCEDER: [],
    _HARDHEADED: [],
    _RANDOM: [],
    _TFT: []
}

# state transition matrix
t_mat = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

# matrix that contains the values for P(obs | strategy)
prob = {
    _CONCEDER: [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
    _HARDHEADED: [0.01, 0.04, 0.05, 0.05, 0.05, 0.6, 0.2],
    _RANDOM: [0.2, 0.2, 0.15, 0.15, 0.1, 0.05, 0.15],
    _TFT: [0.2, 0.2, 0.15, 0.1, 0.1, 0.15, 0.1]
}

# matrix needed to count the number of times a certain move is made
freqs = {
        _CONCEDER: [0, 0, 0, 0, 0, 0, 0],
        _HARDHEADED: [0, 0, 0, 0, 0, 0, 0],
        _TFT: [0, 0, 0, 0, 0, 0, 0],
        _RANDOM: [0, 0, 0, 0, 0, 0, 0]
    }


def better(prob, old_prob):

    better = True
    # state transition matrix
    t_mat = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    for strat in ['conceder', 'hardheaded', 'random', 'tft']:
        for obs in observations[strat]:

            # transform the observations in numbers
            o = []
            for i in range(len(obs)):
                a1 = u.movetype_to_number(obs[i])
                o.append(a1)
            o = np.array(o)

            o_mat_new = np.array([prob['conceder'], prob['hardheaded'], prob['random'], prob['tft']])
            fw_new = u.filtering(t_mat, o_mat_new.transpose(), np.array([0.25, 0.25, 0.25, 0.25]), o)

            o_mat_old = np.array([old_prob['conceder'], old_prob['hardheaded'], old_prob['random'], old_prob['tft']])
            fw_old = u.filtering(t_mat, o_mat_old.transpose(), np.array([0.25, 0.25, 0.25, 0.25]), o)

            s = u.strategy_to_number(strat)

            if fw_new[s, o.size] <= fw_old[s, o.size]:
                better = False
                break
    return better


for name in fileNames:
    #print(name)
    freqs[_CONCEDER] = [0, 0, 0, 0, 0, 0, 0]
    freqs[_HARDHEADED] = [0, 0, 0, 0, 0, 0, 0]
    freqs[_RANDOM] = [0, 0, 0, 0, 0, 0, 0]

    old_prob = prob

    strategy_names = name.split('.')[0].split('_')
    strat1 = u.get_strat_name(strategy_names[0])
    strat2 = u.get_strat_name(strategy_names[1])
    obs = u.get_obs(name)

    o1 = []
    for o in obs:
        o1.append(o[0])
    observations[strat1].append(o1)

    o2 = []
    for o in obs:
        o2.append(o[1])
    observations[strat2].append(o2)

    for i in range(len(obs)):
        a1 = obs[i][0]
        a2 = obs[i][1]

        a1 = u.movetype_to_number(a1)
        a2 = u.movetype_to_number(a2)

        freqs[strat1][a1] += 1
        freqs[strat2][a2] += 1

    for j in range(len(prob[strat1])):
        prob[strat1][j] = freqs[strat1][j] / (sum(freqs[strat1]))
        prob[strat1][j] = prob[strat1][j] + _PRE[strat1][j]

    prob[strat1] = u.normalize(prob[strat1])

    # update only if we obtain a better prediction
    if not better(prob, old_prob):
        prob = old_prob
        #print('no update')
    old_prob = prob

    for j in range(len(prob[strat2])):
        prob[strat2][j] = freqs[strat2][j] / (sum(freqs[strat2]))
        prob[strat2][j] = prob[strat2][j] + _PRE[strat2][j]
    prob[strat2] = u.normalize(prob[strat2])

    # update only if we obtain a better prediction
    if not better(prob, old_prob):
        prob = old_prob
        #print('no update')


print("Concede-selfish-fortune-unfortune-nice-silent-unchange")

pprint(prob)

with open('output.json', 'w') as outputfile:
    json.dump(prob, outputfile)


print('training done')



