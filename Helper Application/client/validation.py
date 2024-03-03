# validation.py

import socket
from tkinter import messagebox
import tkinter as tk


def validate_ip_address(address):
    """
    Validate an IP address.
    :param address: Input IP address
    :return: Valid IP address or False if invalid
    """
    try:
        parts = address.split(".")
    except Exception as e:
        print(f"Problem in split: {address}, {e}")
        return False

    if len(parts) != 4:
        print("IP address {} is not valid".format(address))
        return False

    for part in parts:
        try:
            num = int(part)
            if not 0 <= num <= 255:
                print("IP address {} is not valid".format(address))
                return False
        except ValueError:
            print("IP address {} is not valid".format(address))
            return False

    print("IP address {} is valid".format(address))
    return address


def validate_code(code_entry):
    """
    Validate a code entry.
    :param code_entry: Code entry widget
    :return: Valid server code or False if invalid
    """
    if code_entry == "":
        return False

    str_code = code_entry.get()
    print(str_code)

    if not str_code.isdigit():
        tk.messagebox.showerror("Error", "Code must be a number.")
        code_entry.delete(0, "end")
        return False

    serverCode = int(str_code)
    return serverCode


def is_active_socket(sock):
    """
    Check if a socket is active.
    :param sock: Socket object
    :return: True if the socket is active, False otherwise
    """
    # Get the real file descriptor value of the socket
    fileno = sock.fileno()
    return fileno != (-1)
