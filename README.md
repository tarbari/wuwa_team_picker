# Wuwa Team Picker

A terminal-based helper for Wuthering Waves that picks random characters and helps you build teams via simple interactive modes:
- Random Character Picker
- Team Roulette

This project was written with the help of AI assistance to accelerate refactors and boilerplate, and then reviewed and integrated by a human.

## Requirements

- Python 3.12+
- A terminal that supports curses (Linux/macOS; Windows via WSL works)

## Installation

Using uv (recommended):
- Install uv: https://docs.astral.sh/uv/getting-started/installation/
- From the project root:
  - Install runtime deps: `uv sync`
  - Optionally install dev tools (PyInstaller, etc.): `uv sync --group dev`

Using pip:
- Create and activate a virtual environment:
  - `python -m venv .venv && source .venv/bin/activate`
- Install the package (and its dependencies):
  - `python -m pip install .`

## Running

- Run the app:
  - `python src/main.py`
- Optional arguments:
  - `--file, -f` Path to the character CSV. Default: `~/.local/share/gaming_tools/data/wuwa_characters.csv`
  - Example:
    - `python src/main.py --file ~/.local/share/gaming_tools/data/wuwa_characters.csv`

## Building a single executable

A build script is provided using PyInstaller.

- Build:
  - `./scripts/build.sh`
- Run the packaged executable (after build):
  - `./dist/wuwa-team-picker`

You can set APP_NAME to change the output binary name, or pass a different entry script:
- `APP_NAME=my-picker ./scripts/build.sh`
- `./scripts/build.sh src/wuwa_char_random.py`

## Notes

- The CSV schema is validated at load time; invalid keys will raise an error.
- Terminal UI is implemented with curses; make sure your terminal window is large enough for the character cards.
