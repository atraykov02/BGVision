import math
import random

from Crypto.Util.number import getRandomNBitInteger


def is_probably_prime(n, k=10):
    # Miller-Rabin primality test
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Perform k rounds of testing
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_compatible_modulus(lambda_bits, plaintext_modulus):
    # Generate properly compatible moduls for modulus switching.
    
    print(f"Generating compatible modulus for λ={lambda_bits}, t={plaintext_modulus}")
    
    # Step 1: Generate small modulus that's coprime with plaintext_modulus
    small_bits = max(32, lambda_bits // 2)
    attempts = 0
    max_attempts = 100
    
    while attempts < max_attempts:
        small_modulus = getRandomNBitInteger(small_bits)
        
        # Ensure it's odd and > plaintext_modulus
        if small_modulus % 2 == 0:
            small_modulus += 1
        if small_modulus <= plaintext_modulus:
            small_modulus = plaintext_modulus * 2 + 1
        
        # Check if coprime with plaintext_modulus
        if math.gcd(small_modulus, plaintext_modulus) == 1:
            print(f"✅ Found small_modulus: {small_modulus} ({small_modulus.bit_length()} bits)")
            break
        attempts += 1
    
    if attempts >= max_attempts:
        # Fallback: use a safe small modulus
        
        small_modulus = plaintext_modulus * 2 + 1
        while math.gcd(small_modulus, plaintext_modulus) != 1:
            small_modulus += 2
        print(f"⚠️  Using fallback small_modulus: {small_modulus}")
    
    # Step 2: Find delta such that delta ≡ 1 (mod plaintext_modulus)
    # This ensures optimal compatibility for modulus switching
    target_delta_bits = lambda_bits + 32  # Security buffer   
    
    # Find the first value >= 2^target_delta_bits that's ≡ 1 (mod t)
    min_delta = 2 ** target_delta_bits
    if min_delta % plaintext_modulus == 1:
        delta = min_delta
    else:
        remainder = min_delta % plaintext_modulus
        delta = min_delta + (plaintext_modulus - remainder + 1)
    
    # Try to make delta prime for better security (optional)
    delta_attempts = 0
    while delta_attempts < 50:
        if is_probably_prime(delta):
            break
        delta += plaintext_modulus  # Maintain the ≡ 1 (mod t) property
        delta_attempts += 1
    
    print(f"✅ Found delta: {delta} ({delta.bit_length()} bits)")
    print(f"   delta ≡ {delta % plaintext_modulus} (mod {plaintext_modulus}) - should be 1")
    
    # Step 3: Calculate large modulus
    large_modulus = small_modulus * delta
    
    # Verify all constraints
    print(f"\n🔍 VERIFICATION:")
    print(f"   gcd(small_mod, t) = {math.gcd(small_modulus, plaintext_modulus)} (should be 1)")
    print(f"   gcd(delta, t) = {math.gcd(delta, plaintext_modulus)} (should be 1)")
    print(f"   delta mod t = {delta % plaintext_modulus} (should be 1)")
    print(f"   large_mod % small_mod = {large_modulus % small_modulus} (should be 0)")
    print(f"   Security level: ~{large_modulus.bit_length()} bits")
    
    # Final verification
    assert large_modulus % small_modulus == 0, f"Divisibility check failed"
    assert math.gcd(small_modulus, plaintext_modulus) == 1, f"small_modulus not coprime with plaintext_modulus"
    assert math.gcd(delta, plaintext_modulus) == 1, f"delta not coprime with plaintext_modulus"
    assert delta % plaintext_modulus == 1, f"delta ≢ 1 (mod plaintext_modulus)"
    
    print(f"✅ All constraints satisfied!\n")
    
    return large_modulus, small_modulus, delta


def verify_modulus_compatibility(large_modulus, small_modulus, plaintext_modulus):
    # Verify that modulus are compatible for modulus switching
    errors = []
    
    # Check basic divisibility
    if large_modulus % small_modulus != 0:
        errors.append(f"Large modulus ({large_modulus}) is not divisible by small modulus ({small_modulus})")
    
    # Check coprimality
    if math.gcd(small_modulus, plaintext_modulus) != 1:
        errors.append(f"Small modulus ({small_modulus}) is not coprime with plaintext modulus ({plaintext_modulus})")
    
    # Check delta property
    if large_modulus % small_modulus == 0:
        delta = large_modulus // small_modulus
        if math.gcd(delta, plaintext_modulus) != 1:
            errors.append(f"Delta ({delta}) is not coprime with plaintext modulus ({plaintext_modulus})")
        
        if delta % plaintext_modulus != 1:
            errors.append(f"Delta ({delta}) ≢ 1 (mod {plaintext_modulus}) - this may cause switching errors")
    
    return errors