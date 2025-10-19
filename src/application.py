from typing import List

from character import Character
from game_mode import GameMode
from ui.types import UI


class Application:
    def __init__(self, scr: UI, characters: List[Character]):
        self.scr = scr
        self.characters = characters
        self.game_mode = GameMode(self.scr, self.characters)

    def run(self):
        while True:
            self.scr.show_menu()
            key = self.scr.getkey()
            if key == 'q':
                break
            elif key == '1':
                self.game_mode.random_character_mode()
            elif key == '2':
                self.game_mode.abyss_roulette_mode()
