# process_info.py

import os
import psutil
from datetime import datetime


def send_able(data: object) -> object:
    """
    Ensure data is a non-empty string. If empty, appends "?" to make it non-empty.
    :param data: Input data
    :return: Non-empty string
    """
    while len(data) < 1:
        data = data + "?"
    return data


def terminate(name):
    """
    Terminate a process by name.
    :param name: Name of the process to terminate
    :return: True if successful, False otherwise
    """
    if os.system("TASKKILL /f /im " + name) == 0:
        return True
    return False


def get_processes_info():
    """
    Get information about all running processes.
    :return: List of lists containing process information
    """
    processes = []

    for process in psutil.process_iter():
        with process.oneshot():
            pid = process.pid

            if pid == 0:
                continue

            name = process.name()

            try:
                create_time = datetime.fromtimestamp(process.create_time())
            except OSError:
                # System processes, using boot time instead
                create_time = datetime.fromtimestamp(psutil.boot_time())

            try:
                # Get the number of CPU cores that can execute this process
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0

            try:
                # Get the CPU usage percentage
                cpu_usage = process.cpu_percent()
                cpu_usage = round(cpu_usage, 2)
            except psutil.AccessDenied:
                cpu_usage = 0

            # Get the status of the process (running, idle, etc.)
            status = process.status()

            try:
                # Get the process priority (a lower value means a more prioritized process)
                nice = int(process.nice())
            except psutil.AccessDenied:
                nice = 0

            try:
                # Get the memory usage in bytes
                memory = process.memory_full_info().uss
                total_memory = psutil.virtual_memory().total
                memory_usage = round(((memory / total_memory)*100), 2)

            except psutil.AccessDenied:
                memory_usage = 0

            # Total process read and written bytes
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes

            # Get the number of total threads spawned by this process
            n_threads = process.num_threads()

            # Get the username of the user who spawned the process
            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "N/A"

            to_add = [
                send_able(str(pid)),
                send_able(name),
                send_able(str(create_time)),
                send_able(str(cores)),
                send_able(str(cpu_usage)),
                send_able(status),
                send_able(str(nice)),
                send_able(str(memory_usage)),
                send_able(str(read_bytes)),
                send_able(str(write_bytes)),
                send_able(str(n_threads)),
                send_able(username)
            ]

            processes.append(to_add)

    return processes
