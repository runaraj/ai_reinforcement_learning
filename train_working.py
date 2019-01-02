import util as u
import os
from pprint import pprint
import json

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

freqs = {
        _CONCEDER: [1, 1, 1, 1, 1, 1, 1],
        _HARDHEADED: [1, 1, 1, 1, 1, 1, 1],
        _TFT: [1, 1, 1, 1, 1, 1, 1],
        _RANDOM: [1, 1, 1, 1, 1, 1, 1]
}
fileNames = os.listdir(training_folder)
testFileName = ""

for name in fileNames:
    strategy_names = name.split('.')[0].split('_')
    strat1 = u.get_strat_name(strategy_names[0])
    strat2 = u.get_strat_name(strategy_names[1])
    obs = u.get_obs(name)

    for i in range(len(obs)):
        a1 = obs[i][0]
        a2 = obs[i][1]

        a1 = u.movetype_to_number(a1)
        a2 = u.movetype_to_number(a2)
        freqs[strat1][a1] += 1

        freqs[strat2][a2] += 1
print("Concede-selfish-fortune-unfortune-nice-silent-unchange")
for k in freqs.keys():
    freqs[k] = u.normalize(freqs[k])

for k in freqs.keys():
    freqs[k] = u.combine_and_normalize(freqs[k], _PRE[k])
pprint(freqs)

with open('output.json', 'w') as outputfile:
    json.dump(freqs, outputfile)


print('training done')


