import numpy as np 
import shutil
import os
import pandas as pd
import copy

folderName = "Lab_Materials/covid-19/Code/Mobility prediction/mobility_prediction_data/"
parentFolderName = "Lab_Materials/covid-19/Code/Mobility prediction/"
whichfolder = os.listdir(folderName)

two_dim_list = []
two_dim_list_size = 0
number_of_timesteps_considered = 10
# number_of_routes = 100

#final_three_dim_list is a list, each entry of this list is a train/test sample, this will
#be converted to a numpy array
final_three_dim_list = []
for file in whichfolder:
	# print(file)
	data=pd.read_csv(folderName+str(file))
	mobility_dataList=data['mobility_amount'].tolist()
	two_dim_list.append(mobility_dataList)
	two_dim_list_size = two_dim_list_size + 1
	# print(two_dim_list_size)
	if two_dim_list_size == number_of_timesteps_considered:
		# print("Print here", len(two_dim_list))
		two_dim_list_tmp = copy.deepcopy(two_dim_list)
		final_three_dim_list.append(two_dim_list_tmp)
		two_dim_list.pop(0)
		two_dim_list_size = two_dim_list_size - 1

# print(len(final_three_dim_list[0]))
final_three_dim_nparray = np.array(final_three_dim_list)
print(final_three_dim_nparray.shape)
np.save(parentFolderName + "X_train.npy", final_three_dim_nparray)

