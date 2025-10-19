import sys
import time
from queue import Queue, Empty
from typing import List

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QMessageBox
)

from character import Character
from constants import GAME_MODES


class QtScreenPrinter:
    """Minimal Qt-based UI that mimics ScreenPrinter's API."""

    def __init__(self, *_args, **_kwargs) -> None:
        self.app = QApplication.instance() or QApplication(sys.argv)

        self._key_queue: Queue[str] = Queue()

        self.win = QMainWindow()
        self.win.setWindowTitle("Wuthering Waves Character Picker")
        central = QWidget(self.win)
        self.win.setCentralWidget(central)

        self.top_bar = QLabel("=" * 30 + "\n" + "Wuthering Waves Character Picker" + "\n" + "=" * 30)
        self.top_bar.setTextInteractionFlags(Qt.NoTextInteraction)
        self.instruction = QLabel("")
        self.instruction.setTextInteractionFlags(Qt.NoTextInteraction)

        self.text = QTextEdit()
        self.text.setReadOnly(True)

        # Buttons reflecting current flows (1/2/3, n, q)
        self.btns: dict[str, QPushButton] = {
            "1": QPushButton("1"),
            "2": QPushButton("2"),
            "3": QPushButton("3"),
            "n": QPushButton("n"),
            "q": QPushButton("Quit (q)"),
        }
        for key, btn in self.btns.items():
            btn.clicked.connect(lambda _=False, k=key: self._key_queue.put(k))

        btn_row = QHBoxLayout()
        for key in ["1", "2", "3", "n", "q"]:
            btn_row.addWidget(self.btns[key])

        layout = QVBoxLayout(central)
        layout.addWidget(self.top_bar)
        layout.addWidget(self.instruction)
        layout.addWidget(self.text)
        layout.addLayout(btn_row)

        self._show_menu_buttons()
        self.win.resize(800, 600)
        self.win.show()

        # Keep processing events periodically even if getkey is blocking
        self._timer = QTimer()
        self._timer.setInterval(30)
        self._timer.timeout.connect(lambda: None)
        self._timer.start()

    def _show_menu_buttons(self):
        # Menu: show options 1,2 and q; hide 3,n
        self.btns["1"].setVisible(True)
        self.btns["2"].setVisible(True)
        self.btns["q"].setVisible(True)
        self.btns["3"].setVisible(False)
        self.btns["n"].setVisible(False)

    def _show_pick_buttons(self):
        # Picking: show 1,2,3 and q
        self.btns["1"].setVisible(True)
        self.btns["2"].setVisible(True)
        self.btns["3"].setVisible(True)
        self.btns["q"].setVisible(True)
        self.btns["n"].setVisible(False)

    def _show_random_buttons(self):
        # Random character: show n and q
        self.btns["1"].setVisible(False)
        self.btns["2"].setVisible(False)
        self.btns["3"].setVisible(False)
        self.btns["q"].setVisible(True)
        self.btns["n"].setVisible(True)

    # Parity with ScreenPrinter API

    def print_character_cards(self, characters: List[Character], start_y: int, start_x: int = 0) -> None:
        # Render simple text blocks; start_y/start_x are ignored in GUI
        blocks = []
        for c in characters:
            block = "\n".join([
                "=" * 30,
                f"Character: {c.name}",
                "=" * 30,
                f"Level: {c.level}",
                f"Ascension: {c.ascension}",
                "Talents:",
                f"  - Basic Atk: {c.talent_basic_atk}",
                f"  - Skill: {c.talent_skill}",
                f"  - Forte: {c.talent_forte}",
                f"  - Liberation: {c.talent_liberation}",
                f"  - Intro: {c.talent_intro}",
                f"Sequence: {c.sequence}",
                f"Element: {c.element}",
                "=" * 30,
            ])
            blocks.append(block)
        self.text.append("\n\n".join(blocks))

    def print_top_bar(self, text: str) -> None:
        self.top_bar.setText("=" * 30 + "\n" + text + "\n" + "=" * 30)

    def print_instruction_bar(self, text: str) -> None:
        self.instruction.setText(text)

    def show_menu(self) -> None:
        self.clear()
        self.print_top_bar("Wuthering Waves Character Picker")
        self.text.append(f"1. {GAME_MODES['random']}\n2. {GAME_MODES['roulette']}\n\nPress 'q' to quit.")
        self.instruction.setText("Select an option (1-2):")
        self._show_menu_buttons()
        self.refresh()

    def print_random_character(self, c: Character) -> None:
        self.clear()
        self.print_top_bar(GAME_MODES["random"])
        self.print_character_cards([c], 0)
        self.print_instruction_bar("Press 'n' to pick another character or 'q' to return to the menu.")
        self._show_random_buttons()
        self.refresh()

    def warning_three_rows(self, rows: List[str]) -> None:
        msg = QMessageBox(self.win)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText("\n".join(rows))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def getkey(self) -> str:
        # Block until a key-equivalent is queued; keep UI responsive
        while True:
            try:
                return self._key_queue.get_nowait()
            except Empty:
                self.app.processEvents()
                time.sleep(0.01)

    def clear(self) -> None:
        self.text.clear()

    def refresh(self) -> None:
        self.app.processEvents()
