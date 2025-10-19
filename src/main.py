#!/usr/bin/python3

import argparse
import curses

from data_loader import DataLoader
from application import Application
from screen_printer import ScreenPrinter


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

