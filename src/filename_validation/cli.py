"""Filename validation CLI."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Sequence

from . import __version__

PROG = 'validate-filename'
SNAKE_CASE_REGEX = re.compile('^[a-z_]+$')


def is_valid_filename(filename: str, min_len: int = 3) -> bool:
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
    name = Path(filename).stem

    if too_short := len(name) < min_len:
        print(f'Name too short ({min_len=}): {filename}')

    if not_snake_case := SNAKE_CASE_REGEX.search(name) is None:
        print(f'Filename is not in snake case: {filename}')

    failure = too_short or not_snake_case
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
        'filenames',
        nargs='*',
        help='Filenames to process.',
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        '--min-len',
        default=3,
        type=int,
        help='Minimum length for a filename.',
    )

    args = parser.parse_args(argv)

    results = (
        not is_valid_filename(filename, args.min_len) for filename in args.filenames
    )
    return int(any(results))


if __name__ == '__main__':
    raise SystemExit(main())
