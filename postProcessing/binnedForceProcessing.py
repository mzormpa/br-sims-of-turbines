#!/usr/bin/env python

# ## Initialize

import matplotlib.pyplot as plt 
import numpy as np
import sys

import seaborn as sns
palette = sns.color_palette("tab10")


plt.rcParams.update({
"font.family": "Nimbus Roman" ,
"mathtext.default":"regular" 
})

# ============================== #
# ============ MAIN ============ #
# ============================== #

if len(sys.argv) > 1:
	print(f" Arguments Passed: {sys.argv[1:]}")
	filename =  sys.argv[1]
else:
	print(" Provide 1 argument; the name of the bin forces file you'd like to process!")
	exit(1)


header = []
with open(filename) as f:
	for line in f:
		tokens = line.split()
		if (tokens[0] == "#"):
			header.append(tokens)
		else:
			break

nBins = int(header[0][3])
print(" Number of bins in file ", filename , " is ", nBins)
coors = np.zeros([nBins,3])
for iBin in np.arange(nBins):
    coors[iBin,0] = float(header[5][4+iBin])
    coors[iBin,1] = float(header[6][4+iBin])
    coors[iBin,2] = float(header[7][4+iBin])

    if (int(coors[iBin,0]+coors[iBin,1])!=0):
        print(" This script only works for a z-oriented blade. Please adjsut script or coordinate system")
        exit(1)

dr = coors[1,2]-coors[0,2] ## strictly z oriented
r = coors[-1,2] ## strictly z oriented
print(" First bin (", coors[0,0],",",coors[0,1],",",coors[0,2],")")
print(" Last bin (",coors[-1,0],",",coors[-1,1],",",coors[-1,2],")")
print(" Dr = ", dr)
print("  r = ", coors[-1,2]) 


rawData = np.genfromtxt(filename, comments="#")
nTimes = rawData.shape[0]
print(" Number of available iterations is ", nTimes)

data = np.zeros([nBins,3,nTimes])
for iBin in np.arange(nBins):
    for iCoor in np.arange(3):
        for iTime in np.arange(nTimes):
            data[iBin,iCoor,iTime] = rawData[iTime,int(1+(iBin*12)+iCoor)]

time = rawData[:,0]

####################
# PLOT CONVERGENCE # 
####################

print(" Plotting convergence ...")
fig, axes = plt.subplots(3, 1, figsize=(7, 8), sharex=True)

# --- X plot ---
axisName = [r"$F_x$",r"$F_y$",r"$F_z$"]
binsPercentages = [0.25,0.5,0.75,0.95]
startFrom = int(nTimes*0.1)


for iCoor in [0,1,2]:
	for j in binsPercentages:
		idBin = int(j*nBins)	
		axes[iCoor].plot(time[startFrom:], data[idBin,iCoor,startFrom:], '-', ms=3, lw=1.5, label=str(j*100)+"%")
		axes[iCoor].set_ylabel(axisName[iCoor]+"[N]", fontsize=13)
		axes[iCoor].legend(fontsize=11, loc='best', frameon=False)
		axes[iCoor].grid(True, linestyle='--', alpha=0.5)
		axes[iCoor].tick_params(labelsize=11)

axes[2].set_xlabel("Iteration")
# Optional title
fig.suptitle('Convergence of sectional forces', fontsize=15)

# Tight layout to avoid overlap
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()
plt.savefig("forceConvergence.png", dpi=300, bbox_inches='tight')

###########################
# PLOT FORCE DISTRIBUTION # 
###########################

print(" Plotting force distributions ...")
fig, axes = plt.subplots(1, 3, figsize=(5, 15))
for iPlot in [0,1,2]:
    axes[iPlot].set_xlabel("r/R")

axes[0].plot(coors[:,2]/r, data[:,0,-1],'-o', ms=3, lw =1.5)
axes[0].set_ylabel("Thrust per unit span [N/m]")

axes[1].plot(coors[:,2]/r, data[:,1,-1],'-o', ms=3, lw =1.5)
axes[1].set_ylabel("Tangential Force per unit span [Nm/m]")

axes[2].plot(coors[:,2]/r, data[:,2,-1],'-o', ms=3, lw =1.5, label= str("Radial force per unit span [N/m]"))
axes[2].set_ylabel("Radial force per unit span [N/m]")

fig.suptitle('Sectional force distributions', fontsize=15)
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()
plt.savefig("sectionalForces.png", dpi=300, bbox_inches='tight')

storeData = np.zeros([nBins,5])
storeData[:,0] = coors[:,2]
storeData[:,1] = coors[:,2]/r
storeData[:,2] = data[:,0,-1]/dr
storeData[:,3] = data[:,1,-1]/dr
storeData[:,4] = data[:,2,-1]/dr

np.savetxt(
    'forces.dat',          
    storeData,            
    fmt='%.5f',            # format numbers (2 decimal places)
    delimiter='\t',        # tab-separated (you can use ',' or ' ')
    header='#r \t R/r \t Fax \t Ftan \t Fr' 
)

