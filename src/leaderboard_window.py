import tkinter as tk
from typing import Callable

from src import setups
from src.database import Database


class LeaderboardWindow:
    def __init__(self, root: tk.Tk, open_menu_callback: Callable):
        self.open_menu_callback = open_menu_callback

        self.mainframe = tk.Frame(root, bg=setups.BackgroundColor)
        self.mainframe.pack(fill=tk.BOTH, expand=1)

        tk.Button(self.mainframe, text='Главное меню', command=self.open_menu, font=setups.ButtonsFont).pack(
            side=tk.TOP, anchor=tk.NE
        )

        db = Database()

        element_width_elements = 30

        for res_idx, (name, result) in enumerate(db.results.items()):
            result_row = f'{res_idx + 1}. {name}'
            dots_num = element_width_elements - len(result_row) - len(str(result))
            result_row = f'{result_row}{"".join(["."] * dots_num)}{result}'
            tk.Label(self.mainframe, text=result_row, font=setups.MainInfoFont).pack(side=tk.TOP)

        root.mainloop()

    def open_menu(self):
        self.mainframe.destroy()
        self.open_menu_callback()
