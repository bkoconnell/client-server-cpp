#!/usr/bin/env python3
import unittest
import shutil
import os
from pathlib import Path
import lint_directory_names as lint

# Global variables
rootdir = 'rootdir'

class TestLintDirectoryNames(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Path(rootdir).joinpath('dir1').joinpath('subdir1').joinpath('upperCase').mkdir(parents=True, exist_ok=True)
        Path(rootdir).joinpath('dir2').joinpath('subdir2').joinpath('a space').mkdir(parents=True, exist_ok=True)
        Path(rootdir).joinpath('dir3').joinpath('subdir3').joinpath(' space').mkdir(parents=True, exist_ok=True)
        Path(rootdir).joinpath('dir3').joinpath('subdir3').joinpath('space ').mkdir(parents=True, exist_ok=True)
        Path(rootdir).joinpath('Case and Space').mkdir(exist_ok=True)
        Path(rootdir).joinpath('123').mkdir(exist_ok=True)
        Path(rootdir).joinpath('atestfile.testfile').touch(exist_ok=True)

    def test_resolve_path(self):
        path = Path(rootdir)
        self.assertEqual(path.resolve(), lint.resolve_path(path))
    
    def test_resolve_path_filenotfound(self):
        with self.assertRaises(FileNotFoundError):
            path = Path('This is not a valid path')
            lint.resolve_path(path)

    def test_is_directory(self):
        path = Path(rootdir).joinpath('dir1')
        self.assertEquals(path.is_dir(), lint.is_directory(path))

    def test_is_directory_sysexit(self):
        with self.assertRaises(SystemExit) as cm:
            path = Path(rootdir).joinpath('atestfile.testfile')
            lint.is_directory(path)
        self.assertEqual(cm.exception.code, 2)

    def test_store_excluded_dirs(self):
        dir1 = 'this/is/path/01'
        dir2 = 'this/is/path/02'
        path1 = os.path.join(rootdir, dir1)
        path2 = os.path.join(rootdir, dir2)
        dirs = [dir1, dir2]
        paths = [path1, path2]
        self.assertEqual(paths, lint.store_excluded_dirs(rootdir, dirs))
    
    def test_store_excluded_dirs_empty(self):
        dirs = None
        self.assertIsNotNone(lint.store_excluded_dirs(rootdir, dirs))

    # def test_get_dirs_to_check(self):
    #     # Valid directories
    #     dir1 = Path(rootdir).joinpath('dir1')
    #     dir2 = Path(rootdir).joinpath('dir1').joinpath('subdir1')
    #     dir3 = Path(rootdir).joinpath('dir1').joinpath('subdir1').joinpath('upperCase')
    #     dir4 = Path(rootdir).joinpath('dir2')
    #     dir5 = Path(rootdir).joinpath('dir2').joinpath('subdir2')
    #     dir6 = Path(rootdir).joinpath('dir2').joinpath('subdir2').joinpath('a space')
    #     dir7 = Path(rootdir).joinpath('dir3')
    #     valid_dirs = [dir1, dir2, dir3, dir4, dir5, dir6, dir7]
    #     # Excluded directories
    #     exc1 = os.path.join(rootdir, 'dir3')
    #     exc2 = os.path.join(rootdir, 'Case and Space')
    #     exc3 = os.path.join(rootdir, '123')
    #     excluded_dirs = [exc1, exc2, exc3]

    #     self.assertListEqual(valid_dirs, lint.get_dirs_to_check(rootdir, excluded_dirs))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(rootdir)


# Entry Point
if __name__ == "__main__":
    unittest.main()