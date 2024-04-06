import tkinter as tk

from src.game_window import GameWindow
from src.menu_window import MainMenu
from src.result_window import ResultWindow
from src.leaderboard_window import LeaderboardWindow


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        window_w = self.root.winfo_screenwidth()
        window_h = self.root.winfo_screenheight()
        window_w = 800
        window_h = 600
        pad = 3
        self.root.geometry(f"{window_w - pad}x{window_h - pad}+0+0")
        self.root.title = 'Broken keyboard'

        self.username = ''

        self.words = []
        self.load_words()

        self.key_mapping = {}
        self.load_keys_mapping()

        self.timer_init = 10

        self.open_menu()

    def set_user_name_and_start_game(self, username):
        self.username = username
        GameWindow(
            self.root,
            self.words,
            self.key_mapping,
            self.timer_init,
            interrupt_game_callback=self.open_menu,
            set_results_callback=self.open_result_window,
        )

    def open_leaderboard(self):
        LeaderboardWindow(self.root, open_menu_callback=self.open_menu)

    def open_menu(self):
        self.username = ''
        MainMenu(
            self.root,
            set_user_callback=self.set_user_name_and_start_game,
            open_leaderboard_callback=self.open_leaderboard,
        )

    def open_result_window(self, result: int, finished_words: list[str]):
        ResultWindow(self.root, self.username, result, finished_words, menu_callback=self.open_menu)

    def load_words(self):
        with open('words.txt', 'r') as f:
            for row in f:
                self.words.append(row.rstrip('\n'))

    def load_keys_mapping(self):
        with open('keyboard.txt', 'r') as f:
            for row in f:
                keys = row.rstrip('\n').split(':')
                self.key_mapping[keys[0]] = keys[1]
