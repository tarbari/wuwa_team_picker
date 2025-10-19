#!/usr/bin/python3

import argparse
import curses
from typing import List
from threading import Lock

from character import Character
from data_loader import DataLoader
from game_mode import GameMode
from constants import GAME_MODES

# Constants imported from constants.py




# Metaclass to make the ScreenPrinter a singleton. This is thread safe for future proofing.
class ScreenPrinterMeta(type):
    __instances = {}
    __lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                instance = super().__call__(*args, **kwargs)
                cls.__instances[cls] = instance
        return cls.__instances[cls]


# TODO: Add checks if screen is too small and print a message telling to make the window bigger.
# Singleton facade
class ScreenPrinter(metaclass=ScreenPrinterMeta):
    def __init__(self, stdscr: curses.window) -> None:
        self.__stdscr = stdscr

    def print_character_cards(self, characters: List[Character], start_y: int, start_x: int = 0):
        for idx, character in enumerate(characters):
            self.print_character(character, 6 + (start_y * 14), start_x + idx * 35)

    def print_top_bar(self, text: str):
        self.__stdscr.addstr(0, 0, "=" * 30)
        self.__stdscr.addstr(1, 0, text)
        self.__stdscr.addstr(2, 0, "=" * 30)

    def print_instruction_bar(self, text: str):
        self.__stdscr.addstr(4, 0, text)

    def print_character(self, character: Character, y: int, x: int):
        self.__stdscr.addstr(y, x, "=" * 30)
        self.__stdscr.addstr(y + 1, x, f"Character: {character.name}")
        self.__stdscr.addstr(y + 2, x, "=" * 30)
        self.__stdscr.addstr(y + 3, x, f"Level: {character.level}")
        self.__stdscr.addstr(y + 4, x, f"Ascension: {character.ascension}")
        self.__stdscr.addstr(y + 5, x, "Talents:")
        self.__stdscr.addstr(y + 6, x, f"  - Basic Atk: {character.talent_basic_atk}")
        self.__stdscr.addstr(y + 7, x, f"  - Skill: {character.talent_skill}")
        self.__stdscr.addstr(y + 8, x, f"  - Forte: {character.talent_forte}")
        self.__stdscr.addstr(y + 9, x, f"  - Liberation: {character.talent_liberation}")
        self.__stdscr.addstr(y + 10, x, f"  - Intro: {character.talent_intro}")
        self.__stdscr.addstr(y + 11, x, f"Sequence: {character.sequence}")
        self.__stdscr.addstr(y + 12, x, f"Element: {character.element}")
        self.__stdscr.addstr(y + 13, x, "=" * 30)

    def show_menu(self):
        curses.curs_set(0)
        self.__stdscr.clear()
        self.print_top_bar("Wuthering Waves Character Picker")
        self.__stdscr.addstr(4, 0, f"1. {GAME_MODES['random']}")
        self.__stdscr.addstr(5, 0, f"2. {GAME_MODES['roulette']}")
        self.__stdscr.addstr(7, 0, "Press 'q' to quit.")
        self.__stdscr.addstr(9, 0, "Select an option (1-2):")
        self.__stdscr.refresh()

    def print_random_character(self, c: Character):
        self.__stdscr.clear()
        self.print_top_bar(GAME_MODES["random"])
        self.print_character_cards([c], 0)
        self.print_instruction_bar("Press 'n' to pick another character or 'q' to return to the menu.")
        self.__stdscr.refresh()

    # TODO: Make this reusable
    def warning_three_rows(self, rows: List[str]):
        self.__stdscr.addstr(4, 0, f"Warning: Not enough characters left for {GAME_MODES['roulette']}!")
        self.__stdscr.addstr(5, 0, "Returning to the main menu.")
        self.__stdscr.addstr(6, 0, "Press any key to continue.")
        self.__stdscr.refresh()
        self.__stdscr.getkey()

    # Public version of getkey()
    def getkey(self) -> str:
        key = self.__stdscr.getkey()
        return key

    # Public version of clear()
    def clear(self):
        self.__stdscr.clear()

    # Public version of refresh()
    def refresh(self):
        self.__stdscr.refresh()

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

