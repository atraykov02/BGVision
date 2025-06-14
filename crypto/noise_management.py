import numpy as np

from core.bgv import decrypt
from core.modulus_switch import scale2


def check_noise_level(c0, c1, sk, plaintext_modulus):
    try:
        current_modulus = c0.coef_modulus
        
        if current_modulus != sk.coef_modulus:
            decrypt_sk = sk.copy()
            decrypt_sk.coef_modulus = current_modulus
        else:
            decrypt_sk = sk
        
        _, noise = decrypt(c0, c1, decrypt_sk, plaintext_modulus, return_noise=True)
        max_noise = current_modulus // 2
        
        noise_length = len(str(noise))
        max_length = len(str(max_noise))
        
        percentage = (float(noise) / float(max_noise)) * 100 if max_noise > 0 else 100.0
        
        return {
            'noise': noise,
            'max_noise': max_noise,
            'noise_length': noise_length,
            'max_length': max_length,
            'percentage': percentage,
            'current_modulus': current_modulus
        }
        
    except Exception as e:
        return {
            'noise': 0,
            'max_noise': 1,
            'noise_length': 1,
            'max_length': 1,
            'percentage': 0.0,
            'current_modulus': c0.coef_modulus,
            'error': str(e)
        }


def calculate_switching_threshold_from_max_length(max_length):
    return max(1, int(max_length * 0.63))


def apply_modulus_switching(cryptogram_name, c0, c1, sk, small_modulus, 
                                       large_modulus, plaintext_modulus, log_func=None):
    # Apply modulus switching

    def log(message):
        if log_func:
            log_func(message)
        else:
            print(message)
    
    try:
        current_modulus = c0.coef_modulus
        
        if current_modulus == large_modulus:
            decrypt_sk = sk
            target_small_modulus = small_modulus
        else:
            return c0, c1, False
        
        noise_info = check_noise_level(c0, c1, decrypt_sk, plaintext_modulus)
        
        # applying switching - 63% from max_length
        switching_threshold = calculate_switching_threshold_from_max_length(noise_info['max_length'])
        critical_threshold = int(noise_info['max_length'] * 0.85)  # 85% from max
        
        log(f"   • Шум: {noise_info['noise_length']} числа")
        log(f"   • Switching праг: {switching_threshold} (63% от {noise_info['max_length']})")
        log(f"   • Критичен праг: {critical_threshold} (85% от {noise_info['max_length']})")
        
        if noise_info['noise_length'] > switching_threshold:
            if noise_info['noise_length'] <= critical_threshold:
                try:
                    temp_decrypt, _ = decrypt(c0, c1, decrypt_sk, plaintext_modulus, return_noise=True)
                    
                    c0_switched = scale2(c0, large_modulus, target_small_modulus, plaintext_modulus)
                    c1_switched = scale2(c1, large_modulus, target_small_modulus, plaintext_modulus)
                    
                    c0_switched.coef_modulus = target_small_modulus
                    c1_switched.coef_modulus = target_small_modulus
                    
                    temp_sk = sk.copy()
                    temp_sk.coef_modulus = target_small_modulus
                    
                    new_decrypt, new_noise = decrypt(c0_switched, c1_switched, temp_sk, plaintext_modulus, return_noise=True)
                    new_noise_length = len(str(new_noise))
                    
                    matches = np.sum(temp_decrypt.coef == new_decrypt.coef)
                    match_ratio = matches / len(temp_decrypt.coef)
                    
                    log(f"   • Съвпадение: {match_ratio*100:.1f}% коефициенти")
                    
                    if match_ratio >= 0.7:
                        log(f"✅ Шумът е успешно редуциран!")
                        log(f"   • Стар шум: {noise_info['noise_length']} числа")
                        log(f"   • Нов шум: {new_noise_length} числа")
                        log(f"   • Запазени: {match_ratio*100:.1f}% коефициенти")
                        
                        return c0_switched, c1_switched, True
                    else:
                        log(f"❌ Switching се провали - само {match_ratio*100:.1f}% съвпадение")
                        log(f"   • Оригинал: {temp_decrypt.coef}")
                        log(f"   • След switching: {new_decrypt.coef}")
                        return c0, c1, False
                        
                except Exception as e:
                    log(f"❌ Грешка в switching: {str(e)}")
                    return c0, c1, False
            else:
                log(f"❌ Твърде висок шум за switching ({noise_info['noise_length']} > {critical_threshold})")
                return c0, c1, False
        else:
            log(f"✅ Шумът е OK ({noise_info['noise_length']} <= {switching_threshold})")
            return c0, c1, False
            
    except Exception as e:
        log(f"❌ Глобална грешка: {str(e)}")
        return c0, c1, False