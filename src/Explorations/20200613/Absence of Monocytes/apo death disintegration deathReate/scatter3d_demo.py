'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''

import numpy as np
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

apoThresholdList,apoDurationList,disintegrationDurationList,deathRateList,viabilityList,remainingCellRatioList = [],[],[],[],[],[]
with open('table1-point.csv', 'r') as file_read :
	data =  file_read.readlines()
	for line in data[7:] :
		line = line.replace('\"', '').split(';')
		run_number,apoThreshold,apoDuration,disintegrationDuration,deathRate,viability,remainingCellRatio = int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[6]),float(line[7])
		apoThresholdList.append(apoThreshold)
		apoDurationList.append(apoDuration)
		disintegrationDurationList.append(disintegrationDuration)
		deathRateList.append(deathRate)
		viabilityList.append(viability)
		remainingCellRatioList.append(remainingCellRatio)

def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin

fig = plt.figure(figsize=(8,6))

ax = fig.add_subplot(111,projection='3d')

xs = np.array(viabilityList)
ys = np.array(remainingCellRatioList) 
zs = np.array(apoDurationList)  

# ax.plot3D(xs, ys, zs, 'gray')

colmap = cm.ScalarMappable(cmap=cm.hsv)
colmap.set_array(xs)

yg = ax.scatter(xs, ys, zs,  marker='o', c=cm.hsv(xs/max(xs), s=xs))
# yg = ax.scatter3D(xs, ys, zs,  marker='o', c=cm.hsv(zs/max(zs))
cb = fig.colorbar(colmap)

ax.set_xlabel('viability')
ax.set_ylabel('remaining cells')
ax.set_zlabel('death rate')


plt.show()


# ax = plt.axes(projection='3d')

# # Data for a three-dimensional line
# zline = np.linspace(0, 15, 1000)
# xline = np.sin(zline)
# yline = np.cos(zline)
# ax.plot3D(xline, yline, zline, 'gray')

# # Data for three-dimensional scattered points
# zdata = 15 * np.random.random(100)
# xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
# ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
# ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');
# plt.show()