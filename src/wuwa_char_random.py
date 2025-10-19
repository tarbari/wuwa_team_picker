#!/usr/bin/python3

import argparse
import curses
from typing import List

from character import Character
from data_loader import DataLoader
from game_mode import GameMode
from constants import GAME_MODES
from screen_printer import ScreenPrinter

# Constants imported from constants.py




# ScreenPrinter moved to screen_printer package

# GameMode moved to game_mode.py

class Application:
    def __init__(self, scr, characters: List[Character]):
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

def parse_args():
    parser = argparse.ArgumentParser(
        description="Chooses a random character from your Wuthering Waves characters."
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        default="~/.local/share/gaming_tools/data/wuwa_characters.csv",
        help="Path to character data csv. Default: ~/.local/share/gaming_tools/data/wuwa_characters.csv"
    )
    return parser.parse_args()

def main(stdscr: curses.window):
    args = parse_args()
    characters = DataLoader.read_characters_from_csv(args.file)
    screen_printer = ScreenPrinter(stdscr)
    app = Application(screen_printer, characters)
    app.run()

if __name__ == "__main__":
    curses.wrapper(main)

