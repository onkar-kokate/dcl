import java.rmi.*;

public class Client {
    public static void main(String[] args) throws Exception {
        AddService stub = (AddService) Naming.lookup("rmi://localhost:2000/AddService");
        int result = stub.add(10, 20);
        System.out.println("Result: " + result);
    }
}
