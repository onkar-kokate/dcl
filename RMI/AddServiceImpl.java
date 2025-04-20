import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;

public class AddServiceImpl extends UnicastRemoteObject implements AddService {
    public AddServiceImpl() throws RemoteException {
        super();
    }

    public int add(int a, int b) throws RemoteException {
        return a + b;
    }
}
