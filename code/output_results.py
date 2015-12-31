"""
This file will output the accuracy % to stdout

:param testFile (actual output) will use the first token on each line to make comparison
:param outputFile (predicted output) to compare against(each line has one output)

"""

__author__ = 'vaibhav'


def _output_accuracy(testFile, outputFile, metricsF):
    testF = open(testFile, 'r')
    outputF = open(outputFile, 'r')
    outputF = outputF.readlines()
    correct = 0
    length = 0
    mismatchDict = {}
    for lineIdx, testLine in enumerate(testF, start=0):
        outputLine = outputF[lineIdx].rstrip('\n')
        testLine = testLine.rstrip('\n')
        testValues = testLine.split('\t')
        if outputLine == testValues[0]:
            correct += 1
        else:
            key = outputLine + '->' + testValues[0]
            if key in mismatchDict:
                mismatchDict[key] += 1
            else:
                mismatchDict[key] = 1
        length += 1
    mismatchSorted = sorted(mismatchDict.items(), key=lambda mismatchDict: mismatchDict[1], reverse=True)
    for i in range(0, 10):
        dic = mismatchSorted[i]
        print(dic[0] + '\t' + str(dic[1]), file=metricsF)
    return 100 * correct / length
