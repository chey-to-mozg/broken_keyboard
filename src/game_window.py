import copy
import random
import time
import tkinter as tk
from typing import Callable

from src import common, setups


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
        self._results = common.GameResults()

        self._current_word_idx = 0
        self._current_letter_index = 0
        self._game_started = False
        self._timer_start = timer_init

        self._interrupt_game_callback = interrupt_game_callback
        self._set_results_callback = set_results_callback

        self._words = copy.copy(words)
        random.shuffle(self._words)

        # add mode with change key mapping on every word
        self._key_mapping = key_mapping

        self._init_controls(root)

        self._mainframe.bind_all('<KeyPress>', self._process_button_press)
        self._mainframe.bind_all('<KeyRelease>', self._process_button_release)

        root.mainloop()

    def _init_controls(self, root: tk.Tk):
        self._mainframe = tk.Canvas(root, bg=setups.BackgroundColor)
        self._mainframe.pack(fill=tk.BOTH, expand=1)

        button = common.gen_button(self._mainframe, 'menu_button', self._interrupt_game)
        button.pack(side=tk.TOP, anchor=tk.NE, padx=60, pady=60)

        self._timer_value = tk.StringVar(value='')
        self._gen_timer_value(self._timer_start)
        self._time_of_start: float | None = None
        tk.Label(
            self._mainframe,
            width=7,
            textvariable=self._timer_value,
            font=setups.LettersFont,
            bg=setups.BackgroundColor,
            fg='#1E21AA',
        ).pack(side=tk.TOP)

        self._word_frame: tk.Frame | None = None
        self._render_current_word()

        # keyboard layout from left to right, from top to bottom
        self._render_keyboard()

        self.logo_image = common.load_image('logo')
        self._mainframe.create_image(94, 60, anchor=tk.NW, image=self.logo_image)

    def _render_current_word(self):
        if self._word_frame:
            self._word_frame.destroy()

        self._word_frame = tk.Frame(self._mainframe, bg=setups.BackgroundColor,)
        self._word_frame.pack(side=tk.TOP, pady=(120, 0))
        self._letter_labels = []

        self.label_image = common.load_image('letter_field')

        for letter in self._words[self._current_word_idx]:
            label = tk.Label(
                self._word_frame, image=self.label_image, text=letter, compound='center', font=setups.LettersFont,
                bg=setups.BackgroundColor,
            )
            label.pack(side=tk.LEFT, padx=5)
            self._letter_labels.append(label)

    def _render_keyboard(self):
        keyboard_frame = tk.Frame(self._mainframe, bg=setups.BackgroundColor)
        keys_on_keyboard = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ''],
        ]
        self._keys_to_label_mapping = {}

        self.key_image = common.load_image('key')
        self.key_correct_image = common.load_image('key_correct')
        self.key_wrong_image = common.load_image('key_wrong')

        for row in keys_on_keyboard:
            row_frame = tk.Frame(keyboard_frame, bg=setups.BackgroundColor)
            row_frame.pack()
            for key in row:
                swapped_key = self._key_mapping.get(key, key)
                if key != '':
                    label = tk.Label(
                        row_frame,
                        image=self.key_image,
                        text=swapped_key,
                        compound='center',
                        font=setups.LettersFont,
                        bg=setups.BackgroundColor,
                    )
                    self._keys_to_label_mapping[swapped_key] = label
                else:
                    label = tk.Label(row_frame, text='', bg=setups.BackgroundColor, width=10)
                label.pack(side=tk.LEFT)

        keyboard_frame.pack(side=tk.BOTTOM, pady=(0, 160))

    def _process_button_press(self, event):
        if 97 <= event.keysym_num <= 122:
            self._results.total_keys += 1
            if not self._game_started:
                self._game_started = True
                self._time_of_start = time.time()
                self._mainframe.after(100, self._update_timer)

            key = event.char
            swapped_key = self._key_mapping.get(key, key)
            correct_key = False
            if swapped_key == self._words[self._current_word_idx][self._current_letter_index]:
                self._letter_labels[self._current_letter_index].config(fg=setups.GreenTextColor)
                self._current_letter_index += 1
                correct_key = True
                self._results.correct_keys += 1
            if self._current_letter_index >= len(self._letter_labels):
                self._current_letter_index = 0
                self._current_word_idx += 1
                self._results.total_words += 1
                self._render_current_word()
            if correct_key:
                self._keys_to_label_mapping[swapped_key].config(image=self.key_correct_image)
            else:
                self._letter_labels[self._current_letter_index].config(fg=setups.RedTextColor)
                self._keys_to_label_mapping[swapped_key].config(image=self.key_wrong_image)

    def _process_button_release(self, event):
        if 97 <= event.keysym_num <= 122:
            key = event.char
            swapped_key = self._key_mapping.get(key, key)
            self._keys_to_label_mapping[swapped_key].config(image=self.key_image)

    def _destroy_window(self):
        self._mainframe.unbind_all('<KeyPress>')
        self._mainframe.unbind_all('<KeyRelease>')
        self._mainframe.destroy()

    def _set_result(self):
        self._destroy_window()
        self._set_results_callback(self._results, self._words[: self._current_word_idx])

    def _interrupt_game(self, *args):
        self._destroy_window()
        self._interrupt_game_callback()

    def _gen_timer_value(self, seconds: int):
        minutes = seconds // 60
        seconds = seconds % 60
        self._timer_value.set(f'{minutes}:{0 if seconds < 10 else ""}{seconds}')

    def _update_timer(self):
        diff = time.time() - self._time_of_start
        current_timer = int(self._timer_start - diff)
        if current_timer <= 0:
            self._set_result()

        self._gen_timer_value(current_timer)
        self._mainframe.after(100, self._update_timer)
