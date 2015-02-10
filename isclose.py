#!/usr/bin/env python3

"""
Test implementation for an isclose() function, for possible inclusion in
the Python standard library -- PEP0485

This is the result of much discussion on the python-ideas list
in January, 2015:

   https://mail.python.org/pipermail/python-ideas/2015-January/030947.html

   https://mail.python.org/pipermail/python-ideas/2015-January/031124.html

   https://mail.python.org/pipermail/python-ideas/2015-January/031313.html

Copyright: Christopher H. Barker
License: Apache License 2.0 http://opensource.org/licenses/apache2.0.php
"""

import math


def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    """
    returns True if a is close in value to b. False otherwise

    :param a: one of the values to be tested

    :param b: the other value to be tested

    :param rel_tol=1e-9: The relative tolerance -- the amount of error
                         allowed, relative to the absolute value of the
                         larger input values.

    :param abs_tol=0.0: The minimum absolute tolerance level -- useful
                        for comparisons to zero.

    NOTES:

    -inf, inf and NaN behave similarly to the IEEE 754 Standard. That
    is, NaN is not close to anything, even itself. inf and -inf are
    only close to themselves.

    The function can be used with any type that supports comparison,
    substratcion and multiplication, including Decimal, Fraction, and
    Complex

    Complex values are compared based on their absolute value.

    See PEP-0485 for a detailed description

    """

    if a == b:  # short-circuit exact equality
        return True

    if rel_tol < 0.0 or abs_tol < 0.0:
        raise ValueError('error tolerances must be non-negative')

    # use cmath so it will work with complex ot float
    if math.isinf(abs(a)) or math.isinf(abs(b)):
        # This includes the case of two infinities of opposite sign, or
        # one infinity and one finite number. Two infinities of opposite sign
        # would otherwise have an infinite relative tolerance.
        return False
    diff = abs(b - a)

    return (((diff <= abs(rel_tol * b)) or
             (diff <= abs(rel_tol * a))) or
            (diff <= abs_tol))
