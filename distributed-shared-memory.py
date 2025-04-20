import multiprocessing
import time
import random

def writer(shared_memory, semaphore, writer_id):
    for _ in range(3):
        time.sleep(random.uniform(0.5, 1.5))  # Simulate computation or network delay
        semaphore.acquire()
        try:
            new_value = random.randint(1, 100)
            print(f"[Writer {writer_id}] Writing {new_value} to shared memory.")
            shared_memory.value = new_value
        finally:
            semaphore.release()

def reader(shared_memory, semaphore, reader_id):
    for _ in range(3):
        time.sleep(random.uniform(0.5, 1.5))
        semaphore.acquire()
        try:
            value = shared_memory.value
            print(f"[Reader {reader_id}] Read {value} from shared memory.")
        finally:
            semaphore.release()

if __name__ == '__main__':
    # Shared memory variable (integer)
    shared_memory = multiprocessing.Value('i', 0)

    # Binary semaphore (acts like a mutex)
    semaphore = multiprocessing.Semaphore(1)

    # Spawn writer and reader processes
    writers = [multiprocessing.Process(target=writer, args=(shared_memory, semaphore, i)) for i in range(2)]
    readers = [multiprocessing.Process(target=reader, args=(shared_memory, semaphore, i)) for i in range(2)]

    # Start all processes
    for p in writers + readers:
        p.start()

    # Wait for all processes to complete
    for p in writers + readers:
        p.join()

    print("\nAll read/write operations completed.")
