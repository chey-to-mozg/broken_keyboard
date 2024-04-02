import tkinter as tk
from tkinter import ttk
from functools import partial
from typing import Callable


class MainMenu:
    def __init__(self, root: tk.Tk, set_user_callback: Callable):
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky='NWES')

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Button(self.mainframe, text='Leaderboard', command=None).grid(row=1, column=3)

        self.username = tk.StringVar(value='@username')

        username_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.username)
        username_entry.grid(row=2, column=2, sticky='WE')

        ttk.Button(self.mainframe, text="Start game", command=partial(self.set_user, set_user_callback)).grid(row=3, column=2, sticky='W')

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        username_entry.focus()
        root.mainloop()

    def set_user(self, callback: Callable, *args):
        self.mainframe.destroy()
        callback(self.username.get())


