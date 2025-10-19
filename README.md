# Wuwa Team Picker

A terminal-based helper for Wuthering Waves that picks random characters and helps you build teams via simple interactive modes:
- Random Character Picker
- Team Roulette

This project was written by AI as an experiment on how to vibe code. While it does run on the creators machine, treat it like it has not been verified by a human.

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

You can build using uv, which installs and runs the project's build entry point.

TUI (default):
- Build:
  - `uv run build`
- Run the packaged executable (after build):
  - `./dist/wuwa-team-picker`

GUI (PySide6):
- Make sure GUI dependencies are installed (first time only):
  - `uv sync --group gui`
- Build:
  - `uv run build -- --gui`
- Run the packaged executable (after build):
  - `./dist/wuwa-team-picker-gui`

Advanced:
- Change output binary name:
  - `APP_NAME=my-picker uv run build`
- Build a different entry script:
  - `uv run build -- src/wuwa_char_random.py`
- You can still call the underlying script directly:
  - `./scripts/build.sh` or `UI_FLAVOR=gui ./scripts/build.sh`

## Notes

- The CSV schema is validated at load time; invalid keys will raise an error.
- Terminal UI is implemented with curses; make sure your terminal window is large enough for the character cards.

## CSV schema

```csv
name,level,ascension,talent_basic_atk,talent_skill,talent_forte,talent_liberation,talent_intro,sequence,element,quality
```
