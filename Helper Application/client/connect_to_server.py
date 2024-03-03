from api import api_server
import tkinter as tk
import socket
import threading
from tkinter import messagebox
from validation import validate_code, validate_ip_address
import tkinter.ttk as ttk
from user_display import window

global connection_win
global client_socket
server_port = 4000


def open_window():
    global connection_win
    connection_win = tk.Tk()
    s = ttk.Style()
    s.configure('my.TButton', font=('calibre', 16, 'bold'), foreground='#008080', background="#008080")
    windowWidth = connection_win.winfo_reqwidth()
    windowHeight = connection_win.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(connection_win.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(connection_win.winfo_screenheight() / 2 - windowHeight / 2)
    # Positions the window in the center of the page.
    connection_win.geometry("+{}+{}".format(positionRight, positionDown))
    connection_win.title('Easy Support Service')
    connection_win.resizable(True, True)
    welcome_label = tk.Label(connection_win, text="Contact your admin for connection data", font=40, fg="white",
                             bg="#008080", padx=10)
    welcome_label.pack()
    ip_label = tk.Label(connection_win, text="IP Address", font=('calibre', 16, 'bold'), pady=10, padx=20, fg="#008080")
    ip_label.pack()
    ipaddress = tk.StringVar()
    ip_address_Entry = tk.Entry(connection_win, textvariable=ipaddress, font=('calibre', 16, 'bold'),
                                highlightthickness=2, highlightbackground="#008080")
    ip_address_Entry.pack(fill="both", pady=10, padx=20)
    # ip_address_Entry.insert(0, "192.168.1.221")
    code_label = tk.Label(connection_win, text="Code", font=('calibre', 16, 'bold',), pady=10, padx=20, fg="#008080")
    code_label.pack()
    code = tk.StringVar()
    code_entry = tk.Entry(connection_win, textvariable=code, font=('calibre', 16, 'bold'),
                          highlightthickness=2, highlightbackground="#008080")
    code_entry.pack(fill="both", padx=20, pady=10)
    # validateLogin = partial(validate_login, ipaddress, port)
    login_button = ttk.Button(connection_win, text="Connect", style='my.TButton',
                              command=lambda: connect_to_server("Neta", ip_address_Entry.get(), code_entry))
    login_button.pack(fill="both", padx=20, pady=10)
    connection_win.mainloop()

def connect_to_server(name, ipaddress, code):
    global client_socket
    global connection_win
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = validate_ip_address(ipaddress)
    server_code = validate_code(code)

    if server_ip and server_code:
        try:
            client_socket.connect((server_ip, server_port))
        except socket.error as E:
            print("Can't connect:", E)
            messagebox.showerror("Incorrect input", "Connection error \nPlease check the input and try again")
            return

        client_socket.send(
            str(server_code).encode())
        res = client_socket.recv(1024).decode()
        while res == "Wrong_code":
            messagebox.showerror("Error", "Incorrect code")
            print("client status", client_socket)
            client_socket.close()
            client_socket.connect((server_ip, server_port))
            client_socket.send(str(server_code).encode())
            res = client_socket.recv(1024).decode()

        if res == "success":
            print(socket.gethostbyname(socket.gethostname()))
            client_socket.send(name.encode())
            hold = threading.Thread(target=api_server, args=(client_socket,))
            connection_win.destroy()
            waiting_window = threading.Thread(target=window, args=(client_socket,))
            waiting_window.start()
            hold.start()

    else:
        messagebox.showerror("Incorrect input", "Please check the data and try again")
