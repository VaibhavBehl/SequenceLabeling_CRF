"""
outputs to stdout the frequency of features for each act_tag for debugging purposes
"""

import sys
import collections

__author__ = 'vaibhav'

crfsFile = sys.argv[1]  # a file in crfs format './cv/kx__train'
crfsF = open(crfsFile, 'r+')
allFreqDict = {}

for lineIdx, crfsLine in enumerate(crfsF, start=0):
    crfsLine = crfsLine.rstrip('\n')
    if len(crfsLine) > 0:
        crfsValues = crfsLine.split('\t')
        actTag = crfsValues[0]
        if actTag not in allFreqDict:
            allFreqDict[actTag] = {}

        actTagDict = allFreqDict[actTag]
        for i in range(1,len(crfsValues)):
            featureKey = crfsValues[i]
            if featureKey not in actTagDict:
                actTagDict[featureKey] = 1
            else:
                actTagDict[featureKey] += 1

odAllFreqDict = collections.OrderedDict(sorted(allFreqDict.items()))

for actTag in odAllFreqDict:  # each od is also a dic which we have to show in descending order
    sys.stdout.write('\n')
    sys.stdout.write('\n')
    sys.stdout.write(actTag + ' -> ')
    actTagDict = odAllFreqDict[actTag]
    actTagDictSorted = sorted(actTagDict.items(), key=lambda actTagDict: actTagDict[1], reverse=True)
    for i in range(0, len(actTagDictSorted)):
        actTagDictEle = actTagDictSorted[i]
        feat = actTagDictEle[0]
        if actTagDictEle[1] > 99 and (not feat.startswith('T_')):
            sys.stdout.write(actTagDictEle[0] + ':' + str(actTagDictEle[1]) + ' ')
