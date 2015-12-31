"""
This file will do a k_fold cross validation on TRAIN data and
report accuracy percentage for each kth iteration and
also show the mean accuracy.

:param k sys.argv[1] number of folds
:param pythonCreateFeatureFile sys.argv[2] File name to be used to create CRFS format (baseline or advanced)
:param trainDataDir sys.argv[3] Relative Path for train data eg. ../data/train
:param metricsFile sys.argv[4] File to output the metrics to

:return stdout

"""

from output_results import _output_accuracy
import sys
import os
import random
import math
import shutil

k = int(sys.argv[1])  # 3
pythonCreateFeatureFile = sys.argv[2]  # 'create_baseline_features.py'
trainDataDir = sys.argv[3]  # '../data/train'
metricsFile = sys.argv[4]  # 'metrics.txt'

allFiles = []

for subdir, dirs, files in os.walk(trainDataDir):
    for file in files:
        if not file.startswith('.'):
            allFiles.append(os.path.join(subdir, file))

random.shuffle(allFiles)
lenAllFiles = len(allFiles)
testLength = math.floor(lenAllFiles / k)
CV_FOLDER = "./cv/"
MODEL_FILE = ".model"
OUTPUT_FILE = ".output"
CRSF_TRAIN_FILE = "_trainfile"
CRSF_TEST_FILE = "_testfile"
CRSF_TRAIN_LOG_FILE = "_train_log"
if os.path.exists('./cv'):
    shutil.rmtree('./cv')
os.makedirs(os.path.dirname(CV_FOLDER), exist_ok=True)
metricsF = open(metricsFile, 'w+')

totalAccuracy = 0
for i in range(0, k):  # k fold times, for k=3, (0,1,2)
    # starting for ith CV
    kStamp = 'k'+str(i+1)+'_'
    modelFile = CV_FOLDER+kStamp+MODEL_FILE
    outputFile = CV_FOLDER+kStamp+OUTPUT_FILE
    logFile = CV_FOLDER+kStamp+CRSF_TRAIN_LOG_FILE

    allTrainFile = CV_FOLDER+kStamp+CRSF_TRAIN_FILE
    allTestFile = CV_FOLDER+kStamp+CRSF_TEST_FILE
    testArray = allFiles[i * testLength:(i + 1) * testLength]
    trainArray = [ele for ele in allFiles if ele not in testArray]
    print(trainArray, file=metricsF)
    for trFile in trainArray:
        os.system('python3 ' + pythonCreateFeatureFile + ' ' + trFile + ' >> ' + allTrainFile)
        os.system('echo $\'\n\' >> ' + allTrainFile)
    os.system('./crfsuite learn -m ' + modelFile + ' ' + allTrainFile + ' > ' + logFile)
    print(testArray, file=metricsF)
    for teFile in testArray:
        os.system('python3 ' + pythonCreateFeatureFile + ' ' + teFile + ' >> ' + allTestFile)
        os.system('echo $\'\n\' >> ' + allTestFile)
    os.system('./crfsuite tag -m ' + modelFile + ' ' + allTestFile + ' > ' + outputFile)
    accuracy = _output_accuracy(allTestFile, outputFile, metricsF)
    sys.stdout.write('Accuracy for ' + str(i+1) + ' iteration = ' + str(accuracy) + '\n')
    metricsF.write('Accuracy for ' + str(i+1) + ' iteration = ' + str(accuracy) + '\n')
    totalAccuracy += accuracy


sys.stdout.write('Average Accuracy = ' + str(totalAccuracy/k) + '\n')
metricsF.write('Average Accuracy = ' + str(totalAccuracy/k) + '\n')
metricsF.close()