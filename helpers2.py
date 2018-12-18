import numpy

'''
@t = transition probs
@init = initial state probs
@obs_state = prob of evidence given state
@evidence = list of evidence
'''
def forward(t, init, obs_state, evidence):
    alpha = numpy.zeros((len(evidence), init.shape[1]))
    # first row is what we know initially
    # print(obs_state)
    # print(obs_state[:, evidence[0]])
    # print(alpha)
    # print(init)
    # print(alpha[0,:])
    print(evidence)
    # print(obs_state[:, evidence[0]])
    # print(init*obs_state[:, evidence[0]])
    alpha[0, :] = init * obs_state[:, evidence[0]]
    alpha[0, :] = normalize(alpha[0, :])
    for i in range(1, len(evidence)):
        for j in range(len(init)):
            for k in range(len(init)):
                alpha[i, j] += alpha[i-1, k]*t[k,j]*obs_state[j, evidence[i]]
            alpha[j, :] = normalize(alpha[j, :])
    alpha = numpy.round(alpha, 3)
    return alpha, numpy.sum(alpha[len(evidence)-1, :])

'''
@t = transition probs
@init = initial state probs
@obs_state = prob of evidence given state
@evidence = list of evidence
'''
def backward(t, init, obs_state, evidence):
    beta = numpy.zeros((len(evidence), init.shape[0]))
    beta[len(evidence)-1, :] = 1

    for i in range(len(evidence)-2, -1, -1):
        for j in range(len(init)):
            for k in range(len(init)):
                beta[i, j] += beta[i+1, k] * t[j,k]*obs_state[k, evidence[i+1]]
    beta = numpy.round(beta,3)
    return beta

def normalize(array):
    s = numpy.sum(array)
    return array/s

# ====== TESTING Forward ======
# tes = numpy.array([[1, 0], [2, 3]])
# test_transition = numpy.array([
#     [0.7, 0.3],
#     [0.3, 0.7]
# ])
# test_init = numpy.array(
#     [0.5, 0.5]
# )
# test_obs_state = numpy.array([
#     [0.9, 0.1],
#     [0.2, 0.8]
# ])
# test_evidence = numpy.array(
#     [0, 0]
# )
# print(forward(test_transition, test_init, test_obs_state, test_evidence))
# ======================================================


# # ====== TESTING Backward =======
# test_transition = numpy.array([
#     [0.7, 0.3],
#     [0.3, 0.7]
# ])
# test_init = numpy.array(
#     [0.5, 0.5]
# )
# test_obs_state = numpy.array([
#     [0.9, 0.1],
#     [0.2, 0.8]
# ])
# test_evidence = numpy.array(
#     [0, 0]
# )
# print(backward(test_transition, test_init, test_obs_state, test_evidence))
# ====================================