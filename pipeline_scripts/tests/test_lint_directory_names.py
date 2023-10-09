#!/usr/bin/env python3
import unittest
import shutil
from pathlib import Path


class TestLintDirectoryNames(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._rootdir = 'rootdir'
        Path(cls._rootdir).joinpath('dir1').joinpath('subdir1').joinpath('upperCase').mkdir(parents=True, exist_ok=True)
        Path(cls._rootdir).joinpath('dir2').joinpath('subdir2').joinpath('a space').mkdir(parents=True, exist_ok=True)
        Path(cls._rootdir).joinpath('dir3').joinpath('subdir3').joinpath(' space').mkdir(parents=True, exist_ok=True)
        Path(cls._rootdir).joinpath('dir3').joinpath('subdir3').joinpath('space ').mkdir(parents=True, exist_ok=True)
        Path(cls._rootdir).joinpath('Case and Space').mkdir(exist_ok=True)
        Path(cls._rootdir).joinpath('123').mkdir(exist_ok=True)
        Path(cls._rootdir).joinpath('atestfile.testfile').touch(exist_ok=True)
    
    def test_resolve_path_r(self):
        pass

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._rootdir)


# Entry Point
if __name__ == "__main__":
    unittest.main()