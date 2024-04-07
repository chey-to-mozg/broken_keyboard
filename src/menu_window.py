import tkinter as tk
import webbrowser
from typing import Callable

from src import setups


class MainMenu:
    def __init__(self, root: tk.Tk, set_user_callback: Callable, open_leaderboard_callback: Callable):
        self.set_user_callback = set_user_callback
        self.open_leaderboard_callback = open_leaderboard_callback

        self.mainframe = tk.Canvas(root, bg=setups.BackgroundColor)
        self.mainframe.pack(fill=tk.BOTH, expand=1)

        self.username = tk.StringVar(value='@telegram_tag')

        self.leaderboard_button = tk.Button(
            self.mainframe,
            text='Таблица лидеров',
            command=self.open_leaderboard,
            font=setups.ButtonsFont,
        )
        self.leaderboard_button.pack(side=tk.TOP, anchor=tk.NE)

        combined_frame = tk.Frame(self.mainframe, bg='#808080')
        combined_frame.pack(expand=1)

        username_description = tk.Label(combined_frame, text='Введи свой телеграм-ник', font=setups.MainInfoFont)
        username_description.pack(pady=5, padx=5)

        username_description = tk.Label(
            combined_frame, text='так мы сможем связаться с победителями', font=setups.AdditionalInfoFont
        )
        username_description.pack(pady=5, padx=5)

        username_entry = tk.Entry(combined_frame, width=20, textvariable=self.username, font=setups.MainInfoFont)
        username_entry.pack(pady=5, padx=5)

        start_button = tk.Button(
            combined_frame, text="Начать игру", command=self.set_user_and_start, font=setups.ButtonsFont
        )
        start_button.pack(pady=5, padx=5)

        policy_text = tk.Label(
            self.mainframe,
            text='Мы не будем передавать твои контакты рекрутерам, слать рассылки.\n'
            'Нам просто нужно как-то сообщить о результатах игры победителям.\n'
            'Но для этого нужно твое согласие:',
            font=setups.AdditionalInfoFont,
        )
        policy_link = tk.Label(
            self.mainframe,
            text='Согласие на обработку персональных данных',
            fg='blue',
            font=setups.AdditionalInfoFont,
        )
        policy_link.bind('<Button-1>', self.open_link)
        policy_link.pack(side=tk.BOTTOM)
        policy_text.pack(side=tk.BOTTOM)

        image = tk.PhotoImage(file='test.png')
        self.mainframe.create_image(10, 10, anchor=tk.NW, image=image)

        username_entry.focus()
        root.mainloop()

    def set_user_and_start(self, *args):
        self.mainframe.destroy()
        self.set_user_callback(self.username.get())

    def open_leaderboard(self, *args):
        self.mainframe.destroy()
        self.open_leaderboard_callback()

    def open_link(self, *args):
        link = 'https://engineer.yadro.com/wp-content/uploads/2024/03/privacy-policy.pdf'
        webbrowser.open(link)
