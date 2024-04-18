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
        self._mainframe = tk.Canvas(root, bg=setups.BackgroundColor)
        self._mainframe.pack(fill=tk.BOTH, expand=1)

        db = Database()
        results_to_render = db.get_table_results()

        table_frame = tk.Frame(self._mainframe, bg=setups.BackgroundColor)
        table_frame.pack(side=tk.LEFT, anchor=tk.CENTER, padx=(729, 0))

        self.results_header_image = common.load_image('results_header')
        header_label = tk.Label(table_frame, image=self.results_header_image, borderwidth=0, highlightthickness=0, bg=setups.BackgroundColor)
        header_label.pack(side=tk.TOP)

        self.results_body_image = common.load_image('results_body')
        self.results_body_image = self.results_body_image.zoom(1, len(results_to_render) + 2)
        results_frame = tk.Canvas(
            table_frame,
            bg=setups.BackgroundColor,
            height=self.results_body_image.height(),
            width=self.results_body_image.width() + 10,
            borderwidth=0,
            highlightthickness=0,
        )
        results_frame.pack_propagate(False)
        results_frame.create_image(5, 0, anchor=tk.NW, image=self.results_body_image)

        tk.Label(results_frame, text='ТАБЛИЦА ЛИДЕРОВ (ТОП-20):', font=setups.MainInfoFontBold, bg=setups.PanelBackgroundColor).pack(
            side=tk.TOP
        )

        # make array and add loop to row generation
        position_header = 'Позиция'
        tag_header = 'Телеграм тэг'
        result_header = 'Верных слов'
        total_keys_header = 'Верных символов'
        accuracy_header = 'Точность ввода'
        position_combined_frame = tk.Frame(results_frame, bg=setups.PanelBackgroundColor)
        tag_combined_frame = tk.Frame(results_frame, bg=setups.PanelBackgroundColor)
        result_combined_frame = tk.Frame(results_frame, bg=setups.PanelBackgroundColor)
        headers = [position_header, tag_header, result_header]
        frames = [position_combined_frame, tag_combined_frame, result_combined_frame]
        for header, frame in zip(headers, frames):
            tk.Label(frame, text=header, bg=setups.PanelBackgroundColor, font=setups.MainInfoFont).pack(side=tk.TOP)

        # generate table with correct sizes
        for res_idx, (name, result) in enumerate(results_to_render.items()):
            position = f'{res_idx + 1}.'
            row = []
            row_values = [position, name, str(result[0])]  #, str(result[1]), str(result[2])]
            for value, frame in zip(row_values, frames):
                tk.Label(frame, text=value, font=setups.MainInfoFont, bg=setups.PanelBackgroundColor).pack(
                    side=tk.TOP
                )

        position_combined_frame.pack(side=tk.LEFT, expand=1, anchor=tk.E)
        tag_combined_frame.pack(side=tk.LEFT, expand=1)
        result_combined_frame.pack(side=tk.LEFT, expand=1, anchor=tk.W)

        results_frame.pack(side=tk.TOP)

        self.results_footer_image = common.load_image('results_footer')
        footer_label = tk.Label(table_frame, image=self.results_footer_image, borderwidth=0, highlightthickness=0, bg=setups.BackgroundColor)
        footer_label.pack(side=tk.TOP)

        button = common.gen_button(self._mainframe, 'menu_button', self._open_menu)
        button.pack(side=tk.RIGHT, anchor=tk.NE, padx=60, pady=60)

        self.logo_image = common.load_image('logo')
        self._mainframe.create_image(94, 60, anchor=tk.NW, image=self.logo_image)

        self.bug = common.load_image('bug_say')
        self._mainframe.create_image(350, 400, anchor=tk.NW, image=self.bug)

    def _spaces(self, num: int):
        if num <= 0:
            spaces = ''
        else:
            spaces = ''.join([' '] * num)
        return spaces

    def _open_menu(self, *args):
        self._mainframe.destroy()
        self._open_menu_callback()
