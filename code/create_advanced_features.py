"""
This will use the hw3_corpus_tool and take as input ONE csv(train/test) and
output it in CRFSuite format to STDOUT.

:param fileName Fully qualified file name to be specified in sys.argv[1]

:return stdout Print in CRFS format to stdout

example usage: python3 create_advanced_features.py $file > data_CRFsuite.txt
"""

from hw3_corpus_tool import *
import sys

__author__ = 'vaibhav'


fileName = sys.argv[1]
dictDialogUtterance = get_utterances_from_filename(fileName)

tokenFeature = "T_"
posFeature = "P_"
lastSpeaker = None
firstUtterance = True
continueSpeak = 1

for i in range(0, len(dictDialogUtterance)):
    if i != 0:
        sys.stdout.write('\n')
    tokenList = []
    posList = []
    dialogUtterance = dictDialogUtterance[i]
    act_tag = dialogUtterance[0]
    speaker = dialogUtterance[1]
    pos = dialogUtterance[2]
    text = dialogUtterance[3]

    if act_tag is None:
        sys.stdout.write('UNKNOWN')
    else:
        sys.stdout.write(act_tag)

    if lastSpeaker is None:
        lastSpeaker = speaker
    if lastSpeaker != speaker:
        sys.stdout.write('\tS_C')  # SPEAKER_CHANGED
        lastSpeaker = speaker
        continueSpeak = 1  # reset distance
    if continueSpeak > 1:
        sys.stdout.write('\tD'+str(continueSpeak))  # someone continues to speak # ADV_FEAT
    continueSpeak += 1

    if firstUtterance:
        sys.stdout.write('\tF_U')  # FIRST_UTTERANCE
        firstUtterance = False
    if i == len(dictDialogUtterance)-1:
        sys.stdout.write('\tL_U')  # LAST_UTTERANCE # ADV_FEAT

    if pos is not None:
        for posTag in pos:
            if posTag[0]:  # not in '.,':  # (removed)ADV_FEAT
                tokenList.append(tokenFeature + posTag[0])
            if posTag[1] not in '.,':  # ADV_FEAT
                posList.append(posFeature + posTag[1])

        #
        # ADV_FEAT - n-gram

        # # JUST BIGRAMS
        # newTokenList = []
        # newPosList = []
        # for j in range(0, len(tokenList)-1):
        #     newTokenList.append(tokenFeature + tokenList[j])
        #     newTokenList.append(tokenFeature + tokenList[j] + tokenList[j+1])
        # tokenList = newTokenList
        # for j in range(0, len(posList)-1):
        #     newPosList.append(posFeature + posList[j])
        #     newPosList.append(posFeature + posList[j] + posList[j+1])
        # posList = newPosList

        # # 1..N GRAMS: for each word -> 1 gram, 2 gram.. n gram
        # gram = 2
        # newTokenList = []
        # newPosList = []
        # for j in range(0, len(tokenList)-gram):
        #     for k in range(1, gram+1):  # gram times(1,2,3)
        #         tokenGramj = ''
        #         for l in range(0, k):  # 1 times for 1 gram, 2 times for 2 gram, 3 times for 3 gram
        #             tokenGramj += tokenList[l+j]
        #         newTokenList.append(tokenFeature + tokenGramj)
        # # tokenList = newTokenList

        # for j in range(0, len(posList)-gram):
        #     for k in range(1, gram+1):  # gram times(1,2,3)
        #         posGramj = ''
        #         for l in range(0, k):  # 1 times for 1 gram, 2 times for 2 gram, 3 times for 3 gram
        #             posGramj += posList[l+j]
        #         newPosList.append(posFeature + posGramj)
        # # posList = newPosList

    else:
        sys.stdout.write('\t'+text)  # ADV_FEAT

    if tokenList:
        tokenList.insert(0, 'F_' + tokenList[0])  # First Token # ADV_FEAT
        tokenList.append('L_' + tokenList[-1])  # Last token # ADV_FEAT
        sys.stdout.write('\t')
        sys.stdout.write('\t'.join(tokenList))
    if posList:
        posList.insert(0, 'F_' + posList[0])  # First POS # ADV_FEAT
        posList.append('L_' + posList[-1])  # Last POS # ADV_FEAT
        sys.stdout.write('\t')
        sys.stdout.write('\t'.join(posList))
