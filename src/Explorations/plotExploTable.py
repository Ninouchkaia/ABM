#!/usr/bin/python
# -*- coding: utf-8 -*-
# jupyter notebook --browser='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'


import timeit
start = timeit.default_timer()

import sys
import os
import csv
from operator import itemgetter
import networkx as nx
from networkx.algorithms import community
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from collections import defaultdict
from collections import OrderedDict
import statistics 
import re
import gzip
import numpy as np

# viability_dict = {}
# remaining_dict = {}
# viability_mean_list = []
# with open('randomness/test_10_g.csv', 'r') as file_read :
# 	data =  file_read.readlines()
# 	for line in data[7:] :
# 		line = line.replace('\"', '').split(',')
# 		run_number,step,viability,remainingCellRatio = int(line[0]), int(line[1]), float(line[2]), float(line[3])
# 		print(run_number,step,viability,remainingCellRatio)
# 		if run_number not in viability_dict :
# 			viability_dict[run_number] = []
# 		# viability_dict[run_number].append((step, viability))
# 		viability_dict[run_number].append(viability)
# 		if run_number not in remaining_dict :
# 			remaining_dict[run_number] = []
# 		remaining_dict[run_number].append(remainingCellRatio)	
# 		# remaining_dict[run_number].append((step, remainingCellRatio))

# df_viability = pd.DataFrame.from_dict(viability_dict) #  orient='index')
# print(df_viability)

# df_remaining = pd.DataFrame.from_dict(remaining_dict)


# my_list = [0,24,24*2,24*3,24*4,24*5,24*6,24*7,24*8,24*9,24*10,24*11,24*12,24*13]

# filtered_df_viability = df_viability[df_viability.index.isin(my_list)]
# filtered_df_remaining = df_remaining[df_remaining.index.isin(my_list)]

# # df_viability.plot(title='Viability',legend=False)
# # df_remaining.plot(title='Remaining Cells', legend=False)

# filtered_df_viability.plot(title='Viability',legend=False, ylim=(25,110))
# filtered_df_remaining.plot(title='Remaining Cells', legend=False, ylim=(30,110))

# # (filtered_df_viability.mean(axis = 1)).plot(title='Average viability (50 simulations)', color='magenta')

# plt.show()



## plot each plot separately
# for index in range(1,51) :
# 	print(index)
# 	filtered_df_viability[index].plot(title='viability %s' % index)
# 	plt.savefig('viability_%sa.png' % index)
# 	# plt.show()
# 	plt.close()

# for index in range(1,51) :
# 	print(index)
# 	filtered_df_remaining[index].plot(title='remaining %s' % index)
# 	plt.savefig('remaining_%sa.png' % index)
# 	# plt.show()
# 	plt.close()








viability_dict = {}
remaining_dict = {}
signalStrength_dict = {}
chemicalB_dict = {}
viability_mean_list = []
with open('CLL-update-fusionReversible-forSeedExperiment-withoutGui NinaExploStochasticity-table.csv', 'r') as file_read :
	data =  file_read.readlines()
	for line in data[7:] :
		line = line.replace('\"', '').split(',')
		run_number,step,viability,remainingCellRatio,signalStrengthMean,chemicalBMean = int(line[0]), int(line[1]), float(line[2]), float(line[3]), float(line[5]), float(line[7])
		print(run_number,step,viability,remainingCellRatio,signalStrengthMean,chemicalBMean)
		if run_number not in viability_dict :
			viability_dict[run_number] = []
		# viability_dict[run_number].append((step, viability))
		viability_dict[run_number].append(viability)
		if run_number not in remaining_dict :
			remaining_dict[run_number] = []
		remaining_dict[run_number].append(remainingCellRatio)	
		# remaining_dict[run_number].append((step, remainingCellRatio))
		if run_number not in signalStrength_dict :
			signalStrength_dict[run_number] = []
		signalStrength_dict[run_number].append(signalStrengthMean)
		if run_number not in chemicalB_dict :
			chemicalB_dict[run_number] = []
		chemicalB_dict[run_number].append(chemicalBMean)

df_viability = pd.DataFrame.from_dict(viability_dict) #  orient='index')
print(df_viability)

df_remaining = pd.DataFrame.from_dict(remaining_dict)

df_signalStrength = pd.DataFrame.from_dict(signalStrength_dict)

df_chemicalB = pd.DataFrame.from_dict(chemicalB_dict)

my_list = [0,24,24*2,24*3,24*4,24*5,24*6,24*7,24*8,24*9,24*10,24*11,24*12,24*13]

filtered_df_viability = df_viability[df_viability.index.isin(my_list)]
filtered_df_remaining = df_remaining[df_remaining.index.isin(my_list)]
filtered_df_signalStrength = df_signalStrength[df_signalStrength.index.isin(my_list)]
filtered_df_chemicalB = df_chemicalB[df_chemicalB.index.isin(my_list)]


# df_viability.plot(title='Viability',legend=False)
# df_remaining.plot(title='Remaining Cells', legend=False)

# filtered_df_viability.plot(title='Viability',legend=False, ylim=(0,110))
# filtered_df_remaining.plot(title='Remaining Cells', legend=False, ylim=(0,110))
# filtered_df_signalStrength.plot(title='Signal Strength in monocytes and macrophages (mean)', legend=False, ylim=(0,2000))
# filtered_df_chemicalB.plot(title='Chemical B in cancer cells (mean)', legend=False, ylim=(0,100))

# (filtered_df_viability.mean(axis = 1)).plot(title='Average viability (50 simulations)', color='magenta')

## plot each plot separately
# for index in range(1,101) :
# 	print(index)
# 	filtered_df_viability[index].plot(title='viability %s' % index)
# 	plt.savefig('viability_%s.png' % index)
# 	# plt.show()
# 	plt.close()


for index in range(1,101) :
	fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(5,9))
	fig.tight_layout()
	plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)
	print(index)
	filtered_df_viability[index].plot(ax=axes[0],title='viability %s' % index, color='orange')
	filtered_df_remaining[index].plot(ax=axes[1],title='remaining %s' % index, color='green')
	filtered_df_signalStrength[index].plot(ax=axes[2],title='signal strength %s' % index, color='blue')
	filtered_df_chemicalB[index].plot(ax=axes[3],title='chemical B %s' % index, color='magenta')	

	plt.savefig('viability_remaining_signalStrength_chemicalB%s.png' % index)
	# plt.show()
	plt.close()


# plt.show()

stop = timeit.default_timer()
print(stop - start)  