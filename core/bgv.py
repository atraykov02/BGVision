import numpy as np

from core.polynomial import (QuotientRingPoly, random_normal_poly,
                        random_ternary_poly, random_uniform_poly)


def gen_secret_key(coef_modulus: int, poly_modulus: np.ndarray):
    # Draw the secret
    
    s = random_ternary_poly(coef_modulus, poly_modulus)
    return s


def gen_public_key(
    sk: QuotientRingPoly,
    coef_modulus: int,
    poly_modulus: np.ndarray,
    plaintext_modulus: int,
):
    # Generate noise e
    e = random_normal_poly(coef_modulus, poly_modulus)
    
    # Generate unifrom poly a
    a = random_uniform_poly(coef_modulus, poly_modulus)
    
    # RLWE instance b
    b = a * sk + e * plaintext_modulus
    return b, -a


def encrypt(
    msg: QuotientRingPoly,
    pk0: QuotientRingPoly,
    pk1: QuotientRingPoly,
    coef_modulus: int,
    poly_modulus: np.ndarray,
    plaintext_modulus: int,
):
    u = random_ternary_poly(coef_modulus, poly_modulus)
    e0 = random_normal_poly(coef_modulus, poly_modulus)
    e1 = random_normal_poly(coef_modulus, poly_modulus)
    
    # Mask the message with a rlwe instance (b * r + te)
    c0 = pk0 * u + e0 * plaintext_modulus + msg
    c1 = pk1 * u + e1 * plaintext_modulus
    return c0, c1


def decrypt(
    c0: QuotientRingPoly,
    c1: QuotientRingPoly,
    sk: QuotientRingPoly,
    plaintext_modulus: int,
    return_noise: bool = False,
):
    msg = c0 + c1 * sk
    noise = np.max(np.abs(msg.coef))
    msg = msg % plaintext_modulus

    if return_noise:
        msg_not_reduced = np.max((c0 + c1 * sk).coef)
        noise = np.max(np.abs(msg_not_reduced))
        return msg, noise
    else:
        return msg

def decrypt_quad(c0, c1, c2, sk, plaintext_modulus, return_noise: bool = False):
    # Evaluate the quadratic equation
   
    msg = c0 + c1 * sk + c2 * sk * sk
    noise = np.max(np.abs(msg.coef))
    msg = msg % plaintext_modulus

    if return_noise:
        return msg, noise
    else:
        return msg