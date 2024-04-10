from src.game_window import GameWindow
from src.leaderboard_window import LeaderboardWindow
from src.menu_window import MainMenu
from src.result_window import ResultWindow
from src.setups import ROOT
from src import common


class MainWindow:
    def __init__(self, initial_timer: int):
        self._root = ROOT
        self._root.state('zoomed')
        self._root.title('Broken keyboard')

        self._username = ''

        # load current game words
        self._words = []
        self._load_words()

        # load current key mapping
        self._key_mapping = {}
        self._load_keys_mapping()

        self._timer_init = initial_timer

        # open menu window on start
        self._open_menu()

    def _set_user_name_and_start_game(self, username):
        self._username = username
        GameWindow(
            self._root,
            self._words,
            self._key_mapping,
            self._timer_init,
            interrupt_game_callback=self._open_menu,
            set_results_callback=self._open_result_window,
        )

    def _open_leaderboard(self):
        LeaderboardWindow(self._root, open_menu_callback=self._open_menu)

    def _open_menu(self):
        self._username = ''
        MainMenu(
            self._root,
            set_user_callback=self._set_user_name_and_start_game,
            open_leaderboard_callback=self._open_leaderboard,
        )

    def _open_result_window(self, results: common.GameResults, finished_words: list[str]):
        ResultWindow(self._root, self._username, results, finished_words, menu_callback=self._open_menu)

    def _load_words(self):
        with open('words.txt', 'r') as f:
            for row in f:
                self._words.append(row.rstrip('\n'))

    def _load_keys_mapping(self):
        with open('keyboard.txt', 'r') as f:
            for row in f:
                keys = row.rstrip('\n').split(':')
                self._key_mapping[keys[0]] = keys[1]
