import socket
import time
import threading

no_of_servers = 2 #these server means only worker servers, not includes centralized server

s = socket.socket()
print("Central server socket created successfully.")
port = 12340
s.bind(('', port))		 
print ("Central server socket binded to %s" %(port)) 
s.listen(5)	 
print ("socket is listening")

c_list = []
addr_list = []
how_many_worker_servers = no_of_servers
for i in range(0, how_many_worker_servers):
	c, addr = s.accept()
	print('Got connection from', addr)
	c_list.append(c)
	addr_list.append(addr)

def listenToWorkers(sok):
	while True:
		for eachClient in c_list:
			msg = eachClient.recv(11)
			msgStr = msg.decode("utf-8")
			if(len(msgStr) > 1):
				print("A command received:", msgStr)
				print("\n")
				msgStrList = msgStr.strip().split()
				if(msgStrList[0] == "FH"):
					which_worker_server = int(msgStrList[2])
					to_send_string = 'SENDD SV '+msgStrList[3]
					c_list[which_worker_server-1].send(to_send_string.encode("utf-8"))
				elif(msgStrList[0] == "REPL"):
					which_worker_server = int(msgStrList[2])
					to_send_string = 'REPL IS '+msgStrList[1]
					c_list[which_worker_server-1].send(to_send_string.encode("utf-8"))


def processing(dummy):
	while True:
		dummy = 2

t1 = threading.Thread(target=listenToWorkers, args=(s,)) 
t2 = threading.Thread(target=processing, args=(2,)) 

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

