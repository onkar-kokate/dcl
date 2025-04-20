import os
import multiprocessing

def child_process(pipe_write):
    # Write message to the pipe
    message = "Hello from child process!"
    pipe_write.send(message)  # Send the message through the pipe
    pipe_write.close()  # Close the pipe after writing

def parent_process():
    # Create a pipe
    pipe_read, pipe_write = multiprocessing.Pipe()
    
    # Create child process and pass the pipe's write end
    process = multiprocessing.Process(target=child_process, args=(pipe_write,))
    process.start()
    
    pipe_write.close()  # Close the write end in the parent process

    # Read message from the pipe
    message = pipe_read.recv()  # Receive the message from the pipe
    print(f"Parent received: {message}")
    
    pipe_read.close()  # Close the read end after usage
    process.join()  # Wait for the child process to finish

if __name__ == "__main__":
    parent_process()
