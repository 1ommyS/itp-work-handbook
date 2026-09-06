"""Bootstrap and run MkDocs identically on Windows, macOS, Linux and CI."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv"
PYTHON = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
LOCK = ROOT / "requirements.txt"
STAMP = VENV / ".requirements.sha256"


def run(args: list[str], **kwargs: object) -> None:
    subprocess.run(args, cwd=ROOT, check=True, **kwargs)


def bootstrap() -> None:
    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10+ is required; Python 3.12 is used in CI.")
    if not PYTHON.exists():
        print("Creating .venv...", flush=True)
        venv.create(VENV, with_pip=True)
    digest = hashlib.sha256(LOCK.read_bytes()).hexdigest()
    if not STAMP.exists() or STAMP.read_text(encoding="utf-8").strip() != digest:
        run([str(PYTHON), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(LOCK)])
        run([str(PYTHON), "-m", "pip", "check"])
        STAMP.write_text(digest + "\n", encoding="utf-8")


def git_dates_available() -> bool:
    """An empty repository or source archive must work before the first commit."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", "docs"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        return result.returncode == 0 and bool(result.stdout.strip())
    except FileNotFoundError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["bootstrap", "serve", "build", "check"])
    parser.add_argument("--dev-addr", default="127.0.0.1:8000", help="Address for serve")
    args = parser.parse_args()
    bootstrap()
    if args.command == "bootstrap":
        print("Documentation dependencies are ready.")
        return

    env = os.environ.copy()
    env.setdefault("ENABLE_GIT_DATES", "true" if git_dates_available() else "false")
    if args.command == "serve":
        run([str(PYTHON), "-m", "mkdocs", "serve", "--dev-addr", args.dev_addr], env=env)
        return
    if args.command == "check":
        run([str(PYTHON), str(ROOT / "scripts/check_docs.py"), "source"])
    run([str(PYTHON), "-m", "mkdocs", "build", "--strict"], env=env)
    if args.command == "check":
        run([str(PYTHON), str(ROOT / "scripts/check_docs.py"), "site"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(130)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode)
