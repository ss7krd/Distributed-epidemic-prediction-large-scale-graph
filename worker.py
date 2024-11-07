import threading
import socket
import time

#WILL BE DIFFERENT FOR DIFFERENT SERVERS

this_server_id = 1

whichPrimaryNodesThisServer = []

#WILL BE DIFFERENT FOR DIFFERENT ITERATIONS 

current_iteration = 1
fileName = "placement_of_primary_copies_"+str(current_iteration)+".txt"
with open(fileName, 'r', encoding='utf8') as inputFile:
	for line in inputFile:
		lineList = line.strip().split()
		if(int(lineList[1]) == this_server_id):
			whichPrimaryNodesThisServer.append(int(lineList[0]))

# whichPrimaryNodesThisServer.append(1)
sir_s_dictionary = {}
sir_i_dictionary = {}
sir_r_dictionary = {}
# whichPrimaryNodesThisServer.append(12)

s = socket.socket()
port = 12340
s.connect(('127.0.0.1', port))

time.sleep(15)

lock = threading.Lock()

t1 = threading.Thread(target=listenToCentral, args=(s,lock)) 
t2 = threading.Thread(target=processing, args=(s,lock)) 

# starting thread 1 
t1.start() 
# starting thread 2 
t2.start() 

# wait until thread 1 is completely executed 
t1.join() 
# wait until thread 2 is completely executed 
t2.join() 

def listenToCentral(sok, whLock):
	while True:
		msg = sok.recv(11)
		msgStr = msg.decode("utf-8")
		if(len(msgStr) > 1):
			print("A command received:", msgStr)
			print("\n")
			msgStrList = msgStr.strip().split()
			if(msgStrList[0] == "REPT"):
				if(msgStrList[1] == "ADD"):
   					whichNode = int(msgStrList[2])
   					whLock.acquire()
   					whichPrimaryNodesThisServer.append(whichNode)
   					whLock.release()
				elif(msgStrList[1] == "DEL"):
					whichNode = int(msgStrList[2])
					whLock.acquire()
					whichPrimaryNodesThisServer.remove(whichNode)
					whLock.release()
			elif(msgStrList[0] == "RELP"):
				dummy = 2
			elif(msgStrList[0] == "SENDD"):
				to_send_string = 'REPL 222 '+msgStrList[2]
				sok.send(to_send_string.encode("utf-8"))
			elif(msgStrList[0] == "REPL"):
				value = float(msgStrList[2])
				print("The value that I asked for is: ", value)
				print("\n")

def processing():
	mobility_information_from_other_grids = {}
	

	adjacnecyListDestToSrc = {}

	for eachNode in whichPrimaryNodesThisServer:
		adjacnecyListDestToSrc[eachNode] = []
		mobility_information_from_other_grids[eachNode] = {}

	fileName = "graph_structure_itr_"+str(current_iteration)+".txt"
	with open(fileName, 'r', encoding='utf8') as inputFile:
		for line in inputFile:
			lineStrList = line.strip().split()
			srcNode = int(lineStrList[0])
			for element in range(1, len(lineStrList)):
				adjacnecyListDestToSrc[int(lineStrList[element])].append(srcNode)

	for eachNode in whichPrimaryNodesThisServer:	
		for otherSrcNode in adjacnecyListDestToSrc[eachNode]:
			mobility_information_from_other_grids[eachNode][otherSrcNode] = 0

	population_volume = {}
	prev_iteration = current_iteration - 1
	fileName = "SIR_values_itr_"+str(prev_iteration)+".txt"
	with open(fileName, 'r', encoding='utf8') as inputFile:
		for line in inputFile:
			lineStrList = line.strip().split()
			whichCurrNode = int(lineStrList[0])
			currNode_sValue = floor(lineStrList[1])
			currNode_iValue = floor(lineStrList[2])
			currNode_rValue = floor(lineStrList[3])

			if whichCurrNode in whichPrimaryNodesThisServer:
				sir_s_dictionary[whichCurrNode] = currNode_sValue
				sir_s_dictionary[whichCurrNode] = currNode_iValue
				sir_s_dictionary[whichCurrNode] = currNode_rValue

	for eachNode in whichPrimaryNodesThisServer:
		# sir_s_dictionary[eachNode] = 0.5
		# sir_i_dictionary[eachNode] = 0.3
		# sir_r_dictionary[eachNode] = 0.2
		population_volume[eachNode] = 70

	beta = 0.3 
	alpha = 0.5 
	gamma = 0.5 

	for eachNode in whichPrimaryNodesThisServer:
		sir_s_second_term = 0
		sir_s_third_term = 0
		sir_i_fourth_term = 0
		sir_s_second_term = beta*sir_s_dictionary[eachNode]*sir_i_dictionary[eachNode]
		sir_s_second_term = sir_s_second_term / population_volume[eachNode]

		sir_s_third_term_numerator_summ = 0
		sir_s_third_term_denominator_summ = 0
		for otherSrcNode in adjacnecyListDestToSrc[eachNode]:
			mobililty_value = mobility_information_from_other_grids[eachNode][otherSrcNode]
			x_value = sir_i_dictionary[otherSrcNode]/population_volume[otherSrcNode]
			tmpVar = mobililty_value * x_value * beta
			sir_s_third_term_numerator_summ = sir_s_third_term_numerator_summ + tmpVar

			sir_s_third_term_denominator_summ = sir_s_third_term_denominator_summ + mobility_information_from_other_grids[eachNode][otherSrcNode]

		sir_s_third_term = (alpha*sir_s_dictionary[eachNode]*sir_s_third_term_numerator_summ)/(population_volume[eachNode]+sir_s_third_term_denominator_summ)
		sir_i_fourth_term = gamma * sir_i_dictionary[eachNode]

		sir_s_dictionary[eachNode] = sir_s_dictionary[eachNode] - sir_s_second_term - sir_s_third_term
		sir_i_dictionary[eachNode] = sir_i_dictionary[eachNode] + sir_s_second_term + sir_s_third_term - sir_i_fourth_term
		sir_r_dictionary[eachNode] = sir_r_dictionary[eachNode] + sir_i_fourth_term


		fileName = "SIR_values_"+str(this_server_id)+"_itr_"+str(current_iteration)+".txt"
		with open(fileName, 'w', encoding='utf8') as outputFile:
			for eachGrid in whichPrimaryNodesThisServer:
				outputFile.write(str(eachGrid)+" ")
				outputFile.write(str(sir_s_dictionary[eachGrid])+" ")
				outputFile.write(str(sir_i_dictionary[eachGrid])+" ")
				outputFile.write(str(sir_r_dictionary[eachGrid])+"\n")

	# while True:
	# 	whLock.acquire()
	# 	print(whichPrimaryNodesThisServer)
	# 	print("\n")
	# 	whLock.release()
	# 	time.sleep(2)

#MAIN FUNCTION BELOW:
processing()

# s = socket.socket()
# port = 12340
# s.connect(('127.0.0.1', port))

# time.sleep(15)

# lock = threading.Lock()

# t1 = threading.Thread(target=listenToCentral, args=(s,lock)) 
# t2 = threading.Thread(target=processing, args=(s,lock)) 

# # starting thread 1 
# t1.start() 
# # starting thread 2 
# t2.start() 

# # wait until thread 1 is completely executed 
# t1.join() 
# # wait until thread 2 is completely executed 
# t2.join() 

# # both threads completely executed 
# print("Done!") 

