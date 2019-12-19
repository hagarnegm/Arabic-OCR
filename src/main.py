from CharSegmentation import *
from preprocessing import *
from LineSegmentation import *
from WordSegmentation import *
from FeatureExtraction import *
# file= open("test.txt","w",encoding='utf-8')
# word_list = []
# word_list = open('..\Text\capr37.txt', encoding='utf-8').read().split()
# for item in word_list:
#     if item in word_list:
#         continue
#     else:
#         word_list.append(item)
# o=0
# l=0
# p=0
# image = io.imread('..\scanned\capr2.png')
# image = preprocessing(image)
# images = lineSegmentation(image)
# dist = getWordDist(images[0])
# for i in range(len(images)):
#     line = wordSegmentation(images[i], dist)
#     base = getBasline(images[i])
#     trans = getLineOfMaxTransitions(images[i], base)
#
#     for k in range(0,len(line),1):
#         cuts, startend, MFV = getPotentialSeparationPoints(images[i], line[k], trans)
#         cuts = cutsFiltration(line[k], cuts, base, trans, MFV, startend)
#
#
#
#         # for h in range(len(cuts)):
#         #    cv2.line(line[k], (cuts[h], 0), (cuts[h], line[k].shape[0]), (255, 0, 0), 1)
#
#         if len(cuts) == len(word_list[o]):
#             print("yay")
#             for f in range(len(cuts)):
#                 print(MFV)
#                 file.write(str(l)+" "+word_list[o][f]+ " "+str(MFV) +" "+ str(base) +"\n")
#                 l+=1
#
#             for f in range(len(cuts)-1):
#                 image=np.copy(line[k])
#
#                 cv2.imwrite('../data/'+str(p)+'.png', image[:,cuts[f+1]:cuts[f]])
#                 p+=1
#             image = np.copy(line[k])
#             cv2.imwrite('../data/'+str(p) + '.png', image[:, 0:cuts[len(cuts) - 1]])
#             p+=1
#
#         else:
#             print(":(")
#         o+=1
image = io.imread("..\data\\72.png")
#
#
print(Solidity(image))
print(image)
viewer = ImageViewer(image)
viewer.show()

# word_list = []
# word_list = open('test.txt', encoding='utf-8').read().split()
# for item in word_list:
#     if item in word_list:
#         continue
#     else:
#         word_list.append(item)
# print(word_list[0])



