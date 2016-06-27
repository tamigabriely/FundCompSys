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

'''
def main():
    n = 100
    stdDev = 0
    qN = 0
    tqN = 0
    qL = []
    tqL = []
    qVar = 0
    tqVar = 0
    ro = 0

    for i in range(0,n):
        (q0,tq0,ro0) = control()
        qL.append(q0)
        qN = qN + q0
        tqL.append(tq0)
        tqN = tqN + tq0
        ro = ro + ro0
    qAvg = qN/n
    tqAvg = tqN/n
    for item in qL:
        qVar = qVar + math.pow((item - qAvg),2)
    for item in tqL:
        tqVar = tqVar + math.pow((item - tqAvg),2)
    qS = math.sqrt(qVar)
    tqS = math.sqrt(tqVar)

    ro = ro/n

    print("q:")
    print(qAvg)
    print("Tq:")
    print(tqAvg)

    print("std dev q:")
    print(qS)
    print("std dev tq:")
    print(tqS)

    print("ro:")
    print(ro)
'''


def control():
    state = ('idle',0)
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
        #print(q)
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

    print("slowdown IO:")
    print(slIO)
    print("slowdown CPU:")
    print(slCPU)
    
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
    
    if stat[0] == 'idle':
        deathTime = exp(muIO) + time
        name = 'deathIO'
        sched = addToList((deathTime,name),sched)
        stat = ('busy', deathTime)
        itq = itq + deathTime - time # just gets service time
        itqn = itqn + 1
        ts = ts + deathTime - time
        tsn = tsn + 1
    elif (stat[0] == 'busy'):
        # SRTN
        timeTillDeathC = stat[1] - time
        timeTillDeathN = exp(muIO) 
        
        if (timeTillDeathN < timeTillDeathC):
            deathTime = timeTillDeathN + time
            name = 'deathIO'
            sched = addToList((deathTime,name),sched)
            stat = (stat[0], deathTime)
            j = ''
            try:
                sched.remove((stat[1]),'deathIO')
                j = 'IO'
            except:
                pass
            try:
                sched.remove((stat[1]),'deathCPU')
                j = 'CPU'
            except:
                pass

            q.append((deathTime,j,timeTillDeathC))
        else:
            q.append((time, 'IO', timeTillDeathN))
    return (sched,stat, itq,itqn,ts,tsn)

def deathIO(sched,stat,time, q, tQIO, tQNumIO,tQCPU, tQNumCPU,tsIO,tsnIO,tsCPU,tsnCPU):
    if stat[0] == 'busy':
        if len(q) == 0:
            stat = ('idle', 0)
        if len(q) > 0:
            (t,kind, remainingTime) = qpop(q)

            if kind == 'IO':
                deathTime = remainingTime + time
                tQIO = tQIO + deathTime - t
                tQNumIO = tQNumIO + 1
                tsIO = tsIO + deathTime - time
                tsnIO = tsnIO + 1
            else: #if kind == 'CPU'
                deathTime = remainingTime + time
                tQCPU = tQCPU + deathTime - t
                tQNumCPU = tQNumCPU + 1
                tsCPU = tsCPU + deathTime - time
                tsnCPU = tsnCPU + 1

            name = 'death' + kind
            sched = addToList((deathTime,name),sched)
    elif stat[0] == 'idle':
        print("why am I idle?????")
    return (sched,stat,tQIO, tQNumIO,tQCPU, tQNumCPU,tsIO,tsnIO,tsCPU,tsnCPU)

def birthCPU(sched, stat, time, q, itq,itqn, ts, tsn):
    
    birthTime = exp(lCPU) + time
    name = 'birthCPU'
    sched = addToList((birthTime,name),sched)
    
    if stat[0] == 'idle':
        deathTime = exp(muCPU) + time
        name = 'deathCPU'
        sched = addToList((deathTime,name),sched)
        stat = ('busy', deathTime)
        itq = itq + deathTime - time # just gets service time
        itqn = itqn + 1
        ts = ts + deathTime - time
        tsn = tsn + 1
    elif (stat[0] == 'busy'):
        # SRTN
        timeTillDeathC = stat[1] - time
        timeTillDeathN = exp(muIO) 
        
        if (timeTillDeathN < timeTillDeathC):
            deathTime = timeTillDeathN + time
            name = 'deathCPU'
            sched = addToList((deathTime,name),sched)
            stat = (stat[0], deathTime)
            j = ''
            try:
                sched.remove((stat[1]),'deathIO')
                j = 'IO'
            except:
                pass
            try:
                sched.remove((stat[1]),'deathCPU')
                j = 'CPU'
            except:
                pass

            q.append((deathTime,j,timeTillDeathC))
        else:
            q.append((time, 'CPU', timeTillDeathN))
    return (sched,stat, itq,itqn, ts, tsn)

def deathCPU(sched,stat,time, q, tQIO, tQNumIO,tQCPU, tQNumCPU,tsIO,tsnIO,tsCPU,tsnCPU):
    if stat[0] == 'busy':
        if len(q) == 0:
            stat = ('idle',0)
        if len(q) > 0:
            (t,kind, remainingTime) = qpop(q)

            if kind == 'IO':
                deathTime = remainingTime + time
                tQIO = tQIO + deathTime - t
                tQNumIO = tQNumIO + 1
                tsIO = tsIO + deathTime - time
                tsnIO = tsnIO + 1
            else: #if kind == 'CPU'
                deathTime = remainingTime + time
                tQCPU = tQCPU + deathTime - t
                tQNumCPU = tQNumCPU + 1
                tsCPU = tsCPU + deathTime - time
                tsnCPU = tsnCPU + 1
            
            name = 'death' + kind
            sched = addToList((deathTime,name),sched)
    elif stat[0] == 'idle':
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
    if stat[0] == 'busy':
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
    '''
    job = q.pop(0)
    t = job[0]
    kind = job[1]
    remainingTime = job[2]
    return(t,kind,remainingTime)
    '''
    # SRTN
    timeRemaining = 210
    popIndex = -1
    for i in range(0,len(q)):
        if q[0][2] < timeRemaining:
            timeRemaining = q[0][2]
            popIndex = i
    job = q.pop(popIndex)
    t = job[0]
    kind = job[1]
    remainingTime = job[2]
    return(t,kind,remainingTime)


    # RR - 100 ms quantum

    # HSN - timeout of 100 ms
