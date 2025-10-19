#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build the application using PyInstaller.")
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Build the GUI version (sets UI_FLAVOR=gui).",
    )
    parser.add_argument(
        "entry_script",
        nargs="?",
        help="Optional entry script to pass to scripts/build.sh (defaults based on UI_FLAVOR).",
    )
    args = parser.parse_args(argv)

    project_root = Path(__file__).resolve().parent.parent
    build_script = project_root / "scripts" / "build.sh"

    if not build_script.exists():
        print(f"ERROR: Build script not found: {build_script}", file=sys.stderr)
        return 1

    env = os.environ.copy()
    if args.gui:
        env["UI_FLAVOR"] = "gui"

    cmd = [str(build_script)]
    if args.entry_script:
        cmd.append(args.entry_script)

    result = subprocess.run(cmd, env=env)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
