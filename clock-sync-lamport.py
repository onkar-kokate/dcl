import time
import threading

class LamportClock:
    def __init__(self, process_id):
        self.process_id = process_id
        self.timestamp = 0

    def increment(self):
        # Increment the clock before each event
        self.timestamp += 1
        print(f"Process {self.process_id} Event {self.timestamp}")
        return self.timestamp

    def send(self):
        # Simulate sending a message with the timestamp
        timestamp = self.increment()
        print(f"Process {self.process_id} sends message with timestamp {timestamp}")
        return timestamp

    def receive(self, received_timestamp):
        # When receiving a message, update the clock to max(current timestamp, received timestamp) + 1
        self.timestamp = max(self.timestamp, received_timestamp) + 1
        print(f"Process {self.process_id} received message with timestamp {received_timestamp}, updated clock to {self.timestamp}")


# Function to simulate message passing between two processes
def process_communication(clock1, clock2):
    # Process 1 sends a message
    timestamp1 = clock1.send()

    # Simulate a small delay
    time.sleep(1)

    # Process 2 receives the message and updates its clock
    clock2.receive(timestamp1)

    # Process 2 sends a message back to Process 1
    timestamp2 = clock2.send()

    # Simulate a small delay
    time.sleep(1)

    # Process 1 receives the message and updates its clock
    clock1.receive(timestamp2)

def main():
    # Create two Lamport Clocks for two processes
    clock1 = LamportClock(1)
    clock2 = LamportClock(2)

    # Create two threads to simulate communication between two processes
    thread1 = threading.Thread(target=process_communication, args=(clock1, clock2))
    thread2 = threading.Thread(target=process_communication, args=(clock2, clock1))

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for threads to finish
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
