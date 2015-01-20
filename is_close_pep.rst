PEP: XXX
Title: An Function for Testing Approximate Equality
Version: $Revision$
Last-Modified: $Date$
Author: Christopher Barker <Chris.Barker@noaa.gov>
Status: Draft
Type: Standards Track
Python-Version: 3.5
Content-Type: text/x-rst
Created: 20-Jan-2015
Post-History: 30-Aug-2002


Abstract
========

This PEP proposes the addition of a function to the standard library
that determines whether two values are approximately equal or "close"
to each other. 

Rationale
=========

Floating point values contain limited precision, which results in
their being unable to exactly represent some values, and for error to
accumulate with repeated computation.  As a result, it is common advice
to only use an equality comparison in very specific situations.  Often
a inequality comparison fits the bill, but there are times (often in
testing) where the programmer wants to determine whether two values
are "close" to each other, without requiring them to be exactly equal.
This is common enough, particularly in testing, and not always obvious
how to do it, so it would be useful addition to the standard library.


Existing Implementations
------------------------

The standard library includes the
``unittest.TestCase.assertAlmostEqual`` method, but it:

* Is buried in the unittest.TestCase class

* Is an assertion, so you can't use it as a general test (easily)

* Uses number of decimal digits or an absolute delta, which are
  particular use cases that don't provide a general relative error.

The numpy package has the ``allclose()`` and ``isclose()`` functions.

The statistics package tests include an implementation, used for its
unit tests.

One can also find discussion and sample implementations on Stack
Overflow, and other help sites.

These existing implementations indicate that this is a common need,
and not trivial to write oneself, making it a candidate for the
standard library.


Proposed Implementation
=======================

NOTE: this PEP is the result of an extended discussion on the
python-ideas list [1]_.

Relative Difference
-------------------

There are essentially two ways to think about how close two numbers
are to each-other: absolute difference: simple ``abs(a-b)``, and relative
difference: ``abs(a-b)/scale_factor`` [2]_. The absolute difference is
trivial enough that this proposal focuses on the relative difference.

Usually, the scale factor is some function of the values under
consideration, for instance: 

 1) The absolute value of one of the input values

 2) The maximum absolute value of the two

 3) The minimum absolute value of the two.

 4) The arithmetic mean of the two

Symmetry
--------

An advantage of using a particular input value is that it is easy
reason about and answer the question: is the value of a within x% of
b? -- Using b to scale the percent error clearly defines the result.
However, this approach is not symmetric, a may be within 10% of b, but
b is not within x% of a. Consider the case::

  a =  9.0
  b = 10.0

The difference between a and b is 1.0. 10% of a is 0.9, so b is not
within 10% of a. But 10% of b is 10.0, so a is within 10% of b. So
this criteria is not symmetric.

Casual users might reasonably expect that if a is close to b, then b
would also be close to a. the criteria that use both values are
symmetric, and thus less likely to lead to surprises.

This proposed implementation uses the minimum absolute value of the
two values, as it leads to the most strict symmetric solution. This is
known as the "strong" case in the Boost documentation [3]

Behavior near zero.
-------------------

Relative comparison is problematic if either value is zero. In this
case, the difference is relative to zero, and thus will always be
smaller than the prescribe tolerance. To handle this case, an optional
parameter, ``abs_tol`` (default 0.0) can be used to set a minimum
tolerance to be used in the case of very small relative tolerance.
That is the values will be considered close if::

    abs(a-b) <= relative_tolerance or abs(a-b) <= abs_tol

If the user sets the rel_tol parameter to 0.0, then only the absolute
tolerance will be used.


Handling of non-real numbers
----------------------------

The IEEE 754 special values of NaN, inf, and -inf will be handled
according to IEEE rules. Specifically, NaN is not considered close to
any other value, including NaN. inf and -inf are only considered close
to themselves.


Non-float types
----------------

The primary use-case is expected to be floating point numbers.
However, users may want to compare other numeric types similarly. In
theory, it should work for any type that supports ``abs()``,
comparisons, and division.  The code will be written and tested to
accommodate these types:

 * ``Decimal``

 * ``int``

 * ``Fraction``
 
 * ``complex``: for complex, the abs() will be used for scaling and
   comparison.

Expected Uses
=============

The primary expected use case is various forms of testing -- "are the
results computed near what I expect as a result?" This sort of test
may or may not be part of a formal unit testing suite.

The function might be used also to determine if a measured value is
within an expected value.

Inappropriate uses
------------------

One use case for floating point comparison is testing the accuracy of
a numerical algorithm. However, in this case, the numerical analyst
ideally would be doing careful error propagation analysis, and should
understand exactly what to test for. It is also likely that ULP (Unit
in the last Place) comparison may be called for. While this function
may prove useful in such situations, It is not intended to be used in
that way.



Other Approaches
================

Expected Use Cases
==================


.. _Docutils:
.. _Docutils project web site: http://docutils.sourceforge.net/
.. _post a message:
   mailto:docutils-users@lists.sourceforge.net?subject=PEPs
.. _Docutils-users mailing list:
   http://docutils.sf.net/docs/user/mailing-lists.html#docutils-users


References
==========

.. [1] Python-idea list discussion thread
   (https://mail.python.org/pipermail/python-ideas/2015-January/030947.html)

.. [2] Wikipedaia page on relative difference
   (http://en.wikipedia.org/wiki/Relative_change_and_difference)

.. [3] Boost project floating-point comparison algorithms
   (http://www.boost.org/doc/libs/1_35_0/libs/test/doc/components/test_tools/floating_point_comparison.html)

Copyright
=========

This document has been placed in the public domain.


..
   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   coding: utf-8