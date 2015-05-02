package evomutex.func;

import ec.*;
import ec.gp.*;
import ec.util.*;

import evomutex.* ;

public class Not extends GPNode {
	public String toString() {
		return "not";
	}

	public void checkConstraints(final EvolutionState state,
	                             final int tree,
	                             final GPIndividual typicalIndividual,
	                             final Parameter individualBase) {
		super.checkConstraints(state,tree,typicalIndividual,individualBase);
		if (children.length!=1)
			state.output.error("Incorrect number of children for node " +
			                   toStringForError() + " at " +
			                   individualBase);
	}

	// gp got rid of the eval, eval will be taken care by the python
	public void eval(final EvolutionState state,
	                 final int thread,
	                 final GPData input,
	                 final ADFStack stack,
	                 final GPIndividual individual,
	                 final Problem problem) {
		/*TypeData data = (TypeData)input ;
		children[0].eval(state, thread, data, stack,
					individual, problem);
		if(data.ret != 1.0)
			data.ret = 1.0 ;
		else
			data.ret = 0.0 ;*/
	}
}



