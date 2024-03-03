from tkinter import *
from tkinter import Listbox


class MultiListbox(Frame):

    def __init__(self, master, lists):
        # Initialize the MultiListbox class
        Frame.__init__(self, master)

        # Create a vertical scrollbar
        sb = Scrollbar(self, orient="vertical", command=self.OnVsb)
        sb.pack(side="right", fill="y")

        # Initialize the lists attribute
        self.lists = []

        # Create Listbox widgets based on the provided lists
        for to_write, w in lists:
            frame = Frame(self, height=40)
            frame.pack(side=LEFT, expand=YES, fill=BOTH)

            # Create labels for each Listbox
            Label(frame, text=to_write, borderwidth=1, relief=RAISED).pack(fill=X)

            # Create Listbox with specified properties
            lb = Listbox(frame, width=w, borderwidth=1, selectborderwidth=1,
                         relief=FLAT, exportselection=FALSE, height=40, yscrollcommand=sb.set)
            lb.pack(expand=NO, fill=BOTH)
            self.lists.append(lb)

            # Bind events to Listbox widgets
            lb.bind("<MouseWheel>", self.OnMouseWheel)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))



    def delete_all(self):
        # Delete all lines from MultiListbox
        names = list(self.lists[1].get(0, END))
        for name in names:
            self.delete_by_name(name)

    def delete_by_name(self, name):
        # Delete entries by name from MultiListbox
        names = list(self.lists[1].get(0, END))
        i = 0
        while i < len(names):
            if names[i] == name:
                process = self.get_all_process(i)
                self.delete(process)
                names = list(self.lists[1].get(0, END))
                i = 0
            else:
                i = i + 1

    def set_select_by_id(self, id):
        # Set the selection by ID in MultiListbox
        if id[0] != "":
            idis = list(self.lists[0].get(0, END))
            i = 0
            while i < len(idis):
                if idis[i] == id:
                    process = self.get_all_process(i)
                    length = len(process)
                    self.selection_set(i)
                    return
                i = i + 1
        return

    def get_all_process(self, idx):
        # Get the list of processes for a given index
        process = []
        for item in self.lists:
            process.append(list(item.get(0, END))[idx])
        return process

    def _select(self, y):
        # Handle the selection event
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        return 'break'

    def _button2(self, x, y):
        # Handle the button2 event
        for list1 in self.lists:
            list1.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        # Handle the b2motion event
        for list1 in self.lists:
            list1.scan_dragto(x, y)
        return 'break'

    def curselection(self):
        # Get the current selection
        all_selected = []
        for i in range(len(self.lists)):
            current = self.lists[i].curselection()
            total = ""
            for j in current:
                total = total + self.lists[i].get(j)
            all_selected.append(total)
        return all_selected

    def delete(self, process):
        # Delete a process from MultiListbox
        id = list(self.lists[0].get(0, END))
        for i in range(len(process)):
            looking = list(self.lists[i].get(0, END))
            for j in range(len(looking)):
                if looking[j] == process[i] and id[j] == process[0]:
                    self.lists[i].delete(j)



    def insert(self, index, *elements):
        # Insert elements at a specific index
        for e in elements:
            i = 0
            for list1 in self.lists:
                list1.insert(index, e[i])
                i = i + 1

    def selection_clear(self, first, last=None):
        for list1 in self.lists:
            list1.selection_clear(first, last)

    def selection_set(self, first, last=None):
        for list1 in self.lists:
            list1.selection_set(first, last)

    def OnVsb(self, *args):
        # Handle vertical scrollbar movement
        for lst in self.lists:
            lst.yview(*args)

    def OnMouseWheel(self, event):
        # Handle mouse wheel scrolling
        e = event.delta
        unit = 1
        if e > 0:
            unit = -1
        for lst in self.lists:
            lst.yview_scroll(unit, "units")
        # This prevents default bindings from firing, which would end up scrolling the widget twice
        return "break"


