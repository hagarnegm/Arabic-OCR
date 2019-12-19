from allimports import *
from CharSegmentation import *
def Solidity(letter):
    hull=convex_hull_image(letter)
    area=(sum(map(sum, (hull[:,:]))))
    LigatureArea=sum(letter)
    solidity=LigatureArea/area
    return solidity

def pixelcount(letter):
    LetterArray=[]
    for i in range(letter.shape[0]):
        for j in range(letter.shape[1]):
            LetterArray.append(letter[i][j])
    return LetterArray

def projection(letter,baseline):
    HPA=sum(map(sum, (letter[0:baseline,:])))
    HPB=sum(map(sum, (letter[baseline::,:])))

    return HPA,HPB

def HWoverLH(letter):
    seghight=getHeight(letter)[0]
    segwidth=getWidth(letter)
    maxh=max(seghight)
    seghight=seghight/letter.shape[0]
    segwidth=segwidth/letter.shape[0]
    return seghight,segwidth

def HolesF(letter):
    holesf=[]
    seghight=getHeight(letter)[0]
    newSeg=np.copy(letter)
    for i in range(newSeg.shape[1] - 1, -1, -1):
        con, hIndex = checkHolesV(newSeg, i)
        if con:
            holes=checkAllHoles(newSeg, i)
            if holes:
                holesf.append(1)
                holesf.append(1 / seghight)
                break
            else:
                holesf.append(0)
                holesf.append(0)
                break
    return holesf


def dotwidth(letter,MFV):
    dot,hindx=checkDots(letter)
    width=[]
    hight=[]
    dwidth=0
    dhight=0
    pos=-1 #dot above-> 0 / dot below ->1
    if dot:
        x=sum(map(sum, (letter[0:hindx,:])))
        y=sum(map(sum, (letter[hindx::,:])))
        if(x>y):
            for i in range(letter.shape[1]):
                hight.append(sum(letter[hindx::,i]))
            for i in range(hindx,letter.shape[0]):
                width.append(sum(letter[i,:]))
            pos=1
        else:
            for i in range(letter.shape[1]):
                hight.append(sum(letter[0:hindx,i]))
            for i in range(hindx):
                width.append(sum(letter[i,:]))
            pos=0
        dwidth=max(width)/MFV
        dhight=max(hight)/MFV


    return pos,dwidth,dhight



