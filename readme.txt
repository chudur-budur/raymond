How to compile the code and run the experiments
===============================================

We are assuming that the users have latest jdk and python on their system, and all the java classpath environments are setup properly. The codes are structured as follows --

* raymond/lib: 		contains all necessary libraries
* raymond/src: 		contains all codes
* raymond/src/evomutex:	contains all codes related to GP module
* raymond/src/sim: 	contains all codes related to simulator module
* raymond/src/pyglue: 	contains all codes related to java-python interface
* raymond/src/make: 	the bash script to compile and run the experiments

To compile: open a terminal, go to the raymond/src folder and type --
	user@machine:/home/raymond/src$ ./make

To run: type --
	user@machine:/home/raymond/src$ ./make run

After the execution, the results will be saved in raymond/src/out.stat file, this file will contain the best evolved tree at each successive generations, along with their fitness. To run a particular tree, please refer to the raymond/src/sim/tester.py script. 

Users can also use the same script for cleaning up the compiled executables.

To clean: type --
	user@machine:/home/raymond/src$ ./make clean
