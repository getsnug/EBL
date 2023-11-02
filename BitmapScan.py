import PyPhenom as ppi
import math
import time
import csv
from datetime import datetime

runDate = datetime.now()
# import pandas
fileNames = ["images/vaughn/","",""]#Fill in filenames, repeat filenames to repeat images
# IMPORTANT: black is exposed, white is not exposed
offset = (0e-4, 5e-4) #tells where to start writing in relation to initial set point (typically top of scratch mark) in (x,y) coordinates in meters
increment = 2.5e-4 # meters for space between tests (to the right)
yincrement = 1.5e-4
#black_pixel_dwell_time = [30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6]
# black_pixel_dwell_time = [20.0e-6, 20.0e-6, 20.0e-6, 20.0e-6, 20.0e-6, 20.0e-6, 20.0e-6, 20.0e-6, 20.0e-6, 20.0e-6]
#black_pixel_dwell_time = [100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6] #how many seconds to spend on each black pixel

#totaltime = 0.53898
#timeperpixstart = 11.0488
#exposureTimes = [i*totaltime + timeperpixstart for i in range(2)] #just another form of setting the total time for the pattern
timeforoneus = 0.01 #this one is only accounting for black pixels, with one microsecond per pixel, again sometimes only testing a percentage of black pixels


#timeforoneus = 2.8934*.4 #calculated time for one full pattern using one microsecond per pixel accounting for every pixel, sometimes multiplied by a decimal if we only want to consider a percentage of the pixels
# exposureTimes = [timeforoneus*10, timeforoneus*10, timeforoneus*10, timeforoneus*10, timeforoneus*10, timeforoneus*10, timeforoneus*10, timeforoneus*10, timeforoneus*10, timeforoneus*10]
#exposureTimes = [timeforoneus*15, timeforoneus*20, timeforoneus*25, timeforoneus*30, timeforoneus*35, timeforoneus*40, timeforoneus*50, timeforoneus*60, timeforoneus*70, timeforoneus*100]
# exposureTimes = [timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100]
#exposureTimes = [10.6923795, 10.6923795, 10.6923795, 10.6923795, 10.6923795, 10.6923795, 10.6923795, 10.6923795, 10.6923795, 10.6923795]
# exposureTimes = [timeforoneus*100]

exposureTimes = []
for i in range(4):
     exposureTimes.append([2+2*i,2+2*i,2+2*i,2+2*i,2+2*i])#Generate exposureTimes, this will do 5 at 2 seconds, 4, 6, 8 and maybe 10 not sure, but they'll all be in the same row

    

#exposureTimes = [timeforoneus*2, timeforoneus*4, timeforoneus*6, timeforoneus*8, timeforoneus*10, timeforoneus*12, timeforoneus*14, timeforoneus*16, timeforoneus*18, timeforoneus*20, timeforoneus*22, timeforoneus*24, timeforoneus*26, timeforoneus*28, timeforoneus*30, timeforoneus*32, timeforoneus*34, timeforoneus*36, timeforoneus*38, timeforoneus*40]
#^^sets the exposure time, in terms of the one microsecond per pixel total calculated time, so that you dont actually have to calculate the values. Should be associated with black pixel dwell times in microseconds, since time for a pattern with one microsecond per pixel times the true number of microsecond per pixel gives total time for one pattern

# exposureTimes = [6.557 + [1, 2, 3, 4, 5, 6] ]
# exposureTimes = [5.80962 * cycle_time for cycle_time in range(1,6)]
        # [5.80962 * cycle_time for cycle_time in range(1,6)],
        # [5.2456 * cycle_time for cycle_time in range(1,6)],
            # [5.0755 * cycle_time for cycle_time in range(1,6)]
#set up log
logFileName = 'Ramsey_10.31' #this is the name of the CSV that the data will save under. to make a new CSV, just input an unused name.
black_pixel_count = 11020.0
logFile = open('logs/' + logFileName + '.csv', 'a', newline='')
# define the pattern and initialize connection
phenom = ppi.Phenom('192.168.200.101','MVE08554410904L','4JCMC472P911') #instrument IP address, license for software, password
vm = phenom.GetSemViewingMode() #makes instrument tell what mode/makes beam available
pat = ppi.Patterning.BitmapScanPattern() #Writes an image. (Instead of a point or rectangle) for more info see ppi-patterning doc from vince
pat.maskColor = ppi.Bgra32(255, 255, 255, 255) #assuming its making the color associate with depth. "any pixel matching this color will be skipped"- ppi-patterning doc from vince
pat.center = ppi.Position(+0.0, +0.0) #tells to start pattern from the center

#move to initial offset
phenom.MoveBy(offset[0], offset[1])
currentPos = offset
for filename in fileNames:
    #filename = 'images/2D wide border (93 microns)/2Dt0.4.png' #insert file name, remembering to include names of any folders
    # black_pixel_dwell_time = [25.0e-6, 30.0e-6, 35.0e-6, 40.0e-6, 45.0e-6,50.0e-6]
    
    logWriter = csv.writer(logFile, delimiter=',')
    logWriter.writerow([runDate.strftime('%Y-%m-%d %H:%M:%S')])
    logWriter.writerow(['x','y','image_filename','exposure_time','black_pixel_dwell_time'])
    # filename = 'vassar_seal_test1.png'

    
    # phenom = ppi.Phenom('Simulator','','')
    
    pat.SetImage(ppi.Load(filename)) #taking image, make it available for scanning
    
    # pat.size = ppi.SizeD(0.1, 0.1) # maybe change this if the image is not rectangular, 50 microns. These all set the size of the image, units unclear. the associated true size is commented in each version of this line, associated with 2k magnification
    pat.size = ppi.SizeD(0.2, 0.2) # maybe change this if the image is not rectangular, 50 microns. These all set the size of the image, units unclear. the associated true size is commented in each version of this line, associated with 2k magnification
    #pat.size = ppi.SizeD(0.288, 0.288) #72 microns, 2k
    #pat.size = ppi.SizeD(0.372, 0.372) #93 microns, 2k
    #pat.size = ppi.SizeD(0.432, 0.432) #72 microns, 3k
    #pat.size = ppi.SizeD(0.168, 0.056) #30 microns, 2k
    # pat.size = ppi.SizeD(0.464, 0.464) #30 microns, 2k
    # pat.size = ppi.SizeD(0.30624, 0.30624) #30 microns, 2k
    # pat.size = ppi.SizeD(0.4, 0.4) #100 microns, 2k

    pat.rotation = math.radians(0) #rotation of pattern for scanning, input degrees
    pat.intensity = ppi.Patterning.IntensityMapping.MinimumWhite #this is for greyscale
    #$pat.dwellTimeRange = ppi.Range(0, 20e-6) #range of dwell times if not defined earlier
    pat.lineScanStyle = ppi.Patterning.LineScanStyle.Serpentine

    scan = pat.Render()

    phenom.SetSemScanDefinition(scan)

    vm.scanMode = ppi.ScanMode.Pattern
    phenom.SetSemViewingMode(vm)
    # def set_scanpattern(black_dwelltime):
    #     black_pixel_dwell_time = black_dwelltime
    #     pat = ppi.Patterning.BitmapScanPattern()
    #     pat.SetImage(ppi.Load(filename))
    #     pat.maskColor = ppi.Bgra32(255, 255, 255, 255)
    #     pat.center = ppi.Position(+0.0, +0.0)
    #     pat.size = ppi.SizeD(0.2, 0.2) # maybe change this if the image is not rectangular
    #     pat.rotation = math.radians(0)
    #     pat.intensity = ppi.Patterning.IntensityMapping.MinimumWhite
    #     pat.dwellTimeRange = ppi.Range(0, black_dwelltime)
    #     pat.lineScanStyle = ppi.Patterning.LineScanStyle.Serpentine

    #     scan = pat.Render()

    #     phenom.SetSemScanDefinition(scan)
        
    #     vm.scanMode = ppi.ScanMode.Pattern
    #     phenom.SetSemViewingMode(vm)

    # offset = (-0.15e-3, 1.375e-3)
    #exposureTimes = [1.0 + float(time)/4.0 for time in range(28)]
    # exposureTimes = [14, 14, 14, 14, 14]

    # exposureTimes = [5.3897 * cycle_time for cycle_time in range(1,6)]

    # increment = -0.15e-3 # meters for space between tests (to the right)

    for i in range(len(exposureTimes)):
        print('%s -- %f seconds...' % (filename, exposureTimes[i]))
        # set_scanpattern(exposureTimes[i]/float(black_pixel_count))
        logWriter.writerow([currentPos[0],currentPos[1], filename, exposureTimes[i], exposureTimes[i]/float(black_pixel_count)])
        if i != 0:
            currentPos[0] = currentPos[0]+increment
            phenom.MoveBy(increment, 0)
        time.sleep(exposureTimes[i])
        # NB: the Phenom will keep repeating the (meta)pattern until
        # you set the viewing mode to normal imaging again.
        # If you are dealing with sensitive samples, maybe you want to
        # pattern for a fixed amount of time and then blank the beam.
    print('done with all test exposures for %s.' % filename)
    print('moving to next row')
    currentPos[0] = currentPos[0]-increment*(len(exposureTimes-1))
    currentPos[1] = currentPos[1]+yincrement
    phenom.MoveBy(-(len(exposureTimes) - 1)*increment, yincrement) # move back the increments
    #phenom.MoveBy(-offset[0], -offset[1]) # move back the offset
    vm.scanMode = ppi.ScanMode.Imaging
    phenom.SetSemViewingMode(vm)

    # print('positions used (relative to starting point):')
    # for i in range(len(exposureTimes)):
    #     print('    (%f,%f)' % (i*increment + offset[0], offset[1]))

