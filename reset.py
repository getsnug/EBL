import PyPhenom as ppi
#If the instrument stops mid program and is stuck in scanning mode run this to return to imaging mode

phenom = ppi.Phenom('','','') #instrument IP address, license for software, password
vm = phenom.GetSemViewingMode() #makes instrument tell what mode/makes beam available
vm.scanMode = ppi.ScanMode.Imaging#set imaging mode
phenom.SetSemViewingMode(vm)#put machine in imaging mode