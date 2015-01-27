#!/usr/bin/env python3

"""
An implementation for an is_close_to() function, for possible inclusion in
the Python standard library.

This implementation is the result of much discussion on the python-ideas list
in January, 2015:

https://mail.python.org/pipermail/python-ideas/2015-January/030947.html

Copyright: Christopher H. Barker
License: Apache License 2.0 http://opensource.org/licenses/apache2.0.php

"""
import math, cmath

def is_close_to(actual, expected, rel_tolerance=1e-8, abs_tolerance=0.0):
    """
    returns True if actual is close in value to expected. False otherwise

    :param actual: the value that has been computed, measured, etc.

    :param expected: the "known" value.

    :param rel_tolerance=1e-8: the relative tolerance -- the amount of error
                     allowed, relative to the magnitude of the expected
                     value.

    :param abs_tolerance=0.0: the minimum absolute tolerance level -- useful for
                        comparisons to zero.

    NOTES:

    -inf, inf and NaN behave according to the IEEE 754 Standard

    Complex values are compared based on their absolute value.

    The function can be used with Decimal types, of the tolerance(s) are
    specified as Decimals

    """
    print("testing:", actual, expected)
    if rel_tolerance < 0.0 or abs_tolerance < 0.0:
        raise ValueError('error tolerances must be non-negative')

    if actual == expected:  # short-circuit exact equality
        return True
    # use cmath so it will work with complex ot float
    if cmath.isinf(actual) or cmath.isinf(expected):
        # This includes the case of two infinities of opposite sign, or
        # one infinity and one finite number. Two infinities of opposite sign
        # would otherwise have an infinite relative tolerance.
        return False

    diff = abs(expected-actual)
    # print ("diff:", diff)
    # print ("rel_tol:", abs(rel_tolerance*expected))
    # print ("abs_tolerance:", abs_tolerance)
    return (diff <= abs(rel_tolerance*expected)) or (diff <= abs_tolerance)

