# test_renameFiles.py

import unittest
import os
import shutil
import renameFiles

class TestRenameFiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a test directory
        cls.test_dir = 'test_dir'
        os.makedirs(cls.test_dir, exist_ok=True)

        # Create test files
        test_files = ['test1.txt', 'test2.txt', 'IMG-001.jpg', 'IMG-002.jpg']
        for file in test_files:
            open(os.path.join(cls.test_dir, file), 'a').close()

    @classmethod
    def tearDownClass(cls):
        # Clean up the test directory
        shutil.rmtree(cls.test_dir)

    def test_remove_vowels(self):
        self.assertEqual(renameFiles.remove_vowels("mobile"), "mbl")

    def test_change_case(self):
        self.assertEqual(renameFiles.change_case("hello", "upper"), "HELLO")
    
    def test_replace(self):
        self.assertEqual(renameFiles.replace("hello", "l", "w"), "hewwo")
    
    def test_replace_with_renumbering(self):
        self.assertEqual(renameFiles.replace_with_renumbering("IMG-1234", "IMG-\d+", "IMG_{num4}", 1), "IMG_0001")

    def test_matches_pattern(self):
        self.assertTrue(renameFiles.matches_pattern("IMG-1234", "IMG-\d+"))

if __name__ == '__main__':
    unittest.main()

