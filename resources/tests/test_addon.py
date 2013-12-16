#!/usr/bin/env python
'''
This module contains unit tests and integration tests.
'''
import os
import sys
import unittest
# update path so we can import the addon.py file
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import addon

class TestAddon(unittest.TestCase):

    def test_allways_pass(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
