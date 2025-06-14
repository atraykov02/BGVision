import math

import numpy as np

from core.polynomial import QuotientRingPoly


def extended_gcd(a, b):
    # Extended Euclidean algorithm to find gcd and coefficients
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a, m):
    # Find modular inverse of a modulo m
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist for {a} mod {m} (gcd={gcd})")
    return (x % m + m) % m


def scale2_func(
    x: QuotientRingPoly, big_mod: int, small_mod: int, plaintext_modulus: int
) -> QuotientRingPoly:
    #Scales a polynomial x from a big coefficient modulus to a smaller one.
    
    # Verify that big_mod is divisible by small_mod
    if big_mod % small_mod != 0:
        raise ValueError(f"big_mod ({big_mod}) must be divisible by small_mod ({small_mod})")
    
    delta = big_mod // small_mod
    
    # Create result polynomial
    result_coef = np.zeros_like(x.coef, dtype=object)
    
    # Process each coefficient individually
    for i, coeff in enumerate(x.coef):
        # Center the coefficient in [-big_mod/2, big_mod/2)
        centered_coeff = ((coeff % big_mod) + big_mod // 2) % big_mod - big_mod // 2
        
        # Simple scaling: round to nearest multiple of delta, then divide by delta
        scaled_coeff = round(centered_coeff / delta)
        
        # Ensure result is in correct range for small_mod
        result_coef[i] = scaled_coeff % small_mod
    
    # Create new polynomial with small modulus
    result = QuotientRingPoly(result_coef, small_mod, x.poly_modulus)
    
    return result


def scale2_advanced(
    x: QuotientRingPoly, big_mod: int, small_mod: int, plaintext_modulus: int
) -> QuotientRingPoly:
    # More sophisticated modulus switching with error correction
    
    # Verify that big_mod is divisible by small_mod
    if big_mod % small_mod != 0:
        raise ValueError(f"big_mod ({big_mod}) must be divisible by small_mod ({small_mod})")
    
    delta = big_mod // small_mod
    
    # Check if delta and plaintext_modulus are coprime
    gcd_val = math.gcd(delta, plaintext_modulus)
    
    if gcd_val == 1:
        # Use the original algorithm when coprime
        try:
            # Find modular inverse of plaintext_modulus modulo delta
            plaintext_inv = mod_inverse(plaintext_modulus, delta)
            
            # Calculate adjustment term
            adjustment_coef = np.zeros_like(x.coef, dtype=object)
            for i, coeff in enumerate(x.coef):
                # Center coefficient
                centered = ((coeff % big_mod) + big_mod // 2) % big_mod - big_mod // 2
                
                # Calculate adjustment
                adj = ((-centered * plaintext_inv) % delta) * plaintext_modulus
                adjustment_coef[i] = adj
            
            # Create adjustment polynomial
            adjustment = QuotientRingPoly(adjustment_coef, big_mod, x.poly_modulus)
            
            # Apply adjustment and scale
            adjusted = x + adjustment
            
            # Scale by small_mod / big_mod
            result_coef = np.zeros_like(x.coef, dtype=object)
            for i, coeff in enumerate(adjusted.coef):
                scaled = (coeff * small_mod) // big_mod
                result_coef[i] = scaled % small_mod
                
            result = QuotientRingPoly(result_coef, small_mod, x.poly_modulus)
            return result
            
        except Exception as e:
            print(f"Advanced method failed: {e}, falling back to simple method")
            return scale2_func(x, big_mod, small_mod, plaintext_modulus)
    else:
        # Use simple scaling when not coprime
        return scale2_func(x, big_mod, small_mod, plaintext_modulus)


def scale2(
    x: QuotientRingPoly, big_mod: int, small_mod: int, plaintext_modulus: int
) -> QuotientRingPoly:
    # Main scaling function - tries advanced method first, falls back to simple if needed.
    try:
        return scale2_advanced(x, big_mod, small_mod, plaintext_modulus)
    except Exception as e:
        print(f"Advanced scaling failed: {e}")
        print("Falling back to simple scaling method...")
        return scale2_func(x, big_mod, small_mod, plaintext_modulus)


# Functions for compatibility
def scale(
    x: QuotientRingPoly, big_mod: int, small_mod: int, plaintext_modulus: int
) -> QuotientRingPoly:
    return scale2(x, big_mod, small_mod, plaintext_modulus)