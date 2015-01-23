#!/usr/bin/env python3

"""
NOTE: this is an early proposal, using a symetric approach -- an asymetric
approach seems to be prefered -- see is_close_to.py

A proposed implementation for an "is_close" implementation for floating point
(and complex) numbers for python.

This is an attempt to implement the approach used by Boost:

http://www.boost.org/doc/libs/1_34_0/libs/test/doc/components/test_tools/floating_point_comparison.html

With adjustments inspired by discussion on python-ideas list the code written
by Steven D'Aprano  for the statistics module tests.
"""


def is_close(u, v, tol=1e-12, min_tol=0.0):
    """
    Determines if two values are close to each other. Two values are close if
    the absolute value of their difference is less than tol times both of the
    values. i.e. tol is a relative difference. The result is symmetric, i.e.:
    is_close(u,v) == is_close(v,u)

    Note that if one of the values is zero, then nothing is "relatively close"
    to it (except zero itself). If you want a tolerance for near-zero
    values, then you can set min_tol to a value greater than zero. But be
    cautious if u an v may be very small, the min_tol could overwhelm any
    relative tolerance computed.

    :param u: one of the values

    :param v: the other value

    :param tol=1e-12: the relative tolerance
    NOTE: an arbitrary value for now -- how to choose good default?

    :param min_tol=None: The maximum absolute tolerance near zero. If one
                         of the
                          arguments is zero, then no value greater than
                          zero will ever be "close" to zero on a relative
                          scale.

    NOTE: -inf, inf and NaN behave as they "should"

    """
    if tol < 0 or min_tol < 0:
        raise ValueError('error tolerances must be non-negative')
    if u == v:  # short-circuit exact equality
        return True
    diff = abs(u - v)
    ## NOTE: using and, rather than if checks or max() allows it to run a bit
    ##       faster, and lets NaN and inf do the right thing automagically.
    result = ((diff <= tol * abs(u)) and
              (diff <= tol * abs(v)) or
              (diff <= min_tol)
              )
    return result

if __name__ == "__main__":
    ## some simple tests

    # same values had better work!
    exact_values_examples = [(2.0, 2.0),
                             (0.1e200, 0.1e200),
                             ]
    for u, v in exact_values_examples:
        if not is_close(u, v, tol=1e-12):
            print("FAIL: {},{} should be close".format(u, v))

    # negative and positive zero
    assert is_close(0.0, -0.0)

    # very close values:
    close_enough_examples = [(1.000000000001, 1.000000000002),
                             (1e12 + 1.0, 1e12 + 2.0),
                             (1e13 - 1.0, 1e13 - 2.0),
                             (-1e12 - 1.0, -1e12 - 2.0),
                             ]
    tol = 1e-12
    for u, v in close_enough_examples:
        if not is_close(u, v, tol=tol):
            print("FAIL: {},{} should be close to tol: {}".format(u, v, tol))

    tol = 1e-14
    for u, v in close_enough_examples:
        if is_close(u, v, tol=tol):
            print("FAIL: {},{} should be not be close to tol: {}"
                  .format(u, v, tol))

    # ## potential overflow:
    # ## note the boost docs talk about this, but I can't get it to overflow
    # ## and cause a problem. Maybe they were concerned about really large
    # ## values of tol???
    overflow_examples = [(1e308 + 1e294, 1e308 + 2e294),
                         ]
    tol = 1e-12
    for u, v in overflow_examples:
        if not is_close(u, v, tol=tol):
            print("FAIL: {},{} should be close to tol: {}".format(u, v, tol))

    # ## checking close to zero
    zero_examples = [(0.0, 1e-15),
                     (1e-15, 0.0),
                     ]
    tol = 1e-13
    min_tol = 0.0  # nothing should be close
    for u, v in zero_examples:
        if is_close(u, v, tol=tol, min_tol=min_tol):
            print("FAIL: {},{} should be NOT close to tol: {}".format(u, v, tol))

    tol = 1e-13
    min_tol = 1e-12  # very small should hold.
    for u, v in zero_examples:
        if not is_close(u, v, tol=tol, min_tol=min_tol):
            print("FAIL: {},{} should be close to within min_tol: {}".format(u, v, min_tol))

    ## NaN, etc tests
    nan = float('nan')
    inf = float('inf')
    neginf = -inf
    non_real_examples = [(nan, 1.0),
                         (1.0, nan),
                         (nan, nan),
                         (inf, 1.0),
                         (1e300, inf),
                         (-inf, -1e300),
                         (-1e305, -inf),
                         (-inf, inf)
                         ]
    tol = 1e-13
    min_tol = 1e-12  # very small should hold.
    for u, v in non_real_examples:
        if is_close(u, v, tol=tol, min_tol=min_tol):
            print("FAIL: {},{} should NOT be close to within min_tol: {}".format(u, v, min_tol))

    non_real_equal = [(inf, inf),
                      (-inf, inf),
                      ]
    tol = 1e-13
    min_tol = 1e-12  # very small should hold.
    for u, v in non_real_equal:
        if not is_close(u, v, tol=tol, min_tol=min_tol):
            print("FAIL: {},{} should be close to within min_tol: {}".format(u, v, min_tol))

    # ## complex tests
    # ## complex numbers will be handled by:
    # ##   is_close(x.real, y.real) and is_close(x.imag, y.imag)
    # ##   (but i haven't written any code for that yet)

    # # complex_examples = [(1.0+1.0j, 1.000000000001+1.0j ),
    # #                     (1.0+1.0j, 1.0+1.000000000001j ),
    # #                     (-1.0+1.0j, -1.000000000001+1.0j ),
    # #                     (1.0-1.0j, 1.0-0.999999999999j ),
    # #                     ]
    # # tol = 1e-12
    # # for u, v in complex_examples:
    # #     if not is_close(u, v, tol=tol):
    # #         print("FAIL: {},{} should be close to tol: {}".format(u, v, tol))

    # # tol = 1e-13
    # # for u, v in complex_examples:
    # #     if is_close(u, v, tol=tol):
    # #         print("FAIL: {},{} should be NOT close to tol: {}".format(u, v, tol))
