#!/usr/bin/env bash
# Build the application into a single executable using PyInstaller.
# Usage:
#   ./scripts/build.sh [entry_script]
# Example:
#   ./scripts/build.sh
#   ./scripts/build.sh src/main.py
set -euo pipefail

APP_NAME="${APP_NAME:-wuwa-team-picker}"
UI_FLAVOR="${UI_FLAVOR:-tui}"  # 'tui' or 'gui'
ENTRY_SCRIPT="${1:-}"

if [[ -z "${ENTRY_SCRIPT}" ]]; then
  if [[ "${UI_FLAVOR}" == "gui" ]]; then
    ENTRY_SCRIPT="src/main_gui.py"
    if [[ "${APP_NAME}" == "wuwa-team-picker" ]]; then
      APP_NAME="wuwa-team-picker-gui"
    fi
  else
    ENTRY_SCRIPT="src/main.py"
  fi
fi

# Resolve project root (directory containing this script's parent)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# Clean previous builds
rm -rf build dist "${APP_NAME}.spec"

# Choose PyInstaller launcher
if command -v pyinstaller >/dev/null 2>&1; then
  PI_CMD=(pyinstaller)
elif command -v uv >/dev/null 2>&1; then
  PI_CMD=(uvx pyinstaller)
else
  echo "PyInstaller not found. Install it with one of:"
  echo "  uv tool install pyinstaller"
  echo "  pipx install pyinstaller"
  echo "  python -m pip install pyinstaller"
  exit 1
fi

# Configure extra args based on UI flavor
EXTRA_ARGS=()
if [[ "${UI_FLAVOR}" == "gui" ]]; then
  EXTRA_ARGS+=(--hidden-import PySide6.QtCore --hidden-import PySide6.QtGui --hidden-import PySide6.QtWidgets)
fi

# Build single-file executable
"${PI_CMD[@]}" \
  --clean \
  --noconfirm \
  --onefile \
  --name "${APP_NAME}" \
  --paths src \
  "${EXTRA_ARGS[@]}" \
  "${ENTRY_SCRIPT}"

echo "Build complete. Executable is at: dist/${APP_NAME}"
