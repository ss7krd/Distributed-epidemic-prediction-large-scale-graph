import threading

#JAR JEI GRAPH REGARDING UPDATE MSG FROM CENTRALIZED SEITA FIRST E PORLO AND NECESSARY UPDATE KORLO - NOT IMPL

#ei listen khali onno worker er request listen korbe - not impl
def listen():
	#SCP KORE SERVER ER PATHANO FILE TA PORTE THAKBE REGULARLY - NOT IMPL
	#THAT MEANS THAT WORKER SCP PATHABE NA, BUT AKTA SPECIFIC FILE CONTINUOUS READ KORTE THAKBE
	#??DIFF MESSAGE ER JONNO DIFF KAJ - NOT IMPL
	#loop er vitor ei func er processing chalate hobe - not impl
	message = ""
	if(message == ""):
		#SCP KORE DATA PATHABE EI WORKER JEI WORKER REQUEST KORTSE TAKE - NOT IMPL

#ei  thread ei worker er main processing korbe - not impl
#onno worker er data lagle oi worker ke scp korbe - not impl
def processing():
	#loop er vitor ei func er processing chalate hobe - not impl


#main function below:
t1 = threading.Thread(target=listen) 
t2 = threading.Thread(target=processing) 

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

