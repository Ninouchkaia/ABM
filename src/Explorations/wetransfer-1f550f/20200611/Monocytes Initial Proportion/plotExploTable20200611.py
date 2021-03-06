#!/usr/bin/python
# -*- coding: utf-8 -*-
# jupyter notebook --browser='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'


import timeit
start = timeit.default_timer()

import sys
import os
import csv

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
with open('CLL-update-fusionReversible-forSeedExperiment-withoutGui NinaExploStochasticityAndParameters-table2.csv', 'r') as file_read :
	data =  file_read.readlines()
	for line in data[7:] :
		line = line.replace('\"', '').split(',')
		run_number,propMonoInit,step,viability,remainingCellRatio,signalStrengthMean,chemicalBMean = int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[6]), float(line[8])
		print(run_number,propMonoInit,step,viability,remainingCellRatio,signalStrengthMean,chemicalBMean)
		if propMonoInit not in viability_dict :
			viability_dict[propMonoInit] = []
		# viability_dict[propMonoInit].append((step, viability))
		viability_dict[propMonoInit].append(viability)
		if propMonoInit not in remaining_dict :
			remaining_dict[propMonoInit] = []
		remaining_dict[propMonoInit].append(remainingCellRatio)	
		# remaining_dict[propMonoInit].append((step, remainingCellRatio))
		if propMonoInit not in signalStrength_dict :
			signalStrength_dict[propMonoInit] = []
		signalStrength_dict[propMonoInit].append(signalStrengthMean)
		if propMonoInit not in chemicalB_dict :
			chemicalB_dict[propMonoInit] = []
		chemicalB_dict[propMonoInit].append(chemicalBMean)

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


filtered_df_viability.plot(title='Viability',legend=True, ylim=(0,110))
filtered_df_remaining.plot(title='Remaining Cells', legend=True, ylim=(0,110))
filtered_df_signalStrength.plot(title='Signal Strength in monocytes and macrophages (mean)', legend=True, ylim=(0,2000))
filtered_df_chemicalB.plot(title='Chemical B in cancer cells (mean)', legend=True, ylim=(-50,100))

plt.show()

# for index in range(1,101) :
# 	fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(5,9))
# 	fig.tight_layout()
# 	plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)
# 	print(index)
# 	filtered_df_viability[index].plot(ax=axes[0],title='viability %s' % index, color='orange')
# 	filtered_df_remaining[index].plot(ax=axes[1],title='remaining %s' % index, color='green')
# 	filtered_df_signalStrength[index].plot(ax=axes[2],title='signal strength %s' % index, color='blue')
# 	filtered_df_chemicalB[index].plot(ax=axes[3],title='chemical B %s' % index, color='magenta')	

# 	plt.savefig('viability_remaining_signalStrength_chemicalB%s.png' % index)
# 	# plt.show()
# 	plt.close()


# plt.show()

stop = timeit.default_timer()
print(stop - start)  