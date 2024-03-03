import pickle
import socket
import sys
import threading
import time
from tkinter import *
from tkinter import messagebox

# Global variable to keep track of the active sorting method
active_sort = 'id'


# Function to find the index of an item in a list
def get_index(lst, item):
    """
    Find the index of an item in a list.
    """
    index = sys.maxsize
    for i, value in enumerate(lst):
        if value == item:
            index = i
    return index


# Function to sort processes by priority
def sort_by_priority(processes):
    """
    Sort processes by priority.
    """
    global active_sort
    active_sort = 'priority'
    final = []
    prioritys = []

    for item in processes:
        prioritys.append(int(item[6]))

    prioritys.sort()
    for priority in prioritys:
        for proc in processes:
            if priority == int(proc[6]) and get_index(final, proc) == sys.maxsize:
                final.append(proc)

    return final


# Function to sort processes by name
def sort_by_name(processes):
    """
    Sort processes by name.
    """
    global active_sort
    active_sort = 'name'
    final = []
    names = []

    for item in processes:
        names.append(item[1].lower())

    names.sort()
    for name1 in names:
        for proc in processes:
            if name1 == proc[1].lower() and get_index(final, proc) == sys.maxsize:
                final.append(proc)

    return final


# Function to sort processes by ID
def sort_by_id(processes):
    """
    Sort processes by ID.
    """
    global active_sort
    active_sort = 'id'
    final = []
    ids = []

    for item in processes:
        ids.append(int(item[0]))

    ids.sort()
    for id1 in ids:
        for proc in processes:
            if id1 == int(proc[0]) and get_index(final, proc) == sys.maxsize:
                final.append(proc)

    return final


# Function to sort processes by CPU
def sort_by_cpu(processes):
    """
    Sort processes by CPU usage.
    """
    global active_sort
    active_sort = 'cpu'
    final = []
    cpus = []

    for item in processes:
        cpus.append(float(item[4]))

    cpus.sort()
    for cpu1 in cpus:
        for proc in processes:
            if cpu1 == float(proc[4]) and get_index(final, proc) == sys.maxsize:
                final.append(proc)

    return final


# Function to sort processes by memory
def sort_by_memory(processes):
    """
    Sort processes by memory usage.
    """
    global active_sort
    active_sort = 'memory'
    final = []
    memories = []

    for item in processes:
        memories.append(float(item[7]))

    memories.sort()
    for memory1 in memories:
        for proc in processes:
            if memory1 == float(proc[7]) and get_index(final, proc) == sys.maxsize:
                final.append(proc)

    return final


# Function to terminate a process
def terminate(mlb, client):
    """
    Terminate a selected process.
    """
    try:
        selected = mlb.curselection()
        print('selected', selected)

        if selected[0] != '':
            # Send termination request to the server
            client.send("terminate".encode())
            time.sleep(0.01)
            resp = client.recv(1024).decode()

            if resp == "wait_for_task":
                # Send selected process ID to terminate
                client.send(selected[1].encode())
                time.sleep(0.01)
                response = client.recv(1024).decode()

                if response == "managed":
                    time.sleep(0.1)
                    refresh(client, mlb)
                elif response == "permission_denied":
                    messagebox.showinfo("Attention", "Error to delete")
        else:
            messagebox.showinfo("Attention", "Must to pick line")

    except (socket.error, IndexError) as err:
        print(err)
        print('An error occurred during termination')

    return


# Function to refresh the list of processes
def refresh(client, mlb):
    """
    Refresh the list of processes.
    """
    global active_sort

    try:
        all_process = []
        client.send("List_all".encode())
        time.sleep(0.01)

        try:
            length = int(client.recv(1024))
            print('length of refresh', length)

        except socket.error as err:
            print(err)
            print('Please contact your administrator 2')
            sys.exit(-1)

        for _ in range(length):
            try:
                data = pickle.loads(client.recv(4096))
            except socket.error as err:
                print(err)
                print('Please contact your administrator 3')
                sys.exit(-1)

            client.send("go".encode())
            if data[0] == "sent_all":
                client.send("done".encode())
                break
            else:
                all_process.append(data)

        client.send("done".encode())
        print('active_sort', active_sort)
        change_order(all_process, mlb, active_sort)

    except (socket.error, ValueError) as err:
        print(err)
        print('An error occurred during refresh')

    return


def change_order(all_processes, mlb, sorting_method):
    """
    Change the order of displayed processes.
    """
    selected_line = mlb.curselection()
    print('selected line ', selected_line[0])

    try:
        sorted_processes = None
        if sorting_method == 'priority':
            sorted_processes = sort_by_priority(all_processes)
            sorted_processes.reverse()
        elif sorting_method == 'name':
            sorted_processes = sort_by_name(all_processes)
        elif sorting_method == 'id':
            sorted_processes = sort_by_id(all_processes)
        elif sorting_method == 'cpu':
            sorted_processes = sort_by_cpu(all_processes)
            sorted_processes.reverse()
        elif sorting_method == 'memory':
            sorted_processes = sort_by_memory(all_processes)
            sorted_processes.reverse()

        mlb.delete_all()

        for process in sorted_processes:
            mlb.insert(END, process)

        if selected_line[0] != '':
            mlb.set_select_by_id(selected_line[0])

    except Exception as e:
        print(f"Error in change_order: {e}")

    return
