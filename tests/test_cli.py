"""Test the CLI."""

import subprocess
import sys

import pytest

from filename_validation import cli


def test_cli_version(capsys):
    """Confirm that --version works."""
    with pytest.raises(SystemExit):
        cli.main(['--version'])
    assert f'{cli.PROG} {cli.__version__}' == capsys.readouterr().out.strip()


@pytest.mark.parametrize(
    ['filename', 'min_len'], [['x.py', 2], ['x.py', 3], ['/long-path/x.py', 2]]
)
def test_filename_too_short(capsys, filename, min_len):
    """Test that filenames that are too short are flagged."""
    assert not cli.is_valid_filename(filename, min_len=min_len)
    assert 'too short' in capsys.readouterr().out.strip()


@pytest.mark.parametrize(
    'filename',
    ['HelloWorld.py', 'Test.py', '/path/.something.py'],
)
def test_snake_case(capsys, filename):
    """Test that filenames that aren't in snake case are flagged."""
    assert not cli.is_valid_filename(filename)
    assert 'snake case' in capsys.readouterr().out.strip()


@pytest.mark.parametrize('filename', ['AB.py', 'A-B.py'])
def test_invalid_filenames(capsys, filename):
    """Test that filenames invalid in multiple ways are flagged."""
    assert not cli.is_valid_filename(filename, min_len=20)

    out = capsys.readouterr().out.strip()
    assert 'too short' in out and 'snake case' in out


@pytest.mark.parametrize(
    'filename',
    [
        'src/filename_validation/cli.py',
        'src/filename_validation/__init__.py',
        'validate_filename.py',
    ],
)
def test_valid_filenames(filename):
    """Test that valid filenames pass the tests."""
    assert cli.is_valid_filename(filename)


@pytest.mark.parametrize(
    ['filenames', 'min_len', 'expected'],
    [
        ['x.py', 2, 1],
        [
            [
                'src/filename_validation/cli.py',
                'src/filename_validation/__init__.py',
            ],
            3,
            0,
        ],
        [
            [
                'src/filename_validation/cli.py',
                'src/filename_validation/__init__.py',
            ],
            4,
            1,
        ],
        [
            [
                'src/filename_validation/cli.py',
                'HelloWorld.py',
            ],
            4,
            1,
        ],
        [
            [
                'src/filename_validation/cli.py',
                'HelloWorld.py',
            ],
            3,
            1,
        ],
    ],
)
def test_cli(filenames, min_len, expected):
    """Test the CLI."""
    result = cli.main([*filenames, '--min-len', str(min_len)])
    assert result == expected


@pytest.mark.parametrize(['arg', 'return_code'], [['--version', 0], ['x.py', 1]])
def test_main_access_cli(arg, return_code):
    """Confirm that CLI can be accessed via python -m."""
    result = subprocess.run([sys.executable, '-m', 'filename_validation.cli', arg])
    assert result.returncode == return_code
