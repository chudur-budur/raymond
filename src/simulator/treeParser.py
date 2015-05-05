'''
Created on Apr 30, 2015

@author: Malcolm
'''


class Node:
    
    def __init__(self):
        self.instruction = None
        self.arguments = []
        #self.children = []
        self.parent = None
    
    """
    def __str__(self):
        return "("+str(self.instruction)+","+str(self.arguments)+")"
    
    def __repr__(self):
        return "("+str(self.instruction)+","+str(self.arguments)+")"
    """
        
class Parser:
    '''
    Parse a GP tree and put it into a tree structure
    '''
    
    def __init__(self):
        pass
    
    def parse_tree(self, treeString):
        # flatten the string
        treeString = " ".join(treeString.split())
        treeString = treeString.replace("(","( ")
        treeString = treeString.replace(")"," )")
        
        processed = treeString.split()
        
        root = Node()
        root.instruction = "root"
        currNode = root
        prevItem = None
        
        for item in processed:
            if item == "(":
                # new node
                newNode = Node()
                newNode.parent = currNode
                currNode.arguments.append(newNode) # add the new node as an argument (child) of the current node
                currNode = newNode
                
            elif item != "(" and item != ")" and prevItem == "(":
                # instruction
                currNode.instruction = item
            
            elif item != "(" and item != ")" and prevItem != "(":
                # argument
                newNode = Node()
                newNode.instruction = item
                currNode.arguments.append(newNode)
            
            elif item == ")":
                # finished node
                currNode = currNode.parent
            
            prevItem = item
            
        return root


if __name__ == "__main__":
    # test if the parser works...
    
    testTree = '''
    (if in-cs (set-cs false))
    (if want-cs 
        (if has-token (progn
            (set-cs true)
            (set-want-cs false)
            (set-reg-req false)
            (pass))))
    '''
    treeTest = '''
 (if-else (not in-cs) (if-else (not in-cs)
     set-cs-true (progn2 set-cs-true set-cs-true))
     (if-else (not in-cs) (if-else in-cs set-cs-true
         set-cs-true) (progn2 set-cs-true set-cs-true)))
'''
    
    treeTest = '''
 (progn2 (if-else (and (not (and in-cs in-cs))
     (not (not in-cs))) (if-else (and (and in-cs
     in-cs) (not in-cs)) (set-cs true) (if (and
     in-cs in-cs) (set-cs true))) (set-cs false))
     (if-else (not (not (not (and (not in-cs)
         (not in-cs))))) (progn2 (progn2 (if-else
         in-cs (no-op) (no-op)) (if-else in-cs (no-op)
         (no-op))) (progn2 (progn2 (no-op) (no-op))
         (progn2 (no-op) (no-op)))) (set-cs true)))
'''
    


    parser = Parser()
    tree = parser.parse_tree(testTree)
    print tree
    print "finished"
    
    pass
    
    
    
    
    
    
        