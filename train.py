import util as u
import os
import json
import numpy as np



# names observations variables
_CONCEDE = 'concede'
_SILENT = 'silent'
_SELFISH = 'selfish'
_FORTUNATE = 'fortunate'
_UNFORTUNATE = 'unfortunate'
_NICE = 'nice'
_UNCHANGED = 'unchanged'

# names hidden state values
_CONCEDER = 'conceder'
_HARDHEADED = 'hardheaded'
_RANDOM = 'random'
_TFT = 'tft'


fileDir = os.path.dirname(os.path.realpath('__file__'))
folderPath = os.path.join(fileDir, 'training_logs/')
training_folder = os.path.join(fileDir, 'training_logs')
fileNames = os.listdir(training_folder)

# Pre probabilities of how the different agents may act. Based on pre knowledge
# concede - selfish - fortunate - unfortunate - nice - silent - unchanged
_PRE = {
    _CONCEDER: [0.3, 0.05, 0.05, 0.05, 0.15, 0.25, 0.05],
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

# HMM parameters
# state transition matrix
t_mat = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

# evidence probabilities matrix that contains the values for P(obs | strategy)
prob = {
    _CONCEDER: [0.3, 0.05, 0.05, 0.05, 0.15, 0.25, 0.05],
    _HARDHEADED: [0.01, 0.04, 0.05, 0.05, 0.05, 0.6, 0.2],
    _RANDOM: [0.2, 0.2, 0.15, 0.15, 0.1, 0.05, 0.15],
    _TFT: [0.2, 0.2, 0.15, 0.1, 0.1, 0.15, 0.1]
}

# initial probabilities vector
p0 = np.array([0.25, 0.25, 0.25, 0.25])

# matrix needed to count the number of times a certain move is made
freqs = {
        _CONCEDER: [0, 0, 0, 0, 0, 0, 0],
        _HARDHEADED: [0, 0, 0, 0, 0, 0, 0],
        _TFT: [0, 0, 0, 0, 0, 0, 0],
        _RANDOM: [0, 0, 0, 0, 0, 0, 0]
    }

for name in fileNames:
    # reset the frequencies count, except for the tit-for-tat strategy
    freqs[_CONCEDER] = [0, 0, 0, 0, 0, 0, 0]
    freqs[_HARDHEADED] = [0, 0, 0, 0, 0, 0, 0]
    freqs[_RANDOM] = [0, 0, 0, 0, 0, 0, 0]

    # store the previous evidence probabilities matrix
    old_prob = prob

    # extrapolate the strategy IDs from the file name
    strategy_names = name.split('.')[0].split('_')
    strat1 = u.get_strat_name(strategy_names[0])
    strat2 = u.get_strat_name(strategy_names[1])

    # define the observations vector. It would contain couple of moves: [agent1_move, agent2_move]
    obs = u.get_obs(folderPath+name)

    # extrapolate the moves of agent1 and store them
    o1 = []
    for o in obs:
        o1.append(o[0])
    observations[strat1].append(o1)

    # extrapolate the moves of agent2 and store them
    o2 = []
    for o in obs:
        o2.append(o[1])
    observations[strat2].append(o2)

    # count how many moves of each type the agents did
    for i in range(len(obs)):
        a1 = obs[i][0]
        a2 = obs[i][1]

        # each move type correspond to an integer, which is its index in the matrix
        a1 = u.movetype_to_number(a1)
        a2 = u.movetype_to_number(a2)

        freqs[strat1][a1] += 1
        freqs[strat2][a2] += 1

    # compute the probability of each move type, for the strategy being considered
    for j in range(len(prob[strat1])):
        prob[strat1][j] = freqs[strat1][j] / (sum(freqs[strat1]))
        # combine the obtained probability with the prior belief, coming from domain knowledge
        prob[strat1][j] = prob[strat1][j] + _PRE[strat1][j]

    # to make sure that the probabilities sum up to 1
    prob[strat1] = u.normalize(prob[strat1])

    # avoid updating if we obtain worse predictions
    if not u.better(prob, old_prob, t_mat, p0, observations):
        prob = old_prob

    old_prob = prob

    # compute the probability of each move type, for the strategy being considered
    for j in range(len(prob[strat2])):
        prob[strat2][j] = freqs[strat2][j] / (sum(freqs[strat2]))
        # combine the obtained probability with the prior belief, coming from domain knowledge
        prob[strat2][j] = prob[strat2][j] + _PRE[strat2][j]

    # to make sure that the probabilities sum up to 1
    prob[strat2] = u.normalize(prob[strat2])

    # avoid updating if we obtain worse predictions
    if not u.better(prob, old_prob, t_mat, p0, observations):
        prob = old_prob


print('Training done')
print()

print('The obtained evidence probabilities matrix is')
m = np.array([prob['conceder'], prob['hardheaded'], prob['random'], prob['tft']])
print(m)

print()
print('Move type order:')
print("concede - selfish - fortunate - unfortunate - nice - silent - unchanged")

# store the obtained matrix in a json file, to be able to use it when testing
with open('output.json', 'w') as outputfile:
    json.dump(prob, outputfile)





