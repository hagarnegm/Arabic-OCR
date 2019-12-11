import numpy as np
def checkPath(word, s1,s2): #from current cut index to next one
    indices = [[1, 0],[1, -1], [0, -1], [1, 1], [0, 1],[-1, 0],[-1,1],[-1,-1]]
    word[s1,s2] = -1 #visited
    stack1 = [s1]
    stack2=[s2]

    while len(stack1) > 0:
        x = stack1[-1]
        y = stack2[-1]

        stack1.pop()
        stack2.pop()
        for j in range(len(indices)):
            if 0 <= x+indices[j][0] < word.shape[0] and 0 <= y + indices[j][1] < word.shape[1] and\
                    word[x+indices[j][0], y+indices[j][1]] > 0:
                stack1.append(x+indices[j][0])
                stack2.append(y+indices[j][1])
                word[x + indices[j][0], y + indices[j][1]] = -1

word=np.array([[0,1,0,0],[0,1,1,0],[0,0,0,0],[1,1,1,1]])
c=0
for i in range(len(word)):
    for j in range(len(word[0])):
        if word[i][j]>0:
            checkPath(word,i,j)
            c+=1
print(c)