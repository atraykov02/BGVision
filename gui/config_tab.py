from config.config import config
from config.parameter_validator import validate_bgv_parameters
from core.bgv import gen_public_key, gen_secret_key
from core.polynomial import init_poly_modulus
from crypto.modulus_compatibility import (generate_compatible_modulus,
                                          verify_modulus_compatibility)
from crypto.operation_handler import OperationHandler
from gui.styles import Icons
from gui.widget_factory import (DialogFactory, LayoutHelper, WidgetFactory,
                                create_parameter_row)


class ConfigurationTab:
    # Configuration tab class

    def __init__(self, parent_notebook, main_app):
        self.main_app = main_app
        self.parent_notebook = parent_notebook
        
        # UI components
        self.n_entry = None
        self.lambda_combo = None
        self.lambda_var = None
        self.plaintext_entry = None
        self.base_entry = None
        self.coef_display_label = None
        self.key_status_update = None
        
        self.setup_configuration_tab()

    def setup_configuration_tab(self):
        # Setup configuration tab
        
        # Create the main tab
        config_frame = WidgetFactory.create_frame(self.parent_notebook)
        self.parent_notebook.add(config_frame, text=config.ui_texts.CONFIG_TAB_TITLE)

        # Main container
        main_container = WidgetFactory.create_frame(config_frame)
        LayoutHelper.pack_configure(main_container, fill='both', expand=True, 
                                   padx=20, pady=20)

        # TOP ROW - Parameters (left) and Information (right)
        top_row = WidgetFactory.create_frame(main_container)
        LayoutHelper.pack_configure(top_row, fill='both', expand=True)

        # LEFT SIDE: Parameters
        self.setup_parameter_inputs(top_row)

        # RIGHT SIDE: Information
        self.setup_parameter_info(top_row)

    def setup_parameter_inputs(self, parent):
        # Setup LEFT section - Parameters
        
        # Parameters card
        params_card = WidgetFactory.create_labelframe(
            parent, config.ui_texts.SECTION_BGV_PARAMS
        )
        LayoutHelper.pack_configure(params_card, side='left', fill='y', padx=(0, 10))
        
        params_card.configure(width=440)
        params_card.pack_propagate(False)

        # Parameter inputs grid
        self.setup_parameter_grid(params_card)
        
        # Generate button section
        self.setup_generate_section(params_card)
        
        # Status section
        self.setup_status_section(params_card)

    def setup_parameter_grid(self, parent):
        # Setup parameter inputs grid
        grid_frame = WidgetFactory.create_frame(parent)
        LayoutHelper.pack_configure(grid_frame, anchor='w', pady=10)

        for col in range(3):
            grid_frame.grid_columnconfigure(col, weight=0)

        # Polynomial degree
        self.n_entry, _ = create_parameter_row(
            grid_frame, config.ui_texts.PARAM_N, "medium",
            lambda: self.show_help('n'), row=0
        )
        self.n_entry.insert(0, str(config.bgv.N))

        # Security parameter
        lambda_label = WidgetFactory.create_label(
            grid_frame, config.ui_texts.PARAM_LAMBDA, "subheading"
        )
        LayoutHelper.grid_configure(lambda_label, row=1, column=0, sticky='w')

        self.lambda_combo, self.lambda_var = WidgetFactory.create_combo(
            grid_frame, config.bgv.LAMBDA_OPTIONS, "small"
        )
        self.lambda_var.set(str(config.bgv.LAMBDA_SECURITY))
        LayoutHelper.grid_configure(self.lambda_combo, row=1, column=1, sticky='w')

        lambda_help = WidgetFactory.create_button(
            grid_frame, "", lambda: self.show_help('lambda'), "help"
        )
        LayoutHelper.grid_configure(lambda_help, row=1, column=2)

        # Plaintext modulus
        self.plaintext_entry, _ = create_parameter_row(
            grid_frame, config.ui_texts.PARAM_T, "medium",
            lambda: self.show_help('t'), row=2
        )
        self.plaintext_entry.insert(0, str(config.bgv.PLAINTEXT_MODULUS))

        # Base
        self.base_entry, _ = create_parameter_row(
            grid_frame, config.ui_texts.PARAM_BASE, "medium",
            lambda: self.show_help('base'), row=3
        )
        self.base_entry.insert(0, str(config.bgv.BASE))

        # Coefficient modulus display
        coef_label = WidgetFactory.create_label(
            grid_frame, config.ui_texts.PARAM_Q, "subheading"
        )
        LayoutHelper.grid_configure(coef_label, row=4, column=0, sticky='w')

        self.coef_display_label = WidgetFactory.create_label(
            grid_frame, config.ui_texts.PARAM_Q_AUTO, "accent"
        )
        LayoutHelper.grid_configure(self.coef_display_label, row=4, column=1, sticky='w')

    def setup_generate_section(self, parent):
        # Setup generate button section
        
        buttons_frame = WidgetFactory.create_frame(parent)
        LayoutHelper.pack_configure(buttons_frame, pady=30)

        generate_button = WidgetFactory.create_button(
            buttons_frame, config.ui_texts.BTN_GENERATE_KEYS,
            self.generate_keys_with_integrated_logic, "primary"
        )
        LayoutHelper.pack_configure(generate_button)

    def setup_status_section(self, parent):
        # Setup status section
        
        status_frame = WidgetFactory.create_frame(parent)
        LayoutHelper.pack_configure(status_frame, pady=20)

        import tkinter as tk
        status_label = tk.Label(
            status_frame, 
            text=config.ui_texts.STATUS_NO_KEYS,
            font=('Segoe UI', 12, 'bold'), 
            fg='#666666',
            bg='#f0f0f0',
            bd=0,
            relief='flat'
        )
        LayoutHelper.pack_configure(status_label, pady=(0, 15))
        
        # Update status
        def update_status(status_type, text):
            colors = {
                'success': '#28a745',
                'error': '#dc3545',
                'normal': '#666666'
            }
            color = colors.get(status_type, '#666666')
            status_label.config(text=text, fg=color)
        
        self.key_status_update = update_status

        # Reset button with default params
        reset_button = WidgetFactory.create_button(
            status_frame, config.ui_texts.BTN_RESET_DEFAULTS,
            self.reset_to_defaults, "secondary", Icons.REFRESH
        )
        LayoutHelper.pack_configure(reset_button)

    def setup_parameter_info(self, parent):
        # Setup RIGHT section - Information
        
        # Information card
        info_card = WidgetFactory.create_labelframe(
            parent, config.ui_texts.SECTION_PARAM_INFO
        )
        LayoutHelper.pack_configure(info_card, side='right', fill='both', expand=True)

        # Info frame container
        info_frame = WidgetFactory.create_frame(info_card)
        LayoutHelper.pack_configure(info_frame, fill='both', expand=True)

        # Text widget with scrollbar
        info_text_widget, info_scrollbar = WidgetFactory.create_text_widget(
            info_frame, "info", height=20
        )
        info_text_widget.config(font=('Segoe UI', 10))
        LayoutHelper.pack_configure(info_text_widget, side='left', fill='both', expand=True)
        LayoutHelper.pack_configure(info_scrollbar, side='right', fill='y')

        # Insert content
        info_text_widget.config(state='normal')
        info_text_widget.insert('1.0', config.param_info.CONTENT)
        info_text_widget.config(state='disabled')

    def reset_to_defaults(self):
        try:
            # Clear and set default values
            self.n_entry.delete(0, 'end')
            self.n_entry.insert(0, str(config.bgv.N))

            self.lambda_var.set(str(config.bgv.LAMBDA_SECURITY))

            self.plaintext_entry.delete(0, 'end')
            self.plaintext_entry.insert(0, str(config.bgv.PLAINTEXT_MODULUS))

            self.base_entry.delete(0, 'end')
            self.base_entry.insert(0, str(config.bgv.BASE))

            # Reset coefficient modulus display
            self.coef_display_label.config(text=config.ui_texts.PARAM_Q_AUTO)

            # Reset status if keys were generated
            if self.main_app.sk is not None:
                self.key_status_update('normal', "Моля, генерирайте нови ключове.")
            
            # Log the reset
            self.log_reset_action()

            # Show success message
            DialogFactory.show_info("Успех", 
                f"Параметрите са възстановени към стандартните стойности:\n\n"
                f"• Степен на полинома (n): {config.bgv.N}\n"
                f"• Параметър за сигурност (λ): {config.bgv.LAMBDA_SECURITY}\n"
                f"• Модул на открития текст (t): {config.bgv.PLAINTEXT_MODULUS}\n"
                f"• База за релинеаризация: {config.bgv.BASE}\n\n"
                f"Моля, генерирайте нови ключове, за да приложите промените.")

        except Exception as e:
            DialogFactory.show_error("Грешка", "Грешка при възстановяване на стандартните стойности", str(e))

    def log_reset_action(self):
        # Log reset action
        
        if not hasattr(self.main_app, 'operations_tab') or not hasattr(self.main_app.operations_tab, 'results_text'):
            return
            
        results_text = self.main_app.operations_tab.results_text

        # Use direct logging
        from gui.ui_components import log_to_results
        
        log_to_results(results_text, "Параметри възстановени към стандартни стойности:")
        log_to_results(results_text, f"   n = {config.bgv.N}.")
        log_to_results(results_text, f"   λ = {config.bgv.LAMBDA_SECURITY}.")
        log_to_results(results_text, f"   t = {config.bgv.PLAINTEXT_MODULUS}.")
        log_to_results(results_text, f"   База на релинеаризация = {config.bgv.BASE}.")
        log_to_results(results_text, "   Моля, генерирайте нови ключове!")
        log_to_results(results_text, "")

    def show_help(self, parameter_name):
        # Show help
        
        help_texts = {
            'n': config.help.HELP_N,
            'lambda': config.help.HELP_LAMBDA,
            't': config.help.HELP_T,
            'base': config.help.HELP_BASE
        }
        
        help_text = help_texts.get(parameter_name, "Няма помощна информация.")
        DialogFactory.show_info(f"Помощ за {parameter_name}", help_text)

    def generate_keys_with_integrated_logic(self):
        # Generate keys
        
        try:
            # Get parameters
            self.main_app.n = int(self.n_entry.get())
            self.main_app.lambda_security = int(self.lambda_var.get())
            self.main_app.plaintext_modulus = int(self.plaintext_entry.get())
            self.main_app.base = int(self.base_entry.get())

            # Calculate coefficient modulus
            coef_bits = config.get_suggested_coef_bits(
                self.main_app.lambda_security, self.main_app.n
            )
            
            # Update display
            self.coef_display_label.config(
                text=f"≈ 2^{coef_bits} (от λ={self.main_app.lambda_security})"
            )

            # Validate parameters
            errors = validate_bgv_parameters(
                self.main_app.n, self.main_app.lambda_security,
                self.main_app.plaintext_modulus, self.main_app.base
            )
            
            if errors:
                error_msg = "\n".join(f"• {error}" for error in errors)
                DialogFactory.show_error("Невалидни параметри",
                                       "Моля, поправете следните грешки:", error_msg)
                self.key_status_update('error', config.ui_texts.STATUS_INVALID_PARAMS)
                return

            # Generate compatible moduls
            (self.main_app.coef_modulus, 
             self.main_app.small_modulus, 
             self.main_app.delta) = generate_compatible_modulus(
                self.main_app.lambda_security, self.main_app.plaintext_modulus
            )

            # Check compatibility
            compatibility_errors = verify_modulus_compatibility(
                self.main_app.coef_modulus, self.main_app.small_modulus, self.main_app.plaintext_modulus
            )
            if compatibility_errors:
                error_msg = "\n".join(f"• {error}" for error in compatibility_errors)
                DialogFactory.show_error("Incompatible Modulus",
                                       "Modulus compatibility issues:", error_msg)
                self.key_status_update('error', config.ui_texts.STATUS_COMPATIBILITY_ERROR)
                return

            # Initialize poly_modulus and generate keys
            self.main_app.poly_modulus = init_poly_modulus(self.main_app.n)

            # Generate keys
            self.main_app.sk = gen_secret_key(self.main_app.coef_modulus, self.main_app.poly_modulus)
            self.main_app.pk0, self.main_app.pk1 = gen_public_key(
                self.main_app.sk, self.main_app.coef_modulus,
                self.main_app.poly_modulus, self.main_app.plaintext_modulus
            )

            # Create operation handler
            self.main_app.operation_handler = OperationHandler(
                self.main_app.sk, self.main_app.coef_modulus, self.main_app.small_modulus,
                self.main_app.poly_modulus, self.main_app.plaintext_modulus, self.main_app.base
            )

            # Update status
            self.key_status_update('success', config.ui_texts.STATUS_KEYS_SUCCESS)

            # Reset application state
            self.main_app.reset_application_state()

            # Update UI in operations tab
            if hasattr(self.main_app, 'operations_tab'):
                self.main_app.operations_tab.update_crypto_instruction_label()

            # Log success
            self.log_key_generation_success()

            success_msg = f"Ключовете са генерирани успешно!"
            
            DialogFactory.show_info("Успех", success_msg)

        except Exception as e:
            self.key_status_update('error', config.ui_texts.STATUS_GENERATION_ERROR)
            DialogFactory.show_error("Грешка", "Грешка при генериране на ключове", str(e))

    def log_key_generation_success(self):
        # Log successful key generation with details
        
        if not hasattr(self.main_app, 'operations_tab') or not hasattr(self.main_app.operations_tab, 'results_text'):
            return
            
        results_text = self.main_app.operations_tab.results_text

        # Use direct logging
        from gui.ui_components import log_to_results
        
        log_to_results(results_text, "Ключовете са генерирани със следните параметри:")
        log_to_results(results_text, f"   Параметър за сигурност (λ): {self.main_app.lambda_security} бита")
        log_to_results(results_text, f"   Степен на полинома (n): {self.main_app.n}")
        log_to_results(results_text, f"   Модул на явното съобщение (t): {self.main_app.plaintext_modulus} → [0, {self.main_app.plaintext_modulus - 1}]")
        log_to_results(results_text, f"   Параметър за сигурност (δ): {self.main_app.delta}")
        log_to_results(results_text, f"   База за релинеаризация: {self.main_app.base}")
        log_to_results(results_text, "")