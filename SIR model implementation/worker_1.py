import threading
import socket
import time

whichPrimaryNodesThisServer = []
#placing some dummay values in above ds - later del
current_iteration 
whichPrimaryNodesThisServer.append(1)
sir_s_dictionary = {}
sir_i_dictionary = {}
sir_r_dictionary = {}
# whichPrimaryNodesThisServer.append(12)
#JAR JEI GRAPH REGARDING UPDATE MSG FROM CENTRALIZED SEITA FIRST E PORLO AND NECESSARY UPDATE KORLO - NOT IMPL

#ei listen khali onno worker er request listen korbe - not impl
def listenToCentral(sok, whLock):
	#SCP KORE SERVER ER PATHANO FILE TA PORTE THAKBE REGULARLY - NOT IMPL
	#THAT MEANS THAT WORKER SCP PATHABE NA, BUT AKTA SPECIFIC FILE CONTINUOUS READ KORTE THAKBE
	#??DIFF MESSAGE ER JONNO DIFF KAJ - NOT IMPL
	#loop er vitor ei func er processing chalate hobe - not impl
	while True:
		msg = sok.recv(11)
		msgStr = msg.decode("utf-8")
		if(len(msgStr) > 1):
			print("A command received:", msgStr)
			print("\n")
			msgStrList = msgStr.strip().split()
			if(msgStrList[0] == "REPT"):
				if(msgStrList[1] == "ADD"):
					#synchronization use?? - not impl
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
				#what happens if replication related command - not impl
				dummy = 2
			elif(msgStrList[0] == "SENDD"):
				to_send_string = 'REPL 222 '+msgStrList[2]
				sok.send(to_send_string.encode("utf-8"))
			elif(msgStrList[0] == "REPL"):
				value = float(msgStrList[2])
				print("The value that I asked for is: ", value)
				print("\n")


		#SCP KORE DATA PATHABE EI WORKER JEI WORKER REQUEST KORTSE TAKE - NOT IMPL

#ei  thread ei worker er main processing korbe - not impl
#onno worker er data lagle oi worker ke scp korbe - not impl
def processing(sok, whLock):
	to_send_string = 'FH SV 02 01'
	sok.send(to_send_string.encode("utf-8"))

	mobility_information_from_other_grids = {}
	
	adjacnecyListDestToSrc = {}
	#this adjacency list will be loaded from file - not impl

	for eachNode in whichPrimaryNodesThisServer:
		adjacnecyListDestToSrc[eachNode] = []
		mobility_information_from_other_grids[eachNode] = {}
		#this dictionary contains all incoming mobility, center thk send kora file thk read korbe - not impl
		#so this dictionary[eachNode][3] = 15, means from grid 3 to eachNode grid, mobility is 15
		for otherSrcNode in adjacnecyListDestToSrc[eachNode]:
			mobility_information_from_other_grids[eachNode][otherSrcNode] = 0

	population_volume = {}
	#population of all nodes to be processed in this server - not impl
	#aager iteration er sob nodes er (to be processed in this server or not) sir value load korte hobe eikhane from file - not impl
	for eachNode in whichPrimaryNodesThisServer:
		sir_s_dictionary[eachNode] = 0.5
		sir_i_dictionary[eachNode] = 0.3
		sir_r_dictionary[eachNode] = 0.2
		population_volume[eachNode] = 70
		#population of all incoming nodes - not impl

	beta = 0.3 #apaptoto sob somoy sob grid point er jonno beta value constant dhorchi
	#thik hocche, ei constant dhora?? - not impl
	alpha = 0.5 #not impl
	gamma = 0.5 #not impl

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



	
	#loop er vitor ei func er processing chalate hobe - not impl
	while True:
		whLock.acquire()
		print(whichPrimaryNodesThisServer)
		print("\n")
		whLock.release()
		time.sleep(2)

#main function below:

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

