#!/usr/bin/env python3
"""Package save_game_script_cleaner as a single-file executable using PyInstaller.

Detects the current OS and architecture to name the output appropriately.

Steps:
  1. Validate Python venv exists
  2. Install dev dependencies (including PyInstaller) from requirements-dev.txt
  3. Run PyInstaller with --onefile
  4. Verify output exists, report file size

Output naming:
  save_game_script_cleaner-linux-x86_64
  save_game_script_cleaner-linux-arm64
  save_game_script_cleaner-mac-arm64
  save_game_script_cleaner-mac-x86_64
  save_game_script_cleaner-windows-x86_64.exe

Usage:
  python scripts/package_executable.py

Exit codes:
  0 = packaging succeeded
  1 = any step failed
"""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

IS_WINDOWS = platform.system() == "Windows"
VENV_PYTHON = (
    REPO_ROOT / "venv" / "Scripts" / "python.exe"
    if IS_WINDOWS
    else REPO_ROOT / "venv" / "bin" / "python"
)


def _normalize_arch(machine: str) -> str:
    """Normalize platform.machine() to a consistent architecture name."""
    m = machine.lower()
    if m in ("x86_64", "amd64"):
        return "x86_64"
    if m in ("arm64", "aarch64"):
        return "arm64"
    return m


def _os_name() -> str:
    s = platform.system()
    if s == "Linux":
        return "linux"
    if s == "Darwin":
        return "mac"
    if s == "Windows":
        return "windows"
    return s.lower()


def executable_name() -> str:
    """Build the output executable name for this platform."""
    name = (
        f"save_game_script_cleaner-{_os_name()}"
        f"-{_normalize_arch(platform.machine())}"
    )
    if IS_WINDOWS:
        name += ".exe"
    return name


class Logger:
    def info(self, msg: str) -> None:
        print(f"\u2713 {msg}", file=sys.stderr)

    def step(self, msg: str) -> None:
        print(file=sys.stderr)
        print("\u2501" * 47, file=sys.stderr)
        print(f"  {msg}", file=sys.stderr)
        print("\u2501" * 47, file=sys.stderr)

    def error(self, msg: str) -> None:
        print(file=sys.stderr)
        print(f"\u2717 ERROR: {msg}", file=sys.stderr)
        print(file=sys.stderr)


log = Logger()


def run(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[Any]:
    defaults: dict[str, Any] = {"check": True}
    defaults.update(kwargs)
    return subprocess.run(args, **defaults)


def check_venv() -> bool:
    log.step("Checking Python virtual environment")

    if not VENV_PYTHON.exists():
        log.error(f"Python venv not found at {VENV_PYTHON}")
        log.error(f"Run: cd {REPO_ROOT} && python3 -m venv venv")
        return False

    log.info(f"Python venv found: {VENV_PYTHON}")
    return True


def install_dependencies() -> bool:
    log.step("Installing dev dependencies")

    requirements = REPO_ROOT / "requirements-dev.txt"
    try:
        run([str(VENV_PYTHON), "-m", "pip", "install", "-r", str(requirements)])
    except subprocess.CalledProcessError:
        log.error("Failed to install dependencies")
        return False

    log.info("Dependencies installed")
    return True


def run_pyinstaller() -> bool:
    log.step("Running PyInstaller")

    name = executable_name()
    # Strip .exe suffix for PyInstaller --name (it adds .exe on Windows)
    pyinstaller_name = name.removesuffix(".exe")

    cmd = [
        str(VENV_PYTHON),
        "-m",
        "PyInstaller",
        "--onefile",
        "--name",
        pyinstaller_name,
        "--distpath",
        str(REPO_ROOT / "dist"),
        "--workpath",
        str(REPO_ROOT / "build" / "pyinstaller"),
        "--specpath",
        str(REPO_ROOT / "build" / "pyinstaller"),
    ]

    # --strip is only available on Unix
    if not IS_WINDOWS:
        cmd.append("--strip")

    cmd.append(str(REPO_ROOT / "save_game_script_cleaner.py"))

    try:
        run(cmd, cwd=str(REPO_ROOT))
    except subprocess.CalledProcessError:
        log.error("PyInstaller failed")
        return False

    log.info("PyInstaller completed")
    return True


def verify_output() -> bool:
    log.step("Verifying output")

    name = executable_name()
    output = REPO_ROOT / "dist" / name

    if not output.exists():
        log.error(f"Expected output not found: {output}")
        return False

    size_bytes = output.stat().st_size
    if size_bytes >= 1024 * 1024:
        size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        size_str = f"{size_bytes / 1024:.1f} KB"

    log.info(f"Output: {output}")
    log.info(f"Size: {size_str}")

    # On Unix, verify it's executable
    if not IS_WINDOWS and not os.access(output, os.X_OK):
        log.error("Output exists but is not executable")
        return False

    log.info("Executable verified")
    return True


def main() -> int:
    name = executable_name()
    log.step(f"Packaging save_game_script_cleaner: {name}")
    log.info(f"repo_root: {REPO_ROOT}")

    if not check_venv():
        return 1

    if not install_dependencies():
        return 1

    if not run_pyinstaller():
        return 1

    if not verify_output():
        return 1

    log.step("\u2713 Packaging complete!")
    log.info(f"Run: {REPO_ROOT / 'dist' / name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
