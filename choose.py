import png, array
import os

# modify: frameFile
d = {} # index : frames
chosenRange = {}

def clearData():
    d.clear()
    chosenRange.clear()
    print("Cleared")

# seed the dictionary
# returns number of values and number of keys
def seed(seedFile,obj):
    
    ct = 0
    ct2 = 0
    try:
        f = open(seedFile,'r')

        for line in f:
            if line.strip() != "":
                b = line.strip().split(",")
                obj[b[0]] = []
                ct2+=1
                for val in b[1:]:
                    obj[b[0]].append(val)
                    ct+=1
    
        f.close()
    except FileNotFoundError:
        print("no file")
        pass
    return (ct,ct2)


# helper for seedRange
def setRange(keys,n):

    s = ""
    for key in keys:
        s += str(key) + " "
    chosenRange[str(n)].append(s[:-1])

# helper for choosing
def seedRange(n,lower_bound,d=3):
    
    if n<lower_bound: return

    seedRange(n-1,lower_bound)
    
    chosenRange[str(n)] = []
    keys = [0 for _ in range(d)]
    keys[d-1] = n
    
    setRange(keys,n)
    
    while keys[0]!=n:
        while (keys[0]+keys[1])!=n:
            keys[1]+=1
            keys[2]-=1
            setRange(keys,n)
        keys[0]+=1
        keys[1]=0
        keys[2]=n-keys[0]
        setRange(keys,n)


# get all possible combinations of positive and negative range
def expandRange(num):
    num = num.split(" ")
    result = ["" for _ in range(8)]
    pn = [1,-1]
    for i in range(8):
        for j in range(3):
            result[i]+=str(int(num[j])*pn[(i>>j) & 1])+" "
        result[i] = result[i].strip()
    return result

    
# get index value of frameFile in frameDir
def getIndex(frameDir,frameFile,divH=1,divW=1):

    reader = png.Reader(filename=frameDir+frameFile)
    w, h, pixels, metadata = reader.read_flat()

    ss = []
    
    px = len(pixels)
    
    dh = h//divH
    dw = w//divW
    area = dh*dw
    divisor = (area/10)+1

    for row in range(divH):
        iy = row*dh*w*3
        for col in range(divW):
            # calculate average
            val = [[0,0,0],[0,0,0],[0,0,0]]

            ix = col*dw*3
            for i in range(dh):
                iy2 = i*w*3
                for j in range(dw):
                    ix2 = j*3
                    for k in range(3):
                        if pixels[iy+iy2+ix+ix2+k]>191:
                            val[k][0] += 1
                        elif pixels[iy+iy2+ix+ix2+k]>127:
                            val[k][1] += 1
                        elif pixels[iy+iy2+ix+ix2+k]>63:
                            val[k][2] += 1

            ave=["","",""]
            for i in range(3):
                for j in range(3):
                    val[i][j] = str(int(val[i][j]//divisor))
                ave[i] = "".join(val[i])
                    
            s = ave[0]+ave[1]+ave[2]
            #print(frameFile+" #"+str(row)+"-"+str(col)+": "+s)
            ss.append(s)

    return ss

# get index value of frameFile in frameDir using avg RGB
def getIndexAvg(frameDir,frameFile,divH=1,divW=1):

    reader = png.Reader(filename=frameDir+frameFile)
    w, h, pixels, metadata = reader.read_flat()

    ss = []

    # divH: num of rows
    # divW: num of cols
    # i: row index within div
    # j: col index within div
    # dh: height of a div
    # dw: width of a div, not including 3
    # iy: volume of block rows passed
    # iy2: volume of div rows passed
    # ix: pixels of col block in a single row passed
    # ix2: pixels of col passed

    px = len(pixels)
    
    dh = h//divH
    dw = w//divW
    area = dh*dw
    
    for row in range(divH):
        iy = row*dh*w*3
        for col in range(divW):
            # calculate average
            val = [0,0,0]
            ix = col*dw*3
            for i in range(dh):
                iy2 = i*w*3
                for j in range(dw):
                    ix2 = j*3
                    for k in range(3):
                        val[k]+=pixels[iy+iy2+ix+ix2+k]
            ave = [str(int(val[0]/(area))),
                   str(int(val[1]/(area))),
                   str(int(val[2]/(area)))]

            # pad with 0
            for i in range(3):
                while len(ave[i])<3:
                    ave[i] = '0'+ave[i]
                    
            s = ave[0]+ave[1]+ave[2]
            #print(frameFile+" #"+str(row)+"-"+str(col)+": "+s)
            ss.append(s)

    return ss



# saves obj into saveFile
# format:
# key_1,value_1_1,value_1_2,...,value_1_n
# key_2,value_2_1,value_2_2,...,value_2_m
def save(saveFile,obj):

    f = open(saveFile,'w')
    
    for key in obj:
        f.write(key)
        for value in obj[key]:
            f.write(","+str(value))
        f.write('\n')
    
    f.close()

"""
# process the frames, saving periodically
def process(frameDir,resultFile,numberOfFrames,indexFunc):

    period = 100

    frame = 0
    while frame<numberOfFrames:

        print("---------- SEEDING ----------")
        frame = seed(resultFile,d)[0]

        ct = 0
        while ct<period and frame<numberOfFrames:
            frameFile = 'frame'+str(frame)+'.png'
            index = indexFunc(frameDir,frameFile)
            if index not in d: d[index] = []
            d[index].append(str(frame))
            ct+=1
            frame+=1

        save(resultFile,d)
        print("---------- SAVED "+str(frame)+" FRAMES ----------")"""

# process the frames, saving periodically
def process(frameDir,resultFile,numberOfFrames,indexFunc,divH=1,divW=1):

    period = 100
    area = divH*divW

    frame = 0
    while frame<numberOfFrames:

        print("---------- SEEDING ----------")
        frame = seed(resultFile,d)[0]//area

        ct = 0
        while ct<period and frame<numberOfFrames:
            frameFile = 'frame'+str(frame)+'.png'
            print(frameFile)

            index = indexFunc(frameDir,frameFile,divH,divW)
            
            for i in range(divH*divW):
                if index[i] not in d: d[index[i]] = []
                d[index[i]].append(str(frame))
            ct+=1
            frame+=1

        save(resultFile,d)
        print("---------- SAVED "+str(frame)+" FRAMES ----------")


# prep all data
def prep(numberOfFrames, resultFile, frameDir, rangeFile, rangeNumber):
    clearData()
    frame = seed(resultFile,d)[0]
    print("Seeded "+str(frame)+"/"+ str(numberOfFrames) +" frame indexes")
    
    crange = seed(rangeFile,chosenRange)[1]
    print("Seeded "+str(crange)+" index displacements (including 0)")

    if(crange<rangeNumber+1):
        seedRange(rangeNumber,crange)
        print("Loaded "+str(rangeNumber+1-crange)+" more index displacements")
        save(rangeFile,chosenRange)
    print("Range: "+str(rangeNumber))


def end(rangeFile, resultFile):
    save(rangeFile,chosenRange)
    save(resultFile,d)

# copy frames from stream to classifier folders
def getframes(frameRange, frameDir, outDir, pad, padRange):
    
    try: os.mkdir(outDir+"byFrame/")
    except: pass

    try: os.mkdir(outDir+"byIndex/")
    except: pass

    #for index in frameRange:
    for frame in frameRange:
        reader = png.Reader(filename=frameDir+'frame'+str(frame)+'.png')
        w, h, pixels, metadata = reader.read_flat()

        paddedFrame = str(frame)
        while len(paddedFrame)<pad:
            paddedFrame = '0'+paddedFrame
    
        output = open(outDir+'byFrame/frame'+paddedFrame+'.png', 'wb')
        writer = png.Writer(w, h, **metadata)
        writer.write_array(output, pixels)
        output.close()
        
        paddedRange = str(frameRange[frame][0])
        while len(paddedRange)<padRange:
            paddedRange = '0'+paddedRange
            
        output = open(outDir+'byIndex/['+paddedRange+']frame'+paddedFrame+'.png', 'wb')
        writer = png.Writer(w, h, **metadata)
        writer.write_array(output, pixels)
        output.close() 

def processFrame(frame, resDir, frameDir, rangeNumber, pad,
                 maxIndex, indexFunc, divH, divW, accept,copy):
    try: os.mkdir(resDir+str(frame))
    except: pass
                    
    frameFile = 'frame'+str(frame)+'.png'
    indexes = indexFunc(frameDir,frameFile,divH,divW)
    area = divH*divW
    good = {}
    accepted = {}
    acceptBound = accept*rangeNumber*area
    print(frameFile)
    
    for indexIndex in range(len(indexes)):
        print(indexIndex)
        index = indexes[indexIndex]
        indexL = [int(index[:3]), int(index[3:6]), int(index[6:])]

        #frameRange = {}

        for n in range(rangeNumber+1):
            for rnge in chosenRange[str(n)]:
                for r in expandRange(rnge):
                    r = [int(x) for x in r.split(" ")]
                    s = ""
                    for i in range(3):
                        newV = indexL[i]+r[i]
                        if newV>0 and newV<maxIndex:
                            newV=str(newV)
                            while(len(newV)<3): newV = '0'+newV
                            s+=newV
                    if len(s)==9 and s in d:
                        #frameRange[s] = [n]
                        for frameI in d[s]:
                            if frameI not in accepted:
                                if frameI not in good: good[frameI] = 0
                                good[frameI] += rangeNumber - n + 1
                                if good[frameI] > acceptBound:
                                    accepted[frameI] = [good[frameI]]
                            else: accepted[frameI][0] += rangeNumber - n + 1
        #if area>1:save(resDir+str(frame)+"/newrange"+str(indexIndex)+"-"+index+".txt",frameRange))
    print(len(accepted.keys()))
    save(resDir+str(frame)+"/newrange.txt",accepted)
    if copy: getframes(accepted, frameDir,
              resDir+str(frame)+"/", pad,
              len(str(area*rangeNumber + 1)))
    return accepted

def processFrame(frame, resDir, frameDir, rangeNumber, pad,
                 maxIndex, indexFunc, divH, divW, accept,copy):
    try: os.mkdir(resDir+str(frame))
    except: pass

    frameFile = 'frame'+str(frame)+'.png'
    indexes = indexFunc(frameDir,frameFile,divH,divW)
    area = divH*divW
    good = {}
    accepted = {}
    acceptBound = accept*rangeNumber*area
    print(frameFile)

    for indexIndex in range(len(indexes)):
        print(indexIndex)
        index = indexes[indexIndex]
        indexL = [int(index[:3]), int(index[3:6]), int(index[6:])]

        #frameRange = {}

        for n in range(rangeNumber+1):
            for rnge in chosenRange[str(n)]:
                for r in expandRange(rnge):
                    r = [int(x) for x in r.split(" ")]
                    s = ""
                    for i in range(3):
                        newV = indexL[i]+r[i]
                        if newV>0 and newV<maxIndex:
                            newV=str(newV)
                            while(len(newV)<3): newV = '0'+newV
                            s+=newV
                    if len(s)==9 and s in d:
                        #frameRange[s] = [n]
                        for frameStart in d[s]:
                            # start frame
                            frameI = frameStart
                            if frameI not in accepted:
                                if frameI not in good: good[frameI] = 0
                                good[frameI] += (rangeNumber - n + 1)
                                if good[frameI] > acceptBound:
                                    accepted[frameI] = [good[frameI]]
                            else: accepted[frameI][0] += (rangeNumber - n + 1)                        
                            # +/- 3 frames
                            for divisor in range(2,5):
                                # +
                                frameI = str(int(frameStart)+(divisor-1))
                                if frameI not in accepted:
                                    if frameI not in good: good[frameI] = 0
                                    good[frameI] += (rangeNumber - n + 1)//divisor
                                    if good[frameI] > acceptBound:
                                        accepted[frameI] = [good[frameI]]
                                else: accepted[frameI][0] += (rangeNumber - n + 1)//divisor
                                
                                # -
                                frameI = str(int(frameStart)-(divisor-1))
                                if frameI not in accepted:
                                    if frameI not in good: good[frameI] = 0
                                    good[frameI] += (rangeNumber - n + 1)//divisor
                                    if good[frameI] > acceptBound:
                                        accepted[frameI] = [good[frameI]]
                                else: accepted[frameI][0] += (rangeNumber - n + 1)//divisor                                

    save(resDir+str(frame)+"/newrange.txt",accepted)
    if copy: getframes(accepted, frameDir,
                       resDir+str(frame)+"/", pad,
              len(str(area*rangeNumber + 1)))
    return accepted

def processFrame9(frame, resDir, frameDir, rangeNumber, pad,
                 maxIndex, indexFunc, divH, divW, accept,copy):
    try: os.mkdir(resDir+str(frame))
    except: pass
                    
    frameFile = 'frame'+str(frame)+'.png'
    indexes = indexFunc(frameDir,frameFile,divH,divW)
    area = divH*divW
    good = {}
    accepted = {}
    acceptBound = accept*(rangeNumber+1)*area
    print(frameFile)
    
    for indexIndex in range(len(indexes)):
        print(indexIndex)
        index = indexes[indexIndex]
        indexL = [int(x) for x in index]

        for indexNum in d:
            dist = sum([abs(indexL[i]-int(indexNum[i])) for i in range(9)])
            if dist <= rangeNumber:
                for frameI in d[indexNum]:
                    if frameI not in accepted:
                        if frameI not in good: good[frameI] = 0
                        good[frameI] += rangeNumber - dist + 1
                        if good[frameI] > acceptBound:
                            accepted[frameI] = [good[frameI]]
                    else: accepted[frameI][0] += rangeNumber - dist + 1
    print(len(accepted.keys()))
    save(resDir+str(frame)+"/newrange.txt",accepted)
    if copy: getframes(accepted, frameDir,
              resDir+str(frame)+"/", pad,
              len(str(area*rangeNumber + 1)))
    return accepted
    
def getDifference(x,y):

    diff = 0
    for i in range(3):
        df = int(x[i*3:(i+1)*3])-int(y[i*3:(i+1)*3])
        if df<0: df*=-1
        diff+=df

    return diff

def maxRange(givenFrame,frames,frameDir,indexFunc,resultFile):
    print("Frames loaded: "+str(seed(resultFile,d)[0]))
    x = indexFunc(frameDir,"frame"+str(givenFrame)+".png")[0]

    diffs = []
    
    for ind in d:
        for f in d[ind]:
            if int(f) in frames:
                diffs.append(getDifference(x,ind))
                print("Frame "+f+": "+str(diffs[-1]))
                
    return (max(diffs),sum(diffs)/len(diffs))

def test():
    print(len(d.keys()))
    print(len(chosenRange.keys()))

def main(n):
    #1-129 : new = 496, 74.6; old = 195, 147;
    #93
    #142-260
    #281-
    frameDir = "T4/"
    resDir = "T4-100/"  
    rangeFile = "range.txt"
    numberOfFrames = 3747
    rangeNumber = 20
    #frameNums = [26,196,278,325,380,397,405,434,446,513,549,585,629,733,849,932]
    # scene1, scene2, loading, draw, star, pinkheart, heartandstar,
    # scene2pool, menu, scene3, draw2, pinkheart, star, partyroom, emptyroom,
    # browser(look at angles)
    frameNums = ["test1"]
    indexFunctions = [(getIndex,911,"result-freq-5x8.txt"),
                      (getIndexAvg,256,"result4.txt")]
    indexFunc,maxIndex,resultFile = indexFunctions[1]
    divs = [(1,1,0),(10,10,1),(5,8,0.9),(4,4,1.5),(2,2,1),(5,5,1)]
    divH,divW,accept = divs[0]
    pad = len(str(numberOfFrames))
    copy = True

    if(n==1): process(frameDir,resultFile,numberOfFrames,
                      indexFunc,divH,divW)
    elif(n==2):
        print(maxRange(93,[i for i in range(130)],
                       frameDir,indexFunc,resultFile))
    else:
        
        try: os.mkdir(resDir)
        except: pass

        prep(numberOfFrames, resultFile, frameDir,
             rangeFile, rangeNumber)

        for frame in frameNums:
            processFrame(frame, resDir, frameDir,
                         rangeNumber, pad, maxIndex,
                         indexFunc,divH,divW,accept,copy)
    
        end(rangeFile, resultFile)

