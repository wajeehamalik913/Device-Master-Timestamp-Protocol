from mpi4py import MPI
import numpy
from random import randrange
import time

message = 100 ## message that floods between nodes
destination = 3 ##Destination node fixed temporarily

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()
c=0

if (rank == 0): ## Source Node
	 
	list = [] ## contains neighbour nodes

	## opens and reads the file that contains all
        ## the information of nodes and their neighbours (topology)
	
	file1 = open('s.txt', 'r')
	Lines = file1.readlines()
	count = 0
	
	# Strips the newline character
	
	for line in Lines:
		count += 1
		x = line.split(',')

		## Stores information of neighbouring nodes
		
		if (x[0] == str(rank)):
			for i in range(len(x)-1):
				list.append(x[i+1])
			break
		

	## printing node id and its neighbours
	print("I am process (source):", rank)
	print("My neighbours are:")
	for i in range(len(list)):
		print(list[i])

	## sending message to all the neighbouring nodes.
		
	for i in range(len(list)):
		comm.send(message, dest=int(list[i]))
		print(rank ,"sending message to :", list[i])

else:
	list = []

	## opens and reads the file that contains all
        ## the information of nodes and their neighbours
	
	file1 = open('s.txt', 'r')
	Lines = file1.readlines()
	count = 0
	
	# Strips the newline character

	for line in Lines:
		count += 1
		x = line.split(',')
                
                ## Stores information of neighbouring nodes
		
		if (x[0] == str(rank)):
			#print(rank)
			for i in range(len(x)-1):
				list.append(x[i+1])
			
			break

	## printing node id and its neighbours
		
	print("I am process:", rank)
	print("My neighbours are:")
	for i in range(len(list)):
		print(list[i])

        ## Receiving message from source/parent node
		
	status = MPI.Status()
	data = comm.recv(source=MPI.ANY_SOURCE, status=status)
	
	## when destination is reached it displays the
	## destination reached message
	
	if (rank == destination):
	    print("Destination received message")
	    
	print(rank , "got message from:", status.Get_source())

        ## if destination is not reached message will continue flooding and
	## node receiving message will send message to its neighbouring nodes.
	
	for i in range(len(list)):
		if (list[i] != str(status.Get_source())):
			comm.send(message, dest=int(list[i]))
			print(rank ,"sending message to :", list[i])
