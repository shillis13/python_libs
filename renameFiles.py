#!/usr/bin/env python3

import argparse
import os
import re
import sys
import logging
import argparse

from lib_dryrun import dry_run_decorator, dry_run_context, dry_run_flag
from lib_fileinput import get_file_paths_from_input
from lib_logging import *

# setup_logging(level=logging.DEBUG)
setup_logging(level=logging.ERROR)


def dry_run_perform_rename(old_path, new_path, **kwargs):
    return f"Dry-run: '{old_path}' -> '{new_path}'"


@dry_run_decorator(custom_message=dry_run_perform_rename)
def perform_rename(old_path, new_path, dry_run=False):
    try:
        os.rename(old_path, new_path)
        log_info(f"Renamed '{old_path}' to '{new_path}'")
    except OSError as error:
        log_error(f"Error renaming file {old_path} to {new_path}: {error}")


@log_function
def matches_pattern(filename, match_pattern):
    """Check if the filename matches the given match pattern."""
    match_found = bool(re.search(match_pattern, filename))
    return match_found


def remove_vowels(s):
    """Remove vowels from the string.
    :param s: String from which vowels will be removed
    :return: String with vowels removed
    """
    result = re.sub(r'[aeiouAEIOU]', '', s)
    return result


def apply_case_transform(name, case_type):
    """Change the case of the string based on the specified case type.
    Args:
        name (str): String to transform.
        case_type (str): Type of case transformation ('upper', 'lower', 'proper').
    Returns:
        str: Transformed string.
    """
    transformed_name = name  # Default to original if no case_type matches

    if case_type == 'upper':
        transformed_name = name.upper()
    elif case_type == 'lower':
        transformed_name = name.lower()
    elif case_type == 'proper':
        transformed_name = name.title()
    elif case_type == 'title':
        transformed_name = name.title()

    return transformed_name


def replace(filename, pattern, replacement):
    """Replace a pattern in the filename with the specified replacement.
    :param filename: Name of the file
    :param pattern: Pattern to replace in the filename
    :param replacement: Replacement string
    :return: Updated filename with pattern replaced
    """
    return re.sub(pattern, replacement, filename)


@log_function
def process_files(file_paths, args, dry_run):
    """
    Process each file or directory in the provided file paths according to the specified arguments.
    This includes handling dry-run output piped as input for further processing.
    Args:
        file_paths (list): A list of file paths to process, which could come from direct input, a file, or piped from stdin.
        args (Namespace): Arguments containing options for matching, replacement, removing vowels, changing case, etc.
        dry_run (bool): Indicates whether to perform operations as a dry-run.
    """
    match_pattern = args.match if hasattr(args, 'match') and args.match else None

    for file_path in file_paths:
        file_path = file_path.strip()

        # For piped input from a dry-run, the file_path might not exist. Skip os.path checks if dry_run is True.
        if dry_run or os.path.exists(file_path):
            # Determine if the current path is a file (or treated as a file in dry-run mode)
            if not os.path.isdir(file_path) or file_path.endswith('/'):
                # If a match pattern is specified, ensure the file matches; otherwise, process the file
                if not match_pattern or matches_pattern(file_path, match_pattern):
                    rename_file(file_path, args, dry_run)
            else:
                # If it's a directory (and not in dry-run mode), process each file within it
                for filename in os.listdir(file_path):
                    full_path = os.path.join(file_path, filename)
                    if os.path.isfile(full_path) and (not match_pattern or matches_pattern(filename, match_pattern)):
                        rename_file(full_path, args, dry_run)
        else:
            log_debug(f"Skipping non-existing path: {file_path} (in non-dry-run mode)")


@log_function
def rename_file(file_path, args, dry_run):
    """
    Perform the renaming operation on a single file based on the specified transformations.
    Args:
        file_path (str): The path of the file to be renamed.
        args: Argument namespace containing transformation flags and values.
        dry_run (bool): Flag indicating whether to simulate the renaming without making actual changes.

    The function processes the file based on the specified flags and patterns in the order of:
    1. Pattern replacement (applied to the full filename including extension)
    2. Case change (applied to the base name only)
    3. Vowel removal (applied to the base name only)
    """

    directory, full_name = os.path.split(file_path)
    base_name, ext = os.path.splitext(full_name)

    # Apply pattern replacement if the match pattern is specified and the filename matches
    if args.match and args.replace and matches_pattern(full_name, args.match):
        full_name = replace(full_name, args.match, args.replace)
        base_name, ext = os.path.splitext(full_name)  # Re-split if pattern replacement changed the extension

    # Apply case transformation to the base name only
    if args.change_case:
        base_name = apply_case_transform(base_name, args.change_case)

    # Apply vowel removal to the base name only
    if args.remove_vowels:
        base_name = remove_vowels(base_name)

    # Construct the new file path
    new_path = os.path.join(directory, base_name + ext)

    # Perform the rename operation
    if new_path != file_path:
        # Call the decorated renaming function
        perform_rename(file_path, new_path, dry_run=dry_run)

        # if dry_run:
            # In the function that generates dry-run output
            # if dry_run and os.path.isdir(file_path):
                # log_out(f"dry-run: '{file_path}' -> '{new_path}/'")  
            # elif dry_run:
                # log_out(f"dry-run: '{file_path}' -> '{new_path}'")  
        # else:
            # os.rename(file_path, new_path)
            # log_out(f"{file_path}' -> '{new_path}'")  


def parse_arguments():
    parser = argparse.ArgumentParser(description="Rename files based on given patterns and transformations with optional dry-run simulation.")
    parser.add_argument('--dry-run', action='store_true', help="Simulate the rename operations without performing them.")
    parser.add_argument('--match', '-m', help="Match pattern to filter files.")
    parser.add_argument('--replace', '-rp', '-re', help="Replacement string for matched filenames.")
    parser.add_argument('--remove-vowels', '-rv', action='store_true', help="Remove vowels from filenames.")
    parser.add_argument('--change-case', '-cc', choices=['upper', 'lower', 'proper'], help="Change case of filenames.")
    parser.add_argument('--from-file', '-ff', help="Read file names from a file (one per line).")
    parser.add_argument('files', nargs='*', help="Files to be renamed.")
    # Add other arguments as necessary
    return parser.parse_args()


def main():
    args = parse_arguments()
    dry_run_flag = args.dry_run

    if args.replace and not args.match:
        parser.error("--replace requires --match to be specified.")
        sys.exit(1)


    # Determine the file paths to process
    file_paths, detected_dry_run = get_file_paths_from_input(args)

    # If dry-run was detected from piped input, override the script's dry-run state
    if detected_dry_run:
        args.dry_run = True

    process_files(file_paths, args, args.dry_run)


if __name__ == "__main__":
    # Continue with script logic, ensuring `dry_run_flag` is used where appropriate
    main()

