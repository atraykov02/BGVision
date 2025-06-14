import numpy as np


def is_prime(n):
    # Check if a number is prime
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def validate_bgv_parameters(n, lambda_security, plaintext_modulus, base):
   # Validate user input parameters for BGV scheme.
    errors = []
    
    # Validate polynomial degree
    try:
        n = int(n)
        if n <= 0 or (n & (n - 1)) != 0:  # Check if power of 2
            errors.append("Степента на полинома трябва да е положителна степен на двойката (8, 16, 32, 64, 128).")
        elif n > 128:
            errors.append("Степента на полинома е твърде голяма (максимум 128).")
        elif n < 4:
            errors.append("Степента на полинома е твърде малка (минимум 4).")
    except (ValueError, TypeError):
        errors.append("Степента на полинома трябва да е цяло число.")

    # Validate security parameter
    try:
        lambda_security = int(lambda_security)
        if lambda_security < 80:
            errors.append("Параметърът за сигурност трябва да е най-малко 80 бита.")
        elif lambda_security > 512:
            errors.append("Параметърът за сигурност е твърде голям (максимум 256).")
    except (ValueError, TypeError):
        errors.append("Параметърът за сигурност трябва да е валиден.")

    # Validate plaintext modulus
    try:
        plaintext_modulus = int(plaintext_modulus)
        if plaintext_modulus < 2:
            errors.append("Модулът на явното съобщение трябва да е най-малко 2.")
        elif plaintext_modulus > 97:
            errors.append("Модулът на явното съобщение е твърде голям (максимум 97).")
        elif not is_prime(plaintext_modulus):
            errors.append("Модулът на явното съобщение трябва да е просто число.")       
    except (ValueError, TypeError):
        errors.append("Модулът на явното съобщение трябва да е цяло число.")

    # Validate base
    try:
        base = int(base)
        if base < 2:
            errors.append("Базата за релинеаризация трябва да е най-малко 2.")
        elif base > 10:
            errors.append("Базата за релинеаризация е твърде голяма (максимум 10).")
    except (ValueError, TypeError):
        errors.append("Базата за релинеаризация трябва да е цяло число.")

    return errors


def validate_input_values(input_str, n, plaintext_modulus):
    # Validate and parse input values for encryption.

    errors = []
    parsed_values = None
    
    try:
        values = [x.strip() for x in input_str.split(',')]
        
        if len(values) != n:
            errors.append(f"Трябва да въведете точно {n} стойности, но сте въвели {len(values)}.")
            return None, errors

        parsed_values = []
        for i, val in enumerate(values):
            try:
                num = int(val)
                if num < 0:
                    errors.append(f"Стойност {i+1} ({num}) не може да е отрицателна!")
                elif num >= plaintext_modulus:
                    errors.append(f"Стойност {i+1} ({num}) трябва да е между 0 и {plaintext_modulus-1}!")
                else:
                    parsed_values.append(num)
            except ValueError:
                errors.append(f"Стойност {i+1} ('{val}') не е валидно цяло число!")

        if errors:
            return None, errors
        
        return np.array(parsed_values, dtype=object), []

    except Exception as e:
        errors.append(f"Невалиден формат на входните данни: {str(e)}!")
        return None, errors


def validate_operation_inputs(left_operand, right_operand, operation, encrypted_values):
    # Validate inputs for a homomorphic operation.
    
    errors = []
    
    # Check if operands are selected
    if not left_operand or not left_operand.strip():
        errors.append("Изберете лява страна на операцията.")
    
    if not right_operand or not right_operand.strip():
        errors.append("Изберете дясна страна на операцията.")
    
    # Check if operation is valid
    if operation not in ['+', '*']:
        errors.append("Изберете валидна операция (+ или *).")
    
    # Check if operands exist in encrypted values
    if left_operand and left_operand not in encrypted_values:
        errors.append(f"Левият операнд '{left_operand}' не съществува!")
    
    if right_operand and right_operand not in encrypted_values:
        errors.append(f"Десният операнд '{right_operand}' не съществува!")
    
    # Check if trying to operate on the same value (might be intentional, just warn)
    if left_operand and right_operand and left_operand == right_operand:
        # This is actually valid (e.g., A * A), so no error, just info
        pass
    
    return errors