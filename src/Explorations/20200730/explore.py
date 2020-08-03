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
with open('table1.csv', 'r') as file_read :
	data =  file_read.readlines()
	for line in data[7:] :
		line = line.replace('\"', '').split(',')
		"[run number]","gui-BlockedApoptosisThreshold","gui-alpha","[step]","getViability","getRemainingCellRatio"

		run_number, blockedApoptosisThreshold, alpha, step, viability, remainingCellRatio = int(line[0]), float(line[1]), float(line[2]), int(line[3]), float(line[4]),float(line[5])
		# print(run_number,deathRate, alpha, step, viability, remainingCellRatio)
		if (run_number,blockedApoptosisThreshold, alpha)  not in viability_dict :
			viability_dict[(run_number,blockedApoptosisThreshold, alpha)] = []
		viability_dict[(run_number,blockedApoptosisThreshold, alpha)].append(viability)
		if (run_number,blockedApoptosisThreshold, alpha) not in remaining_dict :
			remaining_dict[(run_number,blockedApoptosisThreshold, alpha)] = []
		remaining_dict[(run_number,blockedApoptosisThreshold, alpha)].append(remainingCellRatio)	

df_viability = pd.DataFrame.from_dict(viability_dict) #  orient='index')

df_remaining = pd.DataFrame.from_dict(remaining_dict)


my_list = [0,24,24*2,24*3,24*4,24*5,24*6,24*7,24*8,24*9,24*10,24*11,24*12,24*13]

filtered_df_viability = df_viability[df_viability.index.isin(my_list)]
filtered_df_remaining = df_remaining[df_remaining.index.isin(my_list)]
# print(filtered_df_viability)

# transpose tables 
filtered_df_viability_transposed = filtered_df_viability.transpose()
filtered_df_remaining_transposed = filtered_df_remaining.transpose()
print(filtered_df_viability_transposed)

# concat final values for viability and remaining cells ratio
concat_df_viability_remaining_final_values = pd.concat([filtered_df_viability_transposed[312], filtered_df_remaining_transposed[312]], axis=1)
print(concat_df_viability_remaining_final_values)

#rename columns
concat_df_viability_remaining_final_values.columns = ['final_viability', 'final_remaining_cells_percentage']
print(concat_df_viability_remaining_final_values)

#filter initial conditions by final (output) values for viability and remaining cell ratio
# concat_df_viability_remaining_final_values_top = concat_df_viability_remaining_final_values.loc[(concat_df_viability_remaining_final_values['final viability'] > 90)]
# concat_df_viability_remaining_final_values_top = concat_df_viability_remaining_final_values[(concat_df_viability_remaining_final_values.final_viability > 90) & (concat_df_viability_remaining_final_values.final_remaining_cells_percentage > 40)]
# print(concat_df_viability_remaining_final_values_top)

filtered_df_viability.plot(title='Viability',legend=True, ylim=(0,110))
filtered_df_remaining.plot(title='Remaining Cells', legend=True, ylim=(0,110))
# filtered_df_signalStrength.plot(title='Signal Strength in monocytes and macrophages (mean)', legend=True, ylim=(0,2000))
# filtered_df_chemicalB.plot(title='Chemical B in cancer cells (mean)', legend=True, ylim=(-50,100))

plt.show()


# print(filtered_df_viability[5])
# for (i,j) in filtered_df_viability :
# 	print((i,j))

# for (i,j) in filtered_df_viability :
# 	fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(5,9))
# 	fig.tight_layout()
# 	plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)
# 	print((i,j))
# 	set_of_values = "%s, %s" % (i,j) 
# 	filtered_df_viability[(i,j)].plot(ax=axes[0],title='viability %s' % set_of_values, color='orange')
# 	filtered_df_remaining[(i,j)].plot(ax=axes[1],title='remaining %s' % set_of_values, color='green')
# 	filtered_df_signalStrength[(i,j)].plot(ax=axes[2],title='signal strength %s' % set_of_values, color='blue')
# 	filtered_df_chemicalB[(i,j)].plot(ax=axes[3],title='chemical B %s' % set_of_values, color='magenta')	

# 	plt.savefig('viability_remaining_signalStrength_chemicalB%s.png' % set_of_values)
# 	# plt.show()
# 	plt.close()


# plt.show()


stop = timeit.default_timer()
print(stop - start)  