import math
from typing import List

import numpy as np

from core.bgv import gen_public_key
from core.polynomial import QuotientRingPoly
from core.utils import int2base


def poly2base(poly: QuotientRingPoly, base: int) -> List[QuotientRingPoly]:
   # Converts a polynomial to a list of polynomials that represent the polynomial's coefficients in the given base.

    coef_modulus = poly.coef_modulus
    poly_modulus = poly.poly_modulus
    n_terms = math.ceil(math.log(coef_modulus, base))
    degree = len(poly.poly_modulus) - 1
    # Make a matrix to store the coefficients
    # the rows will represent each coefficient's decomposition in `base`
    # c^(i) will be formed by taking the columns (each coefficient at step i).
    coeffs = np.zeros((degree, n_terms), dtype=object)

    for i, coef in enumerate(poly.coef):
        digits = int2base(coef % coef_modulus, base)
        # Pad with 0s
        pad_len = n_terms - len(digits)
        digits = np.pad(digits, (0, pad_len))
        coeffs[i] = digits

    # Make list of polynomials
    res = []
    for i in range(n_terms):
        p = QuotientRingPoly(
            coeffs[:, i], coef_modulus=coef_modulus, poly_modulus=poly_modulus
        )
        res.append(p)
    return res

def gen_relinearization_key(sk, base, coef_modulus, poly_modulus, plaintext_modulus):
    n_terms = math.ceil(math.log(coef_modulus, base))

    eks = []
    for i in range(n_terms):
        b, ai = gen_public_key(sk, coef_modulus, poly_modulus, plaintext_modulus)
        ek0 = b + (sk * sk) * (base**i)
        ek1 = ai
        eks.append((ek0, ek1))
    return eks

def relinearize(c0, c1, c2, eks, base, coef_modulus, poly_modulus):
    # Decompose c2
    c2_polys = poly2base(c2, base)
    assert len(c2_polys) == len(eks)

    # Construct c0_hat, c1_hat
    c0_hat = c0
    c1_hat = c1
    for c2_i, (ek0, ek1) in zip(c2_polys, eks):
        c0_hat += c2_i * ek0
        c1_hat += c2_i * ek1

    return c0_hat, c1_hat