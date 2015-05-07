package pyglue ;

import java.io.* ;
import java.net.*;
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
	
	public PyGlue(String pydir) throws Exception{
		PythonInterpreter.initialize(System.getProperties(),
		                             System.getProperties(), new String[0]);
		this.interpreter = new PythonInterpreter();
		URL url = this.getClass().getResource(pydir);
		this.interpreter.getSystemState().path.pyadd(new PyString(url.toURI().getPath()));
	}

	public void loadScript( final String fileName ) {
		InputStream is = this.getClass().getResourceAsStream(fileName);
		this.interpreter.execfile(is);
	}

	public PyInstance getInstance( final String className, final String opts ) {
		return (PyInstance) this.interpreter.eval(className + "(" + opts + ")");
	}
	
	public PyInstance getInstance( final String className ) {
		return (PyInstance) this.interpreter.eval(className + "()");
	}

	public static void main( String gargs[] ) {
		PyGlue pg = new PyGlue();
		pg.loadScript("hello.py");
		PyInstance hello = pg.getInstance("Hello", "None");
		hello.invoke("run");
		hello.invoke("hello", new PyString("chudur-budur"));
	}
}
















