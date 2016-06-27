import random
import math

simTime = 100
l = 65
ts = 0.015
mu = 1/ts
q = 0
simulationTime = 2*simTime
sampleRate = l*2


def main():
    state = 'idle'
    schedule = initializeSchedule()
    t = 0.0
    numMEvents = 0
    totalQSize = 0
    totalW = 0
    tQ = 0
    tW = 0
    numBirths = 0
    while (t < simulationTime):
        #print(schedule)
        event = schedule.pop(0)
        t = event[0] # gets the time
        if event[1] == 'birth':
            numBirths = numBirths +1
            (schedule,state,tQ,tW) = birth(schedule,state,t, tQ,tW)
        elif event[1] == 'death':
            (schedule,state,tQ,tW) = death(schedule,state,t,tQ,tW)
        elif event[1] == 'monitor':
            (schedule, currentQ, currentW, numMEvents) = monitor(schedule, state,t,numMEvents)
            if (t > 100):
                totalQSize = totalQSize + currentQ
                totalW = totalW + currentW
    avgQ = totalQSize/numMEvents
    avgW = totalW/numMEvents
    ro = avgW - avgQ
    tQ = tQ/numBirths
    tW = tW/numBirths
    print("q = " + str(avgQ))
    print("w = " + str(avgW))
    print("ro = " + str(ro))
    print("tQ = " + str(tQ))
    print("tW = " + str(tW))
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

def birth(sched, stat, time, tQ,tW):
    birthTime = exp(l) + time
    name = 'birth'
    sched = addToList((birthTime,name),sched)
    if stat == 'idle':
        deathTime = exp(mu) + time
        name = 'death'
        sched = addToList((deathTime,name),sched)
        stat = 'busy'
    elif stat == 'busy':
        global q
        q = q + 1
        tQ = tQ - time
        tW = tW - time
    return (sched,stat,tQ,tW)

def death(sched,stat,time,tQ,tW):
    if stat == 'busy':
        global q
        if q == 0:
            stat = 'idle'
        if q > 0:
            q = q -1
            deathTime = exp(mu) + time
            tW = tW + deathTime
            tQ = tQ + time
            name = 'death'
            sched = addToList((deathTime,name),sched)
    elif stat == 'idle':
        print("why am I idle?????")
    return (sched,stat,tQ,tW)
   
def monitor(sched, stat ,time,num):
    if (time > 100):
        num = num +1
    mTime = exp(sampleRate) + time
    mName = 'monitor'
    m = (mTime,mName)
    sched = addToList(m,sched)
    w = 0
    if stat == 'busy':
        w = q + 1
    return (sched,q,w,num)

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
    
