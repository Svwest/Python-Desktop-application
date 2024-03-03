import pickle
import socket
import sys
import threading
from functools import partial
from tkinter import *
from tkinter import ttk, messagebox
from pc_info_wind import PcInfo  # Assuming this import is correct
from multibox import MultiListbox
from task_func import terminate, refresh, change_order
def client_window(client, client_name):
    def close():
        try:
            # Send a goodbye message to the server before closing the connection
            client.send("goodbye".encode())
            # Ask for confirmation before closing the window
            response = messagebox.askyesno('Wait', "Are you sure you want to close the connection with this client?")
            if response:
                client.close()
                root.destroy()
        except Exception as e:
            print(f"Error during close: {e}")
        return
    # Create the main window
    root = Tk()
    root.title("Support - " + client_name)
    root.state('zoomed')
    root.geometry("1400x800")
    root.resizable(True, True)
    root.protocol("WM_DELETE_WINDOW", close)
    # Label for the process list
    label = Label(root, text='Process List', width=950)
    label.grid(row=0, column=0, columnspan=2)
    root.columnconfigure(0, weight=1)
    try:
        # Check if the server is ready for commands
        is_ready = client.recv(1024).decode() == "command"
        all_process = []
        if is_ready:
            # Request the list of all processes from the server
            client.send("List_all".encode())
            try:
                # Receive the length of the process list
                length = int(client.recv(1024))
            except socket.error as err:
                print(err)
                print('No received data')
                sys.exit(-1)
            # Receive and store each process information
            for _ in range(length):
                try:
                    data = pickle.loads(client.recv(4096))
                except socket.error as err:
                    print(err)
                    print('Received data wrong type')
                    sys.exit(-1)
                client.send("go".encode())
                if data[0] == "sent_all":
                    client.send("done".encode())
                    break
                else:
                    all_process.append(data)
            client.send("done".encode())
            # Create a MultiListbox to display the process information
            mlb = MultiListbox(label, (('Id', 10), ('Name', 20), ('Time', 30), ('Cores', 10), ('Cpu_usage', 20),
                                       ('Status', 20), ('Priority', 10), ('Memory usage', 10), ('Read bytes', 20),
                                       ('Write bytes', 20), ('Threads', 10), ('Username', 25)))
            # Insert each process information into the MultiListbox
            for j in range(len(all_process)):
                mlb.insert(END, all_process[j])
            mlb.pack(expand=NO, fill=BOTH)
            # Create buttons for various actions
            button_frame = Frame(root, width=450)

            s = ttk.Style()
            s.configure('my.TButton', font=('calibre', 18, 'bold'), foreground='#008080', background="#008080")

            button_frame.grid(row=0, column=3, padx=10, pady=20, sticky='nsew')
            change_order_by = partial(change_order, all_process, mlb)

            button1 = ttk.Button(button_frame,
                                 text='By NAME',
                                 style='my.TButton',
                                 width=30,
                                 command=lambda:change_order_by("name"))
            button1.grid(row=0, column=0, padx=5, pady=20)

            button2 = ttk.Button(button_frame,
                                 text='By ID',
                                 style='my.TButton',
                                 width=30,
                                 command=lambda: change_order_by("id"))
            button2.grid(row=1, column=0, padx=5, pady=20)

            button3 = ttk.Button(button_frame,
                                 text='By PRIORITY',
                                 style='my.TButton',
                                 width=30,
                                 command=lambda: change_order_by("priority"))
            button3.grid(row=2, column=0, padx=5, pady=20)

            button4 = ttk.Button(button_frame,
                                 text='By CPU USAGE',
                                 style='my.TButton',
                                 width=30,
                                command=lambda: change_order_by("cpu"))
            button4.grid(row=3, column=0, padx=5, pady=20)

            button5 = ttk.Button(button_frame,
                                 text='By MEMORY USAGE',
                                 style='my.TButton',
                                 width=30,
                                 command=lambda: change_order_by("memory"))
            button5.grid(row=4, column=0, padx=5, pady=20)

            button6 = ttk.Button(button_frame,
                                 text="REFRESH",
                                 style='my.TButton',
                                 width=30,
                                 command=lambda: refresh(client, mlb))
            button6.grid(row=5, column=0, padx=5, pady=20)

            button7 = ttk.Button(button_frame,
                                 text="Show PC Info",
                                 style='my.TButton',
                                 width=30,
                                 command=lambda: PcInfo(client))
            button7.grid(row=6, column=0, padx=5, pady=20)

            button8 = ttk.Button(button_frame,
                                 text='TERMINATE THE PROCESS',
                                 width=30,
                                 command=lambda: terminate(mlb, client),
                                 style='my.TButton')
            button8.grid(row=7, column=0, padx=5, pady=20)

            button9 = ttk.Button(button_frame,
                                 text='Close this connection',
                                 style='my.TButton',
                                 width=30,
                                 command=lambda: close)
            button9.grid(row=8, column=0, padx=5, pady=20)
        # Start the Tkinter main loop
        root.mainloop()
        close()
    except Exception as e:
        print(f"Error in client_window: {e}")
        close()
