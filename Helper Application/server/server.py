# server.py

import socket
import threading
import sys
from tkinter import *
import random
from proccess_win import client_window

# Global variables to store the list of connected clients and their addresses
global list_clients
global addresses

# Server configuration
PORT = 4000
HOST = socket.gethostbyname(socket.gethostname())
address = (HOST, PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(address)


def handle_client(client, client_address, login_code):
    """
    Handle communication with a client.
    :param client: Client socket
    :param client_address: Client address
    :param login_code: Code for validating the client
    """
    global list_clients
    global addresses
    try:
        print("TM HELPER. Connected to %s:%s" % client_address)

        # Receive the login code from the client
        client_code = client.recv(1024).decode()

        # Validate the received code with the server's login code
        if int(client_code) == login_code:
            print("Equal: " + client_code)
            # Send success message to the client
            client.send("success".encode())

            # Receive client name from the client
            client_name = client.recv(1024).decode()

            # Add the client and its address to the global lists
            list_clients.append(client)
            addresses[client] = client_address

            # Open a new window for the client using client_window function
            client_window(client, client_name)
        else:
            # Send a message to the client indicating the wrong code
            client.send("Wrong_code".encode())
            print("Wrong code from client")
    except socket.error as err:
        print(err)
        print('Error handling client')
    finally:
        # Close the client socket
        client.close()


def accept_new_clients():
    """
    Accept new clients and start a thread to handle each client.
    """
    global SERVER
    global list_clients
    global addresses
    list_clients = []
    addresses = {}
    try:
        print("Listening...")
        SERVER.listen(5)
    except socket.error as err:
        print(err)
        print('Error creating server')
        sys.exit(1)

    while True:
        # Accept a new client connection
        (client, client_address) = SERVER.accept()

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client, client_address, login_code))
        client_handler.start()


def create_window():
    """
    Create the initial login window for the server.
    """
    global login_code
    global SERVER
    log_root = Tk()
    log_root.title("TM HELPER")
    log_root.quit()
    canvas1 = Canvas(log_root, width=500, height=300)
    canvas1.pack()

    # Generate a random login code for the server
    login_code = random.randint(100000, 999999)

    # Display login information in the GUI window
    w = Label(log_root, text="Give this login data to user:\n\n\n  IP Address:    " +
                             HOST + "\n\n Random Code:          " + str(login_code),
              pady=30, font=('calibri', 16, 'bold'), fg="#008080")
    w.place(relx=0.5, rely=0, anchor='n')
    log_root.mainloop()

    # Close the server socket when the GUI window is closed
    SERVER.close()


def main():
    # Create a thread for the GUI window
    create_window_thread = threading.Thread(target=create_window)
    create_window_thread.daemon = True
    create_window_thread.start()

    # Start the thread to accept new clients
    accept_clients_thread = threading.Thread(target=accept_new_clients)
    accept_clients_thread.daemon = True
    accept_clients_thread.start()

    # Wait for the GUI thread to finish before exiting
    create_window_thread.join()
    accept_clients_thread.join()

    # Print the list of clients and addresses
    print(list_clients, addresses)

    # Close the server socket
    SERVER.close()
    print("Server is closed")
    sys.exit(0)


if __name__ == "__main__":
    main()
