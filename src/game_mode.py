import curses
import random
from typing import List, TYPE_CHECKING, Any

from character import Character
from constants import GAME_MODES

if TYPE_CHECKING:
    from screen_printer import ScreenPrinter
else:
    ScreenPrinter = Any

class GameMode:
    def __init__(self, scr: ScreenPrinter, characters: List[Character]):
        self.scr = scr
        self.characters = characters

    def random_character_mode(self):
        curses.curs_set(0)  # TODO: This does not belong here. Move to ScreenPrinter?
        while True:
            character = self.pick_character()
            self.scr.print_random_character(character)
            key = self.scr.getkey()
            if key == 'q':
                break
            elif key == 'n':
                continue

    # TODO: Refactor into smaller functions? Also this looks very messy with all the prints. There has to be a better way.
    def abyss_roulette_mode(self):
        curses.curs_set(0)  # TODO: This does not belong here. Move to ScreenPrinter?
        remaining_characters = self.characters.copy()
        team_idx = 0
        all_teams = []
        while True:
            team = []
            if len(remaining_characters) < 9:
                self.scr.clear()
                self.scr.print_top_bar(GAME_MODES["roulette"])
                rows = [f"Warning: Not enough characters left for {GAME_MODES['roulette']}!", "Returning to the main menu.", "Press any key to continue."]
                self.scr.warning_three_rows(rows)
                return
            for round_num in range(3):
                self.scr.clear()
                self.scr.print_top_bar(f"{GAME_MODES['roulette']}: Round {round_num+1}/4")
                self.scr.print_instruction_bar("Select a character (1-3) or press 'q' to return to the menu:")
                if all_teams:
                    for i, t in enumerate(all_teams):
                        self.scr.print_character_cards(t, i)
                characters = self.pick_characters(remaining_characters, 3)
                self.scr.print_character_cards(characters, team_idx)
                self.scr.refresh()
                while True:
                    key = self.scr.getkey()
                    if key == 'q':
                        return
                    if key in ['1', '2', '3']:
                        selected_char = characters[int(key) - 1]
                        team.append(selected_char)
                        remaining_characters.remove(selected_char)
                        break
            self.scr.clear()
            self.scr.print_top_bar(f"{GAME_MODES['roulette']}: Your Teams")
            self.scr.print_instruction_bar("Press 'n' to create another team or any other key to return to the menu.")
            if all_teams:
                for i, t in enumerate(all_teams):
                    self.scr.print_character_cards(t, i)
            self.scr.print_character_cards(team, team_idx)
            self.scr.refresh()
            key = self.scr.getkey()
            if key != 'n':
                break
            all_teams.append(team)
            team_idx += 1

    def pick_character(self) -> Character:
        return random.sample(self.characters, 1)[0]

    def pick_characters(self, chars: List[Character], count: int) -> List[Character]:
        return random.sample(chars, count)
