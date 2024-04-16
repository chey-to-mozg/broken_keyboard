import tkinter as tk
from tkinter import ttk
from typing import Callable

from src import common, setups
from src.database import Database


class LeaderboardWindow:
    def __init__(self, root: tk.Tk, open_menu_callback: Callable):
        self._open_menu_callback = open_menu_callback

        self._init_controls(root)

        root.mainloop()

    def _init_controls(self, root: tk.Tk):
        self._mainframe = tk.Frame(root, bg=setups.BackgroundColor)
        self._mainframe.pack(fill=tk.BOTH, expand=1)

        button = common.gen_button(self._mainframe, 'menu_button', self._open_menu)
        button.pack(side=tk.TOP, anchor=tk.NE)

        db = Database()
        self.results_header_image = common.load_image('results_header')
        header_label = tk.Label(self._mainframe, image=self.results_header_image, borderwidth=0, highlightthickness=0)
        header_label.pack(side=tk.TOP)

        self.results_body_image = common.load_image('results_body')
        self.results_body_image = self.results_body_image.zoom(1, len(db.results) + 2)
        results_frame = tk.Canvas(
            self._mainframe,
            bg=setups.BackgroundColor,
            height=self.results_body_image.height(),
            width=self.results_body_image.width() + 10,
            borderwidth=0,
            highlightthickness=0,
        )
        results_frame.pack_propagate(False)
        results_frame.create_image(5, 0, anchor=tk.NW, image=self.results_body_image)

        tk.Label(results_frame, text='Результаты:', font=setups.MainInfoFont, bg=setups.PanelBackgroundColor).pack(
            side=tk.TOP
        )
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
            text=position_header + tag_header,  # + result_header + total_keys_header + accuracy_header,
            font=setups.MainInfoFont,
            bg=setups.PanelBackgroundColor,
        ).pack(side=tk.TOP)

        # generate table with correct sizes
        for res_idx, (name, result) in enumerate(db.results.items()):
            position = f'{res_idx + 1}.'
            row = []
            headers = [position_header, tag_header]  # , result_header, total_keys_header, accuracy_header]
            row_values = [position, name]  # , str(result[0]), str(result[1]), str(result[2])]
            for col_header, col_value in zip(headers, row_values):
                row.append(f'{col_value}{self._spaces(len(col_header) - len(col_value))}')
            tk.Label(results_frame, text=''.join(row), font=setups.MainInfoFont, bg=setups.PanelBackgroundColor).pack(
                side=tk.TOP
            )

        results_frame.pack(side=tk.TOP)

        self.results_footer_image = common.load_image('results_footer')
        footer_label = tk.Label(self._mainframe, image=self.results_footer_image, borderwidth=0, highlightthickness=0)
        footer_label.pack(side=tk.TOP)

    def _spaces(self, num: int):
        if num <= 0:
            spaces = ''
        else:
            spaces = ''.join([' '] * num)
        return spaces

    def _open_menu(self, *args):
        self._mainframe.destroy()
        self._open_menu_callback()
