import threading
import random
import time

class RingAlgorithm:
    def __init__(self, process_id, num_processes):
        self.process_id = process_id
        self.num_processes = num_processes
        self.active_list = []
        self.coordinator = None
        self.lock = threading.Lock()

    def send_elect(self, next_process):
        print(f"Process {self.process_id} is sending an Elect message to Process {next_process}.")
        time.sleep(random.uniform(0.1, 0.3))
        self.active_list.append(self.process_id)
        print(f"Active List of Process {self.process_id}: {self.active_list}")

    def elect_coordinator(self):
        highest = max(self.active_list)
        print(f"Process {self.process_id} elects Process {highest} as coordinator.")
        return highest

    def election(self):
        next_process = (self.process_id + 1) % self.num_processes
        self.send_elect(next_process)

        if len(self.active_list) == self.num_processes:
            self.coordinator = self.elect_coordinator()
            for process in self.active_list:
                print(f"Process {process} knows Process {self.coordinator} is the coordinator.")
                time.sleep(random.uniform(0.1, 0.3))

    def receive_message(self, message):
        with self.lock:
            if "Elect" in message:
                next_process = (self.process_id + 1) % self.num_processes
                print(f"Process {self.process_id} receives Elect message. Active List: {self.active_list}")
                self.send_elect(next_process)
            elif "Elected" in message:
                self.coordinator = int(message.split()[-1])
                print(f"Process {self.process_id} received elected message: Process {self.coordinator} is the coordinator.")

    def start(self):
        self.election()


def simulate_ring_algorithm():
    num_processes = 5
    processes = [RingAlgorithm(i, num_processes) for i in range(num_processes)]

    threads = []
    for process in processes:
        t = threading.Thread(target=process.start)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


simulate_ring_algorithm()
