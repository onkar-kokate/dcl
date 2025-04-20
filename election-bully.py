import threading
import random
import time

class BullyAlgorithm:
    def __init__(self, process_id, num_processes):
        self.process_id = process_id
        self.num_processes = num_processes
        self.coordinator = None
        self.lock = threading.Lock()

    def send_election(self):
        print(f"Process {self.process_id} is sending an election message.")
        # Send election message to higher processes
        for i in range(self.process_id + 1, self.num_processes):
            print(f"Process {self.process_id} sent election message to Process {i}")
            time.sleep(random.uniform(0.1, 0.3))  # Simulate network delay
            if self.coordinator is None:  # Wait for response
                print(f"Process {self.process_id} waiting for response from higher process.")

    def election(self):
        self.send_election()

        # Process Pi becomes coordinator if no response
        if self.coordinator is None:
            self.coordinator = self.process_id
            print(f"Process {self.process_id} becomes the coordinator.")
            for i in range(self.process_id):
                print(f"Process {self.process_id} sends elected message to Process {i}")
                time.sleep(random.uniform(0.1, 0.3))

    def receive_message(self, message):
        with self.lock:
            if "Election" in message:
                print(f"Process {self.process_id} received an election message.")
                if self.process_id < int(message.split()[-1]):
                    print(f"Process {self.process_id} responds to election from {message.split()[-1]}")
                    self.election()
            elif "Elected" in message:
                self.coordinator = int(message.split()[-1])
                print(f"Process {self.process_id} acknowledges that Process {self.coordinator} is the coordinator.")

    def start(self):
        self.election()


def simulate_bully_algorithm():
    num_processes = 5
    processes = [BullyAlgorithm(i, num_processes) for i in range(num_processes)]

    threads = []
    for process in processes:
        t = threading.Thread(target=process.start)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


simulate_bully_algorithm()
