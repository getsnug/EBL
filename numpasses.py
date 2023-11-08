import PyPhenom as ppi
import math
import time
import csv
import cv2
import numpy as np
from datetime import datetime
#tb is some constant that is determined by the time that the SEM spends on each black pixel
tb = 0.0001
runDate = datetime.now()
### HEADER ###
# This is the main file to run for EBL, the relevant parameters in this file are
# directory and offset, I might move offset into the spreadsheet, but for now I think that it
# makes sense here. 
#make sure that your directory has a control csv titled main.csv, and the images you wish to EBL
directory = "images/"
# Set up a log file, right now the log is pretty useless but I'll fix the outputs (11-3-23)
logFileName = 'Ramsey_10.31'
offset = (0e-4, 5e-4) #tells where to start writing in relation to initial set point,
# (typically top of scratch mark) in (x,y) coordinates in meters if you're not sure what you want
# (0e-4, 5e-4) is a pretty good starting value

# function to determine how long the machine should spend tracing a single pattern
def sleepTime(numPasses,filename):
    img = cv2.imread(filename,0)
    return np.sum(img==0)*tb

black_pixel_count = 11020.0
logFile = open('logs/' + logFileName + '.csv', 'a', newline='')
# define the pattern and initialize connection
phenom = ppi.Phenom('192.168.200.101','MVE08554410904L','4JCMC472P911') #instrument IP address, license for software, password
vm = phenom.GetSemViewingMode() #makes instrument tell what mode/makes beam available
pat = ppi.Patterning.BitmapScanPattern() #Writes an image. (Instead of a point or rectangle) for more info see ppi-patterning doc from vince
pat.maskColor = ppi.Bgra32(255, 255, 255, 255) #assuming its making the color associate with depth. "any pixel matching this color will be skipped"- ppi-patterning doc from vince
pat.center = ppi.Position(+0.0, +0.0) #tells to start pattern from the center

#move to initial offset
with open('main.csv', mode ='r')as file:
  
  # reading the CSV file
    control = csv.reader(file,quoting=csv.QUOTE_NONNUMERIC)
    #skip first line
    next(control)
    #move from initial location
    phenom.MoveBy(offset[0], offset[1])
    #set a known position, the first pattern starts at the origin
    currentPos = [0,0]
  # displaying the contents of the CSV file
    for line in control:
        #retrieve the image filename
        filename = directory+line[1][1:len(line[1])-1]
        #retrieve the exposure times 
        numPasses = line[2:12]
        #initialize log
        logWriter = csv.writer(logFile, delimiter=',')
        logWriter.writerow([runDate.strftime('%Y-%m-%d %H:%M:%S')])
        logWriter.writerow([currentPos,filename,numPasses])
            
        pat.SetImage(ppi.Load(filename)) #taking image, make it available for scanning
        
        #set the image size
        pat.size = ppi.SizeD(line[12], line[13])
        #set the pattern spacing
        increment = line[14]
        yincrement = line[15]
        #not super sure where one would rotate the pattern but it might be useful someday
        pat.rotation = math.radians(0) #rotation of pattern for scanning, input degrees
        pat.intensity = ppi.Patterning.IntensityMapping.MinimumWhite #this is for greyscale
        pat.lineScanStyle = ppi.Patterning.LineScanStyle.Serpentine
        #this is where we tell the SEM to trace out the pattern
        scan = pat.Render()
        phenom.SetSemScanDefinition(scan)

        for i in range(len(numPasses)):
            #print current exposure
            print('%s -- %f seconds...' % (filename, numPasses[i]))
            #log current exposure
            logWriter.writerow([currentPos[0],currentPos[1], filename, numPasses[i]])
            if i != 0:
                #update position and move SEM
                vm.scanMode = ppi.ScanMode.Pattern
                #here the tracing begins, if there's a way to pick a number of times to trace, it would be here
                phenom.SetSemViewingMode(vm)
                for j in range(numPasses(i)):
                    phenom.SetSemViewingMode(vm)
                    time.sleep(sleepTime(numPasses,filename))
                vm.scanMode = ppi.ScanMode.Imaging
                phenom.SetSemViewingMode(vm)
                currentPos[0] = currentPos[0]+increment
                phenom.MoveBy(increment, 0)
            #time.sleep(numPasses[i])
            # NB: the Phenom will keep repeating the (meta)pattern until
            # you set the viewing mode to normal imaging again.
            # If you are dealing with sensitive samples, maybe you want to
            # pattern for a fixed amount of time and then blank the beam.
            # still need to figure out how to blank the beam, ideally we will have a parameter
            # for the number of times that 
        print('done with all test exposures for %s.' % filename)
        print('moving to next row')
        #update position
        currentPos[0] = currentPos[0]-increment*(len(numPasses-1))
        currentPos[1] = currentPos[1]+yincrement
        phenom.MoveBy(-(len(numPasses) - 1)*increment, yincrement) # move back the increments and up a row

        # print('positions used (relative to starting point):')
        # for i in range(len(numPasses)):
        #     print('    (%f,%f)' % (i*increment + offset[0], offset[1]))
