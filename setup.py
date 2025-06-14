#!/usr/bin/env python3
"""
Setup скрипт за BGVision
"""

import sys
import subprocess

def install_requirements():
    """Инсталира необходимите зависимости"""
    requirements = [
        'numpy',
        'pycryptodome'
    ]
    
    print("Инсталиране на зависимости...")
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', req])
            print(f"   ✅ {req}")
        except subprocess.CalledProcessError:
            print(f"   ❌ Грешка при инсталиране на {req}")

if __name__ == "__main__":
    install_requirements()
    print("Готово! Сега можете да стартирате: python run.py")
