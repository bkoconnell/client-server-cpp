#!/usr/bin/env python3
import unittest, shutil, os, sys
from pathlib import Path
import lint_directory_names as lint
import logging

# Global variables
rootdir = 'pipeline_scripts/tests/rootdir'

# Disable logging
logging.disable(logging.CRITICAL)


class TestLintDirectoryNames(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Path(rootdir).joinpath('dir1').joinpath('subdir1').joinpath('upperCase').mkdir(parents=True, exist_ok=True)
        Path(rootdir).joinpath('dir2').joinpath('subdir2').joinpath('a space').mkdir(parents=True, exist_ok=True)
        Path(rootdir).joinpath('dir3').joinpath('subdir3').joinpath(' space').mkdir(parents=True, exist_ok=True)
        Path(rootdir).joinpath('dir3').joinpath('subdir3').joinpath('space ').mkdir(parents=True, exist_ok=True)
        Path(rootdir).joinpath('dir4').joinpath('Case and Space').mkdir(parents=True, exist_ok=True)
        Path(rootdir).joinpath('dir5').joinpath('abc').mkdir(parents=True, exist_ok=True)
        Path(rootdir).joinpath('123').mkdir(exist_ok=True)
        Path(rootdir).joinpath('._!@#$-+=').mkdir(exist_ok=True)
        Path(rootdir).joinpath('atestfile.testfile').touch(exist_ok=True)

    def test_resolve_path(self):
        path = Path(rootdir)
        exp = path.resolve()
        act = lint.resolve_path(path)
        self.assertEqual(exp, act)
    
    def test_resolve_path_filenotfound(self):
        with self.assertRaises(FileNotFoundError):
            path = Path('This is not a valid path')
            lint.resolve_path(path)

    def test_is_directory(self):
        path = Path(rootdir).joinpath('dir1')
        exp = path.is_dir()
        act = lint.is_directory(path)
        self.assertEqual(exp, act)

    def test_is_directory_sysexit(self):
        with self.assertRaises(SystemExit) as cm:
            path = Path(rootdir).joinpath('atestfile.testfile')
            lint.is_directory(path)
        self.assertEqual(2, cm.exception.code)

    def test_store_excluded_dirs(self):
        dir1 = 'this/is/path/01'
        dir2 = 'this/is/path/02'
        path1 = os.path.join(rootdir, dir1)
        path2 = os.path.join(rootdir, dir2)
        dirs = [dir1, dir2]
        exp = [path1, path2]
        act = lint.store_excluded_dirs(rootdir, dirs)
        self.assertEqual(exp, act)
    
    def test_store_excluded_dirs_empty(self):
        dirs = None
        self.assertIsNotNone(lint.store_excluded_dirs(rootdir, dirs))

    def test_get_dirs_to_check(self):
        # Valid directories
        dir1 = Path(rootdir).joinpath('dir1')
        dir2 = Path(rootdir).joinpath('dir1').joinpath('subdir1')
        dir3 = Path(rootdir).joinpath('dir1').joinpath('subdir1').joinpath('upperCase')
        dir4 = Path(rootdir).joinpath('dir2')
        dir5 = Path(rootdir).joinpath('dir2').joinpath('subdir2')
        dir6 = Path(rootdir).joinpath('dir2').joinpath('subdir2').joinpath('a space')
        dir7 = Path(rootdir).joinpath('dir3')
        dir8 = Path(rootdir).joinpath('dir4')
        dir9 = Path(rootdir).joinpath('dir5')
        dir10 = Path(rootdir).joinpath('dir5').joinpath('abc')
        dir11 = Path(rootdir).joinpath('._!@#$-+=')
        exp = [dir1, dir2, dir3, dir4, dir5, dir6, dir7, dir8, dir9, dir10, dir11]
        # Excluded directories
        exc1 = os.path.join(rootdir, 'dir3', 'subdir3')
        exc2 = os.path.join(rootdir, 'dir4', 'Case and Space')
        exc3 = os.path.join(rootdir, '123')
        excluded_dirs = [exc1, exc2, exc3]
        act = lint.get_dirs_to_check(rootdir, excluded_dirs)
        self.assertCountEqual(exp, act)

    def test_validate_dirs_case(self):
        dir1 = Path('lower case')
        dir2 = Path('.lower_case123')
        dir3 = Path('lowercase')
        dirs = [dir1, dir2, dir3]
        exp = []
        act = lint.validate_dirs_case(dirs)
        self.assertEqual(exp, act)

    def test_validate_dirs_case_nums(self):
        path1 = Path(rootdir).joinpath('dir2').joinpath('subdir2')        
        path2 = Path(rootdir).joinpath('123')
        exp = []
        act = lint.validate_dirs_case([path1, path2])
        self.assertEqual(exp, act)

    def test_validate_dirs_case_chars(self):
        path1 = Path(rootdir).joinpath('dir3').joinpath('subdir3').joinpath(' space')
        path2 = Path(rootdir).joinpath('._!@#$-+=')
        exp = []
        act = lint.validate_dirs_case([path1, path2])
        self.assertEqual(exp, act)

    def test_validate_dirs_case_uppercase(self):
        path1 = Path(rootdir).joinpath('dir1').joinpath('subdir1')
        path2 = Path(rootdir).joinpath('dir1').joinpath('subdir1').joinpath('upperCase')
        path3 = Path(rootdir).joinpath('dir4').joinpath('Case and Space')
        exp = [path2, path3]
        act = lint.validate_dirs_case([path1, path2, path3])
        self.assertEqual(exp, act)

    def test_validate_dirs_space(self):
        path1 = Path(rootdir).joinpath('dir1').joinpath('subdir1').joinpath('upperCase')
        path2 = Path(rootdir).joinpath('dir2').joinpath('subdir2').joinpath('a space')
        path3 = Path(rootdir).joinpath('dir3').joinpath('subdir3').joinpath(' space')
        path4 = Path(rootdir).joinpath('dir3').joinpath('subdir3').joinpath('space ')
        path5 = Path(rootdir).joinpath('dir4').joinpath('Case and Space')
        exp = [path2, path3, path4, path5]
        act = lint.validate_dirs_space([path1, path2, path3, path4, path5])
        self.assertEqual(exp, act)

    def test_evaluate_failures(self):
        path1 = Path(rootdir).joinpath('dir2').joinpath('subdir2').joinpath('a space')
        path2 = Path(rootdir).joinpath('dir3').joinpath('subdir3').joinpath(' space')
        dirs = [path1, path2]
        root = Path(rootdir).stem
        failure = 'spaces'
        self.assertTrue(lint.evaluate_failures(root, dirs, failure))

    def test_case_failed(self):
        with self.assertRaises(SystemExit) as cm:
            root = os.path.join(rootdir, 'dir1', 'subdir1')
            sys.argv.extend(['-r', root])
            lint.main()
        self.assertEqual(1, cm.exception.code)

    def test_space_failed(self):
        with self.assertRaises(SystemExit) as cm:
            root = os.path.join(rootdir, 'dir2', 'subdir2')
            sys.argv.extend(['-r', root])
            lint.main()
        self.assertEqual(1, cm.exception.code)

    def test_case_and_space_failed(self):
        with self.assertRaises(SystemExit) as cm:
            root = os.path.join(rootdir, 'dir4')
            sys.argv.extend(['-r', root])
            lint.main()
        self.assertEqual(1, cm.exception.code)

    def test_case_and_space_passed(self):
        root = os.path.join(rootdir, 'dir5')
        sys.argv.extend(['-r', root])
        msg = "test_case_and_space_passed() failed unexpectedly."
        try:
            lint.main()
        except SystemExit:
            self.fail(f'{msg}')


    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(rootdir)


# Entry Point
if __name__ == "__main__":
    unittest.main()