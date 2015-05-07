'''
Created on Apr 30, 2015

@author: Malcolm
'''

from collections import deque


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
            self.inCs = False  # only stay in cs for one step

        if self.wantCs:
            # if a node has the token, then it enters its CS
            if self.hasToken:
                # enter CS
                self.inCs = True
                self.wantCs = False
                self.registeredRequest = False
                pass

            # otherwise, to enter its CS a node i registers its request in its
            # local Q
            elif not self.registeredRequest:
                msg = (self.process.ID)
                self.Q.append(msg)
                self.registeredRequest = True

        # when a node j (that is not holding the token) has a non-empty request
        # Q,
        if (not self.hasToken) and (len(self.Q) != 0) and (not self.waitingForToken):
            # it sends a request to its holder unless j has already done so and
            # is waiting for the token
            # format (sender id, recipient id)
            msgBuf.put((self.process.ID, self.holder))
            self.waitingForToken = True

        # when the root receives a request,
        if (self.holder == self.process.ID) and (not self.inCs) and (len(self.Q) != 0):
            # it sends the token to the neighbor at the head of its local Q
            # after it has completed its own CS.
            recipient = self.Q.popleft()  # should I pop here or just read?
            msgBuf.put(("token", recipient))  # format ("token", recipient id)
            self.hasToken = False
            # then it sets it holder variable to that neighbor
            self.holder = recipient

        # upon receiving a token,
        if self.hasToken and (not self.inCs) and (len(self.Q) != 0):
            self.waitingForToken = False
            # a node j forwards it to the neighbor at the head of its local Q,
            # deletes its request from Q,
            recipient = self.Q.popleft()
            msgBuf.put(("token", recipient))  # format ("token", recipient id)
            self.hasToken = False
            # and sets its holder to that neighbor.
            self.holder = recipient
            # if there are pending requests in Q then j sends another request
            # to its holder
            if len(self.Q) != 0:
                # format (sender id, recipient id)
                msgBuf.put((self.process.ID, self.holder))
                self.waitingForToken = True  # do i need this here?
