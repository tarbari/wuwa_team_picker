import csv
import os
from typing import List, Dict, Union

from character import Character

class DataLoader:
    @staticmethod
    def validate_data(data: Dict[str, str]) -> bool:
        valid_keys = ["name", "level", "ascension", "talent_basic_atk", "talent_skill", "talent_forte", "talent_liberation", "talent_intro", "sequence", "element", "quality"]
        invalid_keys = set(data.keys()) - set(valid_keys)
        if invalid_keys:
            raise KeyError(f"Invalid keys: {invalid_keys}")
        return True

    @staticmethod
    def format_data(key: str, value: str) -> Union[str, int]:
        if key in ["name", "element"]:
            return value
        return int(value)

    # This function will crash the app if somehow the data is not valid but still passess the validation function.
    # So make sure to test the validate_data() function thoroughly.
    @staticmethod
    def read_characters_from_csv(file: str) -> List[Character]:
        path = os.path.expanduser(file)
        with open(path, mode='r') as f:
            result = []
            reader = csv.DictReader(f)
            for row in reader:
                if DataLoader.validate_data(row):
                    result.append(Character(**{k: DataLoader.format_data(k, v) for k, v in row.items()}))  # type: ignore[arg-type]
            return result
