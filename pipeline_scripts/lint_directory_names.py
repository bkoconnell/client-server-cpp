#!/usr/bin/env python3
import argparse, sys, os
from pathlib import Path
import logging

# TODO: Docstring for Script.

# Setup logger
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')


def resolve_path(path):
    """Resolves a given path, directory, or filename. Exception thrown if invalid path."""
    logging.debug("resolve_path() function.")
    try:
        resolved_path = path.resolve(strict=True)
    except FileNotFoundError as err:
        msg = f"Invalid CL arg:  --root '{path}' is not a valid path."
        logging.critical(f"{msg}\nFileNotFoundError: {err}")
        sys.exit(2)
    logging.info(f"--root:\t{resolved_path}")
    return resolved_path


def is_directory(dir):
    """Checks that the given arg is a directory."""
    logging.debug("is_directory() function.")
    if not dir.is_dir():
        msg = f"Invalid CL arg:  --root '{dir}' is not a directory."
        logging.critical(f"{msg}")
        sys.exit(2)


def store_excluded_dirs(root, dirs):
    """Store the CL args passed in for list of directories to be excluded from lint check."""
    logging.debug("store_excluded_dirs() function.")
    excluded = []
    if dirs is not None:
        excluded = [os.path.join(root, dir) for dir in dirs]
    logging.info(f"--exclude:\t{excluded}")
    return excluded


def parse_CL_args():
    """Parses command-line arguments passed in."""
    logging.debug("parse_CL_args() function.")

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root",
                        type=Path,
                        default=('..'),
                        help="""
                        Optionally specify a root directory. Default='.'\n\n
                        Usage: python3 lint_directory_names.py --root "./rel/path/dir_name"\n\n
                        """)
    parser.add_argument("-e", "--exclude",
                        nargs='*',
                        help="""
                        An optional list of directory paths to exclude from lint check.\n\n
                        Usage: python3 lint_directory_names.py 
                        --exclude "rel/path/dir_1" "rel/path/dir_2\n\n"
                        Note: The directory path is relative to the --root directory.\n\n
                        """)
    args = parser.parse_args()
    return args


def get_dirs_to_check(root_dir, excluded):
    """Generates a list of valid directories to be checked."""
    logging.debug("get_dirs_to_check() function.")

    join = os.path.join
    valid_directories = []

    # Store paths for directories/sub-directories, except excluded ones
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [Path(root).joinpath(dir) 
                   for dir in dirs if join(root, dir) not in excluded]
        valid_directories.extend(dirs)

    return valid_directories


def validate_dir_names(dirs):
    """Identifies any directories with uppercase letters or spaces."""
    logging.debug("validate_dir_names()")
    dirs_failed_lower = []
    dirs_failed_spaces = []

    for dir in dirs:
        # Check for any uppercase letters in the name
        if not dir.stem.islower():
            dirs_failed_lower.append(dir)
        # Check for any spaces in the name
        if ' ' in dir.stem:
            dirs_failed_spaces.append(dir)
    
    return dirs_failed_lower, dirs_failed_spaces


def evaluate_failures(root, failed_dirs):
    """Outputs the relative path of directories that failed the lint check."""

    for dir in failed_dirs:
        path = Path()
        root_idx = dir.parts.index(root)
        for part in dir.parts[root_idx+1:]:
            path = os.path.join(path, part)
        print(f'\t\t\t\t{path}')
    print('\n')


def main():

    # Parse & validate CL args
    args = parse_CL_args()
    root = resolve_path(args.root)
    is_directory(root)
    excluded_dirs = store_excluded_dirs(root, args.exclude)

    # Identify valid directories for lint check
    valid_dirs = get_dirs_to_check(root, excluded_dirs)

    # Check if directories conform to Lint requirements
    lower, spaces = validate_dir_names(valid_dirs)

    # Evaluate any failures for Uppercase letters
    if not lower:
        lowercase_failed = False
        logging.info("All directories adhere to the 'lowercase' naming convention.")
    else:
        lowercase_failed = True
        msg = "The following directories failed lint test due to uppercase letters:\n"
        logging.info(msg)
        evaluate_failures(root.stem, lower)
    # Evaluate any failures for Spaces
    if not spaces:
        spaces_failed = False
        logging.info("All directories adhere to the 'no spaces' naming convention.")
    else:
        spaces_failed = True
        msg = "The following directories failed lint test due to spaces in the name:\n"
        logging.info(msg)
        evaluate_failures(root.stem, spaces)

    # End script
    if lowercase_failed or spaces_failed:
        sys.exit(1)
    else:
        sys.exit(0)


# Entry Point
if __name__ == "__main__":
    logging.debug("Start of program.")
    main()