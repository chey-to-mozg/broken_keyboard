import tkinter as tk
from functools import partial
from typing import Callable


class MainMenu:
    def __init__(self, root: tk.Tk, set_user_callback: Callable, open_leaderboard_callback: Callable):
        self.set_user_callback = set_user_callback
        self.open_leaderboard_callback = open_leaderboard_callback

        self.mainframe = tk.Canvas(root, bg='blue')
        self.mainframe.pack(fill=tk.BOTH, expand=1)

        self.username = tk.StringVar(value='@username')

        self.leaderboard_button = tk.Button(self.mainframe, text='Leaderboard', command=self.open_leaderboard)
        self.leaderboard_button.pack(side=tk.TOP, anchor=tk.NE)

        combined_frame = tk.Frame(self.mainframe, bg='green')
        combined_frame.pack(expand=1)
        username_entry = tk.Entry(combined_frame, width=20, textvariable=self.username)
        username_entry.pack(pady=5, padx=5)

        start_button = tk.Button(combined_frame, text="Start game", command=self.set_user_and_start)
        start_button.pack(pady=5, padx=5)

        image = tk.PhotoImage(file='test.png')
        self.mainframe.create_image(50, 50, image=image)

        username_entry.focus()
        root.mainloop()

    def set_user_and_start(self, *args):
        self.mainframe.destroy()
        self.set_user_callback(self.username.get())

    def open_leaderboard(self, *args):
        self.mainframe.destroy()
        self.open_leaderboard_callback()
