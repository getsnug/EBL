import PyPhenom as ppi
import time
phenom = ppi.Phenom()
phenom.SetHFW(ppi.MagnificationToFieldWidth(2000,0.525)) # set magnification

# phenom.MoveToNavCam()
# # acq = phenom.SemAcquireImage(1920, 1200, 16)
# # acq.metadata.label = 'PPI Image'
# # acq = ppi.AddDatabar(acq)
# # ppi.Save(acq, 'Image.tiff')
# ogHT = phenom.GetSemHighTension()
# ogSpot = phenom.GetSemSpotSize()
# def blank():
#     phenom.SetSemHighTension(-5000)
#     phenom.SetSemSpotSize(0.0)

# def unblank():
#     phenom.SetSemHighTension(ogHT)
#     phenom.SetSemSpotSize(ogSpot)

# phenom.SetHFW(ppi.MagnificationToFieldWidth(2000, 0.5))
# time.sleep(1)
# phenom.SetHFW(ppi.MagnificationToFieldWidth(5000, 0.5))
# time.sleep(1)
# phenom.MoveBy(-0.00001,0)
# time.sleep(1)
# phenom.MoveBy(0,-0.00001)
# time.sleep(1)
# phenom.SetHFW(ppi.MagnificationToFieldWidth(2000, 0.5))

# # blank()
# time.sleep(1)

# # phenom.MoveBy(-0.00001,-0.00001)
# time.sleep(1)
# # unblank()
# # phenom.MoveBy(0.001,0.001)