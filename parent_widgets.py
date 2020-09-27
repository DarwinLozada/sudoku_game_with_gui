import tkinter as tk



class NewRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.minsize(550, 550)
        self.maxsize(550, 550)
        self.attributes('-alpha', 0.0)
        self.icon = tk.PhotoImage(file='Images/sudoku_icon.png')
        self.iconphoto(False, self.icon)


class TopLevelWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.overrideredirect(1)
        self.minsize(550, 550)
        self.maxsize(550, 550)
