import random
from enum import Enum

from src import common
from src.game_window import GameWindow
from src.leaderboard_window import LeaderboardWindow
from src.menu_window import MainMenu
from src.result_window import ResultWindow
from src.setups import ROOT


class States(Enum):
    menu = 1
    leaderboard = 2
    game = 3
    results = 4
    exit = 5


class MainWindow:
    def __init__(self, initial_timer: int):
        self._root = ROOT
        self._root.state('zoomed')
        self._root.title('Broken keyboard')

        self._username = ''
        self._results: common.GameResults | None = None

        # load current game words
        self._words = []
        self._load_words()

        # load current key mapping
        self._key_mapping = {}

        self._timer_init = initial_timer

        self._root.protocol("WM_DELETE_WINDOW", self._on_close)
        # open menu window on start
        self._state = States.menu

        self._state_machine()

    def _state_machine(self):
        while True:
            match self._state:
                case States.menu:
                    self._open_menu()
                case States.leaderboard:
                    self._open_leaderboard()
                case States.game:
                    self._start_game()
                case States.results:
                    self._open_result_window()
                case States.exit:
                    return

    def _start_game(self, *args):
        self._gen_key_mapping()
        window = GameWindow(self._root, self._words, self._key_mapping, self._timer_init)
        window.render_window()
        if self._state == States.exit:
            return
        self._results = window.get_results()
        if self._results:
            self._state = States.results
        else:
            self._state = States.menu

    def _open_leaderboard(self):
        window = LeaderboardWindow(self._root)
        window.render_window()
        if self._state == States.exit:
            return
        self._state = States.menu

    def _open_menu(self):
        self._username = ''
        self._results = None
        window = MainMenu(self._root)
        window.render_window()
        if self._state == States.exit:
            return
        self._root.unbind('<Return>')
        if username := window.get_username():
            self._username = username.lower()
            self._state = States.game
        else:
            self._state = States.leaderboard

    def _open_result_window(self):
        window = ResultWindow(self._root, self._username, self._results)
        window.render_window()
        if self._state == States.exit:
            return
        self._state = States.menu

    def _on_close(self):
        self._root.unbind('<Return>')
        self._state = States.exit
        self._root.destroy()

    def _load_words(self):
        with open('words.txt', 'r') as f:
            for row in f:
                self._words.append(row.rstrip('\n').lower().replace(' ', '').replace('-', ''))

    def _load_keys_mapping(self):
        with open('keyboard.txt', 'r') as f:
            for row in f:
                keys = row.rstrip('\n').split(':')
                self._key_mapping[keys[0]] = keys[1]

    def _gen_key_mapping(self):
        self._key_mapping = {}
        keys = [chr(i) for i in range(97, 123)]
        idxs = random.sample(range(len(keys)), 5)
        selected_keys = [keys[i] for i in idxs]
        idxs.append(idxs.pop(0))
        for i, idx in enumerate(idxs):
            self._key_mapping[keys[idx]] = selected_keys[i]
