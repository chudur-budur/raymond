'''
Created on Apr 30, 2015

@author: Malcolm
'''

import Queue
#from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import random

import raymonds
import evoprog
import treeParser


class Process:
    def __init__(self, ID):
        self.ID = ID
        self.neighbors = []
    
    def set_program(self, program):
        self.program = program
        self.program.set_process(self)
    
    def step(self, sendBuf):
        self.program.run(sendBuf)

class Simulator:
    def __init__(self,seed=0,T=100,wantCsRate=0.1):
        self.seed = seed
        self.T = T
        self.wantCsRate = wantCsRate   
        random.seed(self.seed)
    
    
    def run(self,treeString,N=10):
        
        programTree = (treeParser.Parser()).parse_tree(treeString)
        
        # generate a  tree
        # N is number of processes
        B = 2 # branching factor
        
        # create the root which starts with the token
        root = Process(1)
        root.set_program(evoprog.Evoprog(programTree))
        root.program.hasToken = True
        levels = [[root]]
        
        numNodes = 1
        level = 1
        processList = []
        
        while numNodes < N:
            newLevel = []
            for l in range(level):
                for b in range(B):
                    if numNodes == N:
                        break
                        
                    newProcess = Process(numNodes+1)
                    newProcess.set_program(evoprog.Evoprog(programTree))
                    
                    # set the holder to the parent
                    newProcess.program.holder = levels[level-1][l].ID
                    newLevel.append(newProcess)
                    
                    processList.append(newProcess)
                    numNodes += 1
                    
            levels.append(newLevel)
            level += 1
        
        
        # start the simulation
        #
        
        sendBuf = Queue.Queue()
        
        # variables for measuring fitness
        meFitWeight = 0.8
        progFitWeight = 1 - meFitWeight
        mePen = 0.0 # increment when more than one process enters CS
        progPen = 0.0 # increment for each waiting process
        
        # run the simulation
        #print "start"
        
        for i in range(self.T):
            #print "step", i
            
            # make some processes want to enter the CS
            for p in processList:
                if random.random() < self.wantCsRate:
                    p.program.wantCs = True
            
            # calculate the penalties
            numInCs = 0
            numWaiting = 0
            for p in processList:
                numInCs += p.program.inCs
                numWaiting += p.program.wantCs
            if numInCs > 1:
                mePen += numInCs
            progPen += numWaiting
            
            # step
            for p in processList:
                p.step(sendBuf)
            
            # deliver messages
            while not sendBuf.empty():
                msg = sendBuf.get()
                if msg[1] != -1:
                    if msg[0] == "token":
                        processList[msg[1]-1].program.hasToken = True
                    else:
                        processList[msg[1]-1].program.Q.append(msg[0])
            
            #print 
        
        meFitness = 1 - mePen / (self.T*N)
        progFitness = 1 - progPen / (self.T*N)
        combinedFitness = meFitWeight*meFitness + progFitWeight*progFitness
        
        print "mutual exclusion fitness", meFitness
        print "progress fitness", progFitness
        print "combined fitness", combinedFitness
        
        return combinedFitness
    
    
    def run_old(self,treeString):
        """
        programTree = (treeParser.Parser()).parse_tree(treeString)
        
        # create a network of processes
        p1 = Process(1)
        p2 = Process(2)
        p3 = Process(3)
        
        
        # set the program
        p1.set_program(evoprog.Evoprog(programTree))
        p2.set_program(evoprog.Evoprog(programTree))
        p3.set_program(evoprog.Evoprog(programTree))  
        
        #p1.set_program(raymonds.Raymonds())
        #p2.set_program(raymonds.Raymonds())
        #p3.set_program(raymonds.Raymonds())  
        
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
        
        # variables for measuring fitness
        mePen = 0.0 # increment when more than one process enters CS
        progPen = 0.0 # increment for each waiting process
        
        # run the simulation
        #print "start"
        
        for i in range(self.T):
            #print "step", i
            
            # make some processes want to enter the CS
            for p in processList:
                if random.random() < self.wantCsRate:
                    p.program.wantCs = True
            
            # calculate the penalties
            numInCs = 0
            numWaiting = 0
            for p in processList:
                numInCs += p.program.inCs
                numWaiting += p.program.wantCs
            if numInCs > 1:
                mePen += numInCs
            progPen += numWaiting
            
            # step
            for p in processList:
                p.step(sendBuf)
            
            # deliver messages
            while not sendBuf.empty():
                msg = sendBuf.get()
                if msg[1] != -1:
                    if msg[0] == "token":
                        processList[msg[1]-1].program.hasToken = True
                    else:
                        processList[msg[1]-1].program.Q.append(msg[0])
            
            #print 
        
        meFitness = 1 - mePen / (self.T*3)
        progFitness = 1 - progPen / (self.T*3)
        combinedFitness = 0.8*meFitness + 0.2*progFitness
        
        print "mutual exclusion fitness", meFitness
        print "progress fitness", progFitness
        print "combined fitness", combinedFitness
        
        return combinedFitness
    """
    pass
    

if __name__ == "__main__":
    # test the simulator
    
    # code for raymond's algorithm
    testTree = """(progn2
    (enter-cs-temp)
    (progn2
        (if-else want-cs 
            (if has-token (enter-cs))
            (if (not is-regreq) (register-req-q)))
        (progn2
            (if (and (and (not has-token) (not is-q-empty)) is-waiting-for-token)
                (send-req-to holder)
                (progn2
                    (if (and (and is-holder (not is-incs)) (not is-q-empty))
                            (send-token-to q-top))
                    (if (and (and has-token (not is-incs) (not is-q-empty)))
                        (progn2
                            (send-token-to q-top)
                            (if (not is-q-empty)
                                    (send-req-to holder)))))))))
                                    """

    
    sim = Simulator()
    fitness = sim.run(testTree)
    
    print "finished"
    

