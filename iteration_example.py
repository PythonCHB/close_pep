#!/usr/bin/env python3

"""

Example of using is_close_to() in an iterative solution for the
disepersion realtionship for garvity waves in the ocean.

The lnear wave theory dispersion equation:

  omega**2 = g*k*tanh(k*h)

where omega is the wave frequence, g is the accelartion of gravity, k
is the wave number (2*pi/wave_length), and h is the water depth.

In the usual case, the frequencey(omega) is known, and you want the
wave number. As the wave number appears in two places, there is no
direct solution, so a numerical method must be used.

The simplist iterative solution is something like this: recast the
equation as:

k_2 = omega**2 / (g * tanh(k_1 * h))

 - guess a k_1
 - compute k_2
 - check if k_2 is close to k_1
 - if not, set k_1 to k_2 repeat.

"""

import math
import imp
import is_close_to
imp.reload(is_close_to) # because I'm running for ipython
from is_close_to import is_close_to

def dispersion(omega, h, g=9.806):
    "compute the dispersion relation"

    k_1 = 10.0 # initial guess
    while True:
        k_2 = omega**2 / (g * math.tanh(k_1 * h))
        if is_close_to(k_2, k_1, tol=1e-5):
            break
        k_1 = k_2
    return k_1

def iterate(func, x_initial, *args):
    """
    iterate to find a solution to the function passed in
    
    func should be a function that takes x as a first argument,
    and computes an approximation to x as a result.
    
    x_initial is an initial guess for the unknown value
    """
    x_1 = x_initial
    while True:
        x_2 = func(x_1, *args)
        if is_close_to(x_2, x_1):
            break
        x_1 = x_2
    return x_2

def disp(k, omega, h, g=9.806):
    """
    the linear  wave dispersion realationship

    k as a function of k, omega, h, g
    """
    return omega**2 / (g * math.tanh(k * h))

def dispersion(omega, h, g=9.806):
    "compute the dispersion relation"

    k_1 = 10.0 # initial guess
    while True:
        k_2 = omega**2 / (g * math.tanh(k_1 * h))
        if is_close_to(k_2, k_1, tol=1e-12):
            break
        k_1 = k_2
    return k_1

if __name__ == "__main__":

    #Try it for a few values:

    h = 10 # meters water depth
    omega = 2*math.pi / 10 # ten second period

    k = dispersion(omega, h)
    print("omega: {}, h: {}, k: {}, period: {}, wavelength: {}".format(omega, h, k, 2*math.pi/omega, 2*math.pi/k))

    k2 = iterate(disp, 10, omega, h )
    print("omega: {}, h: {}, k: {}, period: {}, wavelength: {}".format(omega, h, k2, 2*math.pi/omega, 2*math.pi/k2))











