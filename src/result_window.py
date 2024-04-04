import tkinter as tk
from typing import Callable
from src.database import Database


class ResultWindow:
    def __init__(self, root: tk.Tk, username: str, result: int, list_of_words: list[str], menu_callback: Callable):
        self.menu_callback = menu_callback

        self.mainframe = tk.Frame(root, bg='green')
        self.mainframe.pack(fill=tk.BOTH, expand=1)

        tk.Button(self.mainframe, text='Main menu', command=self.open_menu).pack(side=tk.TOP, anchor=tk.NE)

        listbox = tk.Listbox(self.mainframe, height=5)
        listbox.pack(side=tk.LEFT)

        # in case of many words:
        # scrollbar = tk.Scrollbar(self.mainframe, orient=tk.VERTICAL, command=listbox.yview)
        # scrollbar.pack(side=tk.LEFT)

        for word in list_of_words:
            listbox.insert('end', word)

        combined_frame = tk.Frame(self.mainframe)
        combined_frame.pack(expand=1)
        tk.Label(combined_frame, width=20, text=username).pack(pady=5, padx=5)
        tk.Label(combined_frame, text=f'Score: {result}').pack(pady=5, padx=5)

        Database().safe_result(username, result)

        root.mainloop()

    def open_menu(self):
        self.mainframe.destroy()
        self.menu_callback()

