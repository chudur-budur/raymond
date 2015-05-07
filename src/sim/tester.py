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
import simulator

if __name__ == "__main__":
    # test the simulator

    # code for raymond's algorithm
    raymondTree = """(progn2
    (exit-cs)
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

    testTree = """
(progn2 
 (if (and (and is-waiting-for-token is-regreq) (not is-regreq)) 
     (send-token-to holder)) 
 (progn2 
  (if-else (and want-cs is-regreq)
	   (progn2 
	    (if (and (and is-waiting-for-token is-regreq) (not is-regreq)) 
		(send-token-to holder)) 
	    (if-else (not (or (not is-regreq) has-token)) 
		     (send-req-to q-top) 
		     (if-else (and want-cs is-regreq) 
			      (if is-q-empty exit-cs)
			      (if has-token enter-cs))))
	   enter-cs)
  (if-else (not (or is-regreq has-token)) 
	   (if is-q-empty exit-cs) 
	   (if-else (and want-cs is-regreq)
		    (if is-q-empty exit-cs) 
		    (if has-token enter-cs)))))
     """
    testTree = """
 (if-else (or (and (or is-incs is-incs) (and
     is-waiting-for-token want-cs)) (not (or has-token
     is-incs))) (progn2 (if (not is-holder) (progn2
     exit-cs enter-cs)) (progn2 (progn2 exit-cs
     exit-cs) (if want-cs register-req-q))) (send-token-to
     q-top))
     """

    seed = [0.363071798408, 0.335530881201, 0.749396843633, 0.686701879371, 0.386633282042,
            0.215041798442, 0.507269447973, 0.220092356997, 0.126875863452, 0.385194855415]
    nodes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    numSteps = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    rates = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]

    for idx, val in enumerate(seed):
        raymond = simulator.Simulator()
        raymond.set_params(
            [seed[idx], nodes[idx], numSteps[idx], rates[idx], 0.4, 0.6, 0.0])
        fr = raymond.run(raymondTree)

        sim = simulator.Simulator()
        sim.set_params(
            [seed[idx], nodes[idx], numSteps[idx], rates[idx], 0.4, 0.6, 0.0])
        ft = sim.run(testTree)
        print "test %d : %.3f %.3f\t%.3f %.3f\t%.3f %.3f\n" % (idx + 1, fr[0], ft[0], fr[1], ft[1], fr[2], ft[2])
