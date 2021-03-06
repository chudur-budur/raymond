'''
Created on Apr 30, 2015

@author: Malcolm
'''

from collections import deque
import Queue

import treeparser


class Executor:

    def __init__(self, programTree):
        self.programTree = programTree
        self.programTree.head = "progn2"

        self.wantCs = False

        self.Q = deque()
        self.holder = None
        self.hasToken = False
        self.waitingForToken = False
        self.registeredRequest = False
        self.inCs = False
        self.csCount = 0

        self.instructions = {
            "if": self.instr_if,
            "if-else": self.instr_if_else,
            "not": self.instr_not,
            "and": self.instr_and,
            "or": self.instr_or,
            "nand": self.instr_nand,
            "nor": self.instr_nor,
            "true": self.instr_true,
            "false": self.instr_false,
            "progn2": self.instr_progn2,
            "is-incs": self.instr_is_incs,
            "has-token": self.instr_has_token,
            "is-regreq": self.instr_is_regreq,
            "is-q-empty": self.instr_is_q_empty,
            "is-waiting-for-token": self.instr_is_waiting_for_token,
            "is-holder": self.instr_is_holder,
            "want-cs": self.instr_want_cs,
            "enter-cs": self.instr_enter_cs,
            "send-req-to": self.instr_send_req_to,
            "register-req-q": self.instr_register_req_q,
            "send-token-to": self.instr_send_token_to,
            "no-op": self.instr_no_op,
            "q-top": self.instr_q_top,
            "holder": self.instr_holder,
            "exit-cs": self.instr_exit_cs
        }

    def set_process(self, process):
        self.process = process.ID

    def set_want_cs(self, wantCs):
        self.wantCs = wantCs

    def run(self, msgBuf):
        # go down the program tree (dfs) and execute self.instructions
        self.instructions[self.programTree.head](
            self.programTree.children, msgBuf)

    ##########################################################################
    # Instruction definitions
    ##########################################################################

    # conditionals
    #

    def instr_if(self, args, msgBuf):
        if self.instructions[args[0].head](args[0].children, msgBuf):
            self.instructions[args[1].head](args[1].children, msgBuf)

    def instr_if_else(self, args, msgBuf):
        if self.instructions[args[0].head](args[0].children, msgBuf):
            self.instructions[args[1].head](args[1].children, msgBuf)
        else:
            self.instructions[args[2].head](args[2].children, msgBuf)

    # logic gates
    #

    def instr_not(self, args, msgBuf):
        return not self.instructions[args[0].head](args[0].children, msgBuf)

    def instr_and(self, args, msgBuf):
        for node in args:
            if not self.instructions[node.head](node.children, msgBuf):
                return False
        return True

    def instr_or(self, args, msgBuf):
        for node in args:
            if self.instructions[node.head](node.children, msgBuf):
                return True
        return False

    def instr_nand(self, args, msgBuf):
        return not self.instr_and(args, msgBuf)

    def instr_nor(self, args, msgBuf):
        return not self.instr_or(args, msgBuf)

    def instr_true(self, args, msgBuf):
        return True

    def instr_false(self, args, msgBuf):
        return False

    # branching
    #

    def instr_progn2(self, args, msgBuf):
        for node in args:
            self.instructions[node.head](node.children, msgBuf)

    # sensors
    #

    def instr_is_incs(self, args, msgBuf):
        return self.inCs

    def instr_has_token(self, args, msgBuf):
        return self.hasToken

    def instr_is_regreq(self, args, msgBuf):
        return self.registeredRequest

    def instr_is_q_empty(self, args, msgBuf):
        return len(self.Q) == 0

    def instr_is_waiting_for_token(self, args, msgBuf):
        return self.waitingForToken

    def instr_is_holder(self, args, msgBuf):
        return self.holder == self.process

    def instr_want_cs(self, args, msgBuf):
        return self.wantCs

    # actions
    #

    def instr_enter_cs(self, args, msgBuf):
        self.inCs = True
        self.wantCs = False
        self.registeredRequest = False
        self.csCount = self.csCount + 1

    def instr_exit_cs(self, args, msgBuf):
        if self.inCs:
            self.inCs = False

    def instr_send_req_to(self, args, msgBuf):
        recipient = self.instructions[
            args[0].head](args[0].children, msgBuf)
        msgBuf.put((self.process, recipient))
        self.waitingForToken = True

    def instr_register_req_q(self, args, msgBuf):
        msg = self.process
        self.Q.append(msg)
        self.registeredRequest = True

    def instr_send_token_to(self, args, msgBuf):
        recipient = self.instructions[
            args[0].head](args[0].children, msgBuf)
        msgBuf.put(("token", recipient))
        self.holder = recipient
        self.hasToken = False

    def instr_no_op(self, args, msgBuf):
        pass

    # node type
    #

    def instr_q_top(self, args, msgBuf):
        if len(self.Q) != 0:
            return self.Q.popleft()
        else:
            return -1

    def instr_holder(self, args, msgBuf):
        return self.holder


if __name__ == "__main__":

    testTree = """
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
    """

    programTree = (treeparser.Parser()).parse_sexp(testTree)
    program = Executor(programTree)

    print programTree

    sendBuf = Queue.Queue()
    program.run(sendBuf)

    print "finished"
    pass
