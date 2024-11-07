#NEED TO GIVE FOLDER NAME ACCORDING TO THE AWS WHERE IT WILL BE REALLY RUNNING
prev_iteration = 1
#IF THE SCRIPT IS RUN BETWEEN ITERATION 1 & 2, THEN PREV_ITERATION WILL BE EQUAL TO 1
folderName = 'Lab_Materials/covid-19/Code'
folderName = folderName + '/SIR_results'
folderName = folderName + '/SIR_results_itr_' + str(prev_iteration)

import os

fileList = os.listdir(folderName)

fileName = "SIR_values_itr_"+str(prev_iteration)+".txt"
with open(fileName, 'a', encoding='utf8') as outputFile:
	for file in fileList:
		fullFilePath = folderName + '/' + file
		with open(fullFilePath, 'r', encoding='utf8') as inputFile:
			for line in inputFile:
				line = line.strip()
				outputFile.write(line)
				outputFile.write("\n")

os.system(Repartition/python3 main_file_centralized_master.py)
os.system(Repartition/python3 worker.py) #similarly for other workers
