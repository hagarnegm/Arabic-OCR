import numpy as np
# def checkPath(word, s1,s2): #from current cut index to next one
#     indices = [[1, 0],[1, -1], [0, -1], [1, 1], [0, 1],[-1, 0],[-1,1],[-1,-1]]
#     word[s1,s2] = -1 #visited
#     stack1 = [s1]
#     stack2=[s2]
#
#     while len(stack1) > 0:
#         x = stack1[-1]
#         y = stack2[-1]
#
#         stack1.pop()
#         stack2.pop()
#         for j in range(len(indices)):
#             if 0 <= x+indices[j][0] < word.shape[0] and 0 <= y + indices[j][1] < word.shape[1] and\
#                     word[x+indices[j][0], y+indices[j][1]] > 0:
#                 stack1.append(x+indices[j][0])
#                 stack2.append(y+indices[j][1])
#                 word[x + indices[j][0], y + indices[j][1]] = -1
#
# word=np.array([[0,1,0,0],[0,1,1,0],[0,0,0,0],[1,1,1,1]])
# c=0
# for i in range(len(word)):
#     for j in range(len(word[0])):
#         if word[i][j]>0:
#             checkPath(word,i,j)
#             c+=1
# print(c)


# x=np.array([[1,2,3,4,5,6,7,8,9,10],[11,12,13,14,15,16,17,18,19,20]])
#
# y=np.array([[[1,1],[1,2],[1,4]]])#,[[4,1],[5,1],[6,1]]])
# x[y[0][:,0],y[0][:,1]]=0
# print(x)

# x=np.array([6,5,4,2,4,2,1])
# y=np.array([1,2,3,4,5,6,[0,1]])
#
# y=y[x==min(x)]
# print(y)
# z=np.array([[5,6,7,8],[11,12,13,14]])
# z[y[0][:][0],y[0][:][1]]=0
# print(z)
#




# from collections import Counter
# x=np.array([[1,2],[2,2],[3,3],[2,2],[1,2],[1,3],[1,2],[1,7]])
# MF = Counter(x[:,1])
# print(MF)
# MF = MF.most_common(1)[0][1]
# #x=x[x[:,1] == MF]
# #lenght=len(x)
# #print(lenght)
# print(MF)
# #print(x)





x=[1,2,3,4,5,5,67,3]
y=x.index(3)
print(y)

