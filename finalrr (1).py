import socket
import struct
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
MAX_BUFFER_SIZE = 1024
TIME_QUANTUM = 2 

class Process:
    def __init__(self, pid, burst_time):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time


class Queue:
    def __init__(self):
        self.data = []
    
    def enqueue(self, process):
        self.data.append(process)
    
    def dequeue(self):
        if len(self.data) > 0:
            return self.data.pop(0)
        else:
            return None

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
    except socket.error as e:
        print("Connection failed:", e)
        exit(1)

    print("Connected to the server")

    ready_queue = Queue()
    current_time = 0
    completed_processes = []

    while True:
        try:
            data = client_socket.recv(MAX_BUFFER_SIZE)
            if data:
                process_info = data.decode().strip().split()
                if len(process_info) == 2:
                    pid = int(process_info[0])
                    burst_time = int(process_info[1])

                    process = Process(pid, burst_time)
                    ready_queue.enqueue(process)
                    #print("\n")
            
            if ready_queue.data:
                current_process = ready_queue.dequeue()

                execute_time = min(TIME_QUANTUM, current_process.remaining_time)
                print(f"Process {current_process.pid} is running from time {current_time} to {current_time + execute_time}")

                current_time += execute_time
                current_process.remaining_time -= execute_time

                if current_process.remaining_time <= 0:
                    completed_processes.append(current_process)
                    print(f"Process {current_process.pid} completed.")
                else:
                    ready_queue.enqueue(current_process)
                #print(f"Ready queue: {[p.pid for p in ready_queue.data]}")
            
            time.sleep(0.1)

        except Exception as e:
            print(f"Error during execution: {e}")
            break

    print("\nCompleted Processes:")
    for process in completed_processes:
        print(f"Process {process.pid}: Total Burst Time {process.burst_time}")

    client_socket.close()


if __name__ == "__main__":
    main()

