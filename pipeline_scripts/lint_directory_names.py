#!/usr/bin/env python3
import argparse, sys, re, os
from pathlib import Path
import logging

# TODO: Docstring for Script.

# Setup logger
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')


def parse_CL_args():
    """Parses command-line arguments passed in."""
    logging.debug("parse_CL_args() function.")
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root",
                        type=Path,
                        default=('.'),
                        help="""
                        Optionally specify a root directory. Default='.'\n\n
                        Usage: python3 lint_directory_names.py --root "./rel/path/dir_name"\n\n
                        """)
    parser.add_argument("-d", "--directories",
                        nargs='*',
                        help="""
                        An optional list of directory paths to exclude from lint check.\n\n
                        Usage: python3 lint_directory_names.py 
                        --directories "rel/path/dir_1" "rel/path/dir_2\n\n"
                        Note: The directory path is relative to the --root directory.\n\n
                        """)
    args = parser.parse_args()
    # Resolve path for 'root' arg
    try:
        root_arg = args.root.resolve(strict=True)
    except FileNotFoundError as err:
        msg = f"Invalid CL arg:  --root '{args.root}' is not a valid path."
        logging.critical(f"{msg}\nFileNotFoundError: {err}")
        sys.exit(2)
    # Verify 'root' arg is a directory, not a file
    if not root_arg.is_dir():
        msg = f"Invalid CL arg:  --root '{args.root}' is not a directory."
        logging.critical(f"{msg}")
        sys.exit(2)
    # Store 'directories' arg
    dir_args = []
    if args.directories is not None:
        dir_args = [os.path.join(root_arg, d) for d in args.directories]
    return root_arg, dir_args


def get_dirs_to_check(root_dir, excluded_dirs):
    """Generates a list of valid directories to be checked."""
    logging.debug("get_dirs_to_check() function.")
    join = os.path.join
    valid_directories = []
    # Store paths for directories/sub-directories, except excluded ones
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [Path(root).joinpath(dir) 
                   for dir in dirs if join(root, dir) not in excluded_dirs]
        valid_directories.extend(dirs)
    return valid_directories


def validate_dir_names(dirs):
    """Identifies any directories with uppercase letters or spaces."""
    logging.debug("validate_dir_names()")
    dirs_failed_lower = []
    dirs_failed_spaces = []
    # TODO: Finish implementing


def main():

    # Parse CL args
    args = parse_CL_args()
    root = args[0].stem

    # Identify valid directories for lint check
    valid_dirs = get_dirs_to_check(args[0], args[1])

    # Initialize bools
    lowercase_failed = False
    spaces_failed = False

    # TODO: Check if directories conform to Lint requirements
    lower, spaces = validate_dir_names(valid_dirs)


# Entry Point
if __name__ == "__main__":
    logging.debug("Start of program.")
    main()