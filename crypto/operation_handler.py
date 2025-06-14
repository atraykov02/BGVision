from core.operations import add, mul
from core.polynomial import QuotientRingPoly
from core.relinearization import gen_relinearization_key, relinearize
from crypto.noise_management import apply_modulus_switching, check_noise_level


class OperationHandler:
    # Operation handler class
    
    def __init__(self, sk, coef_modulus, small_modulus, poly_modulus, 
                 plaintext_modulus, base=5):
        self.sk = sk
        self.coef_modulus = coef_modulus
        self.small_modulus = small_modulus
        self.poly_modulus = poly_modulus
        self.plaintext_modulus = plaintext_modulus
        self.base = base
        self.eks = None
        
        self.switching_ratio = 0.63   # 63% from max_length for switching
        self.warning_ratio = 0.75     # 75% from max_length for warning
        self.critical_ratio = 0.85    # 85% from max_length for blocking
        
    def calculate_dynamic_thresholds(self, max_length):
        # Calculates dynamic thresholds на max_length"""
        switching_threshold = max(1, int(max_length * self.switching_ratio))  # 63% from max_length
        warning_threshold = max(switching_threshold + 3, int(max_length * self.warning_ratio))
        critical_threshold = max(warning_threshold + 3, int(max_length * self.critical_ratio))
        
        return switching_threshold, warning_threshold, critical_threshold
        
    def generate_relinearization_keys(self):
        # Generate relinearization keys if not already generated
        if self.eks is None:
            self.eks = gen_relinearization_key(
                self.sk, self.base, self.coef_modulus, 
                self.poly_modulus, self.plaintext_modulus
            )
    
    def get_operation_depth(self, cryptogram_name, operation_history, original_values):
        # Calculate the multiplicative depth of a cryptogram
        
        # Original cryptograms have depth 0
        if cryptogram_name in original_values:
            return 0
        
        # Find in operation history
        for hist in operation_history:
            if hist.get('result') == cryptogram_name:
                left_op = hist.get('left_op', '')
                right_op = hist.get('right_op', '')
                
                # Recursive calculation
                left_depth = self.get_operation_depth(left_op, operation_history, original_values) if left_op else 0
                right_depth = self.get_operation_depth(right_op, operation_history, original_values) if right_op else 0
                
                if hist.get('op_type') == '*':
                    # Multiplication increases depth
                    return max(left_depth, right_depth) + 1
                else:
                    # Addition doesn't increase depth significantly
                    return max(left_depth, right_depth)
        
        # Fallback for unknown cryptograms
        return 0
    
    def check_operation_feasibility(self, left_operand, right_operand, operation, 
                                   encrypted_values, operation_history, original_values, 
                                   log_func=None):
        # Check if an operation can be performed based on noise levels.

        def log(message):
            if log_func:
                log_func(message)
        
        warnings = []
        can_perform = True
        
        try:
            # Calculate operation depth (informational only)
            try:
                left_depth = self.get_operation_depth(left_operand, operation_history, original_values)
                right_depth = self.get_operation_depth(right_operand, operation_history, original_values)
                
                if operation == "+":
                    new_depth = max(left_depth, right_depth)
                elif operation == "*":
                    new_depth = max(left_depth, right_depth) + 1
                else:
                    new_depth = 0
            except Exception:
                new_depth = 0
                left_depth = 0
                right_depth = 0
            
            # Check noise levels for both operands
            max_noise_length = 0
            critical_operand = None
            max_allowed_length = 0
            
            for operand in [left_operand, right_operand]:
                try:
                    c0, c1 = encrypted_values[operand]
                    noise_info = check_noise_level(c0, c1, self.sk, self.plaintext_modulus)
                    
                    if noise_info['noise_length'] > max_noise_length:
                        max_noise_length = noise_info['noise_length']
                        critical_operand = operand
                        max_allowed_length = noise_info['max_length']
                        
                except Exception as noise_error:
                    # If we can't check noise, assume worst case
                    max_noise_length = 100
                    critical_operand = operand
                    max_allowed_length = 100
            
            switching_threshold, warning_threshold, critical_threshold = self.calculate_dynamic_thresholds(max_allowed_length)
            
            # Check if operation should be blocked
            if max_noise_length > critical_threshold:
                can_perform = False
                if log:
                    log("🚫 ОПЕРАЦИЯТА НЕ МОЖЕ ДА БЪДЕ ИЗПЪЛНЕНА!")
                    log(f"   Критична дължина на шума в {critical_operand}: {max_noise_length} числа")
                    log(f"   Макс дължина: {max_allowed_length} числа")
                    log(f"   Критичен праг: {critical_threshold} числа (85% от {max_allowed_length})")
                    log(f"   Switching праг: {switching_threshold} числа (63% от {max_allowed_length})")
                    if new_depth > 0:
                        log(f"   Дълбочина: {new_depth} (информативно)")
            
            # Check for warnings
            if can_perform and max_noise_length > warning_threshold:
                warnings.append({
                    'type': 'high_noise',
                    'operand': critical_operand,
                    'noise_length': max_noise_length,
                    'threshold': warning_threshold,
                    'depth': new_depth
                })
            
            return can_perform, warnings, {
                'new_depth': new_depth,
                'left_depth': left_depth,
                'right_depth': right_depth,
                'max_noise_length': max_noise_length,
                'critical_operand': critical_operand,
                'switching_threshold': switching_threshold,
                'warning_threshold': warning_threshold,
                'critical_threshold': critical_threshold
            }
            
        except Exception as e:
            # If something goes wrong, block the operation for safety
            if log:
                log(f"❌ Грешка при проверка на операцията: {str(e)}")
            return False, [{'type': 'error', 'message': str(e)}], {'new_depth': 0}
    
    def perform_operation(self, left_operand, operation, right_operand, 
                         encrypted_values, log_func=None):
        # Perform the actual cryptographic operation.
        
        def log(message):
            if log_func:
                log_func(message)
        
        try:
            c0_left, c1_left = encrypted_values[left_operand]
            c0_right, c1_right = encrypted_values[right_operand]
            
            # Check modulus compatibility
            left_modulus = c0_left.coef_modulus
            right_modulus = c0_right.coef_modulus
            
            # Handle modulus mismatch
            if left_modulus != right_modulus:
                # Try to bring both to the same modulus
                if left_modulus == self.coef_modulus and right_modulus != self.coef_modulus:
                    # Left is large, right is small - bring left to small
                    c0_left, c1_left, switched = apply_modulus_switching(
                        left_operand, c0_left, c1_left, self.sk, self.small_modulus, 
                        self.coef_modulus, self.plaintext_modulus, log_func
                    )
                    if switched:
                        encrypted_values[left_operand] = (c0_left, c1_left)
                
                elif right_modulus == self.coef_modulus and left_modulus != self.coef_modulus:
                    # Right is large, left is small - bring right to small
                    c0_right, c1_right, switched = apply_modulus_switching(
                        right_operand, c0_right, c1_right, self.sk, self.small_modulus, 
                        self.coef_modulus, self.plaintext_modulus, log_func
                    )
                    if switched:
                        encrypted_values[right_operand] = (c0_right, c1_right)
            
            # Perform the actual operation
            if operation == "+":
                c0_result, c1_result = add(c0_left, c1_left, c0_right, c1_right)
                op_symbol = "➕"
            elif operation == "*":
                c0_mult, c1_mult, c2_mult = mul(c0_left, c1_left, c0_right, c1_right)
                
                # Determine which relinearization keys to use
                current_modulus = c0_mult.coef_modulus
                
                if current_modulus == self.coef_modulus:
                    # Large modulus - use original keys
                    self.generate_relinearization_keys()
                    c0_result, c1_result = relinearize(c0_mult, c1_mult, c2_mult, self.eks,
                                                       self.base, self.coef_modulus, self.poly_modulus)
                else:
                    # Small modulus - generate temporary keys
                    try:
                        small_sk = self.sk.copy()
                        small_sk.coef_modulus = current_modulus
                        
                        small_eks = gen_relinearization_key(small_sk, self.base, current_modulus, 
                                                          self.poly_modulus, self.plaintext_modulus)
                        
                        c0_result, c1_result = relinearize(c0_mult, c1_mult, c2_mult, small_eks,
                                                           self.base, current_modulus, self.poly_modulus)
                        
                    except Exception as relin_error:
                        if log:
                            log(f"   ❌ Грешка при relinearization: {str(relin_error)}")
                        
                        # Fallback: Use result without relinearization
                        c0_result, c1_result = c0_mult, c1_mult
                
                op_symbol = "✖️"
            else:
                raise ValueError(f"Неподдържана операция: {operation}")
            
            # Check result noise level with dynamic thresholds
            try:
                result_noise_info = check_noise_level(c0_result, c1_result, self.sk, self.plaintext_modulus)
                max_result_length = result_noise_info['max_length']
                
                # Calculate the dynamic thresholds for the result
                _, warning_result_threshold, critical_result_threshold = self.calculate_dynamic_thresholds(max_result_length)
                
                # Block if result has critical noise length
                if result_noise_info['noise_length'] > critical_result_threshold:
                    if log:
                        log("")
                        log("🚫 ОПЕРАЦИЯТА Е БЛОКИРАНА СЛЕД ИЗПЪЛНЕНИЕ!")
                        log(f"   Шумът в резултата е прекалено голям: {result_noise_info['noise_length']} числа")
                        log(f"   Критичен праг: {critical_result_threshold} числа (85% от {max_result_length})")
                        log("   Резултатът няма да бъде запазен!")
                    
                    return None, None, False, {
                        'blocked_reason': 'critical_result_noise',
                        'result_noise_length': result_noise_info['noise_length'],
                        'critical_threshold': critical_result_threshold,
                        'op_symbol': op_symbol
                    }
                
                # Warn if result has long noise but not critical
                if result_noise_info['noise_length'] > warning_result_threshold:
                    if log:
                        log("⚠️ ВНИМАНИЕ: Резултатът има висок шум!")
                        log(f"   Дължина на шума в резултат: {result_noise_info['noise_length']} числа")
                        log(f"   Праг за предупреждение: {warning_result_threshold} числа (75% от {max_result_length})")
                        if result_noise_info['noise_length'] > (critical_result_threshold - 2):
                            log("   🚨 ВНИМАНИЕ: Много близо до критичния праг!")
                
            except Exception as noise_check_error:
                if log:
                    log("⚠️ ВНИМАНИЕ: Не можах да проверя шума в резултата!")
            
            return c0_result, c1_result, True, {
                'op_symbol': op_symbol,
                'success': True
            }
            
        except Exception as e:
            if log:
                log(f"❌ Грешка при операция: {str(e)}")
            
            return None, None, False, {
                'error': str(e),
                'op_symbol': operation
            }
    
    def check_and_apply_auto_switching(self, cryptogram_name, c0, c1, encrypted_values, log_func=None):
        # Check noise and automatically apply modulus switching
        
        def log(message):
            if log_func:
                log_func(message)
        
        try:
            noise_info = check_noise_level(c0, c1, self.sk, self.plaintext_modulus)
            
            switching_threshold, _, _ = self.calculate_dynamic_thresholds(noise_info['max_length'])
            
            # Check if switching should be applied
            if noise_info['noise_length'] > switching_threshold:
                if log:
                    log(f"⚠️ Преди операция: Шумът в {cryptogram_name} е {noise_info['noise_length']} числа")
                    log(f"   Switching праг: {switching_threshold} (63% от {noise_info['max_length']})")
                    log(f"   Прилагане на автоматично modulus switching...")
                
                # Apply switching
                new_c0, new_c1, switching_applied = apply_modulus_switching(
                    cryptogram_name, c0, c1, self.sk, self.small_modulus, 
                    self.coef_modulus, self.plaintext_modulus, log_func
                )
                
                if switching_applied:
                    if log:
                        log(f"✅ Modulus switching успешен за {cryptogram_name}!")
                    # Update stored cryptogram
                    encrypted_values[cryptogram_name] = (new_c0, new_c1)
                    return True
                else:
                    if log:
                        log(f"❌ Modulus switching неуспешен за {cryptogram_name}!")
                    return False
            
            return False
            
        except Exception as e:
            if log:
                log(f"⚠️ Грешка при проверка на шума в '{cryptogram_name}': {str(e)}")
            return False


def calculate_expected_result_for_name(name, operation_history, original_values, plaintext_modulus, poly_modulus, coef_modulus):
    # Calculate expected result for a given encrypted value name
    try:
        # Check if it's an original value first
        if name in original_values:
            return original_values[name]
        
        # For complex operations, try to calculate from history
        for hist in operation_history:
            if hist.get('result') == name and 'Успешно' in hist.get('status', ''):
                left_expected = calculate_expected_result_for_name(
                    hist.get('left_op', ''), operation_history, original_values,
                    plaintext_modulus, poly_modulus, coef_modulus
                )
                right_expected = calculate_expected_result_for_name(
                    hist.get('right_op', ''), operation_history, original_values,
                    plaintext_modulus, poly_modulus, coef_modulus
                )

                if left_expected is not None and right_expected is not None:
                    if hist.get('op_type') == '+':
                        return (left_expected + right_expected) % plaintext_modulus
                    elif hist.get('op_type') == '*':
                        # For polynomial multiplication
                        left_poly = QuotientRingPoly(left_expected, coef_modulus, poly_modulus)
                        right_poly = QuotientRingPoly(right_expected, coef_modulus, poly_modulus)
                        result_poly = (left_poly * right_poly) % plaintext_modulus
                        return result_poly.coef

        # If not found in history, return None (can't calculate expected)
        return None

    except Exception as e:
        print(f"Грешка при изчисляване на очаквания резултат за {name}: {e}")
        return None