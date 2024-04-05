import tkinter as tk
from src.database import Database
from typing import Callable


class LeaderboardWindow:
    def __init__(self, root: tk.Tk, open_menu_callback: Callable):
        self.open_menu_callback = open_menu_callback

        self.mainframe = tk.Frame(root, bg='yellow')
        self.mainframe.pack(fill=tk.BOTH, expand=1)

        tk.Button(self.mainframe, text='Main menu', command=self.open_menu).pack(side=tk.TOP, anchor=tk.NE)

        db = Database()

        listbox = tk.Listbox(self.mainframe, height=5)
        listbox.pack(side=tk.TOP)

        for res_idx, (name, result) in enumerate(db.results.items()):
            result_row = f'{res_idx + 1}. {name}{"".join(["."]*10)}{result}'
            listbox.insert('end', result_row)

        root.mainloop()

    def open_menu(self):
        self.mainframe.destroy()
        self.open_menu_callback()