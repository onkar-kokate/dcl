class Process:
    def __init__(self, pid):
        self.pid = pid  # Process ID
        self.waiting_for = []  # List of processes it is waiting for

    def request_resource(self, resource_holders, initiator):
        """Initiates a probe if the resource request fails."""
        if not resource_holders:
            print(f"Process {self.pid} found no resource holders.")
            return False  # No resource holders, no deadlock

        for holder in resource_holders:
            probe = [initiator, self.pid, holder.pid]  # Probe message
            print(f"Process {self.pid} sending probe {probe} to {holder.pid}")
            if holder.receive_probe(probe):
                print(f" Deadlock detected involving process {initiator}!")
                return True

        return False

    def receive_probe(self, probe):
        """Handles received probe messages."""
        initiator, sender, receiver = probe
        print(f"Process {self.pid} received probe {probe}")

        if self.pid == initiator:  # Cycle detected
            print(f" Cycle detected! Process {self.pid} is in a deadlock.")
            return True

        if not self.waiting_for:  # Not waiting for any process
            print(f"Process {self.pid} is not waiting for any resource. Ignoring probe.")
            return False  # No deadlock

        for next_holder in self.waiting_for:
            new_probe = [initiator, self.pid, next_holder.pid]  # Modify probe
            print(f"Process {self.pid} forwarding probe {new_probe} to {next_holder.pid}")
            if next_holder.receive_probe(new_probe):
                return True

        return False


# ------------------ Example Usage ------------------ #

print("🔍 # Deadlock Example")
p1 = Process(1)
p2 = Process(2)
p3 = Process(3)
p4 = Process(4)

# Defining dependencies (waits-for relationships) - Deadlock case
p1.waiting_for = [p2]
p2.waiting_for = [p3]
p3.waiting_for = [p4]
p4.waiting_for = [p1]  # Creates a cycle (deadlock)

# Initiate probe from p1
if p1.request_resource([p2], p1.pid):
    print(" Deadlock confirmed.\n")
else:
    print(" No deadlock detected.\n")


print(" # No Deadlock Example")
p5 = Process(5)
p6 = Process(6)
p7 = Process(7)
p8 = Process(8)

# Defining dependencies - No cycle
p5.waiting_for = [p6]
p6.waiting_for = [p7]
p7.waiting_for = [p8]
p8.waiting_for = []  # No cycle

# Initiate probe from p5
if p5.request_resource([p6], p5.pid):
    print(" Deadlock confirmed.")
else:
    print(" No deadlock detected.")
