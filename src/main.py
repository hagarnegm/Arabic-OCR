from CharSegmentation import *
from preprocessing import *
from LineSegmentation import *
from WordSegmentation import *

image = io.imread('..\scanned\capr37.png')
image = preprocessing(image)
images = lineSegmentation(image)
dist = getWordDist(images[0])
line = wordSegmentation(images[3], dist)

print(dist)
print(len(line))
base = getBasline(images[3])
trans = getLineOfMaxTransitions(images[3], base)
print(trans)
#len(line)
for i in range(7,8,1):
    cuts, startend, MFV = getPotentialSeparationPoints(images[3], line[i], trans)
    cuts = cutsFiltration(line[i], cuts, base, trans, MFV, startend)

    # i=1
    # end=0
    # while i < len(cuts):
    #     print("loop no: ",i)
    #     if (i==len(cuts)-1):
    #         end=1
    #     else:
    #         end=cuts[i+1]
    #     print("start: ",cuts[i-1],",end: ",end)

    #     con,hindex=checkHolesV(line[15],cuts[i])
    #     if con and checkHolesH(line[15],hindex,cuts[i-1],end):
    #         del cuts[i]
    #         del startend[i]
    #         i-=1
    #     i+=1

    for j in range(len(cuts)):
       cv2.line(line[i], (cuts[j], 0), (cuts[j], line[i].shape[0]), (255, 0, 0), 1)
    viewer = ImageViewer(line[i])
    viewer.show()

