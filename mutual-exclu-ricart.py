class Process:
    def __init__(self, id, total_processes):
        self.id = id
        self.total_processes = total_processes
        self.clock = 0
        self.request_timestamp = None
        self.deferred_replies = []
        self.in_critical_section = False
        
    def increment_clock(self):
        self.clock += 1
        return self.clock
        
    def request_critical_section(self):
        print(f"\nProcess {self.id} wants to enter critical section")
        self.request_timestamp = self.increment_clock()
        print(f"Process {self.id} sets request timestamp = {self.request_timestamp}")
        return self.request_timestamp
        
    def receive_request(self, sender_id, timestamp):
        # Update clock
        self.clock = max(self.clock, timestamp) + 1
        
        # If we're in CS or have an outstanding request with higher priority
        if self.in_critical_section or (self.request_timestamp is not None and 
                                        (self.request_timestamp < timestamp or 
                                        (self.request_timestamp == timestamp and self.id < sender_id))):
            # Defer reply
            self.deferred_replies.append(sender_id)
            print(f"Process {self.id} defers reply to Process {sender_id}")
            return False
        else:
            # Send reply immediately
            print(f"Process {self.id} immediately replies to Process {sender_id}")
            return True
            
    def enter_critical_section(self):
        print(f"Process {self.id} enters critical section")
        self.in_critical_section = True
        
    def exit_critical_section(self):
        print(f"Process {self.id} exits critical section")
        self.in_critical_section = False
        self.request_timestamp = None
        
        # Send all deferred replies
        print(f"Process {self.id} sends deferred replies to: {self.deferred_replies}")
        deferred_list = self.deferred_replies.copy()
        self.deferred_replies = []
        return deferred_list
        
def simulate_ricart_agrawala():
    # Create 3 processes
    processes = [Process(i, 3) for i in range(3)]
    print("Created 3 processes in the distributed system")
    
    print("\n DEMO 1: Process 0 requests critical section")
    # Process 0 requests CS
    p0_timestamp = processes[0].request_critical_section()
    
    # Process 0 sends request to all other processes
    print("Process 0 sends REQUEST messages to all other processes")
    replies_received = 0
    
    # Process 1 receives request and replies
    if processes[1].receive_request(0, p0_timestamp):
        replies_received += 1
        print("Process 0 received REPLY from Process 1")
    
    # Process 2 receives request and replies
    if processes[2].receive_request(0, p0_timestamp):
        replies_received += 1
        print("Process 0 received REPLY from Process 2")
    
    # Process 0 enters CS after receiving all replies
    if replies_received == 2:
        processes[0].enter_critical_section()
        print("Process 0 performs critical section operation")
        
        # Process 0 exits CS
        deferred = processes[0].exit_critical_section()
        # No deferred replies in this example
    
    print("\n DEMO 2: Process 1 and 2 compete for critical section")
    # Process 1 requests CS
    p1_timestamp = processes[1].request_critical_section()
    
    # Process 2 requests CS with higher timestamp (lower priority)
    p2_timestamp = processes[2].request_critical_section()
    
    print("Process 1 sends REQUEST messages to all other processes")
    replies_to_p1 = 0
    
    # Process 0 receives request from Process 1 and replies
    if processes[0].receive_request(1, p1_timestamp):
        replies_to_p1 += 1
        print("Process 1 received REPLY from Process 0")
    
    # Process 2 receives request from Process 1
    # Process 2 has its own request but decides based on timestamps
    if processes[2].receive_request(1, p1_timestamp):
        replies_to_p1 += 1
        print("Process 1 received REPLY from Process 2")
    else:
        print("Process 2 defers REPLY to Process 1 (has higher priority request)")
    
    print("\nProcess 2 sends REQUEST messages to all other processes")
    replies_to_p2 = 0
    
    # Process 0 receives request from Process 2 and replies
    if processes[0].receive_request(2, p2_timestamp):
        replies_to_p2 += 1
        print("Process 2 received REPLY from Process 0")
    
    # Process 1 receives request from Process 2
    # Process 1 has its own request but decides based on timestamps
    if processes[1].receive_request(2, p2_timestamp):
        replies_to_p2 += 1
        print("Process 2 received REPLY from Process 1")
    else:
        print("Process 1 defers REPLY to Process 2 (has higher priority request)")
    
    # Process 1 enters CS if it received all replies
    if replies_to_p1 == 2:
        processes[1].enter_critical_section()
        print("Process 1 performs critical section operation")
        
        # Process 1 exits CS and sends deferred replies
        deferred = processes[1].exit_critical_section()
        
        # If Process 1 deferred a reply to Process 2, send it now
        if 2 in deferred:
            replies_to_p2 += 1
            print("Process 2 received delayed REPLY from Process 1")
    
    # Process 2 enters CS if it received all replies
    if replies_to_p2 == 2:
        processes[2].enter_critical_section()
        print("Process 2 performs critical section operation")
        processes[2].exit_critical_section()
    else:
        print("Process 2 is still waiting for replies")
    
    print("\n Complete")

if __name__ == "__main__":
    print("Ricart-Agrawala Mutual Exclusion Algorithm")
    simulate_ricart_agrawala()