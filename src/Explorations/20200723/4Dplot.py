import numpy as np
from pylab import *
import matplotlib.pyplot as plt

deathRateList,lateApoThresholdList,viabilityList,remainingCellRatioList = [],[],[],[]
with open('A:/Downloads/Projects/ABM/src/Explorations/20200723/selected_data_disinThresh20.csv', 'r') as file_read :
	data =  file_read.readlines()
	for line in data[7:] :
		line = line.replace('\"', '').split(',')
		run_number,deathRate,lateApoThreshold, viability,remainingCellRatio = int(line[0]), float(line[1]), int(line[2]), float(line[4]), float(line[5])
		deathRateList.append(deathRate)
		lateApoThresholdList.append(lateApoThreshold)
		viabilityList.append(viability)
		remainingCellRatioList.append(remainingCellRatio)

fig = plt.figure(figsize=(8,6))

ax = fig.add_subplot(111,projection='3d')

xs = np.array(lateApoThresholdList)
ys = np.array(viabilityList) 
zs = np.array(deathRateList)  
color_data = np.array(remainingCellRatioList) 

colmap = cm.ScalarMappable(cmap=cm.hsv)
colmap.set_array(color_data)

yg = ax.scatter3D(xs, ys, zs,  marker='o', c=cm.hsv(color_data/max(color_data)))
# yg = ax.scatter3D(xs, ys, zs,  marker='o', c=cm.hsv(zs/max(zs))
cb = fig.colorbar(colmap)

ax.set_xlabel('apoptosis onset (h)')
ax.set_ylabel('viability (%)')
ax.set_zlabel('death rate')


plt.show()