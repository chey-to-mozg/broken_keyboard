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

        # TODO move accuracy calculation to the class
        accuracy = int(results.correct_keys / results.total_keys * 100)  # in %

        self._init_controls(root, username, results, list_of_words)

        Database().safe_result(username, results.total_words, results.correct_keys, accuracy)

        root.mainloop()

    def _init_controls(self, root: tk.Tk, username: str, results: common.GameResults, list_of_words: list[str]):
        # TODO create inheritance classes with default background
        self._mainframe = tk.Canvas(root, bg=setups.BackgroundColor)
        self._mainframe.pack(fill=tk.BOTH, expand=1)

        self.menu_button_image = tk.PhotoImage(file=common.get_image_path('menu_button'))
        menu_button = tk.Label(self._mainframe, image=self.menu_button_image, borderwidth=0, highlightthickness=0)
        menu_button.bind("<Button-1>", self._open_menu)
        menu_button.pack(side=tk.TOP, anchor=tk.NE)

        self.logo_image = tk.PhotoImage(file=common.get_image_path('logo'))
        tk.Label(self._mainframe, image=self.logo_image, borderwidth=0, highlightthickness=0).pack(side=tk.TOP, anchor=tk.NW)
        
        combined_frame = tk.Frame(self._mainframe, bg=setups.BackgroundColor)
        combined_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=10)
        
        tk.Label(combined_frame, text='ЗАВЕРШЕННЫЕ СЛОВА', font=setups.MainInfoFont, bg=setups.BackgroundColor, fg=setups.BlueTextColor).pack(pady=5)
        for word in list_of_words:
            tk.Label(combined_frame, text=word.upper(), font=setups.MainInfoFont, bg=setups.BackgroundColor).pack(anchor=tk.NW)

        self.panel_with_results_image = tk.PhotoImage(file=common.get_image_path('panel_with_controls'))
        combined_frame = tk.Canvas(
            self._mainframe,
            bg=setups.BackgroundColor,
            height=self.panel_with_results_image.height() + 10,
            width=self.panel_with_results_image.width() + 10,
            highlightthickness=0,
        )
        combined_frame.pack_propagate(False)
        combined_frame.create_image(5, 5, anchor=tk.NW, image=self.panel_with_results_image)
        combined_frame.pack(expand=1)

        tk.Label(combined_frame, text=username, font=setups.MainInfoFontBigBold, bg=setups.PanelBackgroundColor,).pack(expand=1, pady=5, padx=5)
        tk.Label(
            combined_frame,
            text=f'ЗАВЕРШЕННЫХ СЛОВ: {results.total_words}',
            font=setups.MainInfoFont,
            bg=setups.PanelBackgroundColor,
        ).pack(expand=1, pady=5, padx=5)
        tk.Label(
            combined_frame,
            text=f'ВЕРНЫХ СИМВОЛОВ: {results.total_keys}',
            font=setups.MainInfoFont,
            bg=setups.PanelBackgroundColor,
        ).pack(expand=1, pady=5, padx=5)

        accuracy = int(results.correct_keys / results.total_keys * 100)  # in %
        tk.Label(combined_frame, text=f'ТОЧНОСТЬ: {accuracy} %', font=setups.MainInfoFont, bg=setups.PanelBackgroundColor,).pack(expand=1, pady=5, padx=5)

    def _open_menu(self, *args):
        self._mainframe.destroy()
        self._menu_callback()
