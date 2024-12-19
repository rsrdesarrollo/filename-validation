"""Filename validation CLI."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Sequence

from . import __version__

PROG = "validate-filename"
SNAKE_CASE_REGEX = "^[a-z_]+$"


def is_valid_filename(pattern: re.Pattern, filename: str, min_len: int = 3, verbose: bool = False) -> bool:
    """
    Check if a filename is valid.

    Parameters
    ----------
    filename : str
        The filename to inspect.
    min_len : int, optional
        Minimum acceptable length for filenames.

    Returns
    -------
    bool
        Whether the filename is valid.
    """
    if verbose:
        print(f"Validating {filename}...", end=None)

    name = Path(filename).stem

    if too_short := len(name) < min_len:
        print(f"Name too short ({min_len=}): {filename}")

    if no_regex := pattern.search(name) is None:
        print(f"Filename is not in snake case: {filename}")

    failure = too_short or no_regex

    if verbose and failure:
        print("[FAIL]")
    elif verbose:
        print("[OK]")

    return not failure


def main(argv: Sequence[str] | None = None) -> int:
    """
    Tool for validating a filename meets certain requirements.

    Parameters
    ----------
    argv : Sequence[str] | None, optional
        The arguments passed on the command line.

    Returns
    -------
    int
        Exit code for the process: if the filename fails validation,
        this will be 1 to stop a commit as a pre-commit hook.
    """
    parser = argparse.ArgumentParser(prog=PROG)
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames to process.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--min-len",
        default=3,
        type=int,
        help="Minimum length for a filename.",
    )

    parser.add_argument(
        "--regex",
        default=SNAKE_CASE_REGEX,
        type=str,
        help="Filename valid regex.",
    )

    parser.add_argument("-v", "--verbose", action="store_true")  # on/off flag

    args = parser.parse_args(argv)

    pattern = re.compile(args.regex)

    results = (
        not is_valid_filename(pattern, filename, args.min_len, args.verbose)
        for filename in args.filenames
    )
    return int(any(results))


if __name__ == "__main__":
    raise SystemExit(main())
