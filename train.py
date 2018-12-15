import json
import os
from pprint import pprint
import numpy
import math
import helpers


fileDir = os.path.dirname(os.path.realpath('__file__'))
folderPath = os.path.join(fileDir, 'training_logs/')
training_folder = os.path.join(fileDir, 'training_logs')
print(os.listdir(training_folder))


FILE_TO_LEAVE_OUT = -1

_CONDEDER = 'conceder'
_HARDHEADED = 'hardheaded'
_RANDOM = 'random'
_TFT = 'tft'

_CONCEDE = 'concede'
_SILENT = 'silent'
_SELFISH = 'selfish'
_FORTUNATE = 'fortunate'
_UNFORTUNATE = 'unfortunate'

def train_model(filename):
    name = filename.split('.')[0].split('_')
    with open(folderPath + filename) as f:
        data = json.load(f)
    for i in range(len(data['bids'])):
        print(helpers.getLastXMoveTypes(data, i, name, 3))



def main():
    fileNames = os.listdir(training_folder)
    trainFileName = ""
    if FILE_TO_LEAVE_OUT != -1:
        trainFileName = fileNames[FILE_TO_LEAVE_OUT]
        del fileNames[FILE_TO_LEAVE_OUT]
    for name in fileNames:
        train_model(name)




# Probably only need one agent in state
# P(state)
STATE = {
    _CONDEDER: 0.25,
    _HARDHEADED: 0.25,
    _RANDOM: 0.25,
    _TFT: 0.25
}

# P(evidence | state)
EVIDENCE = {

}

# P(state | evidence) = P(evidence | state)*P(state) / P(evidence)

def calculateState():
    pass
def updateState():
    pass



main()