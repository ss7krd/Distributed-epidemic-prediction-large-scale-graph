import threading
import socket
import time

whichPrimaryNodesThisServer = []
#placing some dummay values in above ds - later del
whichPrimaryNodesThisServer.append(1)
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
			elif(msgStrList[0] == "REPL"):
				dummy = 2
def processing(whLock):
	while True:
		whLock.acquire()
		print(whichPrimaryNodesThisServer)
		print("\n")
		whLock.release()
		time.sleep(2)

#main function below:
s = socket.socket()
port = 12356
s.connect(('127.0.0.1', port))

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

