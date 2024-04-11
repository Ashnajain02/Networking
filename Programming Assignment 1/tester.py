import threading as th

# arr = [1, 2, 3]
# arr.append(2)
# print(arr)
# if 1 in arr:
#     print("True")

myDict = {}

myDict[1] = 'hello'
myDict[2] = 'darkness'


def deletee(ID):
    myDict.pop(ID)
    print(myDict)

#T = th.Timer(3.0, deletee, args=(1,2))
print(myDict)
T = th.Timer(3.0, deletee, [1])
T.start()
T = th.Timer(3.0, deletee, [2])
T.start()
print("Exit Program\n")
