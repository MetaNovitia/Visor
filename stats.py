from random import randint
from choose import prep,processFrame,getIndex,getIndexAvg,clearData,processFrame9,test
import os

frames = {}
statsAve = [0,0,0]

def save(filename,string):
    t = ''
    try:
        f=open(filename,'r')
        t = f.read()
        f.close()
    except FileNotFoundError: print("No file: "+filename)

    f = open(filename,'w')
    f.write(t+'\n'+string)
    f.close()
    

def seedStat(filename,obj):
    
    try:
        f = open(filename,'r')
        framelist = []

        for line in f:
            frameNumber = line.split(" ")[1][5:]
            roomName = line.strip().split(" -> ")[1]
            framelist.append((int(frameNumber),roomName))
    
        f.close()

        for i in range(len(framelist)-1):
            frame = framelist[i]
            nextFrame = framelist[i+1]
            if frame[1] not in obj: obj[frame[1]] = []
            obj[frame[1]].append((frame[0],nextFrame[0]-1))
        

    except FileNotFoundError: print("File not found: "+filename)

def checkRoom(roomName, resDir, frameDir,
                 rangeNumber, pad, maxIndex,
                 indexFunc,divH,divW,accept,numberOfFrames,im,myframe=None):

    
    room = frames[roomName]
    tms = 1
    if im==0:
        randomFrame = room[0][0]
    elif im==1:
        randomFrame = myframe
    else:
        r = randint(0,len(room)-1)
        randomFrame = randint(room[r][0],room[r][1])
        tms = 5

    for _ in range(tms):
    
        accepted = processFrame(randomFrame, resDir, frameDir,
                 rangeNumber, pad, maxIndex,
                 indexFunc,divH,divW,accept,False)
    
        positive = 0
        tp = 0
        fn = 0
        for frange in room:
            positive += frange[1]-frange[0]+1
            for i in range(frange[0],frange[1]+1):
                if str(i) in accepted: tp+=1
                else: fn+=1

        fp = len(accepted.keys()) - tp
        
        negative = numberOfFrames - positive

        save(resDir+"statRes.txt",
         "Room "+roomName+" Frame "+str(randomFrame)+"\n"+
         "False Positive: "+str(fp)+"/"+str(negative)+
         " ("+str(fp/negative*100)[:4]+"%)\n" +
         "False Negative: "+str(fn)+"/"+str(positive)+
         " ("+str(fn/positive*100)[:4]+"%)\n")

        statsAve[0]+=fp/negative*100
        statsAve[1]+=fn/positive*100
        statsAve[2]+=1

        r = randint(0,len(room)-1)
        randomFrame = randint(room[r][0],room[r][1])
        
    
# div = 0:1x1, 1:10x10
# algo = 0:freq, 1:avg
# im = 0:first, 1:pref, 2:randAvg
def main(div,algo,im):
    

    frameNums = [54,276,293,269,478,790,850,1529]
    indexFunctions = [[(getIndex,910,"result4-2fixed.txt"),
                       (getIndexAvg,256,"result4.txt")],
                      [(getIndex,910,"result4-2divfixed.txt"),
                       (getIndexAvg,256,"result4div.txt")],
                      [(getIndex,910,"result-freq-5x8.txt"),
                       (getIndexAvg,256,"result-avg-5x8.txt")],
                      [(None),
                       (getIndexAvg,256,"result-avg-4x4.txt")],
                      [(None),
                       (getIndexAvg,256,"result-avg-2x2.txt")],
                      [(None),
                       (getIndexAvg,256,"result-avg-5x5.txt")]][div]
    indexFunc,maxIndex,resultFile = indexFunctions[algo]
    divs = [(1,1,0),(10,10,0.9),(5,8,0.9),(4,4,0.9),(2,2,1),(5,5,1)]
    divH,divW,accept = divs[div]
    (numberOfFrames, frameDir,
    rangeFile, rangeNumber) = (3747, "T4/","range.txt", 100)
    resDir = [[
              ["stat/freq-1x1-first/","stat/freq-10x10-first/","stat/freq-5x8-first/",
               "stat/freq-4x4-first/","stat/freq-2x2-first/","stat/freq-5x5-first/"],
              ["stat/freq-1x1-pref/","stat/freq-10x10-pref/","stat/freq-5x8-pref/",
               "stat/freq-4x4-pref/","stat/freq-2x2-pref/","stat/freq-5x5-pref/"],
              ["stat/freq-1x1-rand/","stat/freq-10x10-rand/","stat/freq-5x8-rand/",
               "stat/freq-4x4-rand/","stat/freq-2x2-rand/","stat/freq-5x5-rand/"]
              ],[
              ["stat/avg-1x1-first/","stat/avg-10x10-first/","stat/avg-5x8-first/",
               "stat/avg-4x4-first/","stat/avg-2x2-first/","stat/avg-5x5-first/"],
              ["stat/avg-1x1-pref/","stat/avg-10x10-pref/","stat/avg-5x8-pref/",
               "stat/avg-4x4-pref/","stat/avg-2x2-pref/","stat/avg-5x5-pref/"],
              ["stat/avg-1x1-rand/","stat/avg-10x10-rand/","stat/avg-5x8-rand/",
               "stat/avg-4x4-rand/","stat/avg-2x2-rand/","stat/avg-5x5-rand/"]
              ]][algo][im][div]
    pad = len(str(numberOfFrames))

    prep(numberOfFrames, resultFile, frameDir, rangeFile, rangeNumber)
    test()
    
    try: os.mkdir(resDir)
    except: print("mkdir failed: "+resDir)

    for acc in range(7,10):

        accept = acc/10

        for rng in range(0,20,5):
            rangeNumber = rng
            statsAve[0]=statsAve[1]=statsAve[2]=0
            save(resDir+"statRes.txt","RANGE NUMBER: "+str(rng)+"\n")
            ct = 0
            for roomName in frames:
    
                checkRoom(roomName, resDir, frameDir,
		     rangeNumber, pad, maxIndex,
		     indexFunc,divH,divW,accept,numberOfFrames,im,frameNums[ct])
                ct+=1

            if statsAve[2]==0: statsAve[2]= 1
            print("Average: FP "+str(statsAve[0]/statsAve[2])+" FN "+str(statsAve[1]/statsAve[2]))
            save(resDir+"statResSumm.txt","acc:"+str(acc)+" range:"+str(rng)+": FP "+str(statsAve[0]/statsAve[2])+" FN "+str(statsAve[1]/statsAve[2])+"\n-----------------------------------------\n")



filename = "associated2.txt"
seedStat(filename,frames)
algo = 1
div = 1

#(numberOfFrames, frameDir, rangeFile, rangeNumber) = (3747, "T4/","range.txt", 100)
#resultFile = ["result4.txt","result4div.txt","result-freq-5x8.txt","result-freq-4x4.txt","result-freq-2x2.txt","result-freq-5x5.txt"][div]
#prep(numberOfFrames, resultFile, frameDir, rangeFile, rangeNumber)
# div = 0:1x1, 1:10x10, 2:5x8, 3:4x4, 4:2x2, 5:5x5
# algo = 0:freq, 1:avg
# im = 0:first, 1:pref, 2:randAvg
#for div in range(2,6):
#for i in range(3):
main(div,algo,1)
