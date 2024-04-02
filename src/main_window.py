import tkinter as tk
from tkinter import ttk

from src.main_menu import MainMenu


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title = 'Broken keyboard'

        self.username = ''

        self.current_frame: MainMenu | None = None

    def open_menu(self):
        self.current_frame = MainMenu(self.root, set_user_callback=self.set_user_name)

    def set_user_name(self, username):
        self.root.quit()
        self.username = username
        print(username)
