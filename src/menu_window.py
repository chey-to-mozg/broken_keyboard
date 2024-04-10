import tkinter as tk
import webbrowser
from typing import Callable

from src import setups


class MainMenu:
    def __init__(self, root: tk.Tk, set_user_callback: Callable, open_leaderboard_callback: Callable):
        self.set_user_callback = set_user_callback
        self.open_leaderboard_callback = open_leaderboard_callback

        self._username = tk.StringVar(value='@telegram_tag')

        self._init_controls(root)

        root.mainloop()

    def _init_controls(self, root: tk.Tk):
        self._mainframe = tk.Canvas(root, bg=setups.BackgroundColor)
        self._mainframe.pack(fill=tk.BOTH, expand=1)

        tk.Button(
            self._mainframe,
            text='Таблица лидеров',
            command=self._open_leaderboard,
            font=setups.ButtonsFont,
        ).pack(side=tk.TOP, anchor=tk.NE)

        combined_frame = tk.Frame(self._mainframe, bg='#808080')
        combined_frame.pack(expand=1)

        tk.Label(combined_frame, text='Введи свой телеграм-ник', font=setups.MainInfoFont).pack(pady=5, padx=5)
        tk.Label(
            combined_frame,
            text='так мы сможем связаться с победителями',
            font=setups.AdditionalInfoFont,
        ).pack(pady=5, padx=5)

        # add placeholder instead of initial value
        tk.Entry(combined_frame, width=20, textvariable=self._username, font=setups.MainInfoFont).pack(pady=5, padx=5)

        tk.Button(
            combined_frame,
            text="Начать игру",
            command=self._set_user_and_start,
            font=setups.ButtonsFont,
        ).pack(pady=5, padx=5)

        policy_text = tk.Label(
            self._mainframe,
            text='Мы не будем передавать твои контакты рекрутерам, слать рассылки.\n'
            'Нам просто нужно как-то сообщить о результатах игры победителям.\n'
            'Но для этого нужно твое согласие:',
            font=setups.AdditionalInfoFont,
        )
        policy_link = tk.Label(
            self._mainframe,
            text='Согласие на обработку персональных данных',
            fg='blue',
            font=setups.AdditionalInfoFont,
        )
        policy_link.bind('<Button-1>', self._open_link)
        policy_link.pack(side=tk.BOTTOM)
        policy_text.pack(side=tk.BOTTOM)

        image = tk.PhotoImage(file='test.png')
        self._mainframe.create_image(10, 10, anchor=tk.NW, image=image)

    def _set_user_and_start(self, *args):
        self._mainframe.destroy()
        self.set_user_callback(self._username.get())

    def _open_leaderboard(self, *args):
        self._mainframe.destroy()
        self.open_leaderboard_callback()

    def _open_link(self, *args):
        link = 'https://engineer.yadro.com/wp-content/uploads/2024/03/privacy-policy.pdf'
        webbrowser.open(link)
