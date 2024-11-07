# replication implementation

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
placementOfPrimaryCopies_prev = {}

placementOfSecondaryCopies = {}

parentsOfSecondaryCopiesEachServer = {}
weightThreshold = 80
no_of_servers = 8
no_of_nodes = 8

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

def deleteCopy(src, dest):

	#now importantly, data structure guli update kore felo
	# placementOfSecondaryCopies[src].remove(destServer)
	destServer = placementOfPrimaryCopies[dest]
	if(dest in parentsOfSecondaryCopiesEachServer[src][destServer])
		parentsOfSecondaryCopiesEachServer[src][destServer].remove(dest)
	if(len(parentsOfSecondaryCopiesEachServer[src][destServer])==0):
		placementOfSecondaryCopies[src].remove(destServer)


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
def initialEachEdgeChecking(src, dest, weight):
	if weight >= weightThreshold:
		#IF ML EKHANE USE KORTE HOBE - NOT IMPLEMENTED
		#AND ALSO CHECK FOR MAX, IF FULL THEN LRU ONUJAI DELETE APATOTO, PORE LAGLE LFU - NOT IMPLEMENTED
		#can make a copy of src in the server of dest
		makeCopy(src, dest)



for i in range (1, no_of_nodes + 1):
	placementOfPrimaryCopies[i] = i
	placementOfPrimaryCopies_prev[i] = i

	placementOfSecondaryCopies[i] = []
	parentsOfSecondaryCopiesEachServer[i] = {}