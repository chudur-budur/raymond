package evomutex;

import java.io.* ;
import java.util.*;
import ec.*;
import ec.util.*;
import ec.simple.*;
import ec.gp.*;
import ec.gp.koza.*;

// Jython stuffs
import org.python.core.PyInstance;
import org.python.core.PyString;
import org.python.core.PyInteger;
import org.python.core.PyFloat;
import org.python.util.PythonInterpreter;
// python glue is here
import pyglue.*;

// all protocol functions are here
import evomutex.func.*;

public class DistributedSystemProblem extends GPProblem implements SimpleProblemForm {

	PyGlue pg ;
	PyInstance sim ;

	public void setup(final EvolutionState evstate, final Parameter base) {
		super.setup(evstate, base);
		// get a new PyGlue 
		pg = new PyGlue();
		pg.loadScript("/simulator/simulator2.py");
		sim = pg.getInstance("Simulator");
	}

	public void evaluate(final EvolutionState evstate,
	                     final Individual ind,
	                     final int subpopulation,
	                     final int threadnum) {
		if (!ind.evaluated) { // don't bother reevaluating
			// parse this tree to string
			StringWriter stringWriter = new StringWriter();
			PrintWriter writer = new PrintWriter(stringWriter);
			((GPIndividual)ind).trees[0].printTree(evstate, writer);
			String tree = stringWriter.toString();
			tree = "(progn2 (enter-cs-temp)" + tree + ")" ;

			// fireup the python simulator and pass the tree to it.
			sim.invoke("run", new PyString(tree));
			double score = ((PyFloat)sim.invoke("get_fitness")).getValue() + 1.0 ;


			// the fitness better be KozaFitness!
			KozaFitness f = ((KozaFitness)ind.fitness);
			// could "not" divide by 0!
			f.setStandardizedFitness(evstate, (float)(1.0/score));
			f.hits = 0;  // don't care
			ind.evaluated = true;
		}
	}
}
