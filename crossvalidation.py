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
def split_training_test(index,fileNames):
    test_file = fileNames[i]
    train_files = [None]*(len(fileNames)-1)
    j=0
    k=0
    #Just copies array, but jumps over index of test file
    while(j<len(fileNames)-1):
        if(j == i):
            k+=1
        train_files[j] = fileNames[k]
        k+=1
        j+=1
    return test_file, train_files
def better(prob, old_prob,observations):
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
# Pre probabilities of how the different agents may act. Based on pre knowledge
# concede - self - fortun - unfortun - nice - silent - unchange

def train(fileNames):
    _PRE = {
        _CONCEDER: [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
        _HARDHEADED: [0.01, 0.04, 0.05, 0.05, 0.05, 0.6, 0.2],
        _TFT: [0.2, 0.2, 0.15, 0.1, 0.1, 0.15, 0.1],
        _RANDOM: [0.2, 0.2, 0.15, 0.15, 0.1, 0.05, 0.15]
        
    }

    # list of observations from negotiation traces, for each strategy
    observations = {
        _CONCEDER: [],
        _HARDHEADED: [],
         _TFT: [],
        _RANDOM: []
       
    }

    # state transition matrix
    t_mat = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    # matrix that contains the values for P(obs | strategy)
    prob = {
        _CONCEDER: [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
        _HARDHEADED: [0.01, 0.04, 0.05, 0.05, 0.05, 0.6, 0.2],
        _TFT: [0.2, 0.2, 0.15, 0.1, 0.1, 0.15, 0.1],
        _RANDOM: [0.2, 0.2, 0.15, 0.15, 0.1, 0.05, 0.15]     
    }

    # matrix needed to count the number of times a certain move is made
    freqs = {
            _CONCEDER: [0, 0, 0, 0, 0, 0, 0],
            _HARDHEADED: [0, 0, 0, 0, 0, 0, 0],
            _TFT: [0, 0, 0, 0, 0, 0, 0],
            _RANDOM: [0, 0, 0, 0, 0, 0, 0]
        }

    for name in fileNames:
        #print(name)
        freqs[_CONCEDER] = [0, 0, 0, 0, 0, 0, 0]
        freqs[_HARDHEADED] = [0, 0, 0, 0, 0, 0, 0]
        freqs[_TFT] = [0, 0, 0, 0, 0, 0, 0]
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
        if not better(prob, old_prob,observations):
            prob = old_prob
            #print('no update')
        old_prob = prob

        for j in range(len(prob[strat2])):
            prob[strat2][j] = freqs[strat2][j] / (sum(freqs[strat2]))
            prob[strat2][j] = prob[strat2][j] + _PRE[strat2][j]
        prob[strat2] = u.normalize(prob[strat2])

        # update only if we obtain a better prediction
        if not better(prob, old_prob,observations):
            prob = old_prob
            #print('no update')

    print("Concede-selfish-fortune-unfortune-nice-silent-unchange")

    pprint(prob)
    return prob

def classify(prob,filename):
    o_mat = np.array([prob['conceder'], prob['hardheaded'], prob['tft'], prob['random']])


    t_mat = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    observations = np.array(u.create_observations(filename, 0))
    fw = u.filtering(t_mat, o_mat.transpose(), np.array([0.25, 0.25, 0.25, 0.25]), observations)

    print('Result for agent1:')

    f1 = fw[:, observations.size]

    print('Conceder: ', f1[0])
    print('Hardheaded: ', f1[1])
    print('Tft: ', f1[2])
    print('Random: ', f1[3])

    observations = np.array(u.create_observations(filename, 1))


    fw = u.filtering(t_mat, o_mat.transpose(), np.array([0.25, 0.25, 0.25, 0.25]), observations)

    print('Result for agent2:')

    f2 = fw[:, observations.size]

    print('Conceder: ', f2[0])
    print('Hardheaded: ', f2[1])
    print('Tft: ', f2[2])
    print('Random: ', f2[3])
    return f1,f2


fileDir = os.path.dirname(os.path.realpath('__file__'))
folderPath = os.path.join(fileDir, 'training_logs/')
training_folder = os.path.join(fileDir, 'training_logs')
fileNames = os.listdir(training_folder)

print(len(fileNames))
i=0
total_classifications=0
correct_classification=0
while(i<len(fileNames)):
    test_file, train_files = split_training_test(i,fileNames)
    trained_probs = train(train_files)
    prob_agent1, prob_agent2 = classify(trained_probs, 'training_logs/'+test_file)

    strategy_names = test_file.split('.')[0].split('_')
    strat1 = u.strategy_to_number(u.get_strat_name(strategy_names[0]))
    strat2 = u.strategy_to_number(u.get_strat_name(strategy_names[1]))
    #Actual strategy numbers
    print(strat1,strat2)
    #Actual strategy names
    print(strategy_names)

    #Believed strategy after filtering
    print(np.argmax(prob_agent1),np.argmax(prob_agent2))

    if(np.argmax(prob_agent1)==strat1):
        correct_classification+=1
    if(np.argmax(prob_agent2)==strat2):
        correct_classification+=1
    total_classifications+=2
    i+=1
print("Negotiation traces analyzed: {} \n correct classification rate: {}".format(total_classifications,correct_classification/total_classifications))
    



