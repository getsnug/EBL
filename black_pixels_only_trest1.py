import PyPhenom as ppi
import math
import time
import csv
from datetime import datetime

def read_csv_file(file_path):
    # Open the CSV file
    with open(file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Read the contents of the CSV file
        csv_contents = list(csv_reader)

    return csv_contents

#Convert csv data into matrix
def csv_to_matrix(csv_file):
    matrix = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = [int(item) for item in row]  # Convert each item to an integer
            matrix.append(row)
    return matrix

# Usage

data = read_csv_file("data11.csv")

csv_path = 'data11.csv'
matrix = csv_to_matrix(csv_path)
size = len(matrix)

#IMPORTANT: x-coordinates = matrix[i][0], y-coordinates = matrix[i][1]

#This is the part where we access the x and y positions!

#for i in range(size):
#    print(f"{matrix[i][0],matrix[i][1]}") #This is only for demo purposes

#*****************************SEM CODE STARTS HERE*****************************************

runDate = datetime.now()

# IMPORTANT: black is exposed, white is not exposed
#tells where to start writing in relation to initial set point (typically top of scratch mark) in (x,y) coordinates in meters
offset = (0.0e-3, 1e-3)
#meters for space between tests (to the right)
increment = 0.15e-3 
#black_pixel_dwell_time = [20.0e-6, 30.0e-6, 40.0e-6]
black_pixel_dwell_time=1e-6

phenom = ppi.Phenom('','','') #instrument IP address, license for software, password


#********************************Parameters for SEM******************************

vm = phenom.GetSemViewingMode() #makes instrument tell what mode/makes beam available
pat = ppi.Patterning.BitmapScanPattern() #dont know
#pat.SetImage(ppi.Load(filename)) #taking image, make it available for scanning ERROR: no filename
#pat.maskColor = ppi.Bgra32(255, 255, 255, 255) #assiuming its making the color associate with depth
#pat.center = ppi.Position(+0.0, +0.0) #tells to start pattern from the center
#pat.size = ppi.SizeD(0.2, 0.2) # maybe change this if the image is not rectangular, 50 microns. These all set the size of the image, units unclear. the associated true size is commented in each version of this line, associated with 2k magnification
pat.size = ppi.SizeD(0.288, 0.288) #72 microns
# pat.size = ppi.SizeD(0.4, 0.4) #100 microns
#pat.rotation = math.radians(0) #rotation of pattern for scanning
#pat.intensity = ppi.Patterning.IntensityMapping.MinimumWhite #this is for greyscale
#pat.dwellTimeRange = ppi.Range(0, 20e-6) #range of dwell times if not defined earlier
#pat.lineScanStyle = ppi.Patterning.LineScanStyle.Serpentine

#scan = pat.Render() #ERROR: no image

#phenom.SetSemScanDefinition(scan)

vm.scanMode = ppi.ScanMode.Pattern
phenom.SetSemViewingMode(vm)

vm = phenom.GetSemViewingMode() 
phenom.MoveBy(0.0e-3, 2e-3)

for i in range(size):
    sm = ppi.SemViewingMode(ppi.ScanMode.Spot,ppi.ScanParams(range(size),range(size),1,ppi.DetectorMode.All,False,0.005,ppi.Position(matrix[i][0],matrix[i][1])))

    phenom.SetSemViewingMode(sm)
    time.sleep(black_pixel_dwell_time)


vm.scanMode = ppi.ScanMode.Imaging
phenom.SetSemViewingMode(vm)

phenom.MoveBy(-0.0e-3, -2e-3)


