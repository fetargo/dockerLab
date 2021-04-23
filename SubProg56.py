import sys
import threading
import os
from random import random, randrange, randint
from time import sleep

condition = threading.Condition()
stdoutLock = threading.Lock()
calcBarrier = threading.Barrier(3)
path = "file_" + str(os.getpid())
try:
    open(path, "w").close()
except OSError:
    print("Failed to create file")
else:
    print("File created")

def parse(arrayToParse, elementsQuantity):
    array = []
    for i in range(elementsQuantity):
        array.append(int(arrayToParse[i*2]))
        array.append(float(arrayToParse[i*2+1]))
    return array

def printForDispersion(array, elementsQuantity, path):
    print("ForDispersion thread started")
    with condition:
        #condition.wait(timeout=5)
        print("ForDispersion calculation started")
        forDispersion = 0
        delayTime = randint(2,5)
        for i in range(elementsQuantity):
            forDispersion += array[i*2] ** 2 * array[i*2+1]
        print("Sleeping for {} seconds\n".format(str(delayTime)))
        #sleep(delayTime)
        with stdoutLock:
            print("Writing forDispersion ({0}) to {1}".format(round(forDispersion, 2), path))
            with open(path, "a") as lab56_file:
                lab56_file.write("ForDispersion: {}\n".format(round(forDispersion, 2)))
        print("ForDispersion thread is waiting for barrier")
    calcBarrier.wait()


#def printArray(array):
 #   with stdoutLock:
  #  print(array)

def readEV(data):
    try:
        leftIndex = data.index("ExpectedValue: ") + len("ExpectedValue: ")
        rightIndex = data.index("\n", leftIndex)
##        print('left index: {}'.format(str(leftIndex)))
##        print('right index: {}'.format(str(rightIndex)))
    except ValueError:
        print("There's no such substring")
        leftIndex = 0
        rightIndex = 0
    try:
        expectedValue = float(data[leftIndex:rightIndex])
    except:
        print("obosrams s index-om")
        expectedValue = 0
    return expectedValue

def readFD(data):
    try:
        leftIndex = data.index("ForDispersion: ") + len("ForDispersion: ")
        rightIndex = data.index("\n", leftIndex)
##        print('left index: {}'.format(str(leftIndex)))
##        print('right index: {}'.format(str(rightIndex)))
    except ValueError:
        print("There's no such substring")
        leftIndex = 0
        rightIndex = 0
    try:
        forDispersion = float(data[leftIndex:rightIndex])
    except:
        print("obosrams s index-om")
        forDispersion = 0
    return forDispersion

def printExpValue(array, elementsQuantity, path):
    print("ExpVal thread started")
    with condition:
        #condition.wait(timeout=5)
        print("ExpVal calculation started")
        expectedValue = 0
        delayTime = randint(2,5)
        for i in range(elementsQuantity):
            expectedValue += array[i*2] * array[i*2+1]
        print("Sleeping for {} seconds\n".format(str(delayTime)))
        #sleep(delayTime)
        with stdoutLock:
            print("Writing expectedValue ({0}) to {1}".format(round(expectedValue, 2), path))
            with open(path, "a") as lab56_file:
                lab56_file.write ("ExpectedValue: {}\n".format(round(expectedValue, 2)))
        print("ExpVal thread is waiting for barrier")
    calcBarrier.wait()

array2 = sys.stdin.read().split(",")
elementsQuantity = len(array2)//2
array = parse(array2, elementsQuantity)
thread1 = threading.Thread(target=printForDispersion, args=(array, elementsQuantity, path)).start()
thread2 = threading.Thread(target=printExpValue, args=(array, elementsQuantity, path)).start()
print("All threads are waiting for condition\n")
sleep(2)
with condition:
    condition.notify_all()
#array3 = array2.replace("0.", "")
#array2 = array2.split(",")
#array = list(map(int, array))
print("Waiting for expected value and forDispersion calculation (Barrier)\n")
calcBarrier.wait()
print("Expected value and forDispersion calculation done\n (Barrier pass)")
with open(path) as lab56_file:
    data = lab56_file.read()
print(data)
expectedValue = readEV(data)
forDispersion = readFD(data)
dispersion = 0

#sleep(5)

dispersion = forDispersion - expectedValue ** 2
print('Expected value: {}'.format(round(expectedValue, 2)))
print('Dispersion: {}'.format(round(dispersion,2)))
#delete file_ProcessID

