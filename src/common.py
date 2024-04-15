import os

_RESOURCE_PATH = 'resources'

class GameResults:
    def __init__(self):
        self.total_words = 0
        self.total_keys = 0
        self.correct_keys = 0


def get_image_path(filename):
    return os.path.join(_RESOURCE_PATH, f'{filename}.png')
