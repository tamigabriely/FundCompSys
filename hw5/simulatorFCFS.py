import random
import math

simTime = 100

lIO = 6
exptsIO = 0.01
muIO = 1/exptsIO

lCPU = 3
exptsCPU = 0.3
muCPU = 1/exptsCPU


simulationTime = 2*simTime
sampleRate = lIO*2


def main():
    n = 100
    stdDev = 0
    qN = 0
    tqN0 = 0
    tqN1 = 0
    tsN0 = 0
    tsN1 = 0
    qL = []
    tqL = []
    qVar = 0
    tqVar = 0
    ro = 0

    for i in range(0,n):
        (q0,tq0, tq1, ts0, ts1, ro0) = control()
        qL.append(q0)
        qN = qN + q0
        tqL.append(tq0)
        tqN0 = tqN0 + tq0
        tqN1 = tqN1 + tq1
        tsN0 = tsN0 + ts0
        tsN1 = tsN1 + ts1
        ro = ro + ro0
    qAvg = qN/n
    tqAvg0 = tqN0/n
    tqAvg1 = tqN1/n
    tsAvg0 = tsN0/n
    tsAvg1 = tsN1/n
    '''
    for item in qL:
        qVar = qVar + math.pow((item - qAvg),2)

    for item in tqL:
        tqVar = tqVar + math.pow((item - tqAvg),2)
    qS = math.sqrt(qVar)
    tqS = math.sqrt(tqVar)
    '''
    
    ro = ro/n

    print("q:")
    print(qAvg)
    print("Tq IO:")
    print(tqAvg0)
    print("Tq CPU:")
    print(tqAvg1)
    print("Ts IO:")
    print(tsAvg0)
    print("Ts CPU:")
    print(tsAvg1)
    print("slowdown IO:")
    print(tqAvg0/tsAvg0)
    print("slowdown CPU:")
    print(tqAvg1/tsAvg1)    
    print("ro:")
    print(ro)
'''
    print("std dev q:")
    print(qS)
    print("std dev tq:")
    print(tqS)
'''




def control():
    state = 'idle'
    schedule = initializeSchedule()
    t = 0.0
    numMEvents = 0
    totalQSize = 0
    totalW = 0
    numBirths = 0
    q = []

    tQIO = 0
    tQNumIO = 0
    tQCPU = 0
    tQNumCPU = 0

    idleTQIO = 0
    idleTQNumIO = 0
    idleTQCPU = 0
    idleTQNumCPU = 0

    tSIO = 0
    tSCPU = 0
    tSNumIO = 0
    tSNumCPU = 0

    while (t < simulationTime):
        #print(schedule)
        event = schedule.pop(0)
        t = event[0] # gets the time
        if event[1] == 'birthIO':
            numBirths = numBirths +1
            (schedule,state, idleTQIO,idleTQNumIO,tSIO,tSNumIO) = birthIO(schedule,state,t, q,idleTQIO,idleTQNumIO,tSIO,tSNumIO)
        elif event[1] == 'deathIO':
            (schedule,state,tQIO, tQNumIO,tQCPU, tQNumCPU,tSIO,tSNumIO,tSCPU,tSNumCPU) = deathIO(schedule,state,t, q, tQIO, tQNumIO,tQCPU, tQNumCPU,tSIO,tSNumIO,tSCPU,tSNumCPU)
        elif event[1] == 'birthCPU':
            numBirths = numBirths +1
            (schedule,state, idleTQCPU,idleTQNumCPU,tSCPU,tSNumCPU) = birthCPU(schedule,state,t, q,idleTQCPU,idleTQNumCPU,tSCPU,tSNumCPU)
        elif event[1] == 'deathCPU':
            (schedule,state, tQIO, tQNumIO,tQCPU, tQNumCPU,tSIO,tSNumIO,tSCPU,tSNumCPU) = deathCPU(schedule,state,t, q, tQIO, tQNumIO,tQCPU, tQNumCPU,tSIO,tSNumIO,tSCPU,tSNumCPU)
        elif event[1] == 'monitor':
            (schedule, currentQ, currentW, numMEvents) = monitor(schedule, state,t, q, numMEvents)
            if (t > simTime):
                totalQSize = totalQSize + currentQ
                totalW = totalW + currentW
    avgQ = totalQSize/numMEvents
    avgW = totalW/numMEvents
    ro = avgQ - avgW
    
    tQIO = (tQIO+idleTQIO)/(tQNumIO+idleTQNumIO)
    tQCPU = (tQCPU+idleTQCPU)/(tQNumCPU+idleTQNumCPU)

    tSIO = tSIO/tSNumIO
    tSCPU = tSCPU/tSNumCPU

    # Slowdown:

    slIO = tQIO/tSIO
    slCPU = tQCPU/tSCPU
    '''
    print("slowdown IO:")
    print(slIO)
    print("slowdown CPU:")
    print(slCPU)
    '''
    return (avgQ, tQIO,tQCPU, tSIO, tSCPU, ro)

def initializeSchedule():
    bTime = exp(lIO)
    bName = 'birthIO'
    b = (bTime, bName)
    s = [b]
    
    bTime = exp(lCPU)
    bName = 'birthCPU'
    b = (bTime, bName)
    s = addToList(b,s)

    mTime = exp(sampleRate)
    mName = 'monitor'
    m = (mTime,mName)
    s = addToList(m,s)
    return s

def birthIO(sched, stat, time, q, itq,itqn, ts, tsn):
    birthTime = exp(lIO) + time
    name = 'birthIO'
    sched = addToList((birthTime,name),sched)
    if stat == 'idle':
        deathTime = exp(muIO) + time
        name = 'deathIO'
        sched = addToList((deathTime,name),sched)
        stat = 'busy'
        itq = itq + deathTime - time # just gets service time
        itqn = itqn + 1
        ts = ts + deathTime - time
        tsn = tsn + 1
    elif (stat == 'busy'):
        q.append((time, 'IO'))
    return (sched,stat, itq,itqn,ts,tsn)

def deathIO(sched,stat,time, q, tQIO, tQNumIO,tQCPU, tQNumCPU,tsIO,tsnIO,tsCPU,tsnCPU):
    if stat == 'busy':
        if len(q) == 0:
            stat = 'idle'
        if len(q) > 0:
            job = q.pop(0)
            t = job[0]
            kind = job[1]

            if kind == 'IO':
                deathTime = exp(muIO) + time
                tQIO = tQIO + deathTime - t
                tQNumIO = tQNumIO + 1
                tsIO = tsIO + deathTime - time
                tsnIO = tsnIO + 1
            elif kind == 'CPU':
                deathTime = exp(muCPU) + time
                tQCPU = tQCPU + deathTime - t
                tQNumCPU = tQNumCPU + 1
                tsCPU = tsCPU + deathTime - time
                tsnCPU = tsnCPU + 1

            name = 'death' + kind
            sched = addToList((deathTime,name),sched)
    elif stat == 'idle':
        print("why am I idle?????")
    return (sched,stat,tQIO, tQNumIO,tQCPU, tQNumCPU,tsIO,tsnIO,tsCPU,tsnCPU)

def birthCPU(sched, stat, time, q, itq,itqn, ts, tsn):
    birthTime = exp(lCPU) + time
    name = 'birthCPU'
    sched = addToList((birthTime,name),sched)
    if stat == 'idle':
        deathTime = exp(muCPU) + time
        name = 'deathCPU'
        sched = addToList((deathTime,name),sched)
        stat = 'busy'
        itq = itq + deathTime - time # just gets service time
        itqn = itqn + 1
        ts = ts + deathTime - time
        tsn = tsn + 1
    elif (stat == 'busy'):
        q.append((time, 'CPU'))
    return (sched,stat, itq,itqn, ts, tsn)

def deathCPU(sched,stat,time, q, tQIO, tQNumIO,tQCPU, tQNumCPU,tsIO,tsnIO,tsCPU,tsnCPU):
    if stat == 'busy':
        if len(q) == 0:
            stat = 'idle'
        if len(q) > 0:
            (t,kind) = qpop(q)

            if kind == 'IO':
                deathTime = exp(muIO) + time
                tQIO = tQIO + deathTime - t
                tQNumIO = tQNumIO + 1
                tsIO = tsIO + deathTime - time
                tsnIO = tsnIO + 1
            elif kind == 'CPU':
                deathTime = exp(muCPU) + time
                tQCPU = tQCPU + deathTime - t
                tQNumCPU = tQNumCPU + 1
                tsCPU = tsCPU + deathTime - time
                tsnCPU = tsnCPU + 1
            
            name = 'death' + kind
            sched = addToList((deathTime,name),sched)
    elif stat == 'idle':
        print("why am I idle?????")
    return (sched,stat,tQIO, tQNumIO,tQCPU, tQNumCPU,tsIO,tsnIO,tsCPU,tsnCPU)

   
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
    
def qpop(q):
    # FCFS
    job = q.pop(0)
    t = job[0]
    kind = job[1]
    return(t,kind)

    # SRTN

    # RR - 100 ms quantum

    # HSN - timeout of 100 ms
