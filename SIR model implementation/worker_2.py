import threading
import socket
import time

whichPrimaryNodesThisServer = []
#placing some dummay values in above ds - later del
# whichPrimaryNodesThisServer.append(1)
whichPrimaryNodesThisServer.append(2)
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
def processing(whLock):
	#loop er vitor ei func er processing chalate hobe - not impl
	# to_send_string = 'FH SV 02 01'
	while True:
		whLock.acquire()
		print(whichPrimaryNodesThisServer)
		print("\n")
		whLock.release()
		time.sleep(2)

#main function below:
s = socket.socket()
port = 12340
s.connect(('127.0.0.1', port))

time.sleep(15)

lock = threading.Lock()

t1 = threading.Thread(target=listenToCentral, args=(s,lock)) 
t2 = threading.Thread(target=processing, args=(lock,)) 

# starting thread 1 
t1.start() 
# starting thread 2 
t2.start() 

# wait until thread 1 is completely executed 
t1.join() 
# wait until thread 2 is completely executed 
t2.join() 

# both threads completely executed 
print("Done!") 

