from CharSegmentation import *
from preprocessing import *
from LineSegmentation import *
from WordSegmentation import *


image = io.imread('..\scanned\capr6.png')
print("start")
image = preprocessing(image)
line,lindices = lineSegmentation(image)
for i in range(len(lindices)):
     cv2.line(image, (0,lindices[i][0]), (image.shape[1]-1,lindices[i][0]), (255, 0, 0), 1)
     cv2.line(image, (0, lindices[i][1]), (image.shape[1] - 1, lindices[i][1]), (255, 0, 0), 1)
dist = getWordDist(line[0])

for i in range(len(line)):
    base = getBasline(line[i])
    trans = getLineOfMaxTransitions(line[i], base)
    words, windices = wordSegmentation(line[i], dist)
    for j in range(len(words)):
        cv2.line(image, (windices[j][0], lindices[i][0]), (windices[j][0], lindices[i][1]), (255, 0, 0), 1)
        cv2.line(image, (windices[j][1], lindices[i][0]), (windices[j][1], lindices[i][1]), (255, 0, 0), 1)
        cuts, startend, MFV = getPotentialSeparationPoints(line[i], words[j], trans)
        cuts = cutsFiltration(words[j], cuts, base, trans, MFV, startend)
        for k in range(len(cuts)):
            cv2.line(image, (windices[j][0]+cuts[k], lindices[i][0]), (windices[j][0]+cuts[k], lindices[i][1]), (255, 0, 0), 1)
viewer = ImageViewer(image)
viewer.show()








##################################################









#
# image = io.imread('..\scanned\capr6.png')
# image = preprocessing(image)
# images,lindices = lineSegmentation(image)
# dist = getWordDist(images[0])
# line,windices = wordSegmentation(images[0], dist)
#
# print(dist)
# print(len(line))
# base = getBasline(images[0])
# print("base: ",base)
# trans = getLineOfMaxTransitions(images[0], base)
# print(trans)
# #len(line)
# for i in range(11,12,1):
#     cuts, startend, MFV = getPotentialSeparationPoints(images[0], line[i], trans)
#     cuts = cutsFiltration(line[i], cuts, base, trans, MFV, startend)
#     for j in range(len(cuts)):
#        cv2.line(line[i], (cuts[j], 0), (cuts[j], line[i].shape[0]), (255, 0, 0), 1)
#     viewer = ImageViewer(line[i])
#     viewer.show()
