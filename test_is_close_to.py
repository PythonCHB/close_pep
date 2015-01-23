#!/usr/bin/env python3

"""
unit tests for is_close_to function
"""

import unittest
from decimal import Decimal
from fractions import Fraction
from is_close_to import is_close_to


class ErrorTestCase(unittest.TestCase):
    """
    Exceptions should be raised if either toleranc eis set to less than zero
    """
    def test_negative_tol(self):
        with self.assertRaises(ValueError):
            is_close_to(1, 1, -1e-100)

    def test_negative_abstol(self):
        with self.assertRaises(ValueError):
            is_close_to(1, 1, 1e-100, -1e10)

class CloseTestCase(unittest.TestCase):
    """ some methods that make it easier to test a bunch of values"""

    def do_close(self, a, b, *args, **kwargs):
        self.assertTrue(is_close_to(a, b, *args, **kwargs),
                        msg="%s and %s should be close!" % (a, b))

    def do_not_close(self, a, b, *args, **kwargs):
        self.assertFalse(is_close_to(a, b, *args, **kwargs),
                        msg="%s and %s should not be close!" % (a, b))

class ExactTestCase(CloseTestCase):
    """
    Make sure exact values test as close
    """
    exact_examples = [(2.0, 2.0),
                      (0.1e200, 0.1e200),
                      (1.123e-300, 1.123e-300),
                      (12345, 12345.0),
                      (0.0, -0.0),
                      ]
    def test_exact(self):
        for a, b in self.exact_examples:
            self.do_close(a, b, tol=0.0, abs_tol=0.0)


class RelativeTestCase(CloseTestCase):

    nums8 = [(1e9, 1e9+1),
             (-1e-9, -1.000000001e-9),
             (1.12345677, 1.12345678),
             ]

    def test_nums8_close(self):
        # these should be close to tol=1e-8
        for a, b in self.nums8:
            self.do_close(a, b, 1e-8)

    def test_nums8_not_close(self):
        # these should not be close to tol=1e-10
        for a, b in self.nums8:
            self.do_not_close(a, b, 1e-10)


class ZeroTestCase(CloseTestCase):

    nums8 = [(1e-9, 0.0),
             (-1e-9, 0.0),
             (-1e-150, 0.0),
             ]

    def test_nums8_not_close(self):
        # these should not be close to any tol
        for a, b in self.nums8:
            self.do_not_close(a, b, 1)

    def test_nums8_close(self):
        # these should be close to abs_tol=1e-8
        for a, b in self.nums8:
            self.do_close(a, b, abs_tol=1e-8)

class NonFiniteCase(CloseTestCase):
    """ test for nan, inf, -inf """
    inf = float('inf')
    nan = float('nan')
    close_examples = [(inf, inf),
                      (-inf, -inf),
                     ]

    not_close_examples = [(nan, nan),
                          (nan, 1e-100),
                          (1e-100, nan),
                          (inf, nan),
                          (nan, inf),
                          (inf, -inf),
                          (inf, 1.0),
                          (1.0, inf),
                          ]

    def test_close(self):
        for a,b in self.close_examples:
            self.do_close(a, b, abs_tol=1e12)

    def test_not_close(self):
        for a,b in self.not_close_examples:
            self.do_not_close(a, b, abs_tol=1e12)


class AsymetryTest(CloseTestCase):
    """
    tests the assymetry example from the PEP
    """
    def test_close(self):
        self.do_close(9, 10, tol=0.1)

class ComplexTests(CloseTestCase):
    close_examples = [(1.0+1.0j, 1.000000000001+1.0j ),
                      (1.0+1.0j, 1.0+1.000000000001j ),
                      (-1.0+1.0j, -1.000000000001+1.0j ),
                      (1.0-1.0j, 1.0-0.999999999999j ),
                      ]

    def test_close(self):
        for a,b in self.close_examples:
            self.do_close(a, b, tol=1e-12)

    def test_not_close(self):
        for a,b in self.close_examples:
            self.do_not_close(a, b, tol=1e-14)


class TestInteger(CloseTestCase):
    close_examples = [(100000001, 100000000),
                      (123456789, 123456788)
                      ]

    def test_close(self):
        for a,b in self.close_examples:
            self.do_close(a, b, tol=1e-8)

    def test_not_close(self):
        for a,b in self.close_examples:
            self.do_not_close(a, b, tol=1e-9)


class TestDecimal(CloseTestCase):
    close_examples = [(Decimal('1.00000001'), Decimal('1.0')),
                      (Decimal('1.00000001e-20'), Decimal('1.0e-20')),
                      (Decimal('1.00000001e-100'), Decimal('1.0e-100')),
                      ]

    def test_close(self):
        for a,b in self.close_examples:
            self.do_close(a, b, tol=Decimal('1e-8'))

    def test_not_close(self):
        for a,b in self.close_examples:
            self.do_not_close(a, b, tol=Decimal('1e-9'))

class TestFraction(CloseTestCase):
    # could use some more here!
    close_examples = [(Fraction(1, 100000000) + 1, Fraction(1) ),
                      ]

    def test_close(self):
        for a,b in self.close_examples:
            self.do_close(a, b, tol=1e-8)

    def test_not_close(self):
        for a,b in self.close_examples:
            self.do_not_close(a, b, tol=1e-9)



