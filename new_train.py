import util as u
import os
from pprint import pprint
import json


def prob_sequence(obs, prob, strat, x):
    p = 1
    for i in range(len(obs)):
        a = obs[i][x]
        a = u.movetype_to_number(a)
        #print(p)
        #print('prob is ', prob[strat][a])
        p = p * prob[strat][a]
    #print('prob is: ', p)
    return p


def better(prob, old_prob, strat, x):
    better = True
    for obs in observations[strat]:
        #print(strat, obs)
        p_new = 1
        p_old = 1
        for i in range(len(obs)):
            a = obs[i][x]
            a = u.movetype_to_number(a)

            p_new = p_new * prob[strat][a]
            p_old = p_old * old_prob[strat][a]
        if p_old > p_new:
            better = False
            break
    print(better)
    return better

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

# Pre probabilities of how the different agents may act. Based on pre knowledge
# concede - self - fortun - unfortun - nice - silent - unchange
_PRE = {
    _CONCEDER: [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
    _HARDHEADED: [0.01, 0.04, 0.05, 0.05, 0.05, 0.6, 0.2],
    _RANDOM: [0.2, 0.2, 0.15, 0.15, 0.1, 0.05, 0.15],
    _TFT: [0.2, 0.2, 0.15, 0.1, 0.1, 0.15, 0.1]
}
observations = {
    _CONCEDER: [],
    _HARDHEADED: [],
    _RANDOM: [],
    _TFT: []
}


prob = {
    _CONCEDER: [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
    _HARDHEADED: [0.01, 0.04, 0.05, 0.05, 0.05, 0.6, 0.2],
    _RANDOM: [0.2, 0.2, 0.15, 0.15, 0.1, 0.05, 0.15],
    _TFT: [0.2, 0.2, 0.15, 0.1, 0.1, 0.15, 0.1]
}

fileNames = os.listdir(training_folder)
testFileName = ""
freqs = {
        _CONCEDER: [1, 1, 1, 1, 1, 1, 1],
        _HARDHEADED: [1, 1, 1, 1, 1, 1, 1],
        _TFT: [1, 1, 1, 1, 1, 1, 1],
        _RANDOM: [1, 1, 1, 1, 1, 1, 1]
    }

for name in fileNames:
    print(name)
    freqs[_CONCEDER] = [1, 1, 1, 1, 1, 1, 1]
    freqs[_HARDHEADED] = [1, 1, 1, 1, 1, 1, 1]
    freqs[_RANDOM] = [1, 1, 1, 1, 1, 1, 1]

    old_prob = prob
    pprint(old_prob)
    strategy_names = name.split('.')[0].split('_')
    strat1 = u.get_strat_name(strategy_names[0])
    strat2 = u.get_strat_name(strategy_names[1])
    obs = u.get_obs(name)

    observations[strat1].append(obs)
    observations[strat2].append(obs)

    for i in range(len(obs)):
        a1 = obs[i][0]
        a2 = obs[i][1]

        a1 = u.movetype_to_number(a1)
        a2 = u.movetype_to_number(a2)

        freqs[strat1][a1] += 1
        freqs[strat2][a2] += 1
    #pprint(freqs)
    for j in range(len(prob[strat1])):
        prob[strat1][j] = freqs[strat1][j] / (sum(freqs[strat1])) #- freqs[strat1][j])
        prob[strat1][j] = prob[strat1][j] + _PRE[strat1][j]  # toglierlo?
    prob[strat1] = u.normalize(prob[strat1])
            # if prob(obs | thetanew) > prob(obs | thetaold), update
    #if prob_sequence(obs, prob, strat1, 0) < prob_sequence(obs, old_prob, strat1, 0):
     #   prob = old_prob
    if not better(prob, old_prob, strat1, 0):
        prob = old_prob
        print('no update')
    old_prob = prob

    for j in range(len(prob[strat2])):
        prob[strat2][j] = freqs[strat2][j] / (sum(freqs[strat2])) #- freqs[strat2][j])
        prob[strat2][j] = prob[strat2][j] + _PRE[strat2][j]  # toglierlo?
    prob[strat2] = u.normalize(prob[strat2])
            # if prob(obs | thetanew) > prob(obs | thetaold), update
    #if prob_sequence(obs, prob, strat2, 1) < prob_sequence(obs, old_prob, strat2, 1):
     #   prob = old_prob
    if not better(prob, old_prob, strat2, 1):
        prob = old_prob
        print('no update')


    pprint(prob)
print("Concede-selfish-fortune-unfortune-nice-silent-unchange")

pprint(prob)

with open('output.json', 'w') as outputfile:
    json.dump(prob, outputfile)


print('training done')



