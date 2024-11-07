# replication implementation

import socket
import time
import copy

no_of_servers = 2 #these server means only worker servers, not includes centralized server

s = socket.socket()
print("Central server socket created successfully.")
port = 12356
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
#psudo-code is as follows
#initial replication
#proti edge dhore dhore jao,
#dekho current edge ta weight threshold er upore kina
#and ml thk dekho je edge er weight er variance kemon, also rmin??
#and rmax kheyal rakhte hobe


#and jokhon edge add hocche
#dekho weight threshold er upore kina
#and ml thk dekho je edge er weight er variance kemon, also rmin??
#and rmax kheyal rakhte hobe, jodi delete kora lage tahole apatoto
#LRU onushare delete korbo, pore dorkar hoile LFU implement kora jabe
#case by case basis chinta korte hobe for re-partitioning operation


#syncing er beparta 
#asole ki ki sync korte hobe??

#KHALI CENTRALIZED KORLEI TO HOBE NA, WORKER ER CODE O LIKHTE HOBE

#UPDATE THE FOLLOWING TWO DS IN THE PARTITIONING AND RE-PARTITIONING PHASES:

placementOfPrimaryCopies = {}
placementOfPrimaryCopies_dummy = {}
placementOfPrimaryCopies_prev = {}

placementOfSecondaryCopies = {}

parentsOfSecondaryCopiesEachServer = {}

adjacencyListDestToSrces = {}
adjacencyListSrcToDestes = {}

weightThreshold = 80

no_of_nodes = 2
alpha_repartition = 0.2
gamma_repartition = 1.2

#for replication function
def makeCopy(src, dest):
	destServer = placementOfPrimaryCopies[dest]
	#MAKE A COPY OF SRC IN DESTSERVER, USE SCP HERE - NOT IMPL
	#EIKHANE WORKER GULIR MODDHEO CODING ER PART ACHE - NOT IMPL
	#WORKER GULI TE AR KI KI KAJ ACHE SEITA THIK KORTE HOBE - NOT IMPL
	#KI KI COPY KORBO, SEITA THIK KORTE HOBE - NOT IMPL
	#EIKHANE JE JINISHGULI COPY KORBO, SYNC EER SOMOY OI JINISH GULI I SYNC KORE RAKHTE HOBE - NOT IMPL

	#now importantly, data structure guli update kore felo
	if (destServer not in placementOfSecondaryCopies[src]):
		placementOfSecondaryCopies[src].append(destServer)
	if (destServer not in parentsOfSecondaryCopiesEachServer[src].keys()):
		parentsOfSecondaryCopiesEachServer[src][destServer] = []
		parentsOfSecondaryCopiesEachServer[src][destServer].append(dest)
	else:
		if (dest not in parentsOfSecondaryCopiesEachServer[src][destServer]):
			parentsOfSecondaryCopiesEachServer[src][destServer].append(dest)

#for replication function
def deleteCopy(src, dest):

	#now importantly, data structure guli update kore felo
	# placementOfSecondaryCopies[src].remove(destServer)
	destServer = placementOfPrimaryCopies[dest]
	if(dest in parentsOfSecondaryCopiesEachServer[src][destServer]):
		parentsOfSecondaryCopiesEachServer[src][destServer].remove(dest)
	if(len(parentsOfSecondaryCopiesEachServer[src][destServer])==0):
		placementOfSecondaryCopies[src].remove(destServer)

#for replication function
def eachIncrementalEdgeChecking(src, dest, weight):
	# if weight >= weightThreshold:
	# 	#IF ML EKHANE USE KORTE HOBE - NOT IMPLEMENTED
	# 	#AND ALSO CHECK FOR MAX, IF FULL THEN LRU ONUJAI DELETE APATOTO, PORE LAGLE LFU - NOT IMPLEMENTED
	# 	#can make a copy of src in the server of dest
	
	#eikhane case by case basis chinta korte hobe
	#EI SOB CASE E WORKER DERO JANATE HOBE JATE TARAO NECESSARY UPDATE KORE NEI - NOT IMPL

	#Case #1:
	srcServer = placementOfPrimaryCopies[src]
	destServer = placementOfPrimaryCopies[dest]
	if(srcServer == destServer):
		if(destServer in placementOfSecondaryCopies[src]):
			deleteCopy(src, dest)


	#Case #2:
	destServer_prev = placementOfPrimaryCopies_prev[dest]
	if(destServer_prev in placementOfSecondaryCopies[src]):
		deleteCopy(src, dest)

	#Case #3:
	if(srcServer != destServer):
		if(destServer in placementOfSecondaryCopies[src]):
			if(dest not in parentsOfSecondaryCopiesEachServer[src][destServer]):
				parentsOfSecondaryCopiesEachServer[src][destServer].append(dest)

	#Case #4:
	if weight >= weightThreshold:
# 	#IF ML EKHANE USE KORTE HOBE - NOT IMPLEMENTED
# 	#AND ALSO CHECK FOR MAX, IF FULL THEN LRU ONUJAI DELETE APATOTO, PORE LAGLE LFU - NOT IMPLEMENTED
# 	#can make a copy of src in the server of dest
		makeCopy(src, dest)


#ei function ta ki adou lagbe??
#for replication function
def initialEachEdgeChecking(src, dest, weight):
	if weight >= weightThreshold:
		#IF ML EKHANE USE KORTE HOBE - NOT IMPLEMENTED
		#AND ALSO CHECK FOR MAX, IF FULL THEN LRU ONUJAI DELETE APATOTO, PORE LAGLE LFU - NOT IMPLEMENTED
		#can make a copy of src in the server of dest
		makeCopy(src, dest)

def fennelLikeScoringFunctionRepartition(currNode, server):
	serverNeighborNo = 0
	#server e serverneighborno ber koro, directed je hishab rekho seita - not impl
	
	#apatoto khali dest->src er khetre src jodi ei server e primary hishebe thake taile count baraitesi
	#should cosnider also secondary hishebe thaka ?? - not impl

	currNodeAsDestAdjList = adjacencyListDestToSrces[currNode]
	for eachNode in currNodeAsDestAdjList:
		eachNodeWhichServer = placementOfPrimaryCopies[eachNode]
		if eachNodeWhichServer == server:
			serverNeighborNo = serverNeighborNo + 1

	totalServerNode = 0
	#ei server e total koyta node assigned ache seita totalservernode - not impl
	#loop through placementOfPrimatryCopies
	for key in placementOfPrimaryCopies:
		if(placementOfPrimaryCopies[key] == server):
			totalServerNode = totalServerNode + 1

	score_second_term = pow(totalServerNode, gamma_repartition - 1)
	score_second_term = alpha_repartition*(gamma_repartition/2)*score_second_term

	#currently score_val is focused on leopard only, our modified will implement - not impl
	score_val = serverNeighborNo - score_second_term
	return score_val


def whichServerThisNodeForRepartition(currNode):
	#see which server is best for repartition for the currNode acc. to a scoring function like fennel
	currNodeCurrPrimaryServer = placementOfPrimaryCopies[currNode]
	maxScore = fennelLikeScoringFunctionRepartition(currNode, currNodeCurrPrimaryServer)
	maxScoringServer = currNodeCurrPrimaryServer
	for server in range (1, no_of_servers + 1):
		if server == currNodeCurrPrimaryServer:
			continue
		currServerScore = fennelLikeScoringFunctionRepartition(currNode, server)
		if(currServerScore > maxScore):
			maxScore = currServerScore
			maxScoringServer = server

	if maxScoringServer == currNodeCurrPrimaryServer:
		dummy = 2
	else:
		placementOfPrimaryCopies_prev[currNode] = placementOfPrimaryCopies[currNode]
		placementOfPrimaryCopies[currNode] = maxScoringServer

		which_worker_server = placementOfPrimaryCopies_prev[currNode]
		to_send_string = 'REPT DEL '+str("%02d" %(currNode))
		c_list[which_worker_server-1].send(to_send_string.encode("utf-8"))

		which_worker_server = placementOfPrimaryCopies[currNode]
		to_send_string = 'REPT ADD '+str("%02d" %(currNode))
		c_list[which_worker_server-1].send(to_send_string.encode("utf-8"))

#ei function edgeAddForRepartition call korar aage edge er longetivity check korte hobe - not impl
def edgeAddForRepartition(srcNode, destNode):
	consideredNodesForRepartition = []
	consideredNodesForRepartition.append(srcNode)
	consideredNodesForRepartition.append(destNode)

	#srcNode er immediate srcHisebe connected nodes process
	currNode = srcNode
	currAdjList = adjacencyListDestToSrces[currNode]
	for eachNode in currAdjList:
		if eachNode not in consideredNodesForRepartition:
			consideredNodesForRepartition.append(eachNode)

	#srcNode er immediate destHisebe connected nodes process
	currNode = srcNode
	currAdjList = adjacencyListSrcToDestes[currNode]
	for eachNode in currAdjList:
		if eachNode not in consideredNodesForRepartition:
			consideredNodesForRepartition.append(eachNode)	
	#destNode er immediate srcHisebe connected nodes process
	currNode = destNode
	currAdjList = adjacencyListDestToSrces[currNode]
	for eachNode in currAdjList:
		if eachNode not in consideredNodesForRepartition:
			consideredNodesForRepartition.append(eachNode)
	#destNode er immediate destHisebe connected nodes process
	currNode = destNode
	currAdjList = adjacencyListSrcToDestes[currNode]
	for eachNode in currAdjList:
		if eachNode not in consideredNodesForRepartition:
			consideredNodesForRepartition.append(eachNode)

	for eachNode in consideredNodesForRepartition:
		whichServerThisNodeForRepartition(eachNode)

#the following 3 functions are dummy, not real communication
def fennelLikeScoringFunctionRepartition_dummy(currNode, server):
	serverNeighborNo = 0
	#server e serverneighborno ber koro, directed je hishab rekho seita - not impl
	
	#apatoto khali dest->src er khetre src jodi ei server e primary hishebe thake taile count baraitesi
	#should cosnider also secondary hishebe thaka ?? - not impl

	currNodeAsDestAdjList = adjacencyListDestToSrces[currNode]
	for eachNode in currNodeAsDestAdjList:
		eachNodeWhichServer = placementOfPrimaryCopies_dummy[eachNode]
		if eachNodeWhichServer == server:
			serverNeighborNo = serverNeighborNo + 1

	totalServerNode = 0
	#ei server e total koyta node assigned ache seita totalservernode - not impl
	#loop through placementOfPrimatryCopies
	for key in placementOfPrimatryCopies_dummy:
		if(placementOfPrimatryCopies_dummy[key] == server):
			totalServerNode = totalServerNode + 1

	score_second_term = pow(totalServerNode, gamma_repartition - 1)
	score_second_term = alpha_repartition*(gamma_repartition/2)*score_second_term

	#currently score_val is focused on leopard only, our modified will implement - not impl
	score_val = serverNeighborNo - score_second_term
	return score_val

def whichServerThisNodeForRepartition_dummy(currNode):
	#see which server is best for repartition for the currNode acc. to a scoring function like fennel
	currNodeCurrPrimaryServer = placementOfPrimaryCopies_dummy[currNode]
	maxScore = fennelLikeScoringFunctionRepartition_dummy(currNode, currNodeCurrPrimaryServer)
	maxScoringServer = currNodeCurrPrimaryServer
	for server in range (1, no_of_servers + 1):
		if server == currNodeCurrPrimaryServer:
			continue
		currServerScore = fennelLikeScoringFunctionRepartition_dummy(currNode, server)
		if(currServerScore > maxScore):
			maxScore = currServerScore
			maxScoringServer = server

	# placementOfPrimaryCopies_prev[currNode] = placementOfPrimaryCopies[currNode]
	placementOfPrimaryCopies_dummy[currNode] = maxScoringServer

def edgeAddForRepartition_dummy(srcNode, destNode):
	consideredNodesForRepartition = []
	consideredNodesForRepartition.append(srcNode)
	consideredNodesForRepartition.append(destNode)

	#srcNode er immediate srcHisebe connected nodes process
	currNode = srcNode
	currAdjList = adjacencyListDestToSrces[currNode]
	for eachNode in currAdjList:
		if eachNode not in consideredNodesForRepartition:
			consideredNodesForRepartition.append(eachNode)

	#srcNode er immediate destHisebe connected nodes process
	currNode = srcNode
	currAdjList = adjacencyListSrcToDestes[currNode]
	for eachNode in currAdjList:
		if eachNode not in consideredNodesForRepartition:
			consideredNodesForRepartition.append(eachNode)	
	#destNode er immediate srcHisebe connected nodes process
	currNode = destNode
	currAdjList = adjacencyListDestToSrces[currNode]
	for eachNode in currAdjList:
		if eachNode not in consideredNodesForRepartition:
			consideredNodesForRepartition.append(eachNode)
	#destNode er immediate destHisebe connected nodes process
	currNode = destNode
	currAdjList = adjacencyListSrcToDestes[currNode]
	for eachNode in currAdjList:
		if eachNode not in consideredNodesForRepartition:
			consideredNodesForRepartition.append(eachNode)

	for eachNode in consideredNodesForRepartition:
		whichServerThisNodeForRepartition(eachNode)

#following function is for edge life prediction - not impl
def predictLifeTimeOfThisEdge(srcNode, destNode):
	return 2


def ifProfitableRepartitionThisEdge(srcNode, destNode):

	#later del
	# return True

	totalCommunicationCostIfThisRepartitionNotPerf = 0 #not impl-done
	totalCommunicationCostIfThisRepartitionPerf = 0 #not impl-done
	migrationCost = 0 #not impl-done

	lifeTimeOfThisEdge = predictLifeTimeOfThisEdge(srcNode, destNode)

	#to calculate if perf we need to do some dummy simulation, no real communication
	placementOfPrimaryCopies_dummy = copy.deepcopy(placementOfPrimaryCopies)
	edgeAddForRepartition_dummy(srcNode, destNode)

	for currNode in range(1, no_of_nodes + 1):
		currNodeServer = placementOfPrimaryCopies[currNode]
		currNodeServer_dummy = placementOfPrimaryCopies_dummy[currNode]
		if(currNodeServer != currNodeServer_dummy):
			migrationCost = migrationCost + 2

	for currNode in range(1, no_of_nodes + 1):
		currNodeServer = placementOfPrimaryCopies_dummy[currNode]
		currNodeEdgeList = adjacencyListDestToSrces[currNode]
		for eachSrcNode in currNodeEdgeList:
			eachSrcNodeServer = placementOfPrimaryCopies_dummy[eachSrcNode]
			if currNodeServer != eachSrcNodeServer:
				totalCommunicationCostIfThisRepartitionPerf = totalCommunicationCostIfThisRepartitionPerf + 1

	for currNode in range(1, no_of_nodes + 1):
		currNodeServer = placementOfPrimaryCopies[currNode]
		currNodeEdgeList = adjacencyListDestToSrces[currNode]
		for eachSrcNode in currNodeEdgeList:
			eachSrcNodeServer = placementOfPrimaryCopies[eachSrcNode]
			if currNodeServer != eachSrcNodeServer:
				totalCommunicationCostIfThisRepartitionNotPerf = totalCommunicationCostIfThisRepartitionNotPerf + 1


	totalCommunicationCostIfThisRepartitionPerf = totalCommunicationCostIfThisRepartitionPerf * lifeTimeOfThisEdge
	totalCommunicationCostIfThisRepartitionNotPerf = totalCommunicationCostIfThisRepartitionNotPerf * lifeTimeOfThisEdge
	if(migrationCost + totalCommunicationCostIfThisRepartitionPerf < totalCommunicationCostIfThisRepartitionNotPerf):
		return True #meaning this edge regarding repartition is profitable
	else:
		return False

def jobsToDoWhenNewEdgeComes(srcNode, destNode):
	adjacencyListSrcToDestes[srcNode].append(destNode)
	adjacencyListDestToSrces[destNode].append(srcNode)

	if ifProfitableRepartitionThisEdge(srcNode, destNode):
		edgeAddForRepartition(srcNode, destNode)


for i in range (1, no_of_nodes + 1):
	placementOfPrimaryCopies[i] = i
	placementOfPrimaryCopies_prev[i] = i

	#only for replication below: 

	# placementOfSecondaryCopies[i] = []
	# parentsOfSecondaryCopiesEachServer[i] = {}

	adjacencyListDestToSrces[i] = []
	adjacencyListSrcToDestes[i] = []


jobsToDoWhenNewEdgeComes(1, 2)
#testing if central can send to worker servers
#testing delete notification in repartition

# which_worker_server = 1
# currNode = 1
# to_send_string = 'REPT DEL '+str("%02d" %(currNode))
# c_list[which_worker_server-1].send(to_send_string.encode("utf-8"))

#testing add notification in repartition
# which_worker_server = 1
# c_list[which_worker_server-1].send(b'REPT ADD 12')
while True:
	dummy = 2
