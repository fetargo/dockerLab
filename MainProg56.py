from random import random, randrange, randint
import sys
import subprocess 
from subprocess import Popen, PIPE
#arraysQuantity = randint(3,8)
arraysQuantity = 1
maxSubProcesses = 3
#arraysQuantity = 6
activeProcesses = []
processes = []
for j in range(arraysQuantity):
    elementsQuantity = randint(3,5)
    array = []
    lastChance = 1
    for i in range(elementsQuantity-1):
        array.append(randint(-100, 100))
        rnd = random() * (1/elementsQuantity - 0.1) + 0.1
        rnd = round(rnd,1)
        lastChance -= rnd
        array.append(rnd)
    lastChance = round(lastChance, 1)
    array.append(randint(-100, 100))
    array.append(lastChance)
    print(array)
    tostring = str(array).strip('[]')
    #proc = Popen(
    while len(activeProcesses) > maxSubProcesses:
        procQuantity = len(activeProcesses)
        for k in range(procQuantity):
            #print(k)
            if activeProcesses[k].poll() != None:
                #print('deleting')
                activeProcesses.pop(k)
                break
    process = Popen(
        "python3 /home/fetargo/git/ThreadsPy/SubProg.py",
#       "python3 /home/fetargo/git/ProcessPy/test.py",
        shell=True,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True
    )
    #print(tostring)
    processes.append(process)
    activeProcesses.append(process)
    try:
        processes[j].communicate(tostring, 0.5)
    except subprocess.TimeoutExpired:
        continue
    #proc.communicate(tostring)
    #proc.stdin.write(tostring.encode('utf-8'))
    #proc.wait()    # дождаться выполнения
    #output,error = proc.communicate()  # получить tuple('stdout', 'stderr')
    #output,error = processes[j].communicate()  # получить tuple('stdout', 'stderr')
    #if proc.returncode:
    #if processes[j].returncode:
    #    print(error)
    #print('result:', output)
    #log.write(proc.stdout.read())
for j in range(len(processes)):
    output,error = processes[j].communicate()  # получить tuple('stdout', 'stderr')
    if processes[j].returncode:
        print(error)
    print('result:', output)

