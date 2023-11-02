import PyPhenom as ppi
ppi.InstallLicense('MVE085544-10904-L', 'MVE08554410904L', '4JCMC472P911')

# phenom = ppi.Phenom("", "MVE085544-10904-L", "4JCMC472P911")
phenom = ppi.Phenom("Simulator", "", "")

instrument_mode = phenom.GetInstrumentMode()
print('instrument mode: ', type(instrument_mode), instrument_mode)

operational_mode = phenom.GetOperationalMode()
print('operational mode: ', type(operational_mode), operational_mode)