'''
Created on Mar 19, 2015

@author: Malcolm
'''


import Queue
from collections import deque
import networkx


class Process:
	def __init__(self, ID):
		self.ID = ID
		self.neighbors = []
	
	def add_neighbor(self, neighbor):
		self.neighbors.append(neighbor)
	
	def set_program(self, program):
		self.program = program
		self.program.set_process(self)
	
	def step(self, sendBuf):
		self.program.run(sendBuf)
	
	#def __str__(self):
	#	return str(self.ID)
	
	#def __repr__(self):
	#	return str(self.ID)

class Raymonds:
	def __init__(self):
		self.wantCs = False
		
		self.Q = deque()
		self.holder = None
		self.hasToken = False
		self.waitingForToken = False
		self.registeredRequest = False
		self.inCs = False
	
	def set_process(self, process):
		self.process = process
	
	def set_want_cs(self, wantCs):
		self.wantCs = wantCs
	
	def run(self, msgBuf):
		
		if self.inCs:
			self.inCs = False # only stay in cs for one step
		
		if self.wantCs:
			# if a node has the token, then it enters its CS
			if self.hasToken:
				# enter CS
				self.inCs = True
				self.wantCs = False
				self.registeredRequest = False
				pass
			
			# otherwise, to enter its CS a node i registers its request in its local Q
			elif not self.registeredRequest:
				msg = (self.process.ID)
				self.Q.append(msg)
				self.registeredRequest = True
		
		# when a node j (that is not holding the token) has a non-empty request Q,
		if (not self.hasToken)  and ( len(self.Q) != 0) and (not self.waitingForToken):
			# it sends a request to its holder unless j has already done so and is waiting for the token
			msgBuf.put((self.process.ID, self.holder)) # format (sender id, recipient id)
			self.waitingForToken = True
		
		# when the root receives a request,
		if (self.holder == self.process.ID) and (not self.inCs) and (len(self.Q) != 0):
			# it sends the token to the neighbor at the head of its local Q after it has completed its own CS.
			recipient = self.Q.popleft() # should I pop here or just read?
			msgBuf.put(("token", recipient)) # format ("token", recipient id)
			self.hasToken = False
			# then it sets it holder variable to that neighbor
			self.holder = recipient
		
		# upon receiving a token, 
		if self.hasToken and (not self.inCs) and (len(self.Q) != 0):
			self.waitingForToken = False
			# a node j forwards it to the neighbor at the head of its local Q,
			# deletes its request from Q, 
			recipient = self.Q.popleft()
			msgBuf.put(("token", recipient)) # format ("token", recipient id)
			self.hasToken = False
			# and sets its holder to that neighbor.
			self.holder = recipient
			# if there are pending requests in Q then j sends another request to its holder
			if len(self.Q) != 0:
				msgBuf.put((self.process.ID, self.holder)) # format (sender id, recipient id)
				self.waitingForToken = True # do i need this here?
		
			
		# if a node has the token, then it enters its CS. 
		# otherwise, to enter its CS a node i registers its request in its local Q
		
		
		# when a node j (that is not holding the token) has a non-empty request Q,
		# it sends a request to its holder unless j has already done so and is waiting for the token
		
		
		# when the root receives a request, 
		# it sends the token to the neighbor at the head of its local Q after it has completed its own CS.
		# then it sets its holder variable to that neighbor
		
		
		# upon receiving a token, a node j forwards it to the neighbor at the head of its local Q, 
		# deletes its request from Q, and sets its holder to that neighbor.
		# if there are pending requests in Q then j sends another request to its holder

class EvoProgram:
	
	def __init__(self):
		pass
	
	
	
	

if __name__ == "__main__":
	
	# create a tree
	p1 = Process(1)
	p2 = Process(2)
	p3 = Process(3)
	
	# add edge between p1 and p2
	p1.add_neighbor(p2)
	p2.add_neighbor(p1)
	
	# add edge between p1 and p3
	p1.add_neighbor(p3)	
	p3.add_neighbor(p1)
	
	# set the program
	p1.set_program(Raymonds())
	p2.set_program(Raymonds())
	p3.set_program(Raymonds())	
	
	# initialize the simulation
	
	# create a token and set the holders
	# p2 <- p1 <- p3, p2 has token
	p2.program.hasToken = True
	p2.program.holder = p2.ID
	p1.program.holder = p2.ID
	p3.program.holder = p1.ID
	
	p3.program.wantCs = True
	
	processList = [p1, p2, p3]
	sendBuf = Queue.Queue()
	
	# run the simulation
	print "start"
	
	for i in range(10):
		if i == 1:
			p2.program.wantCs = True
			pass
		print 
		print "step", i
		
		for p in processList:
			if p.program.hasToken:
				print p.ID, "has token"
		
		for p in processList:
			p.step(sendBuf)
		
		# deliver messages
		while not sendBuf.empty():
			msg = sendBuf.get()
			if msg[0] == "token":
				processList[msg[1]-1].program.hasToken = True
			else:
				processList[msg[1]-1].program.Q.append(msg[0])
	

	
	
	
	
	
	
	
	
	