import tkinter as tk
from typing import Callable

from src import setups
from src.database import Database


class ResultWindow:
    def __init__(
        self,
        root: tk.Tk,
        username: str,
        result: int,
        correct_keys: int,
        total_keys: int,
        list_of_words: list[str],
        menu_callback: Callable,
    ):
        self.menu_callback = menu_callback

        accuracy = int(correct_keys / total_keys * 100)  # in %

        self.mainframe = tk.Frame(root, bg=setups.BackgroundColor)
        self.mainframe.pack(fill=tk.BOTH, expand=1)

        tk.Button(self.mainframe, text='Главное меню', command=self.open_menu, font=setups.ButtonsFont).pack(
            side=tk.TOP, anchor=tk.NE
        )

        combined_frame = tk.Frame(self.mainframe, bg='grey')
        combined_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(combined_frame, text='Завершенные слова:', font=setups.MainInfoFont).pack(pady=5)
        for word in list_of_words:
            tk.Label(combined_frame, text=word, font=setups.MainInfoFont).pack()

        combined_frame = tk.Frame(self.mainframe)
        combined_frame.pack(expand=1)
        tk.Label(combined_frame, text=username, font=setups.MainInfoFont).pack(pady=5, padx=5)
        tk.Label(combined_frame, text=f'Завершенных слов: {result}', font=setups.MainInfoFont).pack(pady=5, padx=5)
        tk.Label(combined_frame, text=f'Верных символов: {correct_keys}', font=setups.MainInfoFont).pack(pady=5, padx=5)
        tk.Label(combined_frame, text=f'Точность ввода: {accuracy} %', font=setups.MainInfoFont).pack(pady=5, padx=5)

        Database().safe_result(username, result, correct_keys, accuracy)

        root.mainloop()

    def open_menu(self):
        self.mainframe.destroy()
        self.menu_callback()
