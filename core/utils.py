import numpy as np


def mod_center(x, m: int, left_closed: bool = True):
    # [-m // 2, m // 2)
    if left_closed:
        return (x + m // 2) % m - m // 2
    # (-m // 2, m // 2]
    else:
        return (x + m // 2 - 1) % m - m // 2 + 1

def int2base(x: int, base: int):
    digits = []
    while x > 0:
        q, r = divmod(x, base)
        digits.append(r)
        x = q
    return digits

def roundv(array):
    return np.array([round(a) for a in array], dtype=object)

def init_poly_modulus(poly_modulus):
    # If it's int, let it be x ^ poly_modulus + 1, else just init the poly modulus
    if isinstance(poly_modulus, int):
        poly_modulus = np.array([1] + [0] * (poly_modulus - 1) + [1], dtype=object)
    else:
        poly_modulus = poly_modulus
    return poly_modulus

def untrim_seq(poly: np.array, degree: int) -> np.array:
    # Add 0s to the higher powers until we reach degree
    coef = np.append(poly, [0] * (degree - len(poly)))
    return coef

def polydiv(poly1, poly2):
    # Divide poly1 by poly2 and return the quotient and remainder as numpy arrays

    # Ensure that the degree of the second polynomial is less than or equal to the degree of the first polynomial
    while len(poly1) >= len(poly2):
        # Compute the quotient of the leading terms of the two polynomials
        quotient = poly1[-1] // poly2[-1]

        # Compute the product of the quotient and the second polynomial shifted to align with the leading term of the first polynomial
        product = np.zeros(len(poly1), dtype=object)
        product[-len(poly2) :] = quotient * poly2

        # Compute the difference between the first polynomial and the product
        difference = poly1 - product

        # Remove any leading zeros from the difference
        while len(difference) > 0 and difference[-1] == 0:
            difference = difference[:-1]

        # Set the difference as the new value of the first polynomial
        poly1 = difference

    # Return the quotient and remainder as numpy arrays
    quotient = np.zeros(len(poly1) + len(poly2) - 1, dtype=object)
    quotient[-len(poly1) :] = poly1
    remainder = poly1
    return quotient, remainder