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
	print(f"Arguments Passed: {sys.argv[1:]}")
	filename =  sys.argv[1]
else:
	print("Provide 1 argument; the name of the bin forces file you'd like to process!")
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

for iBin in np.arange(nBins):
	print(coors[iBin,0], " " , coors[iBin,1] , " ", coors[iBin,2])


rawData = np.genfromtxt(filename, comments="#")
nTimes = rawData.shape[0]
print(rawData.shape)
print(" Number of available iterations is ", nTimes)

data = np.zeros([nBins,3,nTimes])
for iBin in np.arange(nBins):
    for iCoor in np.arange(3):
        for iTime in np.arange(nTimes):
            data[iBin,iCoor,iTime] = rawData[iTime,int(1+(iBin*12)+iCoor)]

time = rawData[:,0]
print(data.shape)

####################
# PLOT CONVERGENCE # 
####################

fig, axes = plt.subplots(3, 1, figsize=(7, 8), sharex=True)

# --- X plot ---
axisName = [r"$F_x$",r"$F_y$",r"$F_z$"]
binsPercentages = [0.25,0.5,0.75,0.95]

for i in [0,1,2]:
	for j in binsPercentages:
		idBin = int(j*nBins)	
		axes[i].plot(time, data[idBin,i,:], '-o', ms=3, lw=1.5, label=str(j*100)+"%")
		axes[i].set_ylabel(axisName[i], fontsize=13)
		axes[i].legend(fontsize=11, loc='best', frameon=False)
		axes[i].grid(True, linestyle='--', alpha=0.5)
		axes[i].tick_params(labelsize=11)

# Optional title
fig.suptitle('Forces convergence', fontsize=15)

# Tight layout to avoid overlap
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("forceConvergence.png", dpi=300, bbox_inches='tight')

