import java.rmi.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Server {
    public static void main(String[] args) throws Exception {
        AddServiceImpl obj = new AddServiceImpl();
        LocateRegistry.createRegistry(2000); // Start RMI registry on port 2000
        Naming.rebind("rmi://localhost:2000/AddService", obj);
        System.out.println("Server is ready");
    }
}
