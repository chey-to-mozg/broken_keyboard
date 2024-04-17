import tkinter as tk
import webbrowser
from tkinter import ttk
from typing import Callable

from src import common, setups


class MainMenu:
    def __init__(self, root: tk.Tk, set_user_callback: Callable, open_leaderboard_callback: Callable):
        self.set_user_callback = set_user_callback
        self.open_leaderboard_callback = open_leaderboard_callback

        self._username = tk.StringVar(value='@telegram_tag')

        self._init_controls(root)

        root.mainloop()

    def _init_controls(self, root: tk.Tk):
        self._mainframe = tk.Canvas(root, bg=setups.BackgroundColor, highlightthickness=0)
        self._mainframe.pack(fill=tk.BOTH, expand=1)

        button = common.gen_button(self._mainframe, 'table_button', self._open_leaderboard)
        button.pack(side=tk.TOP, anchor=tk.NE, padx=60, pady=60)

        self.panel_with_controls_image = common.load_image('panel_with_controls')
        control_panel = tk.Canvas(
            self._mainframe,
            bg=setups.BackgroundColor,
            height=self.panel_with_controls_image.height() + 10,
            width=self.panel_with_controls_image.width() + 10,
            highlightthickness=0,
        )
        control_panel.pack_propagate(False)
        control_panel.create_image(5, 5, anchor=tk.NW, image=self.panel_with_controls_image)
        control_panel.pack(expand=1)

        combined_frame = tk.Frame(control_panel, bg=setups.PanelBackgroundColor)
        combined_frame.pack(pady=(30, 0))

        tk.Label(
            combined_frame,
            text='Привет!',
            font=setups.MainInfoFontBigBold,
            bg=setups.PanelBackgroundColor,
        ).pack(pady=(40, 16))
        tk.Label(
            combined_frame,
            text='Введи свой телеграм-ник,',
            font=setups.MainInfoFont,
            bg=setups.PanelBackgroundColor,
        ).pack(pady=(0, 1))
        tk.Label(
            combined_frame,
            text='так мы сможем связаться с победителем',
            font=setups.MainInfoFont,
            bg=setups.PanelBackgroundColor,
        ).pack(pady=(0, 30))

        frame = ttk.Frame(combined_frame, style="RoundedFrame", padding=2, width=25, height=5)
        self.username_entity = tk.Entry(
            frame,
            textvariable=self._username,
            borderwidth=0,
            bg=setups.BackgroundColor,
            fg=setups.GrayTextColor,
            font=setups.MainInfoFontBig,
            justify='center',
            width=21,
        )
        self.username_entity.pack(expand=1, pady=(10, 10))
        self.username_entity.bind('<Button-1>', self._clear_username_entity)
        frame.pack(pady=(0, 30))

        button = common.gen_button(combined_frame, 'start_button', self._set_user_and_start)
        button.pack()

        policy_text = tk.Label(
            self._mainframe,
            text='Мы не будем передавать твои контакты рекрутерам, слать рассылки.\n'
            'Нам просто нужно как-то сообщить о результатах игры победителям.\n'
            'Но для этого нужно твое согласие:',
            font=setups.AdditionalInfoFont,
            bg=setups.BackgroundColor,
        )
        policy_link = tk.Label(
            self._mainframe,
            text='Согласие на обработку персональных данных',
            fg=setups.BlueTextColor,
            font=setups.AdditionalInfoFont,
            bg=setups.BackgroundColor,
        )
        policy_link.bind('<Button-1>', self._open_link)
        policy_link.pack(side=tk.BOTTOM)
        policy_text.pack(side=tk.BOTTOM)

        self.logo_image = common.load_image('logo')
        self._mainframe.create_image(94, 60, anchor=tk.NW, image=self.logo_image)

        self.bug = common.load_image('bug')
        self._mainframe.create_image(94, 645, anchor=tk.NW, image=self.bug)

    def _set_user_and_start(self, *args):
        self._mainframe.destroy()
        self.set_user_callback(self._username.get())

    def _clear_username_entity(self, *args):
        if self._username.get() == '@telegram_tag':
            self.username_entity.config(fg='black')
            self._username.set('')

    def _open_leaderboard(self, *args):
        self._mainframe.destroy()
        self.open_leaderboard_callback()

    def _open_link(self, *args):
        link = 'https://engineer.yadro.com/wp-content/uploads/2024/03/privacy-policy.pdf'
        webbrowser.open(link)
