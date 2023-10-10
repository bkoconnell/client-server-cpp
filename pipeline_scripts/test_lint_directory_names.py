#!/usr/bin/env python3
import unittest
import shutil
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
        self.assertEqual(lint.resolve_path(path), path.resolve())
    
    def test_resolve_path_filenotfound(self):
        with self.assertRaises(FileNotFoundError):
            path = Path('This is not a valid path')
            lint.resolve_path(path)

    def test_is_directory(self):
        path = Path(rootdir).joinpath('dir1')
        self.assertEquals(lint.is_directory(path), path.is_dir())

    def test_is_directory_sysexit(self):
        with self.assertRaises(SystemExit) as cm:
            path = Path(rootdir).joinpath('atestfile.testfile')
            lint.is_directory(path)
        self.assertEqual(cm.exception.code, 2)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(rootdir)


# Entry Point
if __name__ == "__main__":
    unittest.main()