'''
Created on Apr 30, 2015

@author: Malcolm
'''

import Queue
# import matplotlib.pyplot as plt
# import networkx as nx
import random

import raymonds
import executor
import treeparser


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

    def __init__(self, seed=0, N=10, T=100, wantCsRate=0.1,
                 meFitWeight=0.5, progFitWeight=0.25, servedFitWeight=0.25):
        self.seed = seed
        self.N = N
        self.T = T
        self.wantCsRate = wantCsRate
        self.meFitWeight = meFitWeight
        self.progFitWeight = progFitWeight
        self.servedFitWeight = servedFitWeight
        random.seed(self.seed)

    def set_params(self, lst):
        if lst:
            self.seed = lst[0]
            self.N = lst[1]
            self.T = lst[2]
            self.wantCsRate = lst[3]
            self.meFitWeight = lst[4]
            self.progFitWeight = lst[5]
            self.servedFitWeight = lst[6]
        else:
            self.seed = 0
            self.N = 10
            self.T = 100
            self.wantCsRate = 0.1
            self.meFitWeight = 0.5
            self.progFitWeight = 0.25
            self.servedFitWeight = 0.25
        random.seed(self.seed)

    def run(self, treeString):
        programTree = (treeparser.Parser()).parse_sexp(treeString)

        # generate a  tree
        # N is number of processes
        B = 2  # branching factor

        # create the root which starts with the token
        root = Process(1)
        root.set_program(executor.Executor(programTree))
        root.program.hasToken = True
        root.program.holder = root.program.process
        levels = [[root]]

        numNodes = 1
        level = 1
        processList = [root]

        while numNodes < self.N:
            newLevel = []
            for l in range(level):
                for b in range(B):
                    if numNodes == self.N:
                        break

                    newProcess = Process(numNodes + 1)
                    newProcess.set_program(executor.Executor(programTree))

                    # set the holder to the parent
                    holder = levels[level - 1][l].ID
                    newProcess.program.holder = holder
                    newLevel.append(newProcess)

                    processList.append(newProcess)
                    numNodes += 1
                    pass

            levels.append(newLevel)
            level += 1

        # start the simulation
        #

        sendBuf = Queue.Queue()

        # variables for measuring fitness
        self.meFitWeight = 0.8
        progFitWeight = 1 - self.meFitWeight
        mePen = 0.0  # increment when more than one process enters CS
        progPen = 0.0  # increment for each waiting process
        totalServed = 0.0

        # run the simulation
        # print "start"

        for i in range(self.T):
            # print "step", i
            # make some processes want to enter the CS
            for p in processList:
                if random.random() < self.wantCsRate:
                    p.program.wantCs = True
            # calculate the penalties
            numInCs = 0
            numWaiting = 0
            numServed = 0
            for p in processList:
                numInCs += p.program.inCs
                numWaiting += p.program.wantCs
                numServed += p.program.csCount

            if (numInCs > 1):
                mePen += numInCs
            progPen += numWaiting
            totalServed += (1.0 * numServed)

            # step
            for p in processList:
                p.step(sendBuf)

            # deliver messages
            while not sendBuf.empty():
                msg = sendBuf.get()
                if msg[1] != -1:
                    if msg[0] == "token":
                        processList[msg[1] - 1].program.hasToken = True
                    else:
                        processList[msg[1] - 1].program.Q.append(msg[0])

        meFitness = 1 - mePen / (self.T * self.N)
        servedFitness = totalServed / (self.N * self.T)
        progFitness = 1 - progPen / (self.T * self.N)
        combinedFitness = self.meFitWeight * meFitness + \
            self.servedFitWeight * servedFitness + progFitWeight * progFitness

        flst = [meFitness, progFitness, servedFitness, combinedFitness]
        return flst
