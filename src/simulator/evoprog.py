'''
Created on Apr 30, 2015

@author: Malcolm
'''

from collections import deque

import parser


class Evoprog:

    def __init__(self, programTree):
        self.programTree = programTree
        self.executionDict = {}
        
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
        # go down the program tree and execute instructions
        
        currNode = self.programTree
        
        
        
        
        
        
        pass





if __name__ == "__main__.py":
    
    testTree = '''
    (if in-cs (set-cs false))
    (if (not want-cs) 
        (if has-token (progn
            (set-cs true)
            (set-want-cs false)
            (set-reg-req false)
            (pass))))
    '''
    
    programTree = parser.Parser().parse_tree(testTree)
    
    
    
    
    pass





        