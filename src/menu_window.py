import tkinter as tk
from functools import partial
from typing import Callable


class MainMenu:
    def __init__(self, root: tk.Tk, set_user_callback: Callable):
        self.mainframe = tk.Canvas(root, bg='blue')
        self.mainframe.pack(fill=tk.BOTH, expand=1)

        self.username = tk.StringVar(value='@username')

        self.leaderboard_button = tk.Button(self.mainframe, text='Leaderboard', command=None)
        self.leaderboard_button.pack(side=tk.TOP, anchor=tk.NE)

        combined_frame = tk.Frame(self.mainframe, bg='green')
        combined_frame.pack(expand=1)
        username_entry = tk.Entry(combined_frame, width=20, textvariable=self.username)
        username_entry.pack(pady=5, padx=5)

        start_button = tk.Button(combined_frame, text="Start game", command=partial(self.set_user, set_user_callback))
        start_button.pack(pady=5, padx=5)

        image = tk.PhotoImage(file='test.png')
        self.mainframe.create_image(50, 50, image=image)

        username_entry.focus()
        root.mainloop()

    def set_user(self, callback: Callable, *args):
        self.mainframe.destroy()
        callback(self.username.get())
