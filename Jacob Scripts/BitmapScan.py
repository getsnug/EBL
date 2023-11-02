import PyPhenom as ppi
import math
agg = ppi.Patterning.AggregateScanPattern()

pat = ppi.Patterning.RectangleScanPattern()
pat.center = ppi.Position(-0.35, -0.25)
pat.size = ppi.SizeD(0.15, 0.15)
pat.pitchX = 1e-3
pat.pitchY = 1e-3
pat.rotation = math.radians(45)
pat.dwellTime = 100e-9
pat.lineScanStyle = ppi.Patterning.LineScanStyle.Serpentine
agg.Add(pat)

pat = ppi.Patterning.BitmapScanPattern()
pat.SetImage(ppi.Load('arne.png'))
pat.maskColor = ppi.Bgra32(255, 255, 255, 255)
pat.center = ppi.Position(+0.0, +0.0)
pat.size = ppi.SizeD(0.2, 0.2)
pat.rotation = math.radians(0)
pat.intensity = ppi.Patterning.IntensityMapping.MinimumWhite
pat.dwellTimeRange = ppi.Range(0, 200e-6)
pat.lineScanStyle = ppi.Patterning.LineScanStyle.Serpentine
agg.Add(pat)

scan = agg.Render()
# You can also render a pattern directly; an "aggegrate" lets you
# add several scan patterns to one "meta-scanpattern" so you can add
# different images/rectanges/lines/points to one set.

# phenom = ppi.Phenom('10.113.145.161','username','password')
phenom = ppi.Phenom('Simulator','','')
phenom.SetSemScanDefinition(scan)

vm = phenom.GetSemViewingMode()
vm.scanMode = ppi.ScanMode.Pattern
phenom.SetSemViewingMode(vm)

input("Press Enter to end patterning...")
# NB: the Phenom will keep repeating the (meta)pattern until
# you set the viewing mode to normal imaging again.
# If you are dealing with sensitive samples, maybe you want to
# pattern for a fixed amount of time and then blank the beam.

vm.scanMode = ppi.ScanMode.Imaging
phenom.SetSemViewingMode(vm)
