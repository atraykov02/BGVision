from dataclasses import dataclass
from typing import List


@dataclass
class BGVDefaults:
    # Default values
    N: int = 16
    LAMBDA_SECURITY: int = 128
    PLAINTEXT_MODULUS: int = 7
    BASE: int = 5
    
    LAMBDA_OPTIONS: List[str] = None
    
    def __post_init__(self):
        if self.LAMBDA_OPTIONS is None:
            self.LAMBDA_OPTIONS = ["80", "128", "192", "256"]


@dataclass
class AppSettings:
    # App settings
    
    # Window
    WINDOW_WIDTH: int = 1400
    WINDOW_HEIGHT: int = 1000
    MIN_WIDTH: int = 1400
    MIN_HEIGHT: int = 800
    
    APP_TITLE: str = "BGVision - практическа демонстрация на криптографската схема BGV"
    APP_SUBTITLE: str = "Софтуер за хомоморфно криптиране с поддръжка на последователни изчисления върху криптирани данни."
    
    MAX_CRYPTOGRAMS: int = 26
    MAX_PARAMETER_ATTEMPTS: int = 100


@dataclass
class UITexts:
    # UI Text information
    
    # Tabs
    CONFIG_TAB_TITLE: str = "⚙️ Конфигурация"
    OPERATIONS_TAB_TITLE: str = "🧮 Хомоморфни операции"
    
    # Sections
    SECTION_BGV_PARAMS: str = "📊 Параметри на BGV схемата"
    SECTION_PARAM_INFO: str = "ℹ️ Информация за параметрите"
    SECTION_CREATE_CRYPTO: str = "🔒 Създаване на криптограми"
    SECTION_EXISTING_CRYPTO: str = "🔐 Съществуващи криптограми"
    SECTION_OPERATIONS: str = "⚡ Хомоморфни операции"
    SECTION_OPERATION_SETTINGS: str = "Настройки на операцията"
    SECTION_OPERATION_HISTORY: str = "История на операциите"
    SECTION_RESULTS: str = "📊 Резултати и декриптиране"
    
    # Params
    PARAM_N: str = "Степен на полинома (n):"
    PARAM_LAMBDA: str = "Параметър за сигурност (λ):"
    PARAM_T: str = "Модул на явното съобщение (t):"
    PARAM_BASE: str = "База за релинеаризация:"
    PARAM_Q: str = "Модул на криптираните съобщения (q):"
    PARAM_Q_AUTO: str = "Автоматично от λ"
    
    # Operations
    OP_LEFT_OPERAND: str = "Лява страна:"
    OP_RIGHT_OPERAND: str = "Дясна страна:"
    OP_OPERATION: str = "Операция:"
    OP_ADD: str = "+ Събиране"
    OP_MULTIPLY: str = "× Умножение"
    
    CURR_CRYPTOGRAM: str = "Текуща криптограма:"
    VALUES_INPUT: str = "Стойности (разделени със запетая):"
    
    # Buttons
    BTN_GENERATE_KEYS: str = "Генерирай ключове"
    BTN_RESET_DEFAULTS: str = "Възстанови стандартни стойности"
    BTN_ENCRYPT: str = "Криптирай"
    BTN_RANDOM: str = "Генерирай случайни стойности"
    BTN_REFRESH: str = "Обнови"
    BTN_VIEW: str = "Преглед"
    BTN_CLEAR_ALL: str = "Изчисти всички"
    BTN_DECRYPT: str = "Декриптирай"
    BTN_CALCULATE: str = "Пресметни"
    BTN_CLEAR_HISTORY: str = "Изчисти историята"
    
    # Status
    STATUS_NO_KEYS: str = "Ключове: Не са генерирани."
    STATUS_KEYS_SUCCESS: str = "Ключове: Генерирани успешно!"
    STATUS_INVALID_PARAMS: str = "Невалидни параметри."
    STATUS_COMPATIBILITY_ERROR: str = "Грешка при съвместимост!"
    STATUS_GENERATION_ERROR: str = "Грешка при генериране!"


@dataclass
class ValidationRules:
    # Validation rules
    
    # Polynomial degree
    N_MIN: int = 4
    N_MAX: int = 128
    
    # Security parameter
    LAMBDA_MIN: int = 80
    LAMBDA_MAX: int = 512
    
    # Plaintext modulus
    T_MIN: int = 2
    T_MAX: int = 100
    
    # Base
    BASE_MIN: int = 2
    BASE_MAX: int = 10
    
    # Coefficient modulus bits
    COEF_BITS_MIN: int = 32
    COEF_BITS_MAX: int = 512
    COEF_BITS_BUFFER: int = 32


@dataclass
class NoiseManagement:
    #Noise management
    
    # Modulus switching limits
    SWITCHING_THRESHOLD: int = 40
    CRITICAL_THRESHOLD_OFFSET: int = 40
    WARNING_THRESHOLD_OFFSET: int = 45
    
    SWITCHING_THRESHOLD_PERCENT: float = 40.0
    CRITICAL_THRESHOLD_PERCENT: float = 60.0
    
    # Maximal attempts
    MAX_SWITCHING_ATTEMPTS: int = 50
    MAX_MODULUS_ATTEMPTS: int = 100


class ParameterDescriptions:
    # Parameter descriptions
    
    N_DESCRIPTION = """Степен на полинома (n):

• Определя размера на векторите за криптиране.
• Трябва да е степен на двойката (4, 8, 16, 32, 64, 128).
• По-голяма стойност = повече сигурност, но по-бавни операции.
• Препоръчително: 16-32 за демонстрация на работата на схемата, 64-128 за по-сложни операции.
• Максимална стойност: 128."""

    LAMBDA_DESCRIPTION = """Параметър за сигурност (λ):

• Определя нивото на криптографска устойчивост.
• λ = 80 бита - минимална сигурност.
• λ = 128 бита - стандартна сигурност (препоръчително).
• λ = 192/256 бита - висока сигурност.
• По-високо λ = по-големи модули = по-бавни операции."""

    T_DESCRIPTION = """Модул на явното съобщение (t):

• Определя пространството на некриптираните съобщения.
• Диапазон на стойностите във вектора за криптиране: от 0 до t-1.
• t трябва да е просто число (2, 3, 5, 7, 11, 13...).
• Малки стойности (2-31) са добри за демонстрация на работата на схемата.
• По-големи стойности позволяват съхранението на повече данни."""

    BASE_DESCRIPTION = """База за релинеаризация:

• Използва се за оптимизация на умножението.
• Препоръчителни стойности: 3-10.
• По-малка база = по-бавна релинеризация.
• По-голяма база = повече памет за релинизиращи ключове.
• Обикновено 3-5 е добър избор.
• Максимална стойност: 10."""

    N_INFO_SHORT = "🔹 Степен на полинома (n): Определя размера на векторите за криптиране.\n   • Числото трябва да е степен на двойката (4, 8, 16, 32, 64, 128).\n   • По-голяма стойност = повече сигурност, но по-бавни операции.\n   • Препоръчително: 16-32 за демонстрация на работата на схемата, 64-128 за по-сложни операции.\n   • Максимална стойност: 128."

    LAMBDA_INFO_SHORT = "🔹 Параметър за сигурност (λ): Определя нивото на криптографска устойчивост (в бита) на криптосистемата, спрямо известни атаки.\n   • λ = 80 бита - минимална сигурност на схемата.\n   • λ = 128 бита - стандартна сигурност (препоръчително).\n   • λ = 192/256 бита - висока сигурност на схемата."

    T_INFO_SHORT = "🔹 Модул на явното съобщение (t): Определя пространството на некриптираните съобщения.\n   • Диапазон на стойностите във вектора за криптиране: от 0 до t-1.\n   • t трябва да е просто число (2, 3, 5, 7, 11, 13...).\n   • Малки стойности (2-31) са добри за демонстрация на работата на схемата.\n   • По-големи стойности позволяват съхранението на повече данни."

    BASE_INFO_SHORT = "🔹 База за релинеаризация: Използва се за оптимизация на умножението.\n   • Препоръчителни стойности: от 3 до 10.\n   • По-малка база = по-бавна операция по релинеаризиране.\n   • По-голяма база = повече памет за релинеаризиращи ключове.\n   • Максимална стойност: 10."

    Q_INFO_SHORT = "🔹 Модул на криптираните съобщения (q): Определя ciphertext space - пространството на криптираните съобщения. \n   Автоматично се изчислява въз основа на λ за оптимална сигурност."


@dataclass
class HelpTexts:
    
    HELP_N: str = ParameterDescriptions.N_DESCRIPTION
    HELP_LAMBDA: str = ParameterDescriptions.LAMBDA_DESCRIPTION  
    HELP_T: str = ParameterDescriptions.T_DESCRIPTION
    HELP_BASE: str = ParameterDescriptions.BASE_DESCRIPTION


@dataclass
class WelcomeMessage:
    # Welcome message in the operations tab
    
    CONTENT: str = """🔹 Добре дошли в BGVision!

🔧 НАЧАЛО:
1. Отидете в таба „Конфигурация" и настройте параметрите.
2. Натиснете „Генерирай ключове".
3. Изберете таба „Хомоморфни операции".

📚 ТАБОВЕ:
• Конфигурация - Настройка на параметри и генериране на ключове.
• Хомоморфни операции - Създаване на криптограми и извършване на операции с тях.

💡 СЪВЕТ: Започнете с по-малки параметри за по-бързи операции!

🔗 СЪЗДАВАНЕ НА КРИПТОГРАМИ:
• Въведете стойности за вашата криптограма.
• Правете операции като A+B→R1, R1*C→R2.
• Следете историята на операциите.
• Декриптирайте резултатите за проверка.
"""


@dataclass
class ParameterInfo:
    
    @property
    def CONTENT(self) -> str:
        return f"""⚙️ ПАРАМЕТРИ НА СХЕМАТА:
{ParameterDescriptions.N_INFO_SHORT}

{ParameterDescriptions.LAMBDA_INFO_SHORT}

{ParameterDescriptions.T_INFO_SHORT}

{ParameterDescriptions.BASE_INFO_SHORT}

{ParameterDescriptions.Q_INFO_SHORT}

⚙️ ВРЪЗКА λ → q: q ≈ 2^(λ + log₂(n)) за постигане на λ-битова сигурност.

⚠️ При промяна на параметрите е необходимо повторно генериране на ключовете!

💡 СЪВЕТИ ЗА ОПТИМАЛНИ ПАРАМЕТРИ:
• За демонстрация и тестови цели: n=16, λ=128, t=7.
• За реални приложения: n ≥ 64, λ ≥ 128, t според необходимостта.
• По-големи параметри = повече сигурност, но по-бавни операции.
• Започнете с малки параметри и ги увеличавайте при нужда.

🎯 ПРАКТИЧЕСКИ ПРЕПОРЪКИ:
• Използвайте просто число за t (2, 3, 5, 7, 11, 13...).
• База 3-5 е оптимална за повечето случаи.
• λ=128 е добър баланс между сигурност и производителност.
"""


class Config:
    # Main config class
    
    def __init__(self):
        self.bgv = BGVDefaults()
        self.app = AppSettings()
        self.ui_texts = UITexts()
        self.validation = ValidationRules()
        self.noise = NoiseManagement()
        self.help = HelpTexts()
        self.welcome = WelcomeMessage()
        self.param_info = ParameterInfo()

        self.descriptions = ParameterDescriptions()
    
    def get_instruction_text(self, n=None, t=None):
        if n is None:
            n = self.bgv.N
        if t is None:
            t = self.bgv.PLAINTEXT_MODULUS
            
        return f"Въведете точно {n} стойности (0 до {t - 1})"
    
    def validate_power_of_two(self, n):
        return n > 0 and (n & (n - 1)) == 0
    
    def get_suggested_coef_bits(self, lambda_security, n):
        import math
        log_n = math.log2(n)
        coef_bits = lambda_security + int(log_n) + self.validation.COEF_BITS_BUFFER
        return max(self.validation.COEF_BITS_MIN, 
                  min(coef_bits, self.validation.COEF_BITS_MAX))

config = Config()

# Export
__all__ = [
    'Config', 'BGVDefaults', 'AppSettings', 'UITexts', 'ValidationRules',
    'NoiseManagement', 'HelpTexts', 'WelcomeMessage', 'ParameterInfo', 
    'ParameterDescriptions', 'config'
]