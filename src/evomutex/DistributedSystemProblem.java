package evomutex;

import java.io.* ;
import java.util.*;
import ec.*;
import ec.util.*;
import ec.simple.*;
import ec.gp.*;
import ec.gp.koza.*;

// Jython stuffs
import org.python.core.*;
import org.python.util.*;
// python glue is here
import pyglue.*;

// all protocol functions are here
import evomutex.func.*;

public class DistributedSystemProblem extends GPProblem implements SimpleProblemForm {

	PyGlue pg ;
	PyInstance sim ;

	// simulation paramters
	double[] seed = {0.363071798408, 0.335530881201, 0.749396843633, 
				0.686701879371, 0.386633282042}; 
	int[] nodes = {10,20,30,40,50};
	int[] numSteps = {100,150,200,250,300};
	double[] rates = {0.2,0.3,0.4,0.5,0.6}; 

	public void setup(final EvolutionState evstate, final Parameter base) {
		super.setup(evstate, base);
		// get a new PyGlue
		try { 
			pg = new PyGlue("/sim");
		} catch(Exception e) {
			e.printStackTrace();
		}
		pg.loadScript("/sim/simulator.py");
	}

	public void evaluate(final EvolutionState evstate,
	                     final Individual ind,
	                     final int subpopulation,
	                     final int threadnum) {
		if (!ind.evaluated) { // don't bother reevaluating
			// parse this tree to string
			StringWriter stringWriter = new StringWriter();
			PrintWriter writer = new PrintWriter(stringWriter);
			GPTree gpt = ((GPIndividual)ind).trees[0];
			int depth = gpt.child.depth();
			int numNodes = gpt.child.numNodes(0);
			gpt.printTree(evstate,writer);
			String tree = stringWriter.toString();
			
			double score = 0.0 ;
			// int idx = evstate.random[threadnum].nextInt(seed.length);
			int idx = evstate.generation % (seed.length - 1); 
			sim = pg.getInstance("Simulator");
			PyList pl = new PyList();
			pl.add(new PyFloat(seed[idx]));	
			pl.add(new PyInteger(nodes[idx]));	
			pl.add(new PyInteger(numSteps[idx]));	
			pl.add(new PyFloat(rates[idx]));	
			// (0.3, 0.7) --> better code than raymond ?
			pl.add(new PyFloat(0.3)); 
			pl.add(new PyFloat(0.7)); 
			pl.add(new PyFloat(0.0));	
			sim.invoke("set_params", pl);
			// fireup the python simulator and pass the tree to it.
			Object[] fvals = 
				((PyList)sim.invoke("run", new PyString(tree))).toArray();
			score = (depth < 5 ? 0.00000001 : 
					((Double)fvals[fvals.length-1]).doubleValue()); 
		
			// the fitness better be KozaFitness!
			KozaFitness f = ((KozaFitness)ind.fitness);
			// could "not" divide by 0!
			f.setStandardizedFitness(evstate, (float)(1.0/score));
			f.hits = 0;  // don't care
			ind.evaluated = true;
		}
	}
}
