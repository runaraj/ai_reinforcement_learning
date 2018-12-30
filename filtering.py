import numpy as np


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

# p0 is the initial state probability vector ([0.25, 0.25, 0.25, 0.25])
# t_matrix is the state transition matrix: for both rows and columns the indexes are 0 for conceder, 1 for hardheaded
# 2 for tit for tat and 3 for random
# o_matrix is the evidence | state matrix (evidence values must be the rows indexes, state values the column ones)
# the indexes for the evidence must have the following correspondence: 0 for conceding, 1 for selfish,
# 2 for unfortunate, 3 for fortunate, 4 for silent and 5 for nice
# observations is a vector containing all the evidences: they must have integer values.
# So we can use: 0 for conceding, 1 for selfish, 2 for unfortunate, 3 for fortunate, 4 for silent and 5 for nice
# I chose these integer values just to be coherent throughout the entire code
# fw at the end is a matrix which contains all the filtering steps. The output in which we are interested is is last
# column, i.e. fw[:, observations.size]
