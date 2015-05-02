package evomutex.func;

import ec.*;
import ec.gp.*;
import ec.util.*;

import evomutex.* ;


public class EnterCs extends GPNode {
	public String toString() {
		return "enter-cs";
	}

	public void checkConstraints(final EvolutionState state,
	                             final int tree,
	                             final GPIndividual typicalIndividual,
	                             final Parameter individualBase) {
		super.checkConstraints(state,tree,typicalIndividual,individualBase);
		if (children.length!=0)
			state.output.error("Incorrect number of children for node " +
			                   toStringForError() + " at " +
			                   individualBase);
	}

	/** The corresponding action for move-south is "Agent.S" **/
	public void eval(final EvolutionState state,
	                 final int thread,
	                 final GPData input,
	                 final ADFStack stack,
	                 final GPIndividual individual,
	                 final Problem problem) {
		/*children[0].eval(state, thread, input, stack, individual, problem);
		TypeData data = (TypeData)input ;
		((MASONProblem)problem).exeStack.currentAction
				= data.direction;*/
	}
}



