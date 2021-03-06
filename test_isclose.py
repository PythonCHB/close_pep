#!/usr/bin/env python3

"""
Unit tests for isclose() function -- candidate for the strandard library
"""

import unittest
from decimal import Decimal
from fractions import Fraction
from isclose import isclose


class ErrorTestCase(unittest.TestCase):
    """
    Exceptions should be raised if either tolerance is set to less than zero
    """
    def test_negative_tol(self):
        with self.assertRaises(ValueError):
            isclose(1, 1.1, -1e-100)

    def test_negative_abstol(self):
        with self.assertRaises(ValueError):
            isclose(1, 1.1, 1e-100, -1e10)


class CloseTestCase(unittest.TestCase):
    """ some methods that make it easier to test a bunch of values"""

    def do_close(self, examples, *args, **kwargs):
        for a, b in examples:
            self.assertTrue(isclose(a, b, *args, **kwargs),
                            msg="%s and %s should be close!" % (a, b))

    def do_not_close(self, examples, *args, **kwargs):
        for a, b in examples:
            self.assertFalse(isclose(a, b, *args, **kwargs),
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
                      (345678, 345678),
                      (Decimal(1.0001), Decimal(1.0001))
                      ]

    def test_exact(self):
        # should return close even with zero tolerances
        self.do_close(self.exact_examples,
                      rel_tol=0.0,
                      abs_tol=0.0)


class RelativeTestCase(CloseTestCase):

    nums8 = [(1e8, 1e8 + 1),
             (-1e-8, -1.000000009e-8),
             (1.12345678, 1.12345679),
             ]

    def test_all_8close(self):
        self.do_close(self.nums8, rel_tol=1e-8)

    def test_all_8_not_close(self):
        self.do_not_close(self.nums8, rel_tol=1e-9)


class ZeroTestCase(CloseTestCase):

    nums0 = [(1e-9, 0.0),
             (-1e-9, 0.0),
             (-1e-150, 0.0),
             ]

    def test_nums0_not_close(self):
        # these should not be close to any rel_tol
        self.do_not_close(self.nums0, rel_tol=0.9)

    def test_nums0_close(self):
        # these should be close to abs_tol=1e-8
        self.do_close(self.nums0, abs_tol=1e-8)

    def test_nums0_(self):
        # these should be close to rel_tol >= 1.0
        self.do_close(self.nums0, rel_tol=1.0)


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

    large_diff_examples = [(1, 1000),
                           (1e-50, 1e50),
                           (-1.0, -1e300),
                           (0.0, 10),
                           (10.0, 0.0),
                           ]

    def test_close(self):
        self.do_close(self.close_examples, abs_tol=0.999999999999999)  # largest tolerance possible less than 1.0

    def test_not_close(self):
        self.do_not_close(self.not_close_examples, abs_tol=0.999999999999999)  # largest tolerance possible less than 1.0

    def test_inf_tolerance(self):
        """anything should be close to an inf tolerance"""
        self.do_close(self.large_diff_examples, rel_tol=float('inf'))

    def test_inf_tolerance(self):
        """nothing should be close to a nan tolerance"""
        self.do_not_close(self.large_diff_examples, rel_tol=float('nan'))


class AsymmetryTest(CloseTestCase):
    """
    tests the assymetry example from the PEP
    """
    # should pass weak test both orders
    def test_close_weak(self):
        self.do_close([(9, 10)], rel_tol=0.1)

    def test_close_weak_reversed(self):
        self.do_close([(10, 9)], rel_tol=0.1)


class ComplexTests(CloseTestCase):
    close_examples = [(1.0+1.0j, 1.000000000001+1.0j),
                      (1.0+1.0j, 1.0+1.000000000001j),
                      (-1.0+1.0j, -1.000000000001+1.0j),
                      (1.0-1.0j, 1.0-0.999999999999j),
                      ]

    def test_close(self):
        self.do_close(self.close_examples, rel_tol=1e-12)

        # for a,b in self.close_examples:
        #     self.do_close(a, b, rel_tol=1e-12)

    def test_not_close(self):
        self.do_not_close(self.close_examples, rel_tol=1e-13)
        # for a,b in self.close_examples:
        #     self.do_not_close(a, b, rel_tol=1e-14)


class TestInteger(CloseTestCase):
    close_examples = [(100000001, 100000000),
                      (123456789, 123456788)
                      ]

    def test_close(self):
        self.do_close(self.close_examples, rel_tol=1e-8)

    def test_not_close(self):
        self.do_not_close(self.close_examples, rel_tol=1e-9)


class TestDecimal(CloseTestCase):
    close_examples = [(Decimal('1.00000001'), Decimal('1.0')),
                      (Decimal('1.00000001e-20'), Decimal('1.0e-20')),
                      (Decimal('1.00000001e-100'), Decimal('1.0e-100')),
                      ]

    def test_close(self):
        self.do_close(self.close_examples, rel_tol=Decimal('1e-8'))

    def test_not_close(self):
        self.do_not_close(self.close_examples, rel_tol=Decimal('1e-9'))

    # def test_close(self):
    #     self.do_close(self.close_examples, rel_tol=1e-8)

    # def test_not_close(self):
    #     self.do_not_close(self.close_examples, rel_tol=1e-9)


class TestFraction(CloseTestCase):
    # could use some more here!
    close_examples = [(Fraction(1, 100000000) + 1, Fraction(1)),
                      ]

    def test_close(self):
        self.do_close(self.close_examples, rel_tol=1e-8)

    def test_not_close(self):
        self.do_not_close(self.close_examples, rel_tol=1e-9)
