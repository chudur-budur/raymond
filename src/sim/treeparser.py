'''
Created on Apr 30, 2015

@author: Malcolm
'''


'''
A node in a parsed s-exp tree
'''


class Node:

    def __init__(self):
        self.head = None
        self.children = []
        self.parent = None

    def __str__(self):
        return str(self.head) + str(self.children)

    def __repr__(self):
        return str(self.head) + str(self.children)

    def is_leaf():
        if self.children:
            return false
        else:
            return true

'''
Parse a GP tree and put it into a tree structure
'''


class Parser:

    def __init__(self):
        pass

    def parse_sexp(self, sexp):
        # flatten the string
        sexp = " ".join(sexp.split())
        sexp = sexp.replace("(", "( ")
        sexp = sexp.replace(")", " )")

        tokens = sexp.split()

        root = Node()
        root.head = "root"
        currNode = root
        prevItem = None

        for item in tokens:
            if item == "(":
                # new node
                newNode = Node()
                newNode.parent = currNode
                # add the new node as an argument (child) of the current node
                currNode.children.append(newNode)
                currNode = newNode

            elif item != "(" and item != ")" and prevItem == "(":
                # head
                currNode.head = item

            elif item != "(" and item != ")" and prevItem != "(":
                # argument
                newNode = Node()
                newNode.head = item
                currNode.children.append(newNode)

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

    testTree = "(* (+ a b) (# (- x y) (+ p q) (% u v)))"

    parser = Parser()
    tree = parser.parse_sexp(testTree)
    print tree

    print "finished"

    pass
