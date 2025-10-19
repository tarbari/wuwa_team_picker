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

# Choose Python from the project venv if present; fall back to system python
if [[ -x ".venv/bin/python" ]]; then
  PYTHON=".venv/bin/python"
else
  PYTHON="$(command -v python3 || command -v python)"
fi

# Ensure GUI deps are available when building GUI
if [[ "${UI_FLAVOR}" == "gui" ]]; then
  if ! "${PYTHON}" -c "import PySide6" >/dev/null 2>&1; then
    echo "ERROR: PySide6 not found in ${PYTHON}."
    echo "Install GUI deps first:"
    echo "  uv sync --group gui"
    echo "or:"
    echo "  ${PYTHON} -m pip install PySide6"
    exit 1
  fi
fi

# Run PyInstaller via the selected Python to use the correct environment
PI_CMD=("${PYTHON}" -m PyInstaller)

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
