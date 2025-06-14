#!/usr/bin/env python3
"""
Главен стартов скрипт за BGVision
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        from main.bgv_app_main import main as app_main
        app_main()
    except ImportError as e:
        print(f"❌ Грешка при import: {e}")
        print("Моля, проверете дали всички файлове са на правилното място.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Неочаквана грешка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
