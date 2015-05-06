'''
Created on Apr 30, 2015

@author: Malcolm
'''


class Node:

    operator = None
    operands = None
    
    def __init__(self):
        self.operator = None
        self.operands = []
        self.parent = None
    
    def __str__(self):
        return str(self.operator) 
    
    def __repr__(self):
        return str(self.operator) 
        
class Parser:
    '''
    Parse a GP tree and put it into a tree structure
    '''
    
    def __init__(self):
        pass

    def flatten(self, treeString):
        # flatten the string
        treeString = " ".join(treeString.split())
        treeString = treeString.replace("(","( ")
        treeString = treeString.replace(")"," )")
        
        processed = treeString.split()
        return processed

    def pop_until(self, stack, end):
        popped = ""
        lst = []
        while (popped != end):
            popped = stack.pop(0)
            lst.append(popped)
    
        lst.pop()
        return lst

    def do_parse(self, treeString):
        tokenList = self.flatten(treeString)
        print tokenList

        stack = []
        stack.append(tokenList[0])
        print stack

        i = 1
        while (not stack):
            if tokenList[i] == ")":
               popped = self.pop_until(stack, "(")               
               node = Node()
               node.operator = popped.pop(0)
               node.operands = popped 
            else
                stack.append(tokenList[i])
    
    def parse_tree(self, treeString):
        # flatten the string
        treeString = " ".join(treeString.split())
        treeString = treeString.replace("(","( ")
        treeString = treeString.replace(")"," )")
        
        processed = treeString.split()
        print processed
        
        root = Node()
        root.operator = "root"
        currNode = root
        prevItem = None
        
        for item in processed:
            if item == "(":
                # new node
                newNode = Node()
                newNode.parent = currNode
                # add the new node as an argument (child) of the current node
                currNode.operands.append(newNode) 
                currNode = newNode
                
            elif item != "(" and item != ")" and prevItem == "(":
                # operator
                currNode.operator = item
            
            elif item != "(" and item != ")" and prevItem != "(":
                # argument
                newNode = Node()
                newNode.operator = item
                currNode.operands.append(newNode)
            
            elif item == ")":
                # finished node
                currNode = currNode.parent
            
            prevItem = item
            
        return root

    def __str__(self):
        return str(root)

if __name__ == "__main__":
    # test if the parser works...
    
    '''
    testTree = """
    (progn2
        (if in-cs (set-cs false))
        (if want-cs 
            (if has-token 
                (progn2
                    (set-cs true)
                    (progn2
                        (set-want-cs false)
                        (set-reg-req false))))))
    """
    '''

    '''
    testTree = """
 (if-else (not in-cs) (if-else (not in-cs)
     set-cs-true (progn2 set-cs-true set-cs-true))
     (if-else (not in-cs) (if-else in-cs set-cs-true
         set-cs-true) (progn2 set-cs-true set-cs-true)))
"""
'''
    
    '''
    testTree = """
 (progn2 (if-else (and (not (and in-cs in-cs))
     (not (not in-cs))) (if-else (and (and in-cs
     in-cs) (not in-cs)) (set-cs true) (if (and
     in-cs in-cs) (set-cs true))) (set-cs false))
     (if-else (not (not (not (and (not in-cs)
         (not in-cs))))) (progn2 (progn2 (if-else
         in-cs (no-op) (no-op)) (if-else in-cs (no-op)
         (no-op))) (progn2 (progn2 (no-op) (no-op))
         (progn2 (no-op) (no-op)))) (set-cs true)))
"""
'''

    testTree = "(- (+ x y) (* a b))"

    parser = Parser()
    stack = ["a", "b", "c", ")", "d"]
    stack.append("e")
    print "stack: " + str(stack)
    popped = parser.pop_until(stack, ")")
    print "popped: " + str(popped)
    print "stack after pop: " + str(stack)

    # parser = Parser()
    # tree = parser.parse_tree(testTree)
    # print tree
    # tree = parser.do_parse(testTree)
    # print tree
    # print "finished"
    
    pass
    
    
    
    
    
    
        
