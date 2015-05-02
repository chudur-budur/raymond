package pyglue ;

import java.io.* ;
import org.python.core.PyInstance;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;


public class PyGlue {

	private PythonInterpreter interpreter = null;

	public PyGlue() {
		PythonInterpreter.initialize(System.getProperties(),
		                             System.getProperties(), new String[0]);
		this.interpreter = new PythonInterpreter();
	}

	public void execfile( final String fileName ) {
		InputStream is = this.getClass().getResourceAsStream(fileName);
		this.interpreter.execfile(is);
	}

	public PyInstance createClass( final String className, final String opts ) {
		return (PyInstance) this.interpreter.eval(className + "(" + opts + ")");
	}

	public static void main( String gargs[] ) {
		PyGlue pg = new PyGlue();
		pg.execfile("hello.py");
		PyInstance hello = pg.createClass("Hello", "None");
		hello.invoke("run");
		hello.invoke("hello", new PyString("chudur-budur"));
	}
}
















