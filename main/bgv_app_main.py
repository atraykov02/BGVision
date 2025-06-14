import tkinter as tk

from config.config import config
from gui.config_tab import ConfigurationTab
from gui.operations_tab import OperationsTab
from gui.styles import Styles
from gui.widget_factory import LayoutHelper


class BGVApp:
    # Main class

    def __init__(self, root):
        self.root = root
        self.setup_window()

        self.style = Styles.setup_ttk_styles()

        # Initialize BGV parameters from config
        self.init_bgv_parameters()
        
        # Initialize application state
        self.init_application_state()

        # Setup UI
        self.setup_ui()

    def setup_window(self):
        # Setup main window with config values
        
        self.root.title(config.app.APP_TITLE)
        self.root.geometry(f"{config.app.WINDOW_WIDTH}x{config.app.WINDOW_HEIGHT}")
        self.root.configure(bg='#f0f0f0')
        
        self.root.minsize(config.app.MIN_WIDTH, config.app.MIN_HEIGHT)
        
        self.center_window()

    def center_window(self):
        # Center window on screen
        
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (config.app.WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (config.app.WINDOW_HEIGHT // 2)
        self.root.geometry(f'{config.app.WINDOW_WIDTH}x{config.app.WINDOW_HEIGHT}+{x}+{y}')

    def init_bgv_parameters(self):
        # Initialize BGV parameters from config
        
        self.n = config.bgv.N
        self.lambda_security = config.bgv.LAMBDA_SECURITY
        self.plaintext_modulus = config.bgv.PLAINTEXT_MODULUS
        self.base = config.bgv.BASE
        
        self.coef_modulus = None
        self.poly_modulus = None
        self.small_modulus = None
        self.delta = None

        self.sk = None
        self.pk0 = None
        self.pk1 = None
        self.operation_handler = None

    def init_application_state(self):
        # Initialize application state
        
        self.encrypted_values = {}
        self.operation_history = []
        self.original_values = {}

        self.next_crypto_letter = ord('A')
        self.result_counter = 1

        # UI component references
        self.notebook = None
        self.config_tab = None
        self.operations_tab = None

    def setup_ui(self):
        # Setup main user interface with new system
        
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        LayoutHelper.pack_configure(main_container, fill='both', expand=True, padx=20, pady=20)

        self.setup_title_section(main_container)

        # Notebook for tabs
        self.setup_notebook(main_container)

        # Setup tabs
        self.config_tab = ConfigurationTab(self.notebook, self)
        self.operations_tab = OperationsTab(self.notebook, self)

    def setup_title_section(self, parent):
        # Setup title section with new system
        
        title_frame = tk.Frame(parent, bg='#ffffff', relief='flat', bd=1)
        LayoutHelper.pack_configure(title_frame, fill='x', pady=(0, 20))

        title_label = tk.Label(
            title_frame, text=config.app.APP_TITLE, 
            font=('Segoe UI', 18, 'bold'), bg='#ffffff'
        )
        LayoutHelper.pack_configure(title_label, pady=15)

        subtitle_label = tk.Label(
            title_frame, text=config.app.APP_SUBTITLE, 
            font=('Segoe UI', 10), bg='#ffffff'
        )
        LayoutHelper.pack_configure(subtitle_label)

    def setup_notebook(self, parent):
        # Setup notebook container with new system
        
        from tkinter import ttk
        self.notebook = ttk.Notebook(parent)
        LayoutHelper.pack_configure(self.notebook, fill='both', expand=True)

    def reset_application_state(self):
        # Reset application state for new key generation
        
        self.encrypted_values = {}
        self.operation_history = []
        self.original_values = {}

        self.next_crypto_letter = ord('A')
        self.result_counter = 1

        # Update UI components in operations tab
        if hasattr(self, 'operations_tab'):
            self.operations_tab.update_all_combos()
            self.operations_tab.update_encrypted_list()
            self.operations_tab.clear_operation_history()
            self.operations_tab.update_next_crypto_label()
            self.operations_tab.left_operand_var.set("")
            self.operations_tab.right_operand_var.set("")
            if hasattr(self.operations_tab, 'results_text'):
                self.operations_tab.results_text.delete('1.0', 'end')
                self.operations_tab.show_welcome_message()


def main():
    # Main function to start the application
    
    root = tk.Tk()

    # Create and run application
    app = BGVApp(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()