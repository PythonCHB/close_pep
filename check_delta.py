#!/usr/bin/env python3

"""
Check to computationally see how much of a difference it can make to use
different algorithms

Example:

With rel_tol == 1e-7:

1.000001 1.0000008999999017 are close only weak standard
1.000001 1.0000009000000016 are close by both

With rel_tol == 1e-8:

1.0 0.9999999900000001 are close by only the weak standard
1.0 0.9999999900000002 are close by both

Note that there no floating point values in between these two -- this is
the ONLY one close to 1.0 that only meets one standard.

With rel_tol == 1e-9:

I couldn't find a value close to 1.0 by only one method:
1.0 0.9999999989999999 are not close by either
1.0 0.999999999 are close by both.

"""

from is_close import is_close

delta = 1.2e-16  # (a touch smaller than eps)
tol = 1e-8
start_value = 0.999999989999999
high_value = 1.0


a = high_value
b = start_value
close_weak = False
close_strong = False
while b < a:
    b += delta
    print("trying:", a, b)
    if is_close(a, b, rel_tol=tol, method='weak'):
        close_weak = True
    if is_close(a, b, rel_tol=tol, method='strong'):
        close_strong = True
    if (close_weak or close_strong) and not (close_weak and close_strong):
        if close_weak:
            print("they are close by only the weak standard")
        elif close_strong:
            print("they are close by only the strong standard")
    elif close_weak and close_strong:
        print("they are close by both")
        break
