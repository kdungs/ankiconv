#!/usr/bin/env python

import argparse
import pathlib
import sys

import ankiconv.converter


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert some markdown to Anki flashcards."
    )
    parser.add_argument("file", type=pathlib.Path)
    args = parser.parse_args()
    result = ankiconv.converter.convert(args.file)
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
