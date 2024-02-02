#!/usr/bin/env python3

import argparse
import os
import shutil
import sys
import logging

from lib_dryrun import dry_run_decorator, dry_run_context
from lib_fileinput import get_file_paths_from_input
from lib_logging import *

# Set up logging
# setup_logging(level=logging.DEBUG)
setup_logging(level=logging.ERROR)


@dry_run_decorator(dry_run_enabled=dry_run_flag)
def move_files(file_paths, destination):
    for file_path in file_paths:
        shutil.move(file_path, destination)


@dry_run_decorator(dry_run_enabled=dry_run_flag)
def delete_files(file_paths):
    for file_path in file_paths:
        os.remove(file_path)


@dry_run_decorator(dry_run_enabled=dry_run_flag)
def copy_files(file_paths, destination):
    for file_path in file_paths:
        shutil.copy(file_path, destination)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Perform actions on files such as move, delete, and copy.")

    parser.add_argument('--move', '-m', help="Move files to the specified directory.")
    parser.add_argument('--delete', '-d', action='store_true', help="Delete the specified files.")
    parser.add_argument('--copy', '-c', help="Copy files to the specified directory.")
    parser.add_argument('files', nargs='*', help="Files to perform actions on.")
    parser.add_argument('--dry-run', action='store_true', help="Simulate the rename operations without performing them.")

    parser.add_argument('--from-file', '-ff', help="Read file names from a file (one per line).")
    parser.add_argument('files', nargs='*', help="Files to be renamed.")

    # Add other arguments as necessary
    return parser.parse_args()



def main():
    args = parser.parse_args()

    # Determine the file paths to process
    file_paths, detected_dry_run = get_file_paths_from_input(args)

    # If dry-run was detected from piped input, override the script's dry-run state
    if detected_dry_run:
        args.dry_run = True

    if args.move:
        move_files(file_paths, args.move)
    elif args.delete:
        delete_files(file_paths)
    elif args.copy:
        copy_files(file_paths, args.copy)
    else:
        print("No action specified. Use --move, --delete, or --copy.")

if __name__ == "__main__":
    main()

