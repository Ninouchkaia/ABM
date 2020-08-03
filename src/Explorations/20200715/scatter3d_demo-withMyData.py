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

alphaList,deathRateList,viabilityList,remainingCellRatioList,stepList = [],[],[],[],[]
with open('.MacrophageDifferentiationModel2.csv', 'r') as file_read :
	data =  file_read.readlines()
	for line in data[7:] :
		line = line.replace('\"', '').replace('\n','').split(',')
		print(line)
		run_number, deathRate, alpha, step, viability, remainingCellRatio = float(line[0]), float(line[4]), float(line[5]), float(line[6]), float(line[7]), float(line[8])
		alphaList.append(alpha)
		deathRateList.append(deathRate)
		viabilityList.append(viability)
		remainingCellRatioList.append(remainingCellRatio)
		stepList.append(step)


fig = plt.figure(figsize=(8,6))

ax = fig.add_subplot(111,projection='3d')

xs = np.array(stepList)
ys = np.array(remainingCellRatioList) 
zs = np.array(viabilityList)  
color_data = np.array(alphaList) 
# ax.plot3D(xs, ys, zs, 'gray')

colmap = cm.ScalarMappable(cmap=cm.hsv)
colmap.set_array(xs)

yg = ax.scatter3D(xs, ys, zs,  marker='o', c=cm.hsv(color_data/max(color_data)))
# yg = ax.scatter3D(xs, ys, zs,  marker='o', c=cm.hsv(zs/max(zs))
cb = fig.colorbar(colmap)

ax.set_xlabel('stepList')
ax.set_ylabel('remainingCellRatioList')
ax.set_zlabel('viabilityList')


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