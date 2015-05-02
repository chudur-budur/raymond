package evomutex.func;

import ec.*;
import ec.gp.*;
import ec.util.*;

import evomutex.* ;

public class And extends GPNode {
	public String toString() {
		return "and";
	}

	public void checkConstraints(final EvolutionState state,
	                             final int tree,
	                             final GPIndividual typicalIndividual,
	                             final Parameter individualBase) {
		super.checkConstraints(state,tree,typicalIndividual,individualBase);
		if (children.length!=2)
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
		/*TypeData data = (TypeData)input ;
		children[0].eval(state, thread, data, stack,
					individual, problem);
		boolean left = (data.ret != 0.0);
		children[1].eval(state, thread, data, stack,
					individual, problem);
		boolean right = (data.ret != 0.0);
		data.ret = (left && right) ? 1.0 : 0.0 ;*/
	}
}



