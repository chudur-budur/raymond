package evomutex.func;

import ec.*;
import ec.gp.*;
import ec.util.*;

import java.io.* ;
import java.util.*;

import evomutex.* ;

public class NodeErc extends ERC {
	public String nodeType ;
	public static final int range = 2 ;
	public String[] nodeTypes = {"q-top","holder"};

	public String toString() {
		return nodeType ;
	}

	public String toStringForHumans() {
		return nodeType ;
	}
	public String encode() {
		return Code.encode(nodeType);
	}

	public boolean decode(DecodeReturn dret) {
		int pos = dret.pos;
		String data = dret.data;
		Code.decode(dret);
		if (dret.type != DecodeReturn.T_STRING) { // uh oh! Restore and signal error.
			dret.data = nodeType;
			dret.pos = pos;
			return false;
		}
		nodeType = dret.data;
		return true;
	}

	public boolean nodeEquals(GPNode node) {
		return (node.getClass() == this.getClass() 
				&& ((NodeErc)node).nodeType.equals(nodeType));
	}

	public void readNode(EvolutionState state, DataInput input) throws IOException {
		nodeType = input.readLine();
	}

	public void writeNode(EvolutionState state, DataOutput output) throws IOException {
		output.writeBytes(nodeType);
	}

	public void resetNode(EvolutionState state, int thread) {
		nodeType = nodeTypes[state.random[thread].nextInt(range)];
	}

	public void mutateNode(EvolutionState state, int thread) {
		nodeType = nodeTypes[state.random[thread].nextInt(range)];
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



