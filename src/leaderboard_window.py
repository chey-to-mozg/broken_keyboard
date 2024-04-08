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
        tk.Label(self.mainframe, text='Результаты:', font=setups.MainInfoFont).pack(side=tk.TOP)
        max_tag_len = 0
        for tag in db.results.keys():
            if len(tag) > max_tag_len:
                max_tag_len = len(tag)
        # make array and add loop to row generation
        position_header = 'Позиция  '
        tag_header = 'Телеграм тэг'
        tag_header = f'{tag_header}{self.spaces(max_tag_len - len(tag_header))}  '
        result_header = 'Верных слов  '
        total_keys_header = 'Верных символов  '
        accuracy_header = 'Точность ввода'
        tk.Label(
            self.mainframe,
            text=position_header + tag_header + result_header + total_keys_header + accuracy_header,
            font=setups.MainInfoFont,
        ).pack(side=tk.TOP)
        # generate table with correct sizes
        for res_idx, (name, result) in enumerate(db.results.items()):
            position = f'{res_idx + 1}.'
            position = f'{position}{self.spaces(len(position_header) - len(position))}'
            name = f'{name}{self.spaces(len(tag_header) - len(name))}'
            result_words = str(result[0])
            result_words = f'{result_words}{self.spaces(len(result_header) - len(result_words))}'
            total_keys = str(result[1])
            total_keys = f'{total_keys}{self.spaces(len(total_keys_header) - len(total_keys))}'
            accuracy = str(result[2])
            accuracy = f'{accuracy}{self.spaces(len(accuracy_header) - len(accuracy))}'
            tk.Label(
                self.mainframe, text=position + name + result_words + total_keys + accuracy, font=setups.MainInfoFont
            ).pack(side=tk.TOP)

        root.mainloop()

    def spaces(self, num: int):
        if num <= 0:
            spaces = ''
        else:
            spaces = ''.join([' '] * num)
        return spaces

    def open_menu(self):
        self.mainframe.destroy()
        self.open_menu_callback()
