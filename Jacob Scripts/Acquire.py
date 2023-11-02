import PyPhenom as ppi
ppi.InstallLicense('MVE085544-10904-L', 'MVE08554410904L', '4JCMC472P911')

# phenom = ppi.Phenom("", "MVE085544-10904-L", "4JCMC472P911")
phenom = ppi.Phenom("Simulator", "", "")

acq = phenom.SemAcquireImage(1920, 1200, 16) #avg over 16 frames
acq.metadata.label = 'PPI Image'
acq = ppi.AddDatabar(acq)
ppi.Save(acq, 'Image.tiff')