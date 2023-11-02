import PyPhenom as ppi
ppi.InstallLicense('MVE085544-10904-L', 'MVE08554410904L', '4JCMC472P911')

# phenom = ppi.Phenom("", "MVE085544-10904-L", "4JCMC472P911")
phenom = ppi.Phenom("Simulator", "", "")

x = 0.0
y = 0.0

'''
Notes:
when acquiring images, they often do something like this:
'''
acqParams = ppi.CamParams()
acqParams.size = ppi.Size(912,912)
# and set other attributes, then acquire:
acqCam = phenom.NavCamAcquireImage(acqParams)
# then save:
ppi.save(acqCam, 'picture.tiff')
'''
Scan parameters [as attributes of an object created through ppi.ScanParams()]:
size - dimensions of image up to 2048x2048, indicated as ppi.Size(width, height)
detector - which detector among All (Backscatter), NorthSouth, EastWest, A, B, C, D, and Sed (secondary) indicated as ppi.DetectorMode.xyz
nFrames - number of frames to average (examples have 16)
hdr - Boolean for "High Dynamic Range mode", True produces a 16bit raw image, False an 8bit image with contrast/brightness applied from the live image
scale - scale of acquisition within the field of view (1/2 means half the field of view? centered at center?)

tiff format preferred (why?)
'''

# NAVIGATION:
phenom.MoveTo(x,y) # absolute coords in meters
phenom.MoveBy(x,y) # relative coords in meters (from current position)

# BEAM:
phenom.SetSemHighTension(-5000) # accelerating voltage between 5k and 15k (negative)
phenom.SetSemSpotSize(3.3) # beam spot intensity, units not specified. From GUI: (2.1,3.3,4.3,5.1) for (low, image, point, map)

# MAGNIFICATION ETC.:
ppi.MagnificationToFieldWidth(5000) # for setting horizontal field width based on magnification
phenom.SemAutoFocus() # find optimal working distance