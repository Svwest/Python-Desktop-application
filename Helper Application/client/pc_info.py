# pc_info.py

import socket
import platform
import uuid
import psutil
import cpuinfo
import GPUtil
from datetime import datetime
import re

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_sys_info():
    """
    This function gets the system information
    :return: a string with system info divided by \n
    """
    uname = platform.uname()
    reply = " System @"
    reply += f"System: {uname.system}\n"
    reply += f"Node Name: {uname.node}\n"
    reply += f"Release: {uname.release}\n"
    reply += f"Version: {uname.version}\n"
    reply += f"Machine: {uname.machine}\n"
    reply += f"Processor: {uname.processor}\n"
    reply += f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}\n"
    reply += f"Ip-Address: {socket.gethostbyname(socket.gethostname())}\n"
    reply += f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}\n"
    return reply

def get_boot_time_info():
    """
    This function gets the PC boot time
    boot time is the time that the PC was turned on
    :return: PC boot time
    """
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)

    reply = " Boot Time @"
    reply += f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
    return reply

def get_cpu_info():
    """
    This function gets the CPU information
    :return: a string with CPU information divided by \n
    """
    reply = " CPU @"
    # number of cores
    reply += f"Physical cores: {psutil.cpu_count(logical=False)}\n"
    reply += f"Total cores: {psutil.cpu_count(logical=True)}\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    reply += f"Max Frequency: {cpufreq.max:.2f}Mhz\n"
    reply += f"Min Frequency: {cpufreq.min:.2f}Mhz\n"
    reply += f"Current Frequency: {cpufreq.current:.2f}Mhz\n"
    # CPU usage
    reply += "CPU Usage Per Core:\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        reply += f"Core {i}: {percentage}%\n"
    reply += f"Total CPU Usage: {psutil.cpu_percent()}%\n"
    return reply

def get_memory_info():
    """
    This function gets the memory information
    :return: a string with memory information divided by \n
    """
    reply = " Memory @"
    # get the memory details
    svmem = psutil.virtual_memory()
    reply += f"Total: {get_size(svmem.total)}\n"
    reply += f"Available: {get_size(svmem.available)}\n"
    reply += f"Used: {get_size(svmem.used)}\n"
    reply += f"Percentage: {svmem.percent}%\n"
    return reply

def get_swap_memory_info():
    """
    This function gets the swap memory information
    swap memory is the overflow of memory that doesn't fit the RAM storage limit,
    which is placed on the hard drive.
    :return: a string with swap memory information divided by \n
    """
    reply = " SWAP @"
    # get the swap memory details(if exists)
    swap = psutil.swap_memory()
    reply += f"Total: {get_size(swap.total)}\n"
    reply += f"Free: {get_size(swap.free)}\n"
    reply += f"Used: {get_size(swap.used)}\n"
    reply += f"Percentage: {swap.percent}%\n"
    return reply

def get_disk_info():
    """
    This function gets the disk information
    :return: a string with disk information divided by \n
    """
    reply = "Disk @"
    reply += "Partitions and Usage:\n"
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        reply += f"=== Device: {partition.device} ===\n"
        reply += f"  Mountpoint: {partition.mountpoint}\n"
        reply += f"  File system type: {partition.fstype}\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be caught due to the disk that isn't ready
            continue
        reply += f"  Total Size: {get_size(partition_usage.total)}\n"
        reply += f"  Used: {get_size(partition_usage.used)}\n"
        reply += f"  Free: {get_size(partition_usage.free)}\n"
        reply += f"  Percentage: {partition_usage.percent}%\n"
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    reply += f"Total read: {get_size(disk_io.read_bytes)}\n"
    reply += f"Total write: {get_size(disk_io.write_bytes)}\n"
    return reply

def get_gpu_info():
    """
    This function gets the GPU info
    :return: a string with the GPU information divided by \n
    """
    reply = "GPU @"
    gpus = GPUtil.getGPUs()

    for gpu in gpus:
        reply += "================"
        # get the GPU id
        reply += f"GPU ID: {gpu.id}\n"
        # name of GPU
        reply += f"Name: {gpu.name}\n"
        # get % percentage of GPU usage of that GPU
        reply += f"Load percent: {gpu.load * 100}%\n"
        # get free memory in MB format
        reply += f"Free memory: {gpu.memoryFree}MB\n"
        # get used memory
        reply += f"Used memory: {gpu.memoryUsed}MB\n"
        # get total memory
        reply += f"Total memory: {gpu.memoryTotal}MB\n"
        # get GPU temperature in Celsius
        reply += f"Temperature: {gpu.temperature} °C\n"
        reply += f"UUID: {gpu.uuid}\n"
    return reply

def get_network_info():
    """
    This function gets the network information
    :return: a string with network information divided by \n
    """
    reply = "Network Information @"
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        reply += f"=== Interface: {interface_name} ===\n"
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                reply += f"  IP Address: {address.address}\n"
                reply += f"  Netmask: {address.netmask}\n"
                reply += f"  Broadcast IP: {address.broadcast}\n"
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                reply += f"  MAC Address: {address.address}\n"
                reply += f"  Netmask: {address.netmask}\n"
                reply += f"  Broadcast MAC: {address.broadcast}\n"
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    reply += f"Total Bytes Sent: {get_size(net_io.bytes_sent)}\n"
    reply += f"Total Bytes Received: {get_size(net_io.bytes_recv)}\n"
    return reply


