#!/usr/bin/python3

import argparse

from data_loader import DataLoader
from application import Application
from ui_qt import QtScreenPrinter


def parse_args():
    parser = argparse.ArgumentParser(
        description="Chooses a random character from your Wuthering Waves characters. (GUI)"
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        default="~/.local/share/gaming_tools/data/wuwa_characters.csv",
        help="Path to character data csv. Default: ~/.local/share/gaming_tools/data/wuwa_characters.csv"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    characters = DataLoader.read_characters_from_csv(args.file)
    screen = QtScreenPrinter()
    app = Application(screen, characters)
    app.run()


if __name__ == "__main__":
    main()
