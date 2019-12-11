from allimports import *


def getBasline(line):
    thinned = thin(line, 10)
    maxProj = 0
    maxIndex = 0
    for i in range(line.shape[0]):
        proj = sum(thinned[i, :])
        if maxProj < proj:
            maxProj = proj
            maxIndex = i
    return maxIndex


def getLineOfMaxTransitions(line, baseline):
    maxTransitions = 0
    maxTransIndex = 0
    for i in range(baseline):
        state = 0
        transitions = 0
        for j in range(line.shape[1]):
            if state == 0 and line[i][j] > 0:
                transitions += 1
                state = 1
            elif state == 1 and line[i][j] == 0:
                transitions += 1
                state = 0
        if maxTransitions < transitions:
            maxTransitions = transitions
            maxTransIndex = i
    return maxTransIndex


def checkCutPoint(word, MFV, start, end):
    print("MFV: ", MFV)
    mid = round((start + end + 1) / 2)
    for i in range(start, end - 1, -1):
        if sum(word[:, i]) == 0:
            print("empty space")
            return i

    if sum(word[:, mid]) == MFV:
        print("just in the middle")
        return mid
    else:
        for i in range(end, mid - 1, -1):
            if sum(word[:, mid]) == MFV:
                print("near the end")
                return i

        for i in range(mid, start + 1):
            if sum(word[:, mid]) == MFV:
                print("near the start")
                return i
    print("bad luck :(")
    return mid

def getHPBnHBA(word,baseline):
    HPA = 0
    for j in range(baseline):
        HPA += sum(word[j,:])
    HPB = 0
    for j in range(baseline + 1, word.shape[0], 1):
        HPB += sum(word[j,:])

    return HPA,HPB

def getPotentialSeparationPoints(line, word, maxTransIndex):
    tempLine = line.copy()
    tempLine = cv2.morphologyEx(tempLine, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    projections = []
    for i in range(tempLine.shape[1]):
        if sum(tempLine[:, i]) > 0:
            projections.append(sum(tempLine[:, i]))
    mostFrValue = mode(projections)
    start = 0
    end = 0
    cut = 0
    state = 1
    allCuts = []
    startend = []
    # finds white pixel means end , find black pixel means start
    for i in range(word.shape[1] - 1, -1, -1):
        if state == 0 and word[maxTransIndex][i] > 0:
            end = i
            print(start, ",", end)
            cut = checkCutPoint(word, mostFrValue, start, end)
            allCuts.append(cut)
            startend.append([start, end])
            state = 1
        elif state == 1 and word[maxTransIndex][i] == 0:
            start = i
            state = 0
    return allCuts, startend, mostFrValue


def checkHolesV(word, cutIndex):
    state = 0
    transitions = 0
    hindex = 0
    for i in range(word.shape[0] - 1, -1, -1):
        if state == 0 and word[i][cutIndex] > 0:
            transitions += 1
            if transitions == 3:
                hindex = i + 1
                return True, hindex
            state = 1
        elif state == 1 and word[i][cutIndex] == 0:
            transitions += 1

            state = 0

    return False, None


def checkHolesH(word, hIndex, start, end):
    state = 0
    transitions = 0
    for i in range(start, end - 1, -1):
        if state == 0 and word[hIndex][i] > 0:
            transitions += 1
            state = 1
        elif state == 1 and word[hIndex][i] == 0:
            transitions += 1
            state = 0

        if transitions == 3:
            return True
    return False


def getStartnEnd(word,hIndex,cutIndex):
    i = cutIndex
    while i < word.shape[1] and checkHolesV(word, i)[0]:
        i += 1
        if i < word.shape[1] and word[hIndex][i] > 0:
            break
    if i==word.shape[1]:
        i-=1
    start = i
    i = cutIndex
    while i >= 0 and checkHolesV(word, i)[0]:
        i -= 1
        if i>=0 and word[hIndex][i] > 0:
            break
    if i<0:
        i=0
    end = i
    return start,end


def checkAllHoles(word,cutIndex):
    i = cutIndex
    con, hIndex = checkHolesV(word, i)
    if con:
        start, end = getStartnEnd(word, hIndex, cutIndex)
        if checkHolesH(word, hIndex, start, end):
            return True
        else:
            con, hIndex2 = checkHolesV(word[0:hIndex, :], i)
            if con:
                start, end = getStartnEnd(word[0:hIndex, :], hIndex2, cutIndex)
                if checkHolesH(word, hIndex2, start, end):
                    return True
    return False


def getHeight(seg):
    HPs = []
    for i in range(seg.shape[0]):
        s = int(sum(seg[i, :]))
        HPs.append(s)
    i = 0
    while i < len(HPs) and HPs[i] == 0:
        i += 1
    start = i
    i = len(HPs) - 1
    while i >= 0 and HPs[i] == 0:
        i -= 1
    end = i
    height = abs(end - start)
    return height, HPs, end

def getWidth(seg):
    VPs = []
    for i in range(seg.shape[1]):
        s = int(sum(seg[:,i]))
        VPs.append(s)
    i = 0
    while i < len(VPs) and VPs[i] == 0:
        i += 1
    start = i
    i = len(VPs) - 1
    while i >= 0 and VPs[i] == 0:
        i -= 1
    end = i
    width = abs(end - start)
    return width

# def checkStroke(seg, baseline, MFV):
#     HPs = []
#     hole = False
#     trash = False
#     dots = False
#     con1 = False
#     con2 = False
#     con3 = False
#     hIndexd=0
#     hIndext = 0
#     for i in range(seg.shape[1]-1,-1,-1):
#         con, hIndex = checkHolesV(seg, i)
#         if con:
#             trash = True
#             hIndext = hIndex
#             if con and sum(seg[hIndex,:]) == 0:
#                 dots = True
#                 hIndexd = hIndex
#                 break
#
#     newSeg = seg.copy()
#     if dots:
#         if hIndexd >=baseline-2:
#             newSeg[hIndexd:newSeg.shape[0], :] = 0
#         else:
#             newSeg[0:hIndexd, :] = 0
#
#     elif trash and not hole:
#         if hIndext >=baseline-2:
#             newSeg[hIndext:newSeg.shape[0], :] = 0
#         else:
#             newSeg[0:hIndext, :] = 0
#
#     for i in range(newSeg.shape[1]-1,-1,-1):
#         con, hIndex = checkHolesV(newSeg, i)
#         if con:
#             if checkHolesH(seg, hIndex, seg.shape[1] - 1, 0):
#                 hole = True
#                 break
#
#     height, HPs, end = getHeight(newSeg)
#     #height = height-abs(baseline-end)
#     HPs = np.array(HPs)
#     secondPeak = 0
#     MF = 0
#     if len(HPs[HPs > 0]) > 0:
#         x = HPs[HPs > 0]
#         x.sort()
#         MF = Counter(x)
#         MF = MF.most_common(1)[0][0]
#     HPA = 0
#     for i in range(baseline):
#         HPA += sum(seg[i, :])
#     HPB = 0
#     for i in range(baseline - 1, seg.shape[0], 1):
#         HPB += sum(seg[i, :])
#     if HPA > HPB:
#         con1 = True
#     if height <= (3/4) * abs(baseline-seg.shape[0]):
#         con2 = True
#     if MF <= MFV:
#         con3 = True
#
#     if con1 and con2 and con3 and not hole:
#         return True, dots
#     return False, dots



def checkDots(seg):
    dots=False
    hIndexd=0
    for i in range(seg.shape[1] - 1, -1, -1):
        con, hIndex = checkHolesV(seg, i)
        if con:
            if con and sum(seg[hIndex,:]) == 0:
                dots = True
                hIndexd = hIndex
                break
    return dots,hIndexd




def checkStroke(seg,baseline,MFV):
    dots = False
    holes=False
    dots, hIndexd=checkDots(seg)
    newSeg = seg.copy()
    # to remove dots
    if dots:
        if hIndexd >=baseline-2:
            newSeg[hIndexd:newSeg.shape[0], :] = 0
        else:
            newSeg[0:hIndexd, :] = 0

    # then check for holes
    for i in range(newSeg.shape[1] - 1, -1, -1):
        con, hIndex = checkHolesV(newSeg, i)
        if con:
            holes=checkAllHoles(newSeg, i)
            if holes:
                return False, dots


    # remove useless characters
    height, HPs, end = getHeight(newSeg)
    #height = height-abs(baseline-end)
    HPs = np.array(HPs)
    secondPeak = 0
    MF = 0
    if len(HPs[HPs > 0]) > 0:
        x = HPs[HPs > 0]
        x.sort()
        MF = Counter(x)
        MF = MF.most_common(1)[0][0]
    HPA,HPB = getHPBnHBA(newSeg, baseline)
    if HPA < HPB:
        return False,dots
    if height > (3/4) * abs(baseline-seg.shape[0]):
        return False,dots
    if MF > MFV+255:
       return False,dots
    return True,dots


def connectedComponent(word, s1, s2):  # from current cut index to next one
    indices = [[1, 0], [1, -1], [0, -1], [1, 1], [0, 1], [-1, 0], [-1, 1], [-1, -1]]
    word[s1, s2] = 3
    stack1 = [s1]
    stack2 = [s2]
    while len(stack1) > 0:
        x = stack1[-1]
        y = stack2[-1]
        stack1.pop()
        stack2.pop()
        for j in range(len(indices)):
            if 0 <= x+indices[j][0] < word.shape[0] and 0 <= y + indices[j][1] < word.shape[1] and word[x+indices[j][0],y+indices[j][1]] > 3:
                word[x + indices[j][0], y + indices[j][1]] = 3
                stack1.append(x+indices[j][0])
                stack2.append(y+indices[j][1])


def checkPath(word,cutIndex,baseline):
    dots, hIndexd=checkDots(word)
    temp= word.copy()
    if dots:
        if hIndexd >= baseline-2:
            temp[hIndexd:temp.shape[0], :] = 0
        else:
            temp[0:hIndexd, :] = 0

    c = 0
    for i in range(temp.shape[0]-1,-1,-1):
        for j in range(temp.shape[1]-1,-1,-1):
            if temp[i][j] > 3:
                connectedComponent(temp, i, j)
                c += 1
    if c > 1:
        return True
    return False


def cutsFiltration(word, cuts, baseline, MTI, MFV, startend):
    valid = []
    i = 0
    while i < len(cuts):
        start = startend[i][0]
        end = startend[i][1]
        HPA, HPB = getHPBnHBA(word[:, end + 1:start], baseline)
        height, HPs, down = getHeight(word[:, end + 1: start + 1])
        con, hIndex = checkHolesV(word, cuts[i])
        # con1, hIndex1 = [False, None]
        # con2, hIndex2 = [False, None]
        if i == len(cuts) - 1:
            endcut = 0
        else:
            # con1, hIndex1 = checkHolesV(word, cuts[i + 1])
            endcut = cuts[i + 1]
        if i >= len(cuts) - 2:
            endcut1 = 0
        else:
            # con2, hIndex2 = checkHolesV(word, cuts[i + 2])
            endcut1 = cuts[i + 2]
        if i >= len(cuts) - 3:
            endcut2 = 0
        else:
            endcut2 = cuts[i + 3]

        stroke1, dots1 = checkStroke(word[:, cuts[i]:cuts[i-1]], baseline, MFV)
        stroke2, dots2 = checkStroke(word[:, endcut:cuts[i]], baseline, MFV)
        stroke3, dots3 = checkStroke(word[:, endcut1:endcut], baseline, MFV)

        if sum(word[:, cuts[i]]) == 0 and i > 0 :  # 2 separated letters
            valid.append(cuts[i])
            print("valid, VP=0: ", i)

        elif i > 0 and checkAllHoles(word[:, endcut:cuts[i-1]+1], abs(cuts[i]-endcut)):  # it has a hole
            print("invalid, hole: ", i)
            del cuts[i]
            continue

        elif checkPath(word[:, endcut:cuts[i] ], cuts[i], baseline):
            valid.append(cuts[i])
            print("valid, no path: ", i)

        elif sum(word[baseline:baseline+1,cuts[i]] )== 0 and i > 0:  # no baseline between start and end of the region
            if HPB >= HPA:
                 print("invalid,no baseline, HPB > HPA: ", i)
                 i+=1
                 continue
        #
        #     elif sum(word[:, cuts[i]]) <= MFV:
        #         valid.append(cuts[i])
        #         print("valid, no baseline,VP <= MFV", i)
        #     else:
        #         print("invalid, no baseline", i)
        #         i+=1
        #         continue

        elif (i == len(cuts)-1 and sum(word[:, cuts[i]]) != 0) or (
                i < len(cuts) - 1 and sum(word[:, cuts[i + 1]]) == 0
                and height < (1 / 2) * abs(baseline - abs(height - down))):
            # last region and height < half baseline to top pixel
            print("invalid, last region or height < baseline to top", i)
            i += 1
            continue

        elif not stroke1:
            valid.append(cuts[i])
            print("not stroke", i)
            # if i < len(cuts)-1:
            #     x=sum(word[baseline, startend[i + 1][1] + 1:startend[i + 1][0] + 1])
            #     y=sum(word[:, cuts[i + 1]])
            #     if not (x == 0 and y <= MFV):
            #         valid.append(cuts[i])
            #         print("not stroke , no baseline, vp at next region <MFV", i)
            #     else:
            #         print("not stroke , baseline, vp at next region > MFV", i)
            #         i += 1
            #         continue

        elif stroke1:
            if dots1:  # dots
                valid.append(cuts[i])
                print("stroke with dots", i)

            if not dots1:     # no dots
                if stroke2:     # next is stroke
                    if not dots2:    # no dots
                        if sum(word[:, endcut2]) > 0:
                            valid.append(cuts[i+2])
                            print("stroke without dots and the next is stroke without dots", i)
                            i += 3
                        else:
                            i += 2
                            print("stroke without dots and the next is stroke without dots", i)

                    elif dots2:    # next is stroke with dots
                        if stroke3 and not dots3:   # next next is stroke without dots
                            valid.append(cuts[i])
                            print("stroke without dots,next is stroke with dots and nn is stroke without dots", i)
                            i += 3
                            continue
                else:  # next is not stroke
                    valid[len(valid)-1] = cuts[i]
                    print("stroke without dots next is not stroke")
        else:
            print("passed all conditions", i)
            valid.append(cuts[i])
        i += 1
    return valid
