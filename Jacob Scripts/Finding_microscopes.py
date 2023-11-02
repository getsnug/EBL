import PyPhenom as ppi
ppi.InstallLicense('MVE085544-10904-L', 'MVE08554410904L', '4JCMC472P911')

phenoms = ppi.FindPhenoms(1)
for phenom in phenoms:
    if phenom.ip == 'MVE085544-10904-L' or phenom.ip == 'MVE08554410904L':
        print('This is the one:')
    else:
        print("here's one that we don't have a license for (or at least, I don't):")
    print('Phenom IP:', phenom.ip)
    print('Phenom ID:', phenom.name)

print('here are the machines we have licenses for:')
for phenom in phenoms:
    if phenom.name in [license.instrumentId for license in ppi.GetLicenses()]:
        print('Phenom IP:', phenom.ip)
        print('Phenom ID:', phenom.name)

print('here are the machines we don\'t have licenses for:')
for phenom in phenoms:
    if phenom.name in [license.instrumentId for license in ppi.GetLicenses()]:
        print('Phenom IP:', phenom.ip)
        print('Phenom ID:', phenom.name)
