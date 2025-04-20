import java.rmi.*;

public interface AddService extends Remote {
    int add(int a, int b) throws RemoteException;
}

// 1. Compile All
// javac *.java

// 2. Generate Stub (if using JDK 8 or older)
// rmic AddServiceImpl
// (Not needed for JDK 11+ as stubs are generated dynamically)

// 3. Start RMI Registry (in background or another terminal)
// rmiregistry
// (Keep it running in the same directory.)

// 4. Start Server
// java Server

// 5. Start Client (in another terminal)
// java Client