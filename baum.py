import json
import os
from pprint import pprint
import numpy
import math
import helpers
import helpers2
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
    [[0.6, 0.1, 0.1, 0.1, 0.1],
    # HardHeaded
    [0.1, 0.2, 0.1, 0.1, 0.4],
    # TFT
    [0.3, 0.3, 0.15, 0.15, 0.1],
    # Random
    [0.2, 0.2, 0.2, 0.2, 0.2]]
)

