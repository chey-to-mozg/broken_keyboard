import random
import time
import tkinter as tk
from typing import Callable


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
        self.result = 0
        self.current_word_idx = 0
        self.current_letter_index = 0
        self.game_started = False

        self.interrupt_game_callback = interrupt_game_callback
        self.set_results_callback = set_results_callback

        self.words = words  # copy?
        random.shuffle(self.words)

        self.key_mapping = key_mapping

        self.mainframe = tk.Frame(root, bg='grey')
        self.mainframe.pack(fill=tk.BOTH, expand=1)

        self.timer_start = timer_init
        self.timer = tk.IntVar(value=self.timer_start)
        self.time_of_start: float | None = None
        tk.Label(self.mainframe, width=7, textvariable=self.timer).pack(side=tk.TOP, anchor=tk.N)

        tk.Button(self.mainframe, text='Main menu', command=self.interupt_game).pack(side=tk.TOP, anchor=tk.NE)

        self.word_frame: tk.Frame | None = None
        self._render_current_word()

        self.last_pressed_key = tk.StringVar(value='')
        self.last_pressed_key_entry = tk.Label(self.mainframe, width=7, textvariable=self.last_pressed_key)
        self.last_pressed_key_entry.pack(side=tk.BOTTOM, anchor=tk.S)

        self.mainframe.bind_all('<KeyPress>', self._process_button_press)

        root.mainloop()

    def _render_current_word(self):
        if self.word_frame:
            self.word_frame.destroy()

        self.word_frame = tk.Frame(self.mainframe)
        self.word_frame.pack(expand=1)
        self.letter_labels = []

        for letter_id, letter in enumerate(self.words[self.current_word_idx]):
            label = tk.Label(self.word_frame, text=letter, width=7, height=7)
            label.pack(side=tk.LEFT)
            self.letter_labels.append(label)
        self.letter_labels[0].config(bg='orange')

    def _process_button_press(self, event):
        if 65 <= event.keycode <= 90:
            if not self.game_started:
                self.game_started = True
                self.time_of_start = time.time()
                self.mainframe.after(100, self.update_timer)

            key = event.char
            swapped_key = self.key_mapping.get(key, key)
            self.last_pressed_key.set(swapped_key)
            correct_key = False
            if swapped_key == self.words[self.current_word_idx][self.current_letter_index]:
                self.letter_labels[self.current_letter_index].config(bg='green')
                self.current_letter_index += 1
                correct_key = True
            if self.current_letter_index >= len(self.letter_labels):
                self.current_letter_index = 0
                self.current_word_idx += 1
                self.result += 1
                self._render_current_word()
            elif correct_key:
                self.letter_labels[self.current_letter_index].config(bg='orange')
                self.last_pressed_key_entry.config(bg='green')
            else:
                self.letter_labels[self.current_letter_index].config(bg='red')
                self.last_pressed_key_entry.config(bg='red')

    def destroy_window(self):
        self.mainframe.unbind_all('<KeyPress>')
        self.mainframe.destroy()

    def set_result(self, *args):
        self.destroy_window()
        self.set_results_callback(self.result, self.words[:self.current_word_idx])

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
