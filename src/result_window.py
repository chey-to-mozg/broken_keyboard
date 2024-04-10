import tkinter as tk
from typing import Callable

from src import setups
from src.database import Database
from src import common


class ResultWindow:
    def __init__(
        self,
        root: tk.Tk,
        username: str,
        results: common.GameResults,
        list_of_words: list[str],
        menu_callback: Callable,
    ):
        self._menu_callback = menu_callback

        accuracy = int(results.correct_keys / results.total_keys * 100)  # in %

        self._init_controls(root, username, results, list_of_words)

        Database().safe_result(username, results.total_words, results.correct_keys, accuracy)

        root.mainloop()

    def _init_controls(self, root: tk.Tk, username: str, results: common.GameResults, list_of_words: list[str]):
        self._mainframe = tk.Frame(root, bg=setups.BackgroundColor)
        self._mainframe.pack(fill=tk.BOTH, expand=1)
        
        tk.Button(
            self._mainframe,
            text='Главное меню',
            command=self._open_menu,
            font=setups.ButtonsFont,
        ).pack(side=tk.TOP, anchor=tk.NE)
        
        combined_frame = tk.Frame(self._mainframe, bg='grey')
        combined_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(combined_frame, text='Завершенные слова:', font=setups.MainInfoFont).pack(pady=5)
        for word in list_of_words:
            tk.Label(combined_frame, text=word, font=setups.MainInfoFont).pack()
        
        combined_frame = tk.Frame(self._mainframe)
        combined_frame.pack(expand=1)
        tk.Label(combined_frame, text=username, font=setups.MainInfoFont).pack(pady=5, padx=5)
        tk.Label(
            combined_frame,
            text=f'Завершенных слов: {results.total_words}',
            font=setups.MainInfoFont,
        ).pack(pady=5, padx=5)
        tk.Label(
            combined_frame,
            text=f'Верных символов: {results.total_keys}',
            font=setups.MainInfoFont,
        ).pack(pady=5, padx=5)

        accuracy = int(results.correct_keys / results.total_keys * 100)  # in %
        tk.Label(combined_frame, text=f'Точность ввода: {accuracy} %', font=setups.MainInfoFont).pack(pady=5, padx=5)

    def _open_menu(self):
        self._mainframe.destroy()
        self._menu_callback()
