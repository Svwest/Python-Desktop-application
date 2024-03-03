# window.py

import tkinter as tk
from tkinter import messagebox
from validation import is_active_socket


def window(server_socket):
    def update_label():
        """
        Update the label text based on the status of the server socket.
        If the socket is active, display a waiting message.
        If the socket is not active, display a completion message.
        """
        def disable_event():
            messagebox.showinfo('Wait', 'Please wait until the admin  will finish.')

        def close():
            root.destroy()

        if is_active_socket(server_socket):
            w.config(text="Fixing the problem....\n Please wait")
            root.after(1000, update_label)  # Re-run the check after 1000 ms (1 sec)
            root.protocol("WM_DELETE_WINDOW", disable_event)
        else:
            w.config(text="DONE \n You can quit now")
            root.protocol("WM_DELETE_WINDOW", close)

    root = tk.Tk()
    root.title("Support")

    canvas1 = tk.Canvas(root, width=400, height=100)
    canvas1.pack()

    w = tk.Label(root, text="Connecting...", font=('calibri', 14, 'bold'), fg="#008080")
    w.place(relx=0.5, rely=0, anchor='n')

    update_label()  # Checking and Update by the socket status

    return root.mainloop()
