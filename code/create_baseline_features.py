"""
This will use the hw3_corpus_tool and take as input ONE csv(train/test) and
output it in CRFSuite format to STDOUT.

:param fileName Fully qualified file name to be specified in sys.argv[1]

:return stdout Print in CRFS format to stdout

example usage: python3 create_baseline_features.py $file > data_CRFsuite.txt
"""

from hw3_corpus_tool import *
import sys

__author__ = 'vaibhav'


fileName = sys.argv[1]
dictDialogUtterance = get_utterances_from_filename(fileName)

speakerChangedFeature = "SPEAKER_CHANGED"
firstUtteranceFeature = "FIRST_UTTERANCE"
tokenFeature = "TOKEN_"
posFeature = "POS_"

lastSpeaker = None
firstUtterance = True

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

    if pos is not None:
        for posTag in pos:
            tokenList.append(tokenFeature + posTag[0])
            posList.append(posFeature + posTag[1])

    if act_tag is None:
        sys.stdout.write('UNKNOWN')
    else:
        sys.stdout.write(act_tag)
    if lastSpeaker is None:
        lastSpeaker = speaker
    if lastSpeaker != speaker:
        sys.stdout.write('\tS_C')  # SPEAKER_CHANGED
        lastSpeaker = speaker
    if firstUtterance:
        sys.stdout.write('\tF_U')  # FIRST_UTTERANCE
        firstUtterance = False

    if tokenList:
        sys.stdout.write('\t')
        sys.stdout.write('\t'.join(tokenList))
    if posList:
        sys.stdout.write('\t')
        sys.stdout.write('\t'.join(posList))
