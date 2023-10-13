#!/usr/bin/env python3
import argparse, sys, os, re
from pathlib import Path
import logging

# TODO: Docstring for Script.

# Setup logger
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
std_format = logging.Formatter(' %(asctime)s - %(levelname)s:  %(message)s')
debug_format = logging.Formatter(' %(asctime)s - %(module)s - %(lineno)d - %(funcName)s - %(levelname)s:  %(message)s')
# Handler for logging console output
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(std_format)
logger.addHandler(console_handler)
# Handler for writing to logfile
logfilepath = 'pipeline_scripts/tmp/'
logfilename = 'lint_directory_names.log'
logfile = os.path.join(logfilepath, logfilename)
os.makedirs(logfilepath, exist_ok=True)
logfile_handler = logging.FileHandler(logfile, 'w', encoding='utf-8')
logfile_handler.setLevel(logging.INFO)
logfile_handler.setFormatter(std_format)
logger.addHandler(logfile_handler)

# -------------------------------------------------

def parse_CL_args():
    """Parses command-line arguments passed in."""
    logger.info("Parsing command-line args...")

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root",
                        type=Path,
                        default=('.'),
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
    parser.add_argument("-l", "--loglevel",
                        default='INFO',
                        choices=['DEBUG', 'debug'],
                        help="""
                        An optional flag for the logfile's logging level.
                        To override the default(INFO), use DEBUG
                        Usage: python3 lint_directory_names.py --loglevel DEBUG
                        """
                        )
    args = parser.parse_args()
    # Check if loglevel should be set to DEBUG for the logfile
    loglevel = args.loglevel.upper()
    if loglevel == 'DEBUG':
        logfile_handler.setLevel(logging.DEBUG)
        logfile_handler.setFormatter(debug_format)
    return args


def resolve_path(path: Path) -> Path:
    """Resolves a given path, directory, or filename. Exception thrown if invalid path."""
    logger.debug(f"Calling resolve_path({path})")
    try:
        resolved_path = path.resolve(strict=True)
    except FileNotFoundError:
        msg = f"Invalid CL arg:  --root '{path}' is not a valid path."
        logger.critical(f"{msg}")
        raise
    logger.info(f"--root:\t{resolved_path}")
    return resolved_path


def is_directory(dir: Path) -> bool:
    """Checks that the given arg is a directory."""
    logger.debug(f"Calling is_directory({dir})")
    if not dir.is_dir():
        msg = f"Invalid CL arg:  --root '{dir}' is not a directory."
        logger.critical(f"{msg}")
        sys.exit(2)
    return True


def store_excluded_dirs(root: Path, dirs: list) -> list:
    """Store the CL args passed in for list of directories to be excluded from lint check."""
    logger.debug(f"Calling store_excluded_dirs({root}, {dirs})")
    excluded = []
    if dirs is not None:
        excluded = [os.path.join(root, dir) for dir in dirs]
    logger.info(f"--exclude:\t{excluded}")
    return excluded


def get_dirs_to_check(root_dir: Path, excluded: list) -> list:
    """Generates a list of valid directories to be checked."""
    logger.debug(f"Calling get_dirs_to_check({root_dir}, {excluded})")
    join = os.path.join
    valid_directories = []
    # Store paths for directories/sub-directories, except excluded ones
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [dir for dir in dirs if join(root, dir) not in excluded]
        path_dirs = [Path(root).joinpath(dir) for dir in dirs]
        valid_directories.extend(path_dirs)
    return valid_directories


def validate_dirs_case(dirs: list) -> list:
    """Identifies directories with uppercase letters in the name."""
    logger.debug(f"Calling validate_dirs_case({dirs})")
    reg = re.compile('[A-Z]')
    dirs_with_upper = [dir for dir in dirs if reg.search(dir.stem) is not None]
    return dirs_with_upper


def validate_dirs_space(dirs: list) -> list:
    """Identifies directories with spaces in the name."""
    logger.debug(f"Calling validate_dirs_space({dirs})")
    dirs_with_space = [dir for dir in dirs if ' ' in dir.stem]
    return dirs_with_space


def evaluate_failures(root: str, failed_dirs: list, failure: str) -> bool:
    """Outputs the relative path of directories that failed the lint check."""
    logger.debug(f"Calling evaluate_failures({root}, {failed_dirs}, {failure})")
    logger.warning(f"The following directories failed lint test due to {failure}:")
    for dir in failed_dirs:
        path = Path()
        root_idx = dir.parts.index(root)
        for part in dir.parts[root_idx+1:]:
            path = os.path.join(path, part)
        logger.warning(f'\t\t{path}')
    return True


def main():

    # Parse & validate CL args
    args = parse_CL_args()
    root = resolve_path(args.root)
    is_directory(root)
    excluded_dirs = store_excluded_dirs(root, args.exclude)

    # Identify valid directories for lint check
    valid_dirs = get_dirs_to_check(root, excluded_dirs)

    # Check if directories conform to Lint requirements
    case_failures = validate_dirs_case(valid_dirs)
    space_failures = validate_dirs_space(valid_dirs)

    # Evaluate any failures for Uppercase letters
    if not case_failures:
        logger.info("All directories adhere to the 'lowercase' naming convention.")
        case_failed = False
    else:
        failure = 'uppercase letters'
        case_failed = evaluate_failures(root.stem, case_failures, failure)

    # Evaluate any failures for Spaces
    if not space_failures:
        logger.info("All directories adhere to the 'no spaces' naming convention.")
        space_failed = False
    else:
        failure = 'spaces in the name'
        space_failed = evaluate_failures(root.stem, space_failures, failure)

    # End script with failures
    if case_failed or space_failed:
        logger.warning(f'''
                      Lint check for directory naming convention has failed.\n
                      Please see the log file saved to Jenkins artifacts, or here:\n
                      {Path(logfile).resolve()}
                      ''')
        sys.exit(1)
    logger.info("Lint check for directory naming convention has passed.")


# Entry Point
if __name__ == "__main__":
    logger.debug("Starting 'lint_directory_names' script.")
    main()