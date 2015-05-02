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
import org.python.util.PythonInterpreter;
// python glue is here
import pyglue.*;

// all protocol functions are here
import evomutex.func.*;

public class DistributedSystemProblem extends GPProblem implements SimpleProblemForm {

	PyGlue pg ;
	PyInstance parser ;

	public void setup(final EvolutionState evstate, final Parameter base) {
		super.setup(evstate, base);
		// get a new PyGlue 
		pg = new PyGlue();
		pg.loadScript("/simulator/parser.py");
		parser = pg.getInstance("Parser");
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

			evstate.output.println("evaluating tree:\n" + tree, threadnum);
			// fireup the python simulator and pass the tree to it.
			parser.invoke("parse_tree", new PyString(tree));
			int score = ((PyInteger)parser.invoke("get_score")).getValue();
			evstate.output.println("score: " + score, threadnum);
			String pystr = ((PyString)parser.invoke("get_tree")).toString();
			evstate.output.println("parser String: \n" + pystr + "\n", threadnum);


			// faking the fitness value for now
			// double score = evstate.random[threadnum].nextDouble();
			score = evstate.random[threadnum].nextInt(100);
			if(score == 0)
				score = 1 ;
			// the fitness better be KozaFitness!
			KozaFitness f = ((KozaFitness)ind.fitness);
			// could "not" divide by 0!
			f.setStandardizedFitness(evstate, (float)(1.0/score));
			f.hits = 0;  // don't care
			ind.evaluated = true;
		}
	}
}
