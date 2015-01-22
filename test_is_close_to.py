#!/usr/bin/env python3

"""
unit tests for is_close_to function
"""

import unittest
from is_close_to import is_close_to


class ErrorTestCase(unittest.TestCase):

    def test_negative_tol(self):
        with self.assertRaises(ValueError):
            is_close_to(1,1,-1e-100)

    def test_negative_abstol(self):
        with self.assertRaises(ValueError):
            is_close_to(1,1,1e-100, -1e10)

class CloseTestCase(unittest.TestCase):
    ## some methods that make it easier to test a bunch of values
    def do_close(self, a, b, *args, **kwargs):
        print kwargs
        self.assertTrue(is_close_to(a, b, *args, **kwargs), msg="%s and %s should be close!"%(a,b))

    def do_not_close(self, a, b, *args, **kwargs):
        self.assertTrue(is_close_to(a, b, *args, **kwargs), msg="%s and %s should not be close!"%(a,b))


class RelativeTestCase(CloseTestCase):

    nums8 = [(1e9, 1e9+1),
              (-1e-9, -1.000000001e-9),
              ]

    def test_nums8_close(self):
        #these should be close to tol=1e-8
        for a, b in self.nums8:
            self.do_close(a, b, 1e-8)

    def test_nums8_not_close(self):
        #these should not be close to tol=1e-9
        for a, b in self.nums8:
            self.do_not_close(a, b, 1e-9)

class ZeroTestCase(CloseTestCase):

    nums8 = [(1e-9, 0.0),
             (-1e-9, 0.0),
             (-1e-150, 0.0),
             ]

    def test_nums8_not_close(self):
        #these should not be close to any tol
        for a, b in self.nums8:
            self.do_not_close(a, b, 1)

    def test_nums8_close(self):
        #these should be close to abs_tol=1e-8
        for a, b in self.nums8:
            self.do_close(a, b, abs_tol=1e-8)

class AsymetryTest(CloseTestCase):
    """
    tests the assymetry example from the PEP
    """
    def test_close(self):
        self.do_close(9, 10, tol=0.1)


