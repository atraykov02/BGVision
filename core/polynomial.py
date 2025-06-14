import random
from typing import Union

import numpy as np
from numpy.polynomial.polynomial import polyadd, polymul

from core.utils import init_poly_modulus, mod_center, polydiv, roundv, untrim_seq


class QuotientRingPoly:
    def __init__(
        self,
        coef: np.array,
        coef_modulus: int,
        poly_modulus: Union[int, np.array],
    ):
        self._coef_modulus = coef_modulus
        self._poly_modulus = init_poly_modulus(poly_modulus)
        self._coef = coef
        # Reduce mod coef and mod poly.
        self.degree = len(poly_modulus) - 1
        self._reduce()

    def _reduce(self):
        self._coef = roundv(self._coef)
        self._coef = mod_center(self._coef, self.coef_modulus)
        _, self._coef = polydiv(self._coef, self.poly_modulus)
        self._coef = mod_center(self._coef, self.coef_modulus)

        # Extend the 0s to match the degree
        self._coef = untrim_seq(self._coef, self.degree)
        # Transform the coeffs to int, sanity check.
        self._coef = roundv(self._coef)

    def _check_qring(self, other):
        if (
            any(self.poly_modulus != other.poly_modulus)
            or self.coef_modulus != other.coef_modulus
        ):
            raise ValueError("Полиномите не са в същия фактор-пръстен.")

    def __neg__(self):
        return QuotientRingPoly(-self._coef, self.coef_modulus, self.poly_modulus)

    def __add__(self, other):
        # Perform addition. If other is int, add to coeff
        if isinstance(other, (int, float)):
            res_coef = self.coef + other
            res = QuotientRingPoly(res_coef, self.coef_modulus, self.poly_modulus)
        else:
            self._check_qring(other)
            res_poly = polyadd(self._coef, other.coef)
            res = QuotientRingPoly(res_poly, self.coef_modulus, self.poly_modulus)
        return res

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            res_coef = self.coef * other
            res = QuotientRingPoly(res_coef, self.coef_modulus, self.poly_modulus)
        else:
            self._check_qring(other)
            # print(np.polymul(self.poly.coef, other.poly.coef))
            res_coef = polymul(self._coef, other.coef)
            res = QuotientRingPoly(res_coef, self.coef_modulus, self.poly_modulus)
        return res

    def __floordiv__(self, other):
        if isinstance(other, (int, float)):
            res_coef = self.coef // other
            res = QuotientRingPoly(res_coef, self.coef_modulus, self.poly_modulus)
        else:
            self._check_qring(other)
            q, _ = polydiv(self.poly, other.poly)
            res = QuotientRingPoly(q, self.coef_modulus, self.poly_modulus)
        return res

    def __mod__(self, other):
        if isinstance(other, (int, float)):
            res_coef = self.coef % other
            res = QuotientRingPoly(res_coef, self.coef_modulus, self.poly_modulus)
        else:
            self._check_qring(other)
            _, r = polydiv(self.poly, other.poly)
            res = QuotientRingPoly(r, self.coef_modulus, self.poly_modulus)
        return res

    def __eq__(self, other):
        return (
            all(self.poly_modulus == other.poly_modulus)
            and self.coef_modulus == other.coef_modulus
            and all(self._coef == other.coef)
        )

    def copy(self) -> "QuotientRingPoly":
        return QuotientRingPoly(self.coef, self.coef_modulus, self.poly_modulus)

    @property
    def poly_modulus(self):
        return self._poly_modulus.copy()

    @property
    def coef_modulus(self):
        return self._coef_modulus

    @coef_modulus.setter
    def coef_modulus(self, value):
        self._coef_modulus = value
        self._reduce()

    @property
    def coef(self):
        return self._coef

    @coef.setter
    def coef(self, value):
        self._coef = value
        self._reduce()

    def __repr__(self):
        r = f"{self.coef}, {self.coef_modulus}, {self.poly_modulus}"
        return r


def random_ternary_poly(
    coef_modulus: int, poly_modulus: Union[int, np.array]
) -> QuotientRingPoly:
    # Generate a random ternary polynomial in the given quotient ring.
    poly_modulus = init_poly_modulus(poly_modulus)
    size = len(poly_modulus) - 1

    # 0 with 1/2 chance, -1 or 1 with 1/2 chance
    # coef = np.random.randint(-1, 2, size, dtype=int)
    coef = np.random.choice(
        np.array([-1, 0, 1], dtype=object), size=size, p=[1 / 4, 1 / 2, 1 / 4]
    )
    return QuotientRingPoly(coef, coef_modulus, poly_modulus)


def random_uniform_poly(
    coef_modulus: int,
    poly_modulus: Union[int, np.array],
    high=None,
) -> QuotientRingPoly:
    # Generate a random polynomial with discrete coefficients uniformly distributed in the given quotient ring.

    if high is None:
        high = coef_modulus - 1
    poly_modulus = init_poly_modulus(poly_modulus)
    size = len(poly_modulus) - 1
    coef = np.array([random.randrange(0, high) for _ in range(size)], dtype=object)
    return QuotientRingPoly(coef, coef_modulus, poly_modulus)


def random_normal_poly(
    coef_modulus: int,
    poly_modulus: Union[int, np.array],
    mu: float = 0,
    std: float = 3.8,
) -> QuotientRingPoly:
    # Generate a random polynomial with discrete coefficients extracted from a normal distribution in the given quotient ring.
    poly_modulus = init_poly_modulus(poly_modulus)
    size = len(poly_modulus) - 1
    coef = np.array([round(random.gauss(mu, std)) for _ in range(size)], dtype=object)
    return QuotientRingPoly(coef, coef_modulus, poly_modulus)