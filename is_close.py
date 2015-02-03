#!/usr/bin/env python3

"""
An implementation for an is_close() function, for possible inclusion in
the Python standard library -- PEP0485

This implementation is the result of much discussion on the python-ideas list
in January, 2015:

   https://mail.python.org/pipermail/python-ideas/2015-January/030947.html

   https://mail.python.org/pipermail/python-ideas/2015-January/031124.html

   https://mail.python.org/pipermail/python-ideas/2015-January/031313.html

Copyright: Christopher H. Barker
License: Apache License 2.0 http://opensource.org/licenses/apache2.0.php

"""
import math, cmath

def is_close(test_val,
             expected,
             rel_tol=1e-8,
             abs_tol=0.0,
             method = 'asymmetric'):
    """
    returns True if test_val is close in value to expected. False otherwise

    :param test_val: the value that has been computed, measured, etc.

    :param expected: the "known" value.

    :param rel_tol=1e-8: the relative tolerance -- the amount of error
                     allowed, relative to the magnitude of the expected
                     value.

    :param abs_tol=0.0: the minimum absolute tolerance level -- useful for
                        comparisons to zero.

    :param method: The method to use. options are:
                  "asymmetric" : the expected value is used for scaling the tolerance
                  "strong" : the difference must be below tolerance scaled by both values
                  "weak" : the difference must be below the tolerance scaled by either of the values.
                  "average" : the tolerance is scaled by the average of the two values.

    NOTES:

    -inf, inf and NaN behave according to the IEEE 754 Standard

    Complex values are compared based on their absolute value.

    The function can be used with Decimal types, of the tolerance(s) are
    specified as Decimals

    """
    if method not in ("asymmetric", "strong", "weak", "average"):
        raise ValueError('method must be one of: "asymmetric", "strong", "weak", "average"')

    # print("testing:", test_val, expected)

    if rel_tol < 0.0 or abs_tol < 0.0:
        raise ValueError('error tolerances must be non-negative')

    if test_val == expected:  # short-circuit exact equality
        return True
    # use cmath so it will work with complex ot float
    if cmath.isinf(test_val) or cmath.isinf(expected):
        # This includes the case of two infinities of opposite sign, or
        # one infinity and one finite number. Two infinities of opposite sign
        # would otherwise have an infinite relative tolerance.
        return False

    diff = abs(expected-test_val)
    # print("diff:", diff)
    # print("tol1", abs(rel_tol*expected))
    # print("tol2", abs(rel_tol*test_val))
    if method == "asymmetric":
        return (diff <= abs(rel_tol*expected)) or (diff <= abs_tol)
    elif method == "strong":
        return ( ( (diff <= abs(rel_tol*expected)) and
                   (diff <= abs(rel_tol*test_val)) ) or
                (diff <= abs_tol) )
    elif method == "weak":
        return ( ( (diff <= abs(rel_tol*expected)) or
                  (diff <= abs(rel_tol*test_val)) ) or
                 (diff <= abs_tol) )
    elif method == "average":
        return ( (diff <= abs(rel_tol*(test_val+expected)/2) or
                 (diff <= abs_tol)) )
    else:
        raise ValueError('method must be one of:'
                         ' "asymmetric", "strong", "weak", "average"')

