import numpy as np
from pylab import *
import matplotlib.pyplot as plt

deathList,blockapoList,disintegrationList,viabilityList,remainingCellRatioList = [],[],[],[],[]
with open('A:/Downloads/Projects/ABM/src/Explorations/20200724/ABM_Probabilistic_Explo_Death_BlockApo_DisintegrationDuration_selectedData.csv', 'r') as file_read :
	data =  file_read.readlines()
	for line in data[7:] :
		line = line.replace('\"', '').split(';')
		run_number, death, blockapo, disintegration, viability, remainingCellRatio = int(line[0]), int(line[1]), int(line[2]), int(line[3]), float(line[5]),float(line[6])
		deathList.append(death)
		blockapoList.append(blockapo)
		disintegrationList.append(disintegration)
		viabilityList.append(viability)
		remainingCellRatioList.append(remainingCellRatio)

fig = plt.figure(figsize=(8,6))

ax = fig.add_subplot(111,projection='3d')

print(len(deathList),len(blockapoList),len(disintegrationList),len(viabilityList),len(remainingCellRatioList))

xs = np.array(deathList)
ys = np.array(blockapoList) 
zs = np.array(disintegrationList)  
color_data = np.array(viabilityList) 

colmap = cm.ScalarMappable(cmap=cm.hsv)
colmap.set_array(color_data)

yg = ax.scatter3D(xs, ys, zs,  marker='o', c=cm.hsv(color_data/max(color_data)))
# yg = ax.scatter3D(xs, ys, zs,  marker='o', c=cm.hsv(zs/max(zs))
cb = fig.colorbar(colmap)

ax.set_xlabel('deathList')
ax.set_ylabel('blockapoList')
ax.set_zlabel('disintegrationList')


plt.show()