"""Command line interface"""

import argparse
from pathlib import Path
import sys

from .morse import MorseCode


def main(argv: list[str] = None) -> None:
    """Read WAV file, process it and write outputs to stdout

    Args:
        argv (list[str]): List of command line arguments. Defaults to None.

    Raises:
        UserWarning: If dash/dot separation cannot be made unambiguosly,
            or if input file does not exist.
    """
    parsed_args = _parse_args(argv)
    file = parsed_args.FILEPATH
    is_mp3 = parsed_args.is_mp3

    if not Path(file).exists():
        sys.stderr.write(f"File {file} not found, exiting.\n")
        sys.exit(1)

    try:
        if is_mp3:
            decoded = MorseCode.from_mp3file(file).decode()
        else:
            decoded = MorseCode.from_wavfile(file).decode()
        sys.stdout.write(decoded + "\n")
    except UserWarning as err:
        sys.stderr.write(f"{err}\n")
        sys.exit(1)


def _parse_args(args: list[str]) -> argparse.Namespace:
    """Parse arguments from command line"""
    parser = argparse.ArgumentParser(
        description="""Read audio file in WAV format, extract the morse code and
        write translated text into standard output."""
    )
    parser.add_argument("FILEPATH", help="Input audio file")
    parser.add_argument('--is_mp3', action='store_true')
    return parser.parse_args(args)


if __name__ == "__main__":
    main()
