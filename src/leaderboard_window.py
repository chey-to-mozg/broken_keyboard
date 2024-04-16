import tkinter as tk
from tkinter import ttk
from typing import Callable

from src import common
from src import setups
from src.database import Database


class LeaderboardWindow:
    def __init__(self, root: tk.Tk, open_menu_callback: Callable):
        self._open_menu_callback = open_menu_callback

        self._init_controls(root)

        root.mainloop()

    def _init_controls(self, root: tk.Tk):
        self._mainframe = tk.Frame(root, bg=setups.BlueTextColor)
        self._mainframe.pack(fill=tk.BOTH, expand=1)

        self.menu_button_image = tk.PhotoImage(file=common.get_image_path('menu_button'))
        menu_button = tk.Label(self._mainframe, image=self.menu_button_image, borderwidth=0, highlightthickness=0)
        menu_button.bind("<Button-1>", self._open_menu)
        menu_button.pack(side=tk.TOP, anchor=tk.NE)

        db = Database()
        self.results_header_image = tk.PhotoImage(file=common.get_image_path('results_header'))
        header_label = tk.Label(self._mainframe, image=self.results_header_image, borderwidth=0, highlightthickness=0)
        header_label.pack(side=tk.TOP)

        results_frame = ttk.Frame(self._mainframe, style='ResultsBody', padding=10)

        tk.Label(results_frame, text='Результаты:', font=setups.MainInfoFont).pack(side=tk.TOP)
        max_tag_len = 0
        for tag in db.results.keys():
            if len(tag) > max_tag_len:
                max_tag_len = len(tag)

        # make array and add loop to row generation
        position_header = 'Позиция  '
        tag_header = 'Телеграм тэг'
        tag_header = f'{tag_header}{self._spaces(max_tag_len - len(tag_header))}  '
        result_header = 'Верных слов  '
        total_keys_header = 'Верных символов  '
        accuracy_header = 'Точность ввода'
        tk.Label(
            results_frame,
            text=position_header + tag_header + result_header + total_keys_header + accuracy_header,
            font=setups.MainInfoFont,
        ).pack(side=tk.TOP)

        # generate table with correct sizes
        for res_idx, (name, result) in enumerate(db.results.items()):
            position = f'{res_idx + 1}.'
            row = []
            headers = [position_header, tag_header, result_header, total_keys_header, accuracy_header]
            row_values = [position, name, str(result[0]), str(result[1]), str(result[2])]
            for col_header, col_value in zip(headers, row_values):
                row.append(f'{col_value}{self._spaces(len(col_header) - len(col_value))}')
            tk.Label(results_frame, text=''.join(row), font=setups.MainInfoFont).pack(side=tk.TOP)

        results_frame.pack(side=tk.TOP)

        self.results_footer_image = tk.PhotoImage(file=common.get_image_path('results_footer'))
        footer_label = tk.Label(self._mainframe, image=self.results_footer_image, borderwidth=0, highlightthickness=0)
        footer_label.pack(side=tk.TOP)

        results_frame.update()
        results_width = results_frame.winfo_reqwidth()
        print(results_width)
        print(results_width // self.results_header_image.width())
        self.results_header_image = self.results_header_image.subsample(results_width / self.results_header_image.width(), 1)
        # header_label.config(width=results_width)
        # footer_label.config(width=results_width)

    def _spaces(self, num: int):
        if num <= 0:
            spaces = ''
        else:
            spaces = ''.join([' '] * num)
        return spaces

    def _open_menu(self, *args):
        self._mainframe.destroy()
        self._open_menu_callback()
