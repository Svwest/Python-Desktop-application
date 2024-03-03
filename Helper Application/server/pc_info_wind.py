import socket
import sys
import tkinter
from tkinter import *
import tkinter.ttk as ttk
import json


class PcInfo:
    def __init__(self, client_socket):
        """
        Constructor for PcInfo class.

        Parameters:
        - client_socket (socket): The socket used for communication with the server.
        """
        try:
            self.client_socket = client_socket

            # Create the main Tkinter window
            root_pc = tkinter.Tk()
            root_pc.title("Computer Info")
            root_pc.geometry("732x712+375+10")
            root_pc.configure(bg="green")

            # Create the top menubar


            # Create tabs menu
            tabControl = ttk.Notebook(root_pc)
            tabControl.pack(expand=1, fill="both")

            # Create tab frames
            tab1 = ttk.Frame(tabControl)
            tab2 = ttk.Frame(tabControl)
            tab3 = ttk.Frame(tabControl)
            tab4 = ttk.Frame(tabControl)
            tab5 = ttk.Frame(tabControl)
            tab6 = ttk.Frame(tabControl)
            tab7 = ttk.Frame(tabControl)
            tab8 = ttk.Frame(tabControl)

            tab_list = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8]

            def get_pc_info():
                """
                Send a request to the server to get computer information and receive the response.

                Returns:
                - pc_info (list): List containing computer information.
                """
                try:
                    # Send request to server
                    self.client_socket.send("get_pc_info".encode())
                    # Receive and decode the response
                    received_data = self.client_socket.recv(4096).decode()
                    # Convert JSON string to a list
                    pc_info = json.loads(received_data)
                    return pc_info
                except socket.error as err:
                    print(f"Socket error: {err}")
                    sys.exit(-1)

            def display_pc_info():
                """
                Display computer information in tabs.
                """
                # Call the get_pc_info function to retrieve computer information
                pc_info = get_pc_info()

                # Populate tabs with pc_info
                for i, sublist in enumerate(pc_info):
                    key_pop = sublist.split('@')
                    # Add a new tab for each set of information
                    tabControl.add(tab_list[i], text=key_pop[0])
                    # Create a Text widget to display information in each tab
                    text_widget = Text(tabControl.winfo_children()[i], wrap="none", height=20, width=60)
                    text_widget.insert("1.0", key_pop[1])
                    text_widget.pack()

            # Call the display_pc_info function to initialize the UI
            display_pc_info()

            # Start the Tkinter main loop
            root_pc.mainloop()

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
