import tkinter as tk
from timeclocks.view import MainFrame

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Timeclocks (Ctrl+S to export time as .txt)")

        MainFrame(self).grid()