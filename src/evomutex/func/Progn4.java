package evomutex.func;

import ec.*;
import ec.gp.*;
import ec.util.*;

import evomutex.* ;

public class Progn4 extends GPNode {
	public String toString() {
		return "progn4";
	}

	public void checkConstraints(final EvolutionState state,
	                             final int tree,
	                             final GPIndividual typicalIndividual,
	                             final Parameter individualBase) {
		super.checkConstraints(state,tree,typicalIndividual,individualBase);
		if (children.length!=4)
			state.output.error("Incorrect number of children for node " +
			                   toStringForError() + " at " +
			                   individualBase);
	}

	public void eval(final EvolutionState state,
	                 final int thread,
	                 final GPData input,
	                 final ADFStack stack,
	                 final GPIndividual individual,
	                 final Problem problem) {
		/*((DistAlgoProblem)problem).exeStack.nodeStack.push(children[0]);
		((DistAlgoProblem)problem).exeStack.nodeStack.push(children[1]);
		((DistAlgoProblem)problem).exeStack.nodeStack.push(children[2]);
		((DistAlgoProblem)problem).exeStack.nodeStack.push(children[3]);
		// The corresponding action for progn4 is "Agent.NOTHING"
		// ((DistAlgoProblem)problem).exeStack.currentAction = Agent.NOTHING ;*/
	}
}



