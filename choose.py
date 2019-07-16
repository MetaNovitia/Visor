import png, array
import os

# modify: frameFile
d = {} # index : frames
chosenRange = {}

# seed the dictionary
# returns number of values and number of keys
def seed(seedFile,obj):
    
    f = open(seedFile,'r')

    ct = 0
    ct2 = 0
    for line in f:
        if line.strip() != "":
            b = line.strip().split(",")
            obj[b[0]] = []
            ct2+=1
            for val in b[1:]:
                obj[b[0]].append(val)
                ct+=1
    
    f.close()
    return (ct,ct2)


# helper for seedRange
def setRange(x,y,z,n):
    chosenRange[str(n)].append(str(x)+" "+str(y)+" "+str(z))

# helper for choosing
def seedRange(n,lower_bound):
    
    if n<lower_bound: return

    seedRange(n-1,lower_bound)
    
    chosenRange[str(n)] = []
    x=0;y=0;z=n
    
    setRange(x,y,z,n)
    while x!=n:
        while (x+y)!=n:
            y+=1
            z-=1
            setRange(x,y,z,n)
        x+=1
        y=0
        z=n-x
        setRange(x,y,z,n)

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
def getIndex(frameDir,frameFile):

    reader = png.Reader(filename=frameDir+frameFile)
    w, h, pixels, metadata = reader.read_flat()

    # calculate average
    val = [0,0,0]
    for i in range(len(pixels)): val[i%3]+=pixels[i]
    ave = [str(int(val[0]/(len(pixels)/3))),
           str(int(val[1]/(len(pixels)/3))),
           str(int(val[2]/(len(pixels)/3)))]

    # pad with 0
    for i in range(3):
        while len(ave[i])<3:
            ave[i] = '0'+ave[i]
            
    s = ave[0]+ave[1]+ave[2]
    print(frameFile+": "+s)

    return s


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


# process the frames, saving periodically
def process(frameDir,resultFile,numberOfFrames):

    period = 100

    frame = 0
    while frame<numberOfFrames:

        print("---------- SEEDING ----------")
        frame = seed(resultFile)[0]

        ct = 0
        while ct<period and frame<numberOfFrames:
            frameFile = 'frame'+str(frame)+'.png'
            index = getIndex(frameDir,frameFile)
            if index not in d: d[index] = []
            d[index].append(str(frame))
            ct+=1
            frame+=1

        save(resultFile)
        print("---------- SAVED "+str(frame)+" FRAMES ----------")

# prep all data
def prep(numberOfFrames, resultFile, frameDir, rangeFile, rangeNumber, resDir):
    frame = seed(resultFile,d)[0]
    print("Seeded "+str(frame)+"/"+ str(numberOfFrames) +" frame indexes")
    
    crange = seed(rangeFile,chosenRange)[1]
    print("Seeded "+str(crange)+" index displacements (including 0)")

    if(crange<rangeNumber+1):
        seedRange(rangeNumber,crange)
        print("Loaded "+str(rangeNumber+1-crange)+" more index displacements")
    print("Range: "+str(rangeNumber))

    try: os.mkdir(resDir)
    except: pass

def end(rangeFile, resultFile):
    save(rangeFile,chosenRange)
    save(resultFile,d)

# copy frames from stream to classifier folders
def getframes(frameRange, frameDir, outDir, pad, padRange):
    
    try: os.mkdir(outDir+"byFrame/")
    except: pass

    try: os.mkdir(outDir+"byIndex/")
    except: pass

    for index in frameRange:
        for frame in d[index]:
            reader = png.Reader(filename=frameDir+'frame'+str(frame)+'.png')
            w, h, pixels, metadata = reader.read_flat()

            paddedFrame = str(frame)
            while len(paddedFrame)<pad:
                paddedFrame = '0'+paddedFrame
    
            output = open(outDir+'byFrame/frame'+paddedFrame+'.png', 'wb')
            writer = png.Writer(w, h, **metadata)
            writer.write_array(output, pixels)
            output.close()
            
            paddedRange = str(frameRange[index][0])
            while len(paddedRange)<padRange:
                paddedRange = '0'+paddedRange
            
            output = open(outDir+'byIndex/['+paddedRange+']frame'+paddedFrame+'.png', 'wb')
            writer = png.Writer(w, h, **metadata)
            writer.write_array(output, pixels)
            output.close() 

def processFrame(frame, resDir, frameDir, rangeNumber, pad):
    try: os.mkdir(resDir+str(frame))
    except: pass
                    
    frameFile = 'frame'+str(frame)+'.png'
    index = getIndex(frameDir,frameFile)

    indexL = [int(index[:3]), int(index[3:6]), int(index[6:])]

    frameRange = {}

    for n in range(rangeNumber+1):
        for rnge in chosenRange[str(n)]:
            for r in expandRange(rnge):
                r = [int(x) for x in r.split(" ")]
                s = ""
                for i in range(3):
                    newV = indexL[i]+r[i]
                    if newV>0 and newV<256:
                        newV=str(newV)
                        while(len(newV)<3): newV = '0'+newV
                        s+=newV
                if len(s)==9 and s in d:
                    frameRange[s] = [n]
    save(resDir+str(frame)+"/newrange.txt",frameRange)
    getframes(frameRange, frameDir, resDir+str(frame)+"/", pad, len(str(rangeNumber)))

def main():
    frameDir = "T1/"
    resultFile = "result.txt"
    resDir = "T3/"  
    rangeFile = "range.txt"
    numberOfFrames = 7500
    rangeNumber = 10
    frameNums = [1087]
    pad = len(str(numberOfFrames))
    
    prep(numberOfFrames, resultFile, frameDir, rangeFile, rangeNumber, resDir)

    for frame in frameNums:
        processFrame(frame, resDir, frameDir, rangeNumber, pad)
    
    end(rangeFile, resultFile)


main()
