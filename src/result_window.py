import tkinter as tk
from typing import Callable

from src import common, setups
from src.database import Database


class ResultWindow:
    def __init__(
        self,
        root: tk.Tk,
        username: str,
        results: common.GameResults
    ):

        # TODO move accuracy calculation to the class
        accuracy = int(results.correct_keys / results.total_keys * 100)  # in %

        self._init_controls(root, username, results)

        Database().safe_result(username, results.total_words, results.correct_keys, accuracy)

    def _init_controls(self, root: tk.Tk, username: str, results: common.GameResults):
        # TODO create inheritance classes with default background
        self._mainframe = tk.Canvas(root, bg=setups.BackgroundColor)
        self._mainframe.pack(fill=tk.BOTH, expand=1)

        combined_frame = tk.Frame(self._mainframe, bg=setups.BackgroundColor)
        combined_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=(103, 0), pady=(180, 0))

        tk.Label(
            combined_frame,
            text='ЗАВЕРШЕННЫЕ СЛОВА',
            font=setups.ResultHeaderFont,
            bg=setups.BackgroundColor,
            fg=setups.BlueTextColor,
        ).pack(anchor=tk.NW, pady=5)
        for word in results.correct_words:
            tk.Label(combined_frame, text=word.upper(), font=setups.ResultWordFont, bg=setups.BackgroundColor).pack(
                anchor=tk.NW, pady=5
            )

        # results
        self.panel_with_results_image = common.load_image('panel_with_results')
        combined_frame = tk.Canvas(
            self._mainframe,
            bg=setups.BackgroundColor,
            height=self.panel_with_results_image.height() + 10,
            width=self.panel_with_results_image.width() + 10,
            highlightthickness=0,
        )
        combined_frame.pack_propagate(False)
        combined_frame.create_image(5, 5, anchor=tk.NW, image=self.panel_with_results_image)
        combined_frame.pack(side=tk.LEFT, anchor=tk.N, padx=(340, 0), pady=(385, 0))

        tk.Label(
            combined_frame,
            text=username,
            font=setups.MainInfoFontBigBold,
            bg=setups.PanelBackgroundColor,
        ).pack(pady=(80, 0))

        row_frame = tk.Frame(combined_frame)
        tk.Label(
            row_frame,
            text='ЗАВЕРШЕННЫХ СЛОВ: ',
            font=setups.StatsFont,
            bg=setups.PanelBackgroundColor,
        ).pack(side=tk.LEFT)
        tk.Label(
            row_frame,
            text=results.total_words,
            font=setups.StatsFontBold,
            bg=setups.PanelBackgroundColor,
            fg=setups.BlueTextColor,
        ).pack(side=tk.LEFT)
        row_frame.pack(pady=(30, 0))

        row_frame = tk.Frame(combined_frame)
        tk.Label(
            row_frame,
            text='ВЕРНЫХ СИМВОЛОВ: ',
            font=setups.StatsFont,
            bg=setups.PanelBackgroundColor,
        ).pack(side=tk.LEFT)
        tk.Label(
            row_frame,
            text=results.correct_keys,
            font=setups.StatsFontBold,
            bg=setups.PanelBackgroundColor,
            fg=setups.BlueTextColor,
        ).pack(side=tk.LEFT)
        row_frame.pack(pady=(30, 0))

        accuracy = int(results.correct_keys / results.total_keys * 100)  # in %
        row_frame = tk.Frame(combined_frame)
        tk.Label(
            row_frame,
            text='ТОЧНОСТЬ: ',
            font=setups.StatsFont,
            bg=setups.PanelBackgroundColor,
        ).pack(side=tk.LEFT)
        tk.Label(
            row_frame,
            text=f'{accuracy}%',
            font=setups.StatsFontBold,
            bg=setups.PanelBackgroundColor,
            fg=setups.BlueTextColor,
        ).pack(side=tk.RIGHT)
        row_frame.pack(pady=(30, 0))

        button = common.gen_button(self._mainframe, 'menu_button', self._open_menu)
        button.pack(side=tk.TOP, anchor=tk.NE, padx=60, pady=60)

        self.logo_image = common.load_image('logo')
        self._mainframe.create_image(94, 60, anchor=tk.NW, image=self.logo_image)

        self.bug = common.load_image('bug_say')
        self._mainframe.create_image(450, 400, anchor=tk.NW, image=self.bug)

    def _open_menu(self, *args):
        self._mainframe.quit()
        self._mainframe.destroy()

    def render_window(self):
        self._mainframe.mainloop()


