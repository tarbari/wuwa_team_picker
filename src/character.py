from dataclasses import dataclass

@dataclass
class Character:
    name: str
    level: int
    ascension: int
    talent_basic_atk: int
    talent_skill: int
    talent_forte: int
    talent_liberation: int
    talent_intro: int
    sequence: int
    element: str
    quality: int
