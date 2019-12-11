from allimports import *


def getWordDist(line):
    words = []
    state = 0
    start = 0
    end = 0
    maxi = 0
    for i in range(line.shape[1] - 1, 0, -1):
        if sum(line[:, i]) > 0 and state == 0:
            start = i
            state = 1
            if maxi < abs(start - end) and end > 0:
                maxi = abs(start - end)
        elif sum(line[:, i]) == 0 and state == 1:
            end = i
            state = 0
    return maxi


def wordSegmentation(line, maxdist):
    segments = []
    start = 0
    state = 0
    pos = 0
    end = 0
    for i in range(line.shape[1] - 1, 0, -1):
        if state == 2 and sum(line[:, i]) > 0:
            state = 1
            if abs(i - pos) >= maxdist - 3 and abs(i - pos) <= maxdist + 2:
                state = 0
                segments.append(np.array(line[:, pos:start + 2]))
        if sum(line[:, i]) > 0 and state == 0:
            start = i
            state = 1
        elif sum(line[:, i]) == 0 and state == 1:
            state = 2
            pos = i
            end = i
    segments.append(np.array(line[:, end:start + 2]))
    return segments











