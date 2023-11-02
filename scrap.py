import PyPhenom as ppi
import time
import csv
from datetime import datetime

'''
This file will lithograph (yes, that's the verb form) an array of images into a 
prepared sample of PMMA coated on a conductive surface. It also produces two 
files for user-friendliness: a CSV log and a PNG preview.

The CSV log contains all the information provided by the user in the lists 
below. Image name, total exposure time, and magnification, as well as exposure 
per pixel are all contained in the log and can be easily extracted. The preview 
is created by extracting these data from the log.

The preview shows an imitation of the lithograph. The images shown are not to 
scale, but they are in order, and can serve as a sort of "map" for the 
lithograph. Some details about each image are displayed as text in the preview.

For simpler uses, no edits will be needed after magnificationsArray is 
initialized (line 50-60 or so). It would not be too difficult, however, to 
extend the capabilities to more parameters of the microscope, like spot size.
'''


simulator_mode = False
packages_working = False
logFileName = 'ITO_res_test' # name for log and preview files
offset = [0.0e-3, 0.5e-3] # starting position [x,y] relative to scratch mark (meters)
increment = [0.15e-3, 0.25e-3] # array spacing [x,y] (meters)
accel_voltage = 15000 # float from 5k to 15k (Volts)
spotSize = 4.3 # float from 1.0 to 10.0 (Amps/sqrt[Volts])

imagePathsArray = [  # paths for the image files
        ['test_res_1.png']*5,
        ['test_res_2.png']*5,
        ['test_res_3.png']*5,
        ['test_res_4.png']*5
        # ['Patterns/test_res_1.png']*5,
        # ['Patterns/test_res_2.png']*5,
        # ['Patterns/test_res_3.png']*5,
        # ['Patterns/test_res_4.png']*5
    ]
exposureTimesArray = [ # total exposure times in seconds
        [5.80962 * cycle_time for cycle_time in range(1,6)],
        [5.2456 * cycle_time for cycle_time in range(1,6)],
        [5.0755 * cycle_time for cycle_time in range(1,6)],
        [5.3897 * cycle_time for cycle_time in range(1,6)]
        # [6.589562 * cycle_time for cycle_time in range(1,6)],
        # [6.341763411764707 * cycle_time for cycle_time in range(1,6)],
        # [6.275387254901962 * cycle_time for cycle_time in range(1,6)],
        # [6.5823368235294115 * cycle_time for cycle_time in range(1,6)]
    ]
magnificationsArray = [ # magnification controls real size of lithograph (doesn't like to do <2000)
        [2000]*len(imagePathsArray[0]),
        [2000]*len(imagePathsArray[1]),
        [2000]*len(imagePathsArray[2]),
        [2000]*len(imagePathsArray[3])
        # [2000]*len(imagePathsArray[4]),
        # [2000]*len(imagePathsArray[5]),
        # [2000]*len(imagePathsArray[6]),
        # [2000]*len(imagePathsArray[7])
    ]


runDate = datetime.now()
beam_current = spotSize * (accel_voltage ** 0.5)#np.sqrt(accel_voltage) # derived current (Amps)

# check that there are the right number of each parameter
if not (
        [len(x) for x in imagePathsArray] == 
        [len(x) for x in exposureTimesArray] == 
        [len(x) for x in magnificationsArray]
    ):
    print('paths: ', [len(row) for row in imagePathsArray])
    print('times: ', [len(row) for row in exposureTimesArray])
    print('mags: ', [len(row) for row in magnificationsArray])
    raise Exception('Inconsistent shapes of parameter lists.')

# open a log file
logFile = open('logs/' + logFileName + '.csv', 'a', newline='')
print('logFile created')

# set up log writer and write datetime as well as header row
logWriter = csv.writer(logFile, delimiter=',')
logWriter.writerow([runDate.strftime('%Y-%m-%d %H:%M:%S')])
logWriter.writerow(['x (mm)','y (mm)','image_filename','exposure_time (s)','max_dwelltime (s)','magnification'])

# make the parts of the pattern that will stay the same
pat = ppi.Patterning.BitmapScanPattern()
pat.maskColor = ppi.Bgra32(255, 255, 255, 255)
pat.center = ppi.Position(+0.0, +0.0)
pat.size = ppi.SizeD(0.2, 0.2)
pat.rotation = 0
pat.intensity = ppi.Patterning.IntensityMapping.MinimumWhite
pat.lineScanStyle = ppi.Patterning.LineScanStyle.Serpentine


# set up phenom object and unchanging parameters
if simulator_mode:
    phenom = ppi.Phenom('Simulator','','')
else:
    phenom = ppi.Phenom()
phenom.SetSemHighTension(-accel_voltage) # set acceleration voltage
phenom.SetSemSpotSize(spotSize) # set current

# set scanning mode to pattern instead of imaging
vm = phenom.GetSemViewingMode()
vm.scanMode = ppi.ScanMode.Pattern
phenom.SetSemViewingMode(vm)


if packages_working:
    import numpy as np
    from PIL import Image

# maximum dwell time per pixel based on image and total exposure.
# Future: replace total_exposure_time with size and maximum dose/area
def max_dwellTime(image_path, total_exposure_time):
    # Load the binary image
    image = Image.open('images/' + image_path)
    binary_array = np.array(image)

    while len(binary_array.shape) > 2:
        binary_array = np.average(binary_array,axis=2)
    print(image_path)
    print('jacob:', (binary_array.size - np.sum(binary_array)/255.0))
    print(' juan:', np.count_nonzero(binary_array == 0))
    # return the total dwell time based on greyscale values of pixels
    return total_exposure_time / (binary_array.size - np.sum(binary_array)/255.0)

def setScanPattern(imagePath, black_pixel_dwellTime):
    # alter pattern
    pat.SetImage(ppi.Load('images/' + imagePath))
    pat.dwellTimeRange = ppi.Range(0, black_pixel_dwellTime)
    # set SEM scanning pattern
    if not simulator_mode:
        phenom.SetSemScanDefinition(pat.Render())

def sleep(t):
    if not simulator_mode:
        time.sleep(t)

og_pos = phenom.GetStageModeAndPosition().position

# ACTUAL EXPOSURES:
counter = 1
for y in range(len(exposureTimesArray)):
    imagePaths = imagePathsArray[y]
    exposureTimes = exposureTimesArray[y]
    magnifications = magnificationsArray[y]
    for x in range(len(imagePaths)):
        # start scanning with the newest image and dwell times
        if packages_working:
            dwellTime = max_dwellTime(imagePaths[x], exposureTimes[x])
        else:
            dwellTime = 20e-6
        setScanPattern(imagePaths[x], dwellTime)
        phenom.SetHFW(ppi.MagnificationToFieldWidth(magnifications[x], 0.525)) # set magnification
        sleep(1) # wait for things to settle in

        # print info about this exposure
        print('starting exposure %i of %i: %s' % (counter, sum([len(row) for row in exposureTimesArray]), imagePaths[x]))
        print('                            %.2fs total' % (exposureTimes[x]))
        # print('                            %.2f\u03bcs per black pixel' % (dwellTime*1e6))
        # print('                            %.2fC total' % (exposureTimes[x]*beam_current))
        # print('                            %.2fmC per black pixel' % (1e3*dwellTime*beam_current))

        counter += 1

        # move to the exposure site
        phenom.MoveTo(og_pos.x + offset[0] + x*increment[0], og_pos.y + offset[1] + y*increment[1])
        
        # expose site and save position
        sleep(exposureTimes[x])
        pos = phenom.GetStageModeAndPosition().position
        
        # move away from the exposure site
        phenom.MoveBy(increment[0]/2.0, 0)
        
        # write to log file
        logWriter.writerow(['%.3f' % (1e3*(pos.x - og_pos.x)), '%.3f' % (1e3*(pos.y - og_pos.y)), imagePaths[x], exposureTimes[x], pat.dwellTimeRange.end, magnifications[x]])
        # print(['%.3f' % (1e3*(pos.x - og_pos.x)), '%.3f' % (1e3*(pos.y - og_pos.y)), imagePaths[x], exposureTimes[x], pat.dwellTimeRange.end, magnifications[x]])

phenom.MoveTo(og_pos)

vm.scanMode = ppi.ScanMode.Imaging
phenom.SetSemViewingMode(vm)

logFile.close()

if packages_working:
    from preview import make_preview
    make_preview(logFileName)