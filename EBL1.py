import PyPhenom as ppi
import math
import time


def scanPattern(dwellTime, center):
    agg = ppi.Patterning.AggregateScanPattern()

    pat = ppi.Patterning.RectangleScanPattern()
    pat.center = ppi.Position(0e-6, -0e-6)
    pat.size = ppi.SizeD(500e-6, 500e-6)
    pat.pitchX = 10e-6
    pat.pitchY = 10e-6
    pat.rotation = math.radians(0)
    # pat.dwellTime = 100e-6
    pat.dwellTime = dwellTime
    pat.lineScanStyle = ppi.Patterning.LineScanStyle.Serpentine
    agg.Add(pat)
    return agg.Render()
100e-6 * 2500
# # pat = ppi.Patterning.BitmapScanPattern()
# # pat.SetImage(ppi.Load('arne.png'))
# # pat.maskColor = ppi.Bgra32(255, 255, 255, 255)
# # pat.center = ppi.Position(+0.0, +0.0)
# # pat.size = ppi.SizeD(0.2, 0.2)
# # pat.rotation = math.radians(0)
# # pat.intensity = ppi.Patterning.IntensityMapping.MinimumWhite
# # pat.dwellTimeRange = ppi.Range(0, 200e-6)
# # pat.lineScanStyle = ppi.Patterning.LineScanStyle.Serpentine
# # agg.Add(pat)

# scan = agg.Render()
# # You can also render a pattern directly; an "aggegrate" lets you
# # add several scan patterns to one "meta-scanpattern" so you can add
# # different images/rectanges/lines/points to one set.

phenom = ppi.Phenom('192.168.200.101','MVE08554410904L','4JCMC472P911')
phenom.MoveBy(1e-3, 1e-3)
# phenom = ppi.Phenom('Simulator','','')
# phenom.SetSemScanDefinition(scan)
for t in range(5):
    print((t+1)*100e-6)
    phenom.SetSemScanDefinition(scanPattern((t+1) * 100e-6, center=ppi.Position(200e-6 * t, 200e-6 * t)))


    vm = phenom.GetSemViewingMode()
    vm.scanMode = ppi.ScanMode.Pattern
    phenom.SetSemViewingMode(vm)
    time.sleep(1.5*2500*(t+1)*100e-6)

input("Press Enter to end patterning...")
# NB: the Phenom will keep repeating the (meta)pattern until
# you set the viewing mode to normal imaging again.
# If you are dealing with sensitive samples, maybe you want to
# pattern for a fixed amount of time and then blank the beam.

phenom.MoveBy(-1e-3, -1e-3)
vm.scanMode = ppi.ScanMode.Imaging
phenom.SetSemViewingMode(vm)
