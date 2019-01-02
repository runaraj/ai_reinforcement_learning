import sys
import numpy as np
import json
import util as u

# call it from the command line passing as argument the filename for test
# e.g. python test_working test1.json
# test1.json must be in the same directory as test_working.py

filename = sys.argv[1]

with open('output.json') as inputfile:
    prob = json.load(inputfile)

o_mat = np.array([prob['conceder'], prob['hardheaded'], prob['random'], prob['tft']])


t_mat = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

observations = np.array(u.create_observations(filename, 0))

fw = u.filtering(t_mat, o_mat.transpose(), np.array([0.25, 0.25, 0.25, 0.25]), observations)

print('Result for agent1:')

f = fw[:, observations.size]

print('Conceder: ', f[0])
print('Hardheaded: ', f[1])
print('Random: ', f[2])
print('Tit-for-tat: ', f[3])

observations = np.array(u.create_observations(filename, 1))

fw = u.filtering(t_mat, o_mat.transpose(), np.array([0.25, 0.25, 0.25, 0.25]), observations)

print('Result for agent2:')

f = fw[:, observations.size]

print('Conceder: ', f[0])
print('Hardheaded: ', f[1])
print('Random: ', f[2])
print('Tit-for-tat: ', f[3])
