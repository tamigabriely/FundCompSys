import random
import math

simTime = 100
l = 40
tsN = 0.025
simulationTime = 2*simTime
sampleRate = 1

def main():
    n = 100
    stdDev = 0
    qN = 0
    wN = 0
    tqN = 0
    qL = []
    wL = []
    tqL = []
    qVar = 0
    wVar = 0
    tqVar = 0
    ro = 0
    for i in range(0,n):
        (q0, w0, tq0,ro0,roN0) = control()
        qL.append(q0)
        qN = qN + q0
        wL.append(w0)
        wN = wN + w0
        tqL.append(tq0)
        tqN = tqN + tq0
        ro = ro + ro0
    qAvg = qN/n
    wAvg = wN/n
    tqAvg = tqN/n
    for item in qL:
        qVar = qVar + math.pow((item - qAvg),2)
    for item in wL:
        #print(item)
        wVar = wVar + math.pow((item - wAvg),2)
    for item in tqL:
        tqVar = tqVar + math.pow((item - tqAvg),2)
    qS = math.sqrt(qVar)
    wS = math.sqrt(wVar)
    tqS = math.sqrt(tqVar)

    ro = ro/n

    print("q:")
    print(qAvg)
    print("w:")
    print(wAvg)
    print("Tq:")
    print(tqAvg)

    print("std dev q:")
    print(qS)
    print("std dev w:")
    print(wS)
    print("std dev tq:")
    print(tqS)

    print("rho:")
    print(ro)


def control():
    schedule = initializeSchedule()
    t = 0.0
    numMEvents = 0
    totalQSize = 0
    totalW = 0

    tQ = 0
    tQNum = 0

    numBirths = 0

    totalQN = 0
    totalWN = 0
    
    qC = []
    qN = []
    qD = []

    stateN = 'idle'
    stateD = 'idle'
    stateC1 = 'idle'
    stateC2 = 'idle' # second CPU server

    while (t < simulationTime):
        event = schedule.pop(0)
        t = event[0] # gets the time
        t0 = event[2] # gets birth time of event
        #print(t0)
        if event[1] == 'birth':
            numBirths = numBirths +1
            (schedule, stateC1, stateC2) = birth(schedule, stateC1, stateC2, t,t0, qC)
        elif event[1] == 'birthC':
            (schedule, stateC1, stateC2) = birthC(schedule,stateC1 , stateC2, t,t0, qC)
        elif event[1] == 'deathC':
            (schedule, stateC1, stateC2,tQ,tQNum) = deathC(schedule, stateC1, stateC2, t,t0, qC,tQ,tQNum)
        elif event[1] == 'birthN':
            (schedule,stateN) = birthN(schedule,stateN,t,t0,qN)
        elif event[1] == 'deathN':
            (schedule,stateN) = deathN(schedule, stateN, t,t0,qN)
        elif event[1] == 'birthD':
            (schedule,stateD) = birthD(schedule,stateD,t,t0,qD)
        elif event[1] == 'deathD':
            (schedule,stateD) = deathD(schedule, stateD, t,t0,qD)
        elif event[1] == 'monitor':
            (schedule, currentQ, currentW, numMEvents) = monitor(schedule, stateC1, stateC2, t,t0, qC, numMEvents)
            # this makes sure the measurement happens at steady state
            #if (t > simTime):
            totalQSize = totalQSize + currentQ
            totalW = totalW + currentW
            temp = len(qN)
            totalWN = temp + totalWN
            if temp != 0:
                totalQN = totalQN + temp + 1
            
    avgQ = totalQSize/numMEvents
    avgW = totalW/numMEvents
    ro = avgQ - avgW
    ro = ro/2
    
    tQ = tQ/tQNum

    # used to calculate utilization of network
    avgQN = totalQN/numMEvents
    avgWN = totalWN/numMEvents
    roN = avgQN - avgWN

    return (avgQ, avgW, tQ,ro, roN)

def initializeSchedule():
    bTime = random.uniform(0.001,0.039)
    bName = 'birth'
    b = (bTime, bName, bTime)
    s = [b]
    mTime = exp(sampleRate)
    mName = 'monitor'
    m = (mTime,mName,mTime)
    s = addToList(m,s)
    return s

def birth(sched, stat, stat2, time,t0, q):
    # Have to schedule a birth no matter what:
    birthTime = exp(l) + time
    name = 'birth'
    sched = addToList((birthTime,name, birthTime),sched)
    return birthC(sched,stat, stat2, time,t0,q)

def birthC(sched,stat, stat2, time,t0,q):
    if stat == 'idle':
        stat = 'busy'
        deathTime = random.uniform(0.001,0.039) + time
        name = 'deathC'
        sched = addToList((deathTime,name,t0),sched)
    elif stat2 == 'idle':
        stat2 = 'busy'
        deathTime = random.uniform(0.001,0.039) + time
        name = 'deathC'
        sched = addToList((deathTime,name,t0),sched)
    elif (stat == 'busy' and stat2 == 'busy'):
        q.append(time)
    return (sched,stat, stat2)

def deathC(sched,stat, stat2, time,t0,q,tQ,deathNum):
    if len(q) == 0:
        if stat == 'busy':
            stat = 'idle'
        elif stat2 == 'busy':
            stat2 = 'idle'
        else:
            print("why am I idle?????")
    if len(q) > 0:
        t = q.pop(0)
        if stat == 'busy':
            deathTime = random.uniform(0.001,0.039) + time
            name = 'deathC'
            sched = addToList((deathTime,name,t),sched)
        elif stat2 == 'busy':
            deathTime = random.uniform(0.001,0.039) + time
            name = 'deathC'
            sched = addToList((deathTime,name,t),sched)
        else:
            print("why am I idle?????")    
    r = random.random()
    if r < 0.5:
        r = r
        #print(time) # used to figure out death rate
        currTQ = time - t0
        #print(currTQ)
        tQ = tQ + currTQ
        deathNum = deathNum +1
    elif r < 0.9:
        birthTime = time
        name = 'birthN'
        sched.insert(0,(birthTime,name,t0))
    elif r > 0.9:
        birthTime = time
        name = 'birthD'
        sched.insert(0,(birthTime,name,t0))
    return(sched,stat, stat2,tQ,deathNum)

def birthN(sched,stateN,time,t0,qN):
    if stateN == 'idle':
        deathTime = tsN + time
        name = 'deathN'
        sched = addToList((deathTime,name,t0),sched)
        stateN = 'busy'
    if stateN == 'busy':
        qN.append(t0)
    return (sched, stateN)

def deathN(sched, stateN, time,t0,qN):
    # schedule a CPU birth
    birthTime = time
    name = 'birthC'
    sched.insert(0,(birthTime,name,t0))
    if len(qN) == 0:
        stateN = 'idle'
    if len(qN) > 0:
        t = qN.pop(0)
        deathTime = tsN + time
        name = 'deathN'
        sched = addToList((deathTime,name,t),sched)
    return (sched,stateN)

def birthD(sched,stateD,time,t0,qD):
    if stateD == 'idle':
        deathTime = random.normalvariate(0.1,0.03) + time
        name = 'deathD'
        sched = addToList((deathTime,name,t0),sched)
        stateD = 'busy'
    if stateD == 'busy':
        qD.append(t0)
    return (sched, stateD)

def deathD(sched, stateD, time,t0,qD):
    r = random.random()
    # schedule a CPU birth with 0.5 chance or a network birth with 0.5 chance
    if r < 0.5:
        birthTime = time
        name = 'birthC'
        sched.insert(0,(birthTime,name,t0))
    else:
        birthTime = time
        name = 'birthN'
        sched.insert(0,(birthTime,name,t0))
    if len(qD) == 0:
        stateD = 'idle'
    if len(qD) > 0:
        t = qD.pop(0)
        deathTime = random.normalvariate(0.1,0.03) + time
        name = 'deathD'
        sched = addToList((deathTime,name,t),sched)
    return (sched,stateD)

   
def monitor(sched, stat, stat2 ,time,t0, q, num):
    #if (time > simTime):
    num = num +1
    mTime = exp(sampleRate) + time
    mName = 'monitor'
    m = (mTime,mName,mTime)
    sched = addToList(m,sched)
    realQ = 0
    if stat == 'busy' and stat2 == 'busy':
        realQ = len(q) + 2
    w = len(q)
    return (sched, realQ, w,num)

def addToList(e,s):
    time = e[0]
    for i in range(0,len(s)):
        if (s[i][0]) > time:
            s.insert(i,e)
            return s
    else:
        s.append(e)
    return s

def exp(r):
    y = random.random()
    x = (- math.log(1.0-y))/r
    return x

