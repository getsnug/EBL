import PyPhenom as ppi
import math
import time
import csv
from datetime import datetime

runDate = datetime.now()
# import pandas

# IMPORTANT: black is exposed, white is not exposed
offset = (0.075e-3, 3.0e-3) #tells where to start writing in relation to initial set point (typically top of scratch mark) in (x,y) coordinates in meters
increment = 0.15e-3 # meters for space between tests (to the right)
#black_pixel_dwell_time = [30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6, 30.0e-6]
# black_pixel_dwell_time = [12.0e-6, 14.0e-6, 16.0e-6, 18.0e-6, 20.0e-6, 22.0e-6, 24.0e-6, 26.0e-6, 28.0e-6, 30.0e-6]
black_pixel_dwell_time = [100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6, 100.0e-6] #how many seconds to spend on each black pixel
# black_pixel_dwell_time = [100.0e-6, 125.0e-6, 150.0e-6, 175.0e-6, 200.0e-6, 225.0e-6, 250.0e-6, 275.0e-6, 300.0e-6, 325.0e-6, 350.0e-6, 375.0e-6, 400.0e-6, 425.0e-6, 450.0e-6, 475.0e-6, 500.0e-6] #how many seconds to spend on each black pixel

#totaltime = 0.53898
#timeperpixstart = 11.0488
#exposureTimes = [i*totaltime + timeperpixstart for i in range(2)] #just another form of setting the total time for the pattern
timeforoneus = 0.02 #this one is only accounting for black pixels, with one microsecond per pixel, again sometimes only testing a percentage of black pixels

#timeforoneus = 0.648023*(0.8) #tneg0.4
#timeforoneus = 0.646135*(0.8) #tneg0.2
#timeforoneus = 0.647079*(0.8) #t0
#timeforoneus = 0.647079*(0.8) #t0.2
#timeforoneus = 0.648023*(0.8) #t0.4

#timeforoneus = 0.256678*(0.8) #2Dtneg0.4
#timeforoneus = 0.268954*(0.8) #2Dtneg0.2
#timeforoneus = 0.250372*(0.8) #2Dt0
#timeforoneus = 0.251878*(0.8) #2Dt0.2
# timeforoneus = 0.250197*(0.8) #2Dt0.4


#exposureTimes = [timeforoneus*30, timeforoneus*30, timeforoneus*30, timeforoneus*30, timeforoneus*30, timeforoneus*30, timeforoneus*30, timeforoneus*30, timeforoneus*30, timeforoneus*30]
# exposureTimes = [timeforoneus*12, timeforoneus*14, timeforoneus*16, timeforoneus*18, timeforoneus*20, timeforoneus*22, timeforoneus*24, timeforoneus*26, timeforoneus*28, timeforoneus*30]
exposureTimes = [timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100, timeforoneus*100]
# exposureTimes = [timeforoneus*100, timeforoneus*125, timeforoneus*150, timeforoneus*175, timeforoneus*200, timeforoneus*225, timeforoneus*250, timeforoneus*275, timeforoneus*300, timeforoneus*325, timeforoneus*350, timeforoneus*375, timeforoneus*400, timeforoneus*425, timeforoneus*450, timeforoneus*475, timeforoneus*500]
#exposureTimes = [timeforoneus*2, timeforoneus*4, timeforoneus*6, timeforoneus*8, timeforoneus*10, timeforoneus*12, timeforoneus*14, timeforoneus*16, timeforoneus*18, timeforoneus*20, timeforoneus*22, timeforoneus*24, timeforoneus*26, timeforoneus*28, timeforoneus*30, timeforoneus*32, timeforoneus*34, timeforoneus*36, timeforoneus*38, timeforoneus*40]
#^^sets the exposure time, in terms of the one microsecond per pixel total calculated time, so that you dont actually have to calculate the values. Should be associated with black pixel dwell times in microseconds, since time for a pattern with one microsecond per pixel times the true number of microsecond per pixel gives total time for one pattern

filename = 'images/Madeleine holes/2D/NRB/4holesNRB.png' #insert file name, remembering to include names of any folders
logFileName = 'Madeleine holes 7.25' #this is the name of the CSV that the data will save under. to make a new CSV, just input an unused name.
black_pixel_count = 11020.0

logFile = open('logs/' + logFileName + '.csv', 'a', newline='')
logWriter = csv.writer(logFile, delimiter=',')
logWriter.writerow([runDate.strftime('%Y-%m-%d %H:%M:%S')])
logWriter.writerow(['x','y','image_filename','exposure_time','black_pixel_dwell_time'])

phenom = ppi.Phenom('','','') #instrument IP address, license for software, password
# define the pattern
vm = phenom.GetSemViewingMode() #makes instrument tell what mode/makes beam available
pat = ppi.Patterning.BitmapScanPattern() #dont know
pat.SetImage(ppi.Load(filename)) #taking image, make it available for scanning
pat.maskColor = ppi.Bgra32(255, 255, 255, 255) #assiuming its making the color associate with depth
pat.center = ppi.Position(-0.5, -0.5) #tells to start pattern from the top left

# pat.size = ppi.SizeD(0.1, 0.1) # maybe change this if the image is not rectangular, 50 microns. These all set the size of the image, units unclear. the associated true size is commented in each version of this line, associated with 2k magnification
#pat.size = ppi.SizeD(0.2, 0.2) # maybe change this if the image is not rectangular, 50 microns. These all set the size of the image, units unclear. the associated true size is commented in each version of this line, associated with 2k magnification
# pat.size = ppi.SizeD(0.288, 0.288) #72 microns, 2k
#pat.size = ppi.SizeD(0.432, 0.432) #72 microns, 3k
#pat.size = ppi.SizeD(0.168, 0.056) #30 microns, 2k
pat.size = ppi.SizeD(0.464, 0.464) #30 microns, 2k
# pat.size = ppi.SizeD(0.928, 0.928) #30 microns, 2k
# pat.size = ppi.SizeD(0.4, 0.4) #100 microns, 2k

pat.rotation = math.radians(0) #rotation of pattern for scanning, input degrees
pat.intensity = ppi.Patterning.IntensityMapping.MinimumWhite #this is for greyscale
pat.lineScanStyle = ppi.Patterning.LineScanStyle.Serpentine

scan = pat.Render()

phenom.SetSemScanDefinition(scan)

vm.scanMode = ppi.ScanMode.Pattern
phenom.SetSemViewingMode(vm)

phenom.MoveBy(offset[0], offset[1])
for i in range(len(exposureTimes)):
    print('%s -- %f seconds...' % (filename, exposureTimes[i]))
    # set_scanpattern(exposureTimes[i]/float(black_pixel_count))
    logWriter.writerow([offset[0] + increment*i, offset[1], filename, exposureTimes[i], exposureTimes[i]/float(black_pixel_count)])
    if i != 0:
        phenom.MoveBy(increment, 0)
    time.sleep(exposureTimes[i])
    # NB: the Phenom will keep repeating the (meta)pattern until
    # you set the viewing mode to normal imaging again.
    # If you are dealing with sensitive samples, maybe you want to
    # pattern for a fixed amount of time and then blank the beam.
print('done with all test exposures for %s.' % filename)
print('Returning to original position...')
phenom.MoveBy(-(len(exposureTimes) - 1)*increment, 0) # move back the increments
phenom.MoveBy(-offset[0], -offset[1]) # move back the offset
vm.scanMode = ppi.ScanMode.Imaging
phenom.SetSemViewingMode(vm)

print('positions used (relative to starting point):')
for i in range(len(exposureTimes)):
    print('    (%f,%f)' % (i*increment + offset[0], offset[1]))
