#!/usr/bin/env python3

import argparse
import os
import fnmatch
import logging

from lib_logging import setup_logging, log_block, log_function
setup_logging(level=logging.ERROR)

from lib_fileinput import get_file_paths_from_input


@log_function
def find_files(directory, file_pattern, recursive=False):
    """
    Searches for files where the filename exactly matches the given pattern.

    :param directory: The directory to search in.
    :param file_pattern: The complete filename pattern to match.
    :param recursive: Whether to search recursively in subdirectories.
    :return: Generator yielding file paths with filenames matching the pattern.
    """

    # print(f"Searching in: {directory} for pattern: {file_pattern}")
    if recursive:
        for root, dirs, files in os.walk(directory):
            # print(f"Checking directory: {root}")
            for filename in files:
                if fnmatch.fnmatch(filename, file_pattern):
                    yield os.path.join(root, filename)
    else:
        for filename in os.listdir(directory):
            # print(f"Checking file: {filename}")
            if fnmatch.fnmatch(filename, file_pattern):
                yield os.path.join(directory, filename)


def main():
    parser = argparse.ArgumentParser(description='Search for files matching a pattern.')
    parser.add_argument('pattern', help='Pattern to search for (e.g., *lib*).')
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='Optional directory to start searching from. Defaults to the current directory if not specified.')
    parser.add_argument('-r', '--recursive', action='store_true', help='Search recursively.')
    args = parser.parse_args()

    with log_block("find_files"):
        for file_path in find_files(args.directory, args.pattern, args.recursive):
            print(file_path)


if __name__ == "__main__":
    main()


