#!/usr/bin/env python3

"""
An implimentaion for an is_close_to() function, for possible inclusion in
the Python standrad library.

This implimentation is the result of much discussion on the python-ideas list
in January, 2015:

https://mail.python.org/pipermail/python-ideas/2015-January/030947.html

Copyright: Christopher H. Barker
License: Apache License 2.0 http://opensource.org/licenses/apache2.0.php

"""
import math, cmath

def is_close_to(actual, expected, tol=1e-8, abs_tol=0.0):
    """
    returns True is actual is close in value to expected. False otherwise


    :param actual: the value that has been computed, measured, etc.

    :param expected: the "known" value.

    :param tol=1e-8: the relative tolerance -- it is the amount of error
                     allowed, relative to the magnitude of the expected value.

    :param abs_tol=0.0: the minimum absolute tolerance level -- useful for
                        comparisons near zero.

    NOTE: -inf, inf and NaN behave according to the IEEE 754 Standard

    """
    print("testing:", actual, expected)
    if tol < 0.0 or abs_tol < 0.0:
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
    print ("diff:", diff)
    print ("rel_tol:", abs(tol*expected))
    print ("abs_tol:", abs_tol)
    print (diff <= abs(tol*expected))
    print (diff <= abs_tol)
    return (diff <= abs(tol*expected)) or (diff <= abs_tol)

