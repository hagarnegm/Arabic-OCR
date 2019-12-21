from allimports import *


def lineSegmentation(image):
    segments = []
    indices=[]
    start = 0
    end = 0
    state = 0
    for i in range(image.shape[0]):
        if sum(image[i, :]) > 0 and state == 0:
            start = i
            state = 1
        elif sum(image[i, :]) == 0 and state == 1:
            end = i
            state = 0
            segments.append(np.array(image[start:end, :]))
            indices.append([start,end])
    return segments,indices
