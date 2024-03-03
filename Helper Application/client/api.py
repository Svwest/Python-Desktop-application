import json
import pickle
import socket
from pc_info import (get_sys_info,
                     get_boot_time_info,
                     get_cpu_info, get_memory_info,
                     get_swap_memory_info,
                     get_disk_info,
                     get_network_info,
                     get_gpu_info)
import process_info
def api_server(server_socket):
    try:
        # Send a command to the client
        server_socket.send("command".encode())
    except socket.error as e:
        print("Error sending command:", e)
        exit(-22)
    while True:
        print("Inside the true loop")
        try:
            # Receive command from the client
            command = server_socket.recv(1024).decode()
            if not command:
                server_socket.close()
                print("Server closed the connection2")
                exit()
            if command == "terminate":
                print("Inside terminate command")
                server_socket.send("wait_for_task".encode())
                print('1')
                task = server_socket.recv(1024).decode()
                task = task.strip()
                print("Task name: " + task + " here")
                if process_info.terminate(task):
                    print("Terminated task")
                    server_socket.send("managed".encode())
                else:
                    server_socket.send("permission_denied".encode())
                command = ""
            if command == "List_all":
                print("Inside List_all command")
                list_of_all = process_info.get_processes_info()
                server_socket.send(str(len(list_of_all)).encode())

                for process in list_of_all:
                    server_socket.send(pickle.dumps(process))
                    response = server_socket.recv(1024).decode()
                response = server_socket.recv(1024).decode()
                if response == "go":
                    server_socket.send("sent_all".encode())
                command = ""
            if command == "get_pc_info":
                print('Inside get_pc_info command')
                pc_info = [get_sys_info(),
                           get_boot_time_info(),
                           get_cpu_info(),
                           get_memory_info(),
                           get_swap_memory_info(),
                           get_disk_info(),
                           get_network_info(),
                           get_gpu_info()]
                pc_info_str = json.dumps(pc_info)
                server_socket.send(pc_info_str.encode())
                command = ""
            if command == "goodbye":
                server_socket.close()
                print("Server closed the connection2")
                exit(8)
        except socket.error as e:
            print("Socket error:", e)
            break
    server_socket.close()
    exit(0)
