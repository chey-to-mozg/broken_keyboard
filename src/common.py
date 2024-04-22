import os
import tkinter as tk
from typing import Any, Callable

_RESOURCE_PATH = 'resources'


class GameResults:
    def __init__(self):
        self.total_words = 0
        self.total_keys = 0
        self.correct_keys = 0
        self.correct_words = []


def get_image_path(filename: str) -> str:
    return os.path.join(_RESOURCE_PATH, f'{filename}.png')


def load_image(filename: str) -> tk.PhotoImage:
    image_path = get_image_path(filename)
    image = tk.PhotoImage(file=image_path)
    image = image.subsample(2)
    return image


def change_button_image(event):
    widget = event.widget
    if widget.hover:
        widget.config(image=widget.image)
    else:
        widget.config(image=widget.image_hover)
    widget.hover = not widget.hover


def gen_button(root: Any, button_name: str, func: Callable) -> tk.Label:
    image = load_image(button_name)
    button = tk.Label(root, image=image, borderwidth=0, highlightthickness=0)
    button.hover = False
    button.image = image
    image = load_image(f'{button_name}_hover')
    button.image_hover = image
    button.bind("<Button-1>", func)
    button.bind('<Enter>', change_button_image)
    button.bind('<Leave>', change_button_image)
    return button
