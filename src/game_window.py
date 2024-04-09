import random
import time
import tkinter as tk
from typing import Callable

from src import setups


class GameWindow:
    def __init__(
        self,
        root: tk.Tk,
        words: list[str],
        key_mapping: dict[str, str],
        timer_init: int,
        interrupt_game_callback: Callable,
        set_results_callback: Callable,
    ):
        # TODO add result class with all fields
        self.result = 0
        self.total_keys = 0
        self.correct_keys = 0

        self.current_word_idx = 0
        self.current_letter_index = 0
        self.game_started = False

        self.interrupt_game_callback = interrupt_game_callback
        self.set_results_callback = set_results_callback

        self.words = words  # copy?
        random.shuffle(self.words)

        self.key_mapping = key_mapping

        self.mainframe = tk.Frame(root, bg=setups.BackgroundColor)
        self.mainframe.pack(fill=tk.BOTH, expand=1)

        tk.Button(self.mainframe, text='Главное меню', command=self.interupt_game, font=setups.ButtonsFont).pack(
            side=tk.TOP, anchor=tk.NE
        )

        self.timer_start = timer_init
        self.timer = tk.IntVar(value=self.timer_start)
        self.time_of_start: float | None = None
        tk.Label(self.mainframe, width=7, textvariable=self.timer, font=setups.MainInfoFont).pack(
            side=tk.TOP, anchor=tk.N
        )

        self.word_frame: tk.Frame | None = None
        self._render_current_word()

        # keyboard layout from left to right, from top to bottom
        keyboard_frame = tk.Frame(self.mainframe, background='black')
        keys_on_keyboard = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ''],
        ]
        self.keys_to_label_mapping = {}
        for row in keys_on_keyboard:
            row_frame = tk.Frame(keyboard_frame, background='black')
            row_frame.pack()
            for key in row:
                key_color = 'grey'
                if key == '':
                    # just add space
                    key_color = 'black'
                swapped_key = self.key_mapping.get(key, key)
                label = tk.Label(row_frame, width=5, text=swapped_key, background=key_color, font=setups.LettersFont)
                if key != '':
                    self.keys_to_label_mapping[swapped_key] = label
                label.pack(side=tk.LEFT, pady=5, padx=5)

        keyboard_frame.pack(side=tk.BOTTOM, pady=(0, 100))

        self.mainframe.bind_all('<KeyPress>', self._process_button_press)
        self.mainframe.bind_all('<KeyRelease>', self._process_button_release)

        root.mainloop()

    def _render_current_word(self):
        if self.word_frame:
            self.word_frame.destroy()

        self.word_frame = tk.Frame(self.mainframe)
        self.word_frame.pack(expand=1)
        self.letter_labels = []

        for letter_id, letter in enumerate(self.words[self.current_word_idx]):
            label = tk.Label(self.word_frame, text=letter, width=6, height=3, font=setups.LettersFont)
            label.pack(side=tk.LEFT)
            self.letter_labels.append(label)
        self.letter_labels[0].config(bg='orange')

    def _process_button_press(self, event):
        if 97 <= event.keysym_num <= 122:
            self.total_keys += 1
            if not self.game_started:
                self.game_started = True
                self.time_of_start = time.time()
                self.mainframe.after(100, self.update_timer)

            key = event.char
            swapped_key = self.key_mapping.get(key, key)
            correct_key = False
            if swapped_key == self.words[self.current_word_idx][self.current_letter_index]:
                self.letter_labels[self.current_letter_index].config(bg='green')
                self.current_letter_index += 1
                correct_key = True
                self.correct_keys += 1
            if self.current_letter_index >= len(self.letter_labels):
                self.current_letter_index = 0
                self.current_word_idx += 1
                self.result += 1
                self._render_current_word()
            if correct_key:
                self.letter_labels[self.current_letter_index].config(bg='orange')
                self.keys_to_label_mapping[swapped_key].config(bg='green')
            else:
                self.letter_labels[self.current_letter_index].config(bg='red')
                self.keys_to_label_mapping[swapped_key].config(bg='red')

    def _process_button_release(self, event):
        if 97 <= event.keysym_num <= 122:
            key = event.char
            swapped_key = self.key_mapping.get(key, key)
            self.keys_to_label_mapping[swapped_key].config(bg='grey')

    def destroy_window(self):
        self.mainframe.unbind_all('<KeyPress>')
        self.mainframe.unbind_all('<KeyRelease>')
        self.mainframe.destroy()

    def set_result(self, *args):
        self.destroy_window()
        self.set_results_callback(self.result, self.correct_keys, self.total_keys, self.words[: self.current_word_idx])

    def interupt_game(self, *args):
        self.destroy_window()
        self.interrupt_game_callback()

    def update_timer(self):
        diff = time.time() - self.time_of_start
        current_timer = int(self.timer_start - diff)
        if current_timer <= 0:
            self.set_result()

        self.timer.set(current_timer)
        self.mainframe.after(100, self.update_timer)
