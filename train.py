import json
import os
from pprint import pprint
import numpy
import math
import helpers


'''
NOT USED/FINISHED
'''

fileDir = os.path.dirname(os.path.realpath('__file__'))
folderPath = os.path.join(fileDir, 'training_logs/')
training_folder = os.path.join(fileDir, 'training_logs')
# print(os.listdir(training_folder))


FILE_TO_LEAVE_OUT = -1

_CONCEDER = 'conceder'
_HARDHEADED = 'hardheaded'
_RANDOM = 'random'
_TFT = 'tft'

_NUMBER_OF_STATEGIES = 4

_CONCEDE = 'concede'
_SILENT = 'silent'
_SELFISH = 'selfish'
_FORTUNATE = 'fortunate'
_UNFORTUNATE = 'unfortunate'

# Strategy order: Conceder, HardHeaded, TFT, Random
# Never changes
TRANSITION = numpy.identity(4)
# State matrices are probabilites of each strategy - sums to 1
INITIAL_STATE = numpy.matrix([0.25, 0.25, 0.25, 0.25])
STATE = INITIAL_STATE
# Probability of evidence given state
# Movetype order: Concede, Selfish, Fortunate, Unfortunate, Selfish
EVIDENCE_PROB = numpy.matrix(
    # Conceder
    [[0.6, 0.1, 0.1, 0.1, 0.1],
    # HardHeaded
    [0.1, 0.2, 0.1, 0.1, 0.4],
    # TFT
    [0.3, 0.3, 0.15, 0.15, 0.1],
    # Random
    [0.2, 0.2, 0.2, 0.2, 0.2]]
)

# TFT reacts to opponent
# Based on the agents not having perfect info or perfect OMs
TFT_CONDITIONAL_EVIDENCE_PROB = numpy.matrix([
    # Opp. concedes
    [0.8, 0.05, 0.05, 0.05, 0.05],
    # Opp. is selfish
    [0.05, 0.8, 0.05, 0.05, 0.05],
    # Opp. is Fortunate
    [0.6, 0.1, 0.1, 0.1, 0.1],
    # Opp. is Unfortunate
    [0.1, 0.6, 0.1, 0.1, 0.1],
    # Opp. is Silent
    [0.1, 0.1, 0.1, 0.1, 0.6]
])

OBSERVATIONS = []
def train_model(filename):
    # name = filename.split('.')[0].split('_')
    with open(folderPath + filename) as f:
        data = json.load(f)
    for i in range(len(data['bids'])):
        if not 'agent1' in data['bids'][i].keys():
            OBSERVATIONS.append(['ACCEPT', 'None'])
            break
        observation_a1 = helpers.get_movetype(data, agent=1, roundNr=i)
        if not 'agent2' in data['bids'][i].keys():
            OBSERVATIONS.append([observation_a1, 'ACCEPT'])
            break
        observation_a2 = helpers.get_movetype(data, agent=2, roundNr=i)
        OBSERVATIONS.append([observation_a1, observation_a2])
    # pprint(OBSERVATIONS)
    belief = None
    belief_string = ""
    for i in range(1, len(OBSERVATIONS)-1):
        print(normalize(prob_observations(i)))
        belief = normalize(prob_observations(i))
        print(belief.index(max(belief)))
        belief_string = number_to_strategy(belief.index(max(belief)))
        print(belief_string)
    EVIDENCE_PROB = update_model(belief)

def main():
    fileNames = os.listdir(training_folder)
    testFileName = ""
    if FILE_TO_LEAVE_OUT != -1:
        testFileName = fileNames[FILE_TO_LEAVE_OUT]
        del fileNames[FILE_TO_LEAVE_OUT]
    for name in fileNames:
        train_model(name)
        print(name)
        if True:
            break
        
    # test on testfile
    print(testFileName)






def normalize(array):
    s = sum(array)
    out = [round(x/s, 3) for x in array]
    return out


# SENSIBLE INITIALIZATION helps (book end of section 20.3.1)
# Probably only need one agent in state
# P(state)
# STATE = {
#     _CONCEDER: 0.25,
#     _HARDHEADED: 0.25,
#     _RANDOM: 0.25,
#     _TFT: 0.25
# }

# P(evidence | state)

def movetype_to_number(m):
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

def number_to_strategy(n):
    if n==0:
        return _CONCEDER
    if n==1:
        return _HARDHEADED
    if n==2:
        return _TFT
    if n==3:
        return _RANDOM

def prob_observations(roundNr):
    previous_round_obs = OBSERVATIONS[roundNr-1]
    previous_self = previous_round_obs[0]
    previous_opp = previous_round_obs[1]
    new_obs = OBSERVATIONS[roundNr]
    new_self = new_obs[0]
    probs = []
    for i in range(4):
        temp = STATE.item(i)
        temp *= EVIDENCE_PROB.item(i, movetype_to_number(previous_self))
        if (i==2):
            temp*= TFT_CONDITIONAL_EVIDENCE_PROB.item(movetype_to_number(previous_opp), movetype_to_number(new_self))
        else:
            temp *= EVIDENCE_PROB.item(i, movetype_to_number(new_self))
        probs.append(temp)
    return probs
    

# P(state | evidence) = P(evidence | state)*P(state) / P(evidence)

def calculateState():
    pass
def updateState():
    pass



def update_model(belief, current):
    temp = []
    for i in range(len(belief)):
        old = current.item(i)
        new = old*belief[i]
        new = normalize(new)
        temp.append(new)
    out = numpy.matrix([
        temp
    ])
    return out
main()