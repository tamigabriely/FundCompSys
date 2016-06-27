import random
import math

simTime = 100
l = 65
ts = 0.015
mu = 1/ts
K = 3
simulationTime = 2*simTime
sampleRate = l*2

def main():
    n = 100
    stdDev = 0
    qN = 0
    tqN = 0
    qL = []
    tqL = []
    qVar = 0
    tqVar = 0
    rej = 0
    ro = 0
    for i in range(0,n):
        (q0,tq0,r0,ro0) = control()
        qL.append(q0)
        qN = qN + q0
        tqL.append(tq0)
        tqN = tqN + tq0
        rej = rej +r0
        ro = ro + ro0
    qAvg = qN/n
    tqAvg = tqN/n
    for item in qL:
        qVar = qVar + math.pow((item - qAvg),2)
    for item in tqL:
        tqVar = tqVar + math.pow((item - tqAvg),2)
    qS = math.sqrt(qVar)
    tqS = math.sqrt(tqVar)

    rej = rej/n
    ro = ro/n

    print("lambda: " + str(l) + " ts: " + str(ts))
    print("q:")
    print(qAvg)
    print("Tq:")
    print(tqAvg)

    print("std dev q:")
    print(qS)
    print("std dev tq:")
    print(tqS)

    print("rejection probability:")
    print(rej)

    #print("effective rho:")
    #print(ro)


def control():
    state = 'idle'
    schedule = initializeSchedule()
    t = 0.0
    numMEvents = 0
    totalQSize = 0
    totalW = 0
    tQ = 0
    tQNum = 0
    numBirths = 0
    q = []
    numRejected = 0

    idleTQ = 0
    idleTQNum = 0

    while (t < simulationTime):
        #print(schedule)
        event = schedule.pop(0)
        t = event[0] # gets the time
        if event[1] == 'birth':
            numBirths = numBirths +1
            (schedule,state,numRejected, idleTQ,idleTQNum) = birth(schedule,state,t, q,numRejected,idleTQ,idleTQNum)
        elif event[1] == 'death':
            (schedule,state,tQ,tQNum) = death(schedule,state,t, q, tQ,tQNum)
        elif event[1] == 'monitor':
            (schedule, currentQ, currentW, numMEvents) = monitor(schedule, state,t, q, numMEvents)
            if (t > simTime):
                totalQSize = totalQSize + currentQ
                totalW = totalW + currentW
    avgQ = totalQSize/numMEvents
    avgW = totalW/numMEvents
    ro = avgQ - avgW
    tQ = (tQ+idleTQ)/(tQNum+idleTQNum)
    rejProb = numRejected/numBirths
    '''
    print("q = " + str(avgQ))
    print("w = " + str(avgW))
    print("ro = " + str(ro))
    print("tQ = " + str(tQ))
    '''
    return (avgQ, tQ,rejProb,ro)

def initializeSchedule():
    bTime = exp(l)
    bName = 'birth'
    b = (bTime, bName)
    s = [b]
    mTime = exp(sampleRate)
    mName = 'monitor'
    m = (mTime,mName)
    s = addToList(m,s)
    return s

def birth(sched, stat, time, q,numRejected, itq,itqn):
    birthTime = exp(l) + time
    name = 'birth'
    sched = addToList((birthTime,name),sched)
    if stat == 'idle':
        deathTime = exp(mu) + time
        name = 'death'
        sched = addToList((deathTime,name),sched)
        stat = 'busy'
        itq = itq + deathTime - time # just gets service time
        itqn = itqn + 1
    elif (stat == 'busy' and len(q) < 3):
        q.append(time)
    elif (len(q) >= 3):
        numRejected = numRejected +1
    return (sched,stat,numRejected, itq,itqn)

def death(sched,stat,time, q, tQ, tQNum):
    if stat == 'busy':
        if len(q) == 0:
            stat = 'idle'
        if len(q) > 0:
            t = q.pop(0)
            # for M/M/1/K
            #deathTime = exp(mu) + time
            # for M/D/1/K
            deathTime = ts + time
            tQ = tQ + deathTime - t
            tQNum = tQNum + 1
            name = 'death'
            sched = addToList((deathTime,name),sched)
    elif stat == 'idle':
        print("why am I idle?????")
    return (sched,stat,tQ, tQNum)
   
def monitor(sched, stat ,time, q, num):
    if (time > simTime):
        num = num +1
    mTime = exp(sampleRate) + time
    mName = 'monitor'
    m = (mTime,mName)
    sched = addToList(m,sched)
    realQ = 0
    if stat == 'busy':
        realQ = len(q) + 1
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
    
