import json
import os
from pprint import pprint
import numpy
import math
import helpers
from helpers2 import forward, backward
from train import get_obs
'''
NOT USED/FINISHED
'''
TRANSITION = numpy.identity(4)
INITIAL_STATE = numpy.matrix([
    0.25,
    0.25,
    0.25,
    0.25
])

EVIDENCE_GIVEN_STATE = numpy.matrix(
    # Conceder
    [[0.6, 0.05, 0.05, 0.1, 0.1, 0.1],
    # HardHeaded
    [0.1, 0.15, 0.1, 0.1, 0.4, 0.05],
    # TFT
    [0.3, 0.3, 0.1, 0.1, 0.1, 0.1],
    # Random
    [0.2, 0.2, 0.2, 0.2, 0.1, 0.2]]
)

def baum(t, init, obs_state, training_data, iter):
    transition = numpy.copy(t)
    init = numpy.copy(init)
    obs_state = numpy.copy(obs_state)
    states = init.shape[0]
    # print(training_data)
    for i in range(iter):
        temp_pi = numpy.zeros_like(init)
        temp_obs_state = numpy.zeros_like(obs_state)
        temp_t = numpy.zeros_like(t)

        for obs in training_data:
            alpha, za = forward(t, init, obs_state, obs)
            beta = backward(t, init, obs_state, obs)

            temp_pi += alpha[0,:]*beta[0,:]/za
            for j in range(0, len(obs)):
                for s1 in range(states):
                    for s2 in range(states):
                        temp_obs_state[s1, s2] += alpha[i-1,s1]*t[s1, s2]*obs_state[s2, obs[i]]*beta[i, s2]/za
        init = temp_pi/numpy.sum(temp_pi)
        for s in range(states):
            # t[s,:] = temp_t[s,:]/numpy.sum(temp_t[s,:])
            obs_state = temp_obs_state[s,:]/numpy.sum(temp_obs_state[s,:])
    
    return init, t, obs_state


fileDir = os.path.dirname(os.path.realpath('__file__'))
folderPath = os.path.join(fileDir, 'training_logs/')
training_folder = os.path.join(fileDir, 'training_logs')
fileNames = os.listdir(training_folder)

data = get_obs(fileNames[0])
# print(data)


init, t, obs_state = baum(TRANSITION, INITIAL_STATE, EVIDENCE_GIVEN_STATE, data, 100)
print(init)
print(t)
print(obs_state)