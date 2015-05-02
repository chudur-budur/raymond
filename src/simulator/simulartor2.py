'''
Created on Apr 30, 2015

@author: Malcolm
'''

import Queue
from collections import deque
import networkx

import raymonds
import evoprog
import treeParser


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
    

if __name__ == "__main__":
    
    testTree = '''
 (progn2 (if (not (and (nand is-q-empty has-token)
     (and is-waiting-for-token is-holder))) (progn2
     (progn2 (send-req-to holder) (if is-regreq
         enter-cs)) (progn2 (send-req-to holder) (send-req-to
     holder)))) (progn2 (progn2 (send-token-to
     holder) (if-else (and has-token is-holder)
     (if-else is-incs register-req-q enter-cs)
     (if is-holder enter-cs))) (if (or (nor is-incs
     is-q-empty) (and want-cs is-incs)) (send-req-to
     holder))))
    '''
    
    testTree = """(progn2
    (if is-incs (set-incs false))
    (progn2
        (if-else want-cs 
            (if has-token (enter-cs))
            (if (not is-regreq (register-req-q))))
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
    
    programTree = (treeParser.Parser()).parse_tree(testTree)
    
    
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
    p1.set_program(evoprog.Evoprog(programTree))
    p2.set_program(evoprog.Evoprog(programTree))
    p3.set_program(evoprog.Evoprog(programTree))    
    
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
    T = 10 # the number of steps to run the simulation
    
    # run the simulation
    print "start"
    
    for i in range(T):
        print "step", i
        
        # for testing. make another process want the CS...
        if i == 1:
            p2.program.wantCs = True
        
        # tell who has the token
        for p in processList:
            if p.program.hasToken:
                print p.ID, "has token"
        
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
            if msg[0] == "token":
                processList[msg[1]-1].program.hasToken = True
            else:
                processList[msg[1]-1].program.Q.append(msg[0])
        
        print
    
    print "mutual exclusion penaly", mePen / (T*3)
    print "progress penalty", progPen / (T*3)
    
