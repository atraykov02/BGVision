from tkinter import ttk


class Colors:
    # Main colors
    PRIMARY = '#007acc'
    SECONDARY = '#0066cc' 
    SUCCESS = '#28a745'
    ERROR = '#dc3545'
    WARNING = '#ffc107'
    INFO = '#007acc'
    
    BACKGROUND = '#f0f0f0'            
    WHITE = '#ffffff'                
    LIGHT_GRAY = '#f8f9fa'          
    CARD_BG = '#f0f0f0'             
    FRAME_BG = '#e8e8e8'            
    WINDOW_BG = '#f0f0f0'           
    
    TEXT_PRIMARY = '#000000'        
    TEXT_SECONDARY = '#444444'      
    TEXT_MUTED = '#777777'           
    TEXT_ACCENT = '#0066cc'          
    
    HOVER_LIGHT = '#e0e0e0'
    FOCUS_BORDER = '#80bdff'


class Fonts:

    FAMILY = 'Segoe UI'
    FAMILY_MONO = 'Courier'
    
    SIZE_LARGE = 16      
    SIZE_HEADING = 14    
    SIZE_SUBHEADING = 10 
    SIZE_NORMAL = 9      
    SIZE_SMALL = 8       
    SIZE_TINY = 7        
    
    WEIGHT_BOLD = 'bold'
    WEIGHT_NORMAL = 'normal'
    
    @classmethod
    def get(cls, size=SIZE_NORMAL, weight=WEIGHT_NORMAL, family=None):
        if family is None:
            family = cls.FAMILY
        return (family, size, weight)
    
    @classmethod
    def title(cls):
        return cls.get(cls.SIZE_LARGE, cls.WEIGHT_BOLD)
    
    @classmethod
    def heading(cls):
        return cls.get(cls.SIZE_HEADING, cls.WEIGHT_BOLD)
    
    @classmethod
    def subheading(cls):
        return cls.get(cls.SIZE_SUBHEADING, cls.WEIGHT_NORMAL)
    
    @classmethod
    def normal(cls):
        return cls.get(cls.SIZE_NORMAL)
    
    @classmethod
    def small(cls):
        return cls.get(cls.SIZE_SMALL)
    
    @classmethod
    def mono(cls, size=SIZE_NORMAL):
        return cls.get(size, family=cls.FAMILY_MONO)
    
    @classmethod
    def button_primary(cls):
        return cls.get(cls.SIZE_NORMAL, cls.WEIGHT_NORMAL)


class Spacing:
    # Padding
    PADDING_SMALL = 5
    PADDING_MEDIUM = 10
    PADDING_LARGE = 15
    PADDING_XLARGE = 20
    PADDING_XXLARGE = 30
    
    # Margins
    MARGIN_SMALL = 5
    MARGIN_MEDIUM = 10
    MARGIN_LARGE = 15
    MARGIN_XLARGE = 20


class Dimensions:
    # Entry fields
    ENTRY_WIDTH_SMALL = 8
    ENTRY_WIDTH_MEDIUM = 12
    ENTRY_WIDTH_LARGE = 25
    ENTRY_WIDTH_XLARGE = 50
    
    # Combo boxes
    COMBO_WIDTH_SMALL = 8
    COMBO_WIDTH_MEDIUM = 15
    COMBO_WIDTH_LARGE = 25
    
    # Listbox
    LISTBOX_HEIGHT = 8
    
    # Buttons
    BUTTON_WIDTH_SMALL = 3
    BUTTON_WIDTH_MEDIUM = 12
    BUTTON_WIDTH_LARGE = 20
    
    # Text widgets
    TEXT_HEIGHT_SMALL = 10
    TEXT_HEIGHT_MEDIUM = 15
    TEXT_HEIGHT_LARGE = 20
    
    # Fixed widths for cards
    CARD_WIDTH_SMALL = 300
    CARD_WIDTH_MEDIUM = 400
    CARD_WIDTH_LARGE = 500


class Styles:
    # Styles for different components
    
    @staticmethod
    def setup_ttk_styles():
        style = ttk.Style()
        style.theme_use('clam')
        
        # Title
        style.configure('Title.TLabel', 
                       font=Fonts.title(), 
                       background=Colors.BACKGROUND,
                       foreground=Colors.TEXT_PRIMARY)
        
        # Heading labels
        style.configure('Heading.TLabel', 
                       font=Fonts.heading(), 
                       background=Colors.BACKGROUND,
                       foreground=Colors.TEXT_PRIMARY)
        
        # Subheading labels
        style.configure('Subheading.TLabel', 
                       font=Fonts.subheading(), 
                       background=Colors.BACKGROUND,
                       foreground=Colors.TEXT_PRIMARY)
        
        # Normal labels
        style.configure('Normal.TLabel', 
                       font=Fonts.normal(), 
                       background=Colors.BACKGROUND,
                       foreground=Colors.TEXT_PRIMARY)
        
        # Small labels
        style.configure('Small.TLabel', 
                       font=Fonts.small(), 
                       background=Colors.BACKGROUND,
                       foreground=Colors.TEXT_SECONDARY)
        
        # Accent text
        style.configure('Accent.TLabel', 
                       font=Fonts.normal(), 
                       foreground=Colors.TEXT_ACCENT,
                       background=Colors.BACKGROUND)
        
        # Muted text
        style.configure('Muted.TLabel', 
                       font=Fonts.small(), 
                       foreground=Colors.TEXT_MUTED,
                       background=Colors.BACKGROUND)
        
        # Status labels
        style.configure('Success.TLabel', 
                       foreground=Colors.SUCCESS, 
                       font=Fonts.normal(),
                       background=Colors.BACKGROUND)
        
        style.configure('Error.TLabel', 
                       foreground=Colors.ERROR, 
                       font=Fonts.normal(),
                       background=Colors.BACKGROUND)
        
        style.configure('Warning.TLabel', 
                       foreground=Colors.WARNING, 
                       font=Fonts.normal(),
                       background=Colors.BACKGROUND)
        
        # Frames
        style.configure('Modern.TFrame', 
                       background=Colors.BACKGROUND,
                       relief='flat', 
                       borderwidth=1)
        
        style.configure('Card.TFrame', 
                       background=Colors.CARD_BG,
                       relief='solid', 
                       borderwidth=1)
        
        # Buttons
        style.configure('Primary.TButton', 
                       font=Fonts.button_primary(),
                       padding=(10, 5))
        
        style.configure('Secondary.TButton', 
                       font=Fonts.normal(),
                       padding=(8, 4))
        
        style.configure('Small.TButton', 
                       font=Fonts.small(),
                       padding=(5, 3))
        
        # LabelFrames
        style.configure('Card.TLabelframe', 
                       background=Colors.CARD_BG,
                       relief='solid',
                       borderwidth=1,
                       labeloutside=True)
        
        style.configure('Card.TLabelframe.Label',
                       font=Fonts.normal(),
                       background=Colors.CARD_BG)
        
        return style


class Icons:
    # Icons
    
    SETTINGS = '⚙️'
    CALCULATE = '🧮'
    ENCRYPT = '🔒'
    DECRYPT = '🔓'
    KEY = '🔑'
    
    ADD = '➕'
    MULTIPLY = '✖️'
    EXECUTE = '🚀'
    
    VIEW = '👁️'
    DELETE = '🗑️'
    REFRESH = '🔄'
    HELP = '❓'
    RANDOM = '🎲'
    
    SUCCESS = '✅'
    ERROR = '❌'
    WARNING = '⚠️'
    INFO = 'ℹ️'
    
    CHART = '📊'
    FOLDER = '📁'
    DOCUMENT = '📄'
    CRYPTOGRAM = '🔐'


class Messages:
    # Messages

    NO_KEYS = "Първо генерирайте ключове в таба „Конфигурация“."
    INVALID_INPUT = "Невалидни входни данни!"
    OPERATION_BLOCKED = "Операцията е блокирана поради критично ниво на шума."
    
    KEYS_GENERATED = "Ключове: Генерирани успешно!"
    ENCRYPTION_SUCCESS = "Криптограмата е създадена успешно!"
    
    HIGH_NOISE = "ВНИМАНИЕ: Висок шум!"
    MAX_CRYPTOGRAMS = "Достигнат е максималният брой криптограми."
    
    CONFIRM_CLEAR = "Искате ли да изчистите всички криптирани стойности?"


class ComponentConfig:
    # Configuration for different UI components
    
    # Entry fields
    ENTRY_SMALL = {
        'width': Dimensions.ENTRY_WIDTH_SMALL,
        'font': ('Segoe UI', 9)
    }
    
    ENTRY_MEDIUM = {
        'width': Dimensions.ENTRY_WIDTH_MEDIUM,
        'font': ('Segoe UI', 9)
    }
    
    ENTRY_LARGE = {
        'width': Dimensions.ENTRY_WIDTH_LARGE,
        'font': ('Segoe UI', 9)
    }
    
    ENTRY_VALUES = {
        'width': Dimensions.ENTRY_WIDTH_XLARGE,
        'font': ('Courier', 8)
    }
    
    # Combo boxes
    COMBO_SMALL = {
        'width': Dimensions.COMBO_WIDTH_SMALL,
        'state': 'readonly'
    }
    
    COMBO_MEDIUM = {
        'width': Dimensions.COMBO_WIDTH_MEDIUM,
        'state': 'readonly'
    }
    
    COMBO_LARGE = {
        'width': Dimensions.COMBO_WIDTH_LARGE,
        'state': 'readonly'
    }
    
    # Listbox
    LISTBOX_DEFAULT = {
        'height': Dimensions.LISTBOX_HEIGHT,
        'font': ('Courier', 8)
    }
    
    # Text widgets
    TEXT_RESULTS = {
        'font': ('Courier', 8),
        'wrap': 'word',
        'bg': Colors.WHITE,
        'fg': Colors.TEXT_PRIMARY
    }
    
    TEXT_INFO = {
        'wrap': 'word',
        'font': ('Segoe UI', 9),
        'state': 'disabled',
        'cursor': 'arrow',
        'bg': Colors.WHITE,
        'fg': Colors.TEXT_PRIMARY
    }
    
    # Buttons
    BUTTON_PRIMARY = {
        'style': 'Primary.TButton'
    }
    
    BUTTON_SECONDARY = {
        'style': 'Secondary.TButton'
    }
    
    BUTTON_SMALL = {
        'style': 'Small.TButton'
    }
    
    BUTTON_HELP = {
        'width': Dimensions.BUTTON_WIDTH_SMALL,
        'style': 'Small.TButton'
    }


class LayoutConfig:
    
    # Padding
    CARD_PADDING = Spacing.PADDING_LARGE
    SECTION_PADDING = Spacing.PADDING_MEDIUM
    BUTTON_PADDING = Spacing.PADDING_SMALL
    
    # Spacing
    ELEMENT_SPACING = Spacing.MARGIN_MEDIUM
    SECTION_SPACING = Spacing.MARGIN_LARGE
    
    # Grid
    GRID_PADX = (0, Spacing.MARGIN_MEDIUM)
    GRID_PADY = Spacing.MARGIN_SMALL
    
    # Pack
    PACK_PADY_SMALL = (0, Spacing.MARGIN_SMALL)
    PACK_PADY_MEDIUM = (0, Spacing.MARGIN_MEDIUM)
    PACK_PADY_LARGE = (0, Spacing.MARGIN_LARGE)


# Export
__all__ = [
    'Colors', 'Fonts', 'Spacing', 'Dimensions', 'Styles', 'Icons', 
    'Messages', 'ComponentConfig', 'LayoutConfig'
]