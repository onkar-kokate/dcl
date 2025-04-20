import java.io.*;
import java.net.*;

public class Server {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(5055);
        Socket socket = serverSocket.accept();

        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
        BufferedReader console = new BufferedReader(new InputStreamReader(System.in));

        // Thread to read messages from client
        new Thread(() -> {
            try {
                String msg;
                while ((msg = in.readLine()) != null) {
                    System.out.println("Client: " + msg);
                }
            } catch (Exception e) {
                // minimal handling
            }
        }).start();

        // Sending messages to client
        String msg;
        while ((msg = console.readLine()) != null) {
            out.println(msg);
        }

        socket.close();
        serverSocket.close();
    }
}

// Compile both files:
// javac Server.java
// javac Client.java

// Run the Server first:
// java Server

// Run the Client in a new terminal:
// java Client