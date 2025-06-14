import random
import tkinter as tk

import numpy as np

from core.bgv import decrypt, encrypt
from config.config import config
from crypto.operation_handler import calculate_expected_result_for_name
from config.parameter_validator import (validate_input_values,
                                 validate_operation_inputs)
from core.polynomial import QuotientRingPoly
from gui.styles import Icons, Messages
from gui.widget_factory import (DialogFactory, LayoutHelper, WidgetFactory,
                            create_button_row)


class OperationsTab:
    # Homomorphic operations tab UI

    def __init__(self, parent_notebook, main_app):
        self.main_app = main_app
        self.parent_notebook = parent_notebook
        
        # UI components
        self.next_crypto_label = None
        self.crypto_values_entry = None
        self.crypto_instruction_label = None
        self.encrypted_listbox = None
        self.left_operand_combo = None
        self.left_operand_var = None
        self.operation_var = None
        self.right_operand_combo = None
        self.right_operand_var = None
        self.history_tree = None
        self.results_text = None
        
        # Tab settings
        self.setup_operations_tab()

    def setup_operations_tab(self):
        # Setup operations tab

        ops_frame = WidgetFactory.create_frame(self.parent_notebook)
        self.parent_notebook.add(ops_frame, text=config.ui_texts.OPERATIONS_TAB_TITLE)

        # Main container
        main_container = WidgetFactory.create_frame(ops_frame)
        LayoutHelper.pack_configure(main_container, fill='both', expand=True, 
                                   padx=20, pady=20)

        # TOP ROW - Two equal sections side by side
        top_row = WidgetFactory.create_frame(main_container)
        LayoutHelper.pack_configure(top_row, fill='x', pady=(0, 15))

        # LEFT: Encryption section
        self.setup_encryption_section(top_row)

        # RIGHT: Existing cryptograms section  
        self.setup_existing_cryptograms_section(top_row)

        # MIDDLE ROW - Operations and Results side by side
        middle_row = WidgetFactory.create_frame(main_container)
        LayoutHelper.pack_configure(middle_row, fill='both', expand=True)

        # LEFT: Operations section
        self.setup_sequential_operations_section(middle_row)

        # RIGHT: Results section  
        self.setup_results_section(middle_row)

    def setup_encryption_section(self, parent):
        # Setup LEFT section - Encryption
        
        # Create card
        encrypt_card = WidgetFactory.create_labelframe(
            parent, config.ui_texts.SECTION_CREATE_CRYPTO
        )
        LayoutHelper.pack_configure(encrypt_card, side='left', fill='both', 
                                   expand=True, padx=(0, 10))

        # Next cryptogram name display
        self.setup_next_crypto_display(encrypt_card)
        
        # Values input section
        self.setup_values_input(encrypt_card)
        
        # Action buttons
        self.setup_encryption_buttons(encrypt_card)

    def setup_next_crypto_display(self, parent):
        # Setup next cryptogram name display
        name_frame = WidgetFactory.create_frame(parent)
        LayoutHelper.pack_configure(name_frame, fill='x', pady=(0, 10))

        name_label = WidgetFactory.create_label(
            name_frame, config.ui_texts.CURR_CRYPTOGRAM, "subheading"
        )
        LayoutHelper.pack_configure(name_label, side='left')

        self.next_crypto_label = WidgetFactory.create_label(
            name_frame, "A", "accent"
        )
        self.next_crypto_label.config(font=('Segoe UI', 12, 'bold'))
        LayoutHelper.pack_configure(self.next_crypto_label, side='left', padx=(10, 0))

    def setup_values_input(self, parent):
        # Setup values input section

        values_label = WidgetFactory.create_label(
            parent, config.ui_texts.VALUES_INPUT, "subheading"
        )
        LayoutHelper.pack_configure(values_label, anchor='w', pady=(10, 5))

        # Entry field
        self.crypto_values_entry = WidgetFactory.create_entry(parent, "values")
        LayoutHelper.pack_configure(self.crypto_values_entry, fill='x', pady=(0, 5))
        
        # Instructions
        instruction_text = config.get_instruction_text()
        self.crypto_instruction_label = WidgetFactory.create_label(
            parent, instruction_text, "muted"
        )
        LayoutHelper.pack_configure(self.crypto_instruction_label, anchor='w', pady=(0, 15))

    def setup_encryption_buttons(self, parent):
        # Setup encryption action buttons
        
        # Encrypt button
        encrypt_button = WidgetFactory.create_button(
            parent, config.ui_texts.BTN_ENCRYPT.replace('🔒 ', ''),
            self.encrypt_custom_values, "secondary", Icons.ENCRYPT
        )
        LayoutHelper.pack_configure(encrypt_button, pady=(0, 10))

        # Random button
        random_button = WidgetFactory.create_button(
            parent, config.ui_texts.BTN_RANDOM.replace('🎲 ', ''),
            self.generate_random_values, "secondary", Icons.RANDOM
        )
        LayoutHelper.pack_configure(random_button)

    def setup_existing_cryptograms_section(self, parent):
        # Setup RIGHT section
        
        # Create card
        existing_card = WidgetFactory.create_labelframe(
            parent, config.ui_texts.SECTION_EXISTING_CRYPTO
        )
        LayoutHelper.pack_configure(existing_card, side='right', fill='both', expand=True)

        # Listbox
        self.encrypted_listbox = WidgetFactory.create_listbox(existing_card)[0]
        LayoutHelper.pack_configure(self.encrypted_listbox, fill='both', expand=True, pady=(0, 10))      

        # Buttons
        self.setup_cryptogram_buttons(existing_card)

    def setup_cryptogram_buttons(self, parent):
        # Setup cryptogram management buttons 
        
        buttons_config = [
            {
                'text': config.ui_texts.BTN_VIEW.replace('👁️ ', ''),
                'command': self.view_cryptogram_details,
                'style_type': 'secondary', 
                'icon': Icons.VIEW,
                'side': 'left',
                'padx': 5
            },
            {
                'text': config.ui_texts.BTN_CLEAR_ALL.replace('🗑️ ', ''),
                'command': self.clear_all_encrypted,
                'style_type': 'secondary',
                'icon': Icons.DELETE,
                'side': 'left',
                'padx': 5
            },
            {
                'text': config.ui_texts.BTN_DECRYPT.replace('🔓 ', ''),
                'command': self.decrypt_selected_from_list,
                'style_type': 'secondary',
                'icon': Icons.DECRYPT,
                'side': 'right'
            }
        ]
        
        buttons_frame, buttons = create_button_row(parent, buttons_config)
        LayoutHelper.pack_configure(buttons_frame, fill='x')

    def setup_sequential_operations_section(self, parent):
        # Setup LEFT section - Sequential operations
        
        # Main operations card
        ops_card = WidgetFactory.create_labelframe(
            parent, config.ui_texts.SECTION_OPERATIONS
        )
        LayoutHelper.pack_configure(ops_card, side='left', fill='both', 
                                   expand=True, padx=(0, 10))

        # Container for side-by-side layout
        ops_container = WidgetFactory.create_frame(ops_card)
        LayoutHelper.pack_configure(ops_container, fill='both', expand=True)

        # LEFT SIDE: Operation controls
        self.setup_operation_controls(ops_container)

        # RIGHT SIDE: Operation history
        self.setup_operation_history(ops_container)

    def setup_operation_controls(self, parent):
        # Setup operation controls
        
        # Controls frame with fixed width
        controls_frame = WidgetFactory.create_labelframe(
            parent, config.ui_texts.SECTION_OPERATION_SETTINGS
        )
        LayoutHelper.pack_configure(controls_frame, side='left', fill='y', padx=(0, 10))
        controls_frame.configure(width=250)
        controls_frame.pack_propagate(False)

        # Left operand
        left_label = WidgetFactory.create_label(
            controls_frame, config.ui_texts.OP_LEFT_OPERAND, "subheading"
        )
        LayoutHelper.pack_configure(left_label, anchor='w', pady=(0, 5))
        
        self.left_operand_combo, self.left_operand_var = WidgetFactory.create_combo(
            controls_frame, size="large"
        )
        LayoutHelper.pack_configure(self.left_operand_combo, fill='x', pady=(0, 15))

        # Operation selection
        operation_label = WidgetFactory.create_label(
            controls_frame, config.ui_texts.OP_OPERATION, "subheading"
        )
        LayoutHelper.pack_configure(operation_label, anchor='w', pady=(0, 5))

        # Radio buttons
        self.operation_var = tk.StringVar(value="+")  # Default is addition
        
        addition_radio = tk.Radiobutton(
            controls_frame, 
            text=config.ui_texts.OP_ADD, 
            variable=self.operation_var, 
            value="+",
            bg='#f0f0f0',
            selectcolor='#f0f0f0',
            activebackground='#f0f0f0',
            font=('Segoe UI', 9)
        )
        LayoutHelper.pack_configure(addition_radio, anchor='w', pady=2)

        multiplication_radio = tk.Radiobutton(
            controls_frame, 
            text=config.ui_texts.OP_MULTIPLY, 
            variable=self.operation_var, 
            value="*",
            bg='#f0f0f0',
            selectcolor='#f0f0f0',
            activebackground='#f0f0f0',
            font=('Segoe UI', 9)
        )
        LayoutHelper.pack_configure(multiplication_radio, anchor='w', pady=(2, 15))

        # Right operand
        right_label = WidgetFactory.create_label(
            controls_frame, config.ui_texts.OP_RIGHT_OPERAND, "subheading"
        )
        LayoutHelper.pack_configure(right_label, anchor='w', pady=(0, 5))
        
        self.right_operand_combo, self.right_operand_var = WidgetFactory.create_combo(
            controls_frame, size="large"
        )
        LayoutHelper.pack_configure(self.right_operand_combo, fill='x', pady=(0, 20))

        # Execute button
        execute_button = WidgetFactory.create_button(
            controls_frame, config.ui_texts.BTN_CALCULATE.replace('🧮 ', ''),
            self.execute_sequential_operation, "primary", Icons.CALCULATE
        )
        LayoutHelper.pack_configure(execute_button, fill='x')

    def setup_operation_history(self, parent):
        # Setup operation history
        
        # History frame
        history_frame = WidgetFactory.create_labelframe(
            parent, config.ui_texts.SECTION_OPERATION_HISTORY
        )
        LayoutHelper.pack_configure(history_frame, side='right', fill='both', expand=True)

        # History treeview container
        tree_container = WidgetFactory.create_frame(history_frame)
        LayoutHelper.pack_configure(tree_container, fill='both', expand=True, pady=(0, 10))

        # History treeview with scrollbar
        history_columns = ('step', 'operation', 'result', 'status')
        self.history_tree, history_scrollbar = WidgetFactory.create_treeview(
            tree_container, columns=history_columns
        )
        
        # Configure column headings
        self.history_tree.heading('step', text='#')
        self.history_tree.heading('operation', text='Операция')
        self.history_tree.heading('result', text='Резултат')
        self.history_tree.heading('status', text='Статус')
        
        # Configure column widths
        self.history_tree.column('step', width=40)
        self.history_tree.column('operation', width=200)
        self.history_tree.column('result', width=100)
        self.history_tree.column('status', width=150)
        
        LayoutHelper.pack_configure(self.history_tree, side='left', fill='both', expand=True)
        LayoutHelper.pack_configure(history_scrollbar, side='right', fill='y')
        

    def setup_results_section(self, parent):
        # Setup results section
        
        # Results card
        results_card = WidgetFactory.create_labelframe(
            parent, config.ui_texts.SECTION_RESULTS
        )
        LayoutHelper.pack_configure(results_card, side='right', fill='both', expand=True)

        # Results text widget
        self.results_text = WidgetFactory.create_text_widget(results_card, "results")

        self.results_text.config(
            font=('Segoe UI', 10),
            wrap='word'
        )
        LayoutHelper.pack_configure(self.results_text, fill='both', expand=True)

        # Show welcome message
        self.show_welcome_message()

    def show_welcome_message(self):
        # Show welcome message

        from gui.ui_components import log_to_results
        log_to_results(self.results_text, config.welcome.CONTENT)

    # Encryption methods
    def update_next_crypto_label(self):
        # Update the label showing next cryptogram name
        if hasattr(self, 'next_crypto_label'):
            if self.main_app.next_crypto_letter <= ord('Z'):
                self.next_crypto_label.config(text=chr(self.main_app.next_crypto_letter))
            else:
                self.next_crypto_label.config(text="MAX")

    def update_crypto_instruction_label(self):
        # Update instructions
        if hasattr(self, 'crypto_instruction_label'):
            instruction_text = config.get_instruction_text(
                self.main_app.n, self.main_app.plaintext_modulus
            )
            self.crypto_instruction_label.config(text=instruction_text)

    def encrypt_custom_values(self):
        # Encrypt custom values
        if not self.main_app.sk:
            DialogFactory.show_warning(Messages.NO_KEYS)
            return

        try:
            # Check cryptogram limit
            if self.main_app.next_crypto_letter > ord('Z'):
                DialogFactory.show_warning(Messages.MAX_CRYPTOGRAMS)
                return

            name = chr(self.main_app.next_crypto_letter)
            input_str = self.crypto_values_entry.get().strip()
            
            if not input_str:
                DialogFactory.show_warning("Въведете стойности за криптиране")
                return

            # Validate and parse input
            parsed_values, errors = validate_input_values(
                input_str, self.main_app.n, self.main_app.plaintext_modulus
            )
            
            if errors:
                error_msg = "\n".join(f"• {error}" for error in errors)
                DialogFactory.show_error(Messages.INVALID_INPUT,
                                       "Намерени са следните грешки:", error_msg)
                return

            # Create polynomial and encrypt
            poly = QuotientRingPoly(parsed_values, self.main_app.coef_modulus, 
                                   self.main_app.poly_modulus)
            c0, c1 = encrypt(poly, self.main_app.pk0, self.main_app.pk1, 
                           self.main_app.coef_modulus, self.main_app.poly_modulus, 
                           self.main_app.plaintext_modulus)

            # Store cryptogram and original values
            self.main_app.encrypted_values[name] = (c0, c1)
            self.main_app.original_values[name] = parsed_values.copy()

            from gui.ui_components import log_to_results
            log_to_results(self.results_text, f"Криптограма „{name}“ създадена: {parsed_values}")

            # Update counters and UI
            self.main_app.next_crypto_letter += 1
            self.update_next_crypto_label()
            self.update_all_combos()
            self.update_encrypted_list()

            # Clear values field
            self.crypto_values_entry.delete(0, tk.END)

        except Exception as e:
            DialogFactory.show_error("Грешка", "Грешка при криптиране", str(e))

    def generate_random_values(self):
        # Generate random values
        if not hasattr(self.main_app, 'n') or not hasattr(self.main_app, 'plaintext_modulus'):
            DialogFactory.show_warning(Messages.NO_KEYS)
            return

        try:
            # Generate random values
            random_values = [random.randint(0, self.main_app.plaintext_modulus - 1) 
                           for _ in range(self.main_app.n)]
            random_string = ','.join(map(str, random_values))

            # Update entry
            self.crypto_values_entry.delete(0, tk.END)
            self.crypto_values_entry.insert(0, random_string)

            # Success message
            success_msg = f"Генерирани {self.main_app.n} случайни стойности в диапазона [0, {self.main_app.plaintext_modulus - 1}]."
            DialogFactory.show_info("Случайни стойности", success_msg)

        except Exception as e:
            DialogFactory.show_error("Грешка", "Грешка при генериране на случайни стойности", str(e))

    def execute_sequential_operation(self):
        # Execute operation using enhanced system
        if not self.main_app.sk or not self.main_app.operation_handler:
            DialogFactory.show_warning(Messages.NO_KEYS)
            return

        try:
            left_operand = self.left_operand_var.get()
            operation = self.operation_var.get()
            right_operand = self.right_operand_var.get()

            # Validate operation inputs
            validation_errors = validate_operation_inputs(
                left_operand, right_operand, operation, self.main_app.encrypted_values
            )
            if validation_errors:
                error_msg = "\n".join(f"• {error}" for error in validation_errors)
                DialogFactory.show_error(Messages.INVALID_INPUT,
                                       "Намерени са следните грешки:", error_msg)
                return

            # Check if operation is feasible
            can_perform, warnings, depth_info = self.main_app.operation_handler.check_operation_feasibility(
                left_operand, right_operand, operation, self.main_app.encrypted_values,
                self.main_app.operation_history, self.main_app.original_values,
                lambda msg: self.log_to_console(msg)
            )

            if not can_perform:
                DialogFactory.show_warning(Messages.OPERATION_BLOCKED + "\nПроверете конзолата за детайли.")
                return

            # Show warnings if any
            if warnings:
                for warning in warnings:
                    if warning['type'] == 'high_noise':
                        self.log_to_console(Messages.HIGH_NOISE)
                        self.log_to_console(f"   Дължина на шума в {warning['operand']}: {warning['noise_length']} числа")

            # Apply automatic modulus switching if needed
            for operand in [left_operand, right_operand]:
                c0, c1 = self.main_app.encrypted_values[operand]
                self.main_app.operation_handler.check_and_apply_auto_switching(
                    operand, c0, c1, self.main_app.encrypted_values,
                    lambda msg: self.log_to_console(msg)
                )

            # Generate result name and perform operation
            result_name = f"R{self.main_app.result_counter}"

            c0_result, c1_result, success, operation_info = self.main_app.operation_handler.perform_operation(
                left_operand, operation, right_operand, self.main_app.encrypted_values,
                lambda msg: self.log_to_console(msg)
            )

            if success:
                # Store result
                self.main_app.encrypted_values[result_name] = (c0_result, c1_result)

                # Check and apply modulus switching on result
                self.main_app.operation_handler.check_and_apply_auto_switching(
                    result_name, c0_result, c1_result, self.main_app.encrypted_values,
                    lambda msg: self.log_to_console(msg)
                )

                # Add to history
                status = 'Успешно'

                self.main_app.operation_history.append({
                    'step': len(self.main_app.operation_history) + 1,
                    'operation': f"{left_operand} {operation_info['op_symbol']} {right_operand}",
                    'result': result_name,
                    'left_op': left_operand,
                    'right_op': right_operand,
                    'op_type': operation,
                    'status': status,
                    'depth': depth_info['new_depth']
                })

                self.main_app.result_counter += 1

                # Update UI
                self.update_all_combos()
                self.update_encrypted_list()
                self.update_operation_history_tree()

                self.left_operand_var.set("")
                self.right_operand_var.set("")
                self.operation_var.set("+")

                # Log result
                operation_msg = f"Извършена е операция: {left_operand} {operation} {right_operand} → {result_name}"
                if depth_info['new_depth'] > 0:
                    operation_msg += f" (дълбочина: {depth_info['new_depth']})"
                    
                self.log_to_console(operation_msg)
            else:
                # Operation failed
                error_msg = operation_info.get('error', 'Неизвестна грешка')
                self.log_to_console(f"Операцията се провали: {error_msg}")
                visual_oper = "➕" if operation == "+" else "✖️" if operation == "*" else operation
                # Add failed operation to history
                self.main_app.operation_history.append({
                    'step': len(self.main_app.operation_history) + 1,
                    'operation': f"{left_operand} {visual_oper} {right_operand}",
                    'result': result_name,
                    'status': 'Неуспешно',
                    'depth': 0
                })

                self.update_operation_history_tree()

        except Exception as e:
            self.log_to_console(f"Глобална грешка при операцията: {str(e)}")
            DialogFactory.show_error("Грешка", "Грешка при операцията", str(e))

    def log_to_console(self, message):
        from gui.ui_components import log_to_results
        log_to_results(self.results_text, message)

    # UI update methods
    def update_all_combos(self):
        # Update all combo boxes with available encrypted values
        
        values = list(self.main_app.encrypted_values.keys())
        self.left_operand_combo['values'] = values
        self.right_operand_combo['values'] = values

    def update_encrypted_list(self):
        # Update the encrypted values listbox
        
        if hasattr(self, 'encrypted_listbox'):
            self.encrypted_listbox.delete(0, tk.END)
            for name in sorted(self.main_app.encrypted_values.keys()):
                self.encrypted_listbox.insert(tk.END, f"{Icons.CRYPTOGRAM} {name}")

    def update_operation_history_tree(self):
        # Update the operation history tree
        
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add history items
        for hist in self.main_app.operation_history:
            self.history_tree.insert('', 'end', values=(
                hist.get('step', ''),
                hist.get('operation', ''),
                hist.get('result', ''),
                hist.get('status', '')
            ))

    def clear_operation_history(self):
        # Clear operation history
        self.main_app.operation_history = []
        self.main_app.result_counter = 1
        self.update_operation_history_tree()

    def clear_all_encrypted(self):
        if DialogFactory.ask_yes_no(Messages.CONFIRM_CLEAR):
            self.main_app.reset_application_state()
            self.log_to_console("Всички криптирани стойности са изчистени")

    # Decryption and viewing methods
    def view_cryptogram_details(self):
        # View cryptogram details
        selection = self.encrypted_listbox.curselection()
        if not selection:
            DialogFactory.show_warning("Изберете криптограма за преглед")
            return

        selected_text = self.encrypted_listbox.get(selection[0])
        selected_name = selected_text.replace(f"{Icons.CRYPTOGRAM} ", "")

        # Use existing detailed view
        from gui.ui_components import show_cryptogram_details
        show_cryptogram_details(
            self.main_app.root, selected_name, self.main_app.encrypted_values, 
            self.main_app.original_values, self.main_app.sk, self.main_app.plaintext_modulus, 
            self.main_app.operation_history, self.main_app.coef_modulus, self.main_app.poly_modulus
        )

    def decrypt_selected_from_list(self):
        # Decrypt selected value using enhanced logging
        if not self.main_app.sk:
            DialogFactory.show_warning(Messages.NO_KEYS)
            return

        selection = self.encrypted_listbox.curselection()
        if not selection:
            DialogFactory.show_warning("Изберете стойност за декриптиране")
            return

        try:
            selected_text = self.encrypted_listbox.get(selection[0])
            selected_name = selected_text.replace(f"{Icons.CRYPTOGRAM} ", "")

            if selected_name not in self.main_app.encrypted_values:
                DialogFactory.show_warning("Избраната стойност не съществува")
                return

            c0, c1 = self.main_app.encrypted_values[selected_name]

            # Use appropriate secret key for decryption
            current_modulus = c0.coef_modulus
            if current_modulus != self.main_app.coef_modulus:
                decrypt_sk = self.main_app.sk.copy()
                decrypt_sk.coef_modulus = current_modulus
            else:
                decrypt_sk = self.main_app.sk

            # Decrypt
            decrypted_poly, noise = decrypt(c0, c1, decrypt_sk, 
                                          self.main_app.plaintext_modulus, return_noise=True)
            decrypted_values = decrypted_poly.coef.astype(int)

            # Check noise info
            from crypto.noise_management import check_noise_level
            noise_info = check_noise_level(c0, c1, self.main_app.sk, self.main_app.plaintext_modulus)

            # Calculate expected result
            expected_result = calculate_expected_result_for_name(
                selected_name, self.main_app.operation_history, self.main_app.original_values,
                self.main_app.plaintext_modulus, self.main_app.poly_modulus, self.main_app.coef_modulus
            )

            # Check correctness
            if expected_result is not None:
                is_correct = np.array_equal(expected_result, decrypted_values)
                correctness_msg = f"{Icons.SUCCESS} ПРАВИЛЕН" if is_correct else f"{Icons.ERROR} ГРЕШЕН"
            else:
                correctness_msg = f"{Icons.INFO} Неизвестен"

            # Log detailed result
            self.log_to_console("=" * 45)
            self.log_to_console(f"ДЕКРИПТИРАНЕ НА: {selected_name}")
            self.log_to_console(f"Декриптиран резултат: {decrypted_values}")
            
            if expected_result is not None:
                self.log_to_console(f"Очакван резултат:    {expected_result}")
                
            self.log_to_console(f"Ниво на шума: {noise}")
            self.log_to_console(f"Дължина на шума: {noise_info['noise_length']} числа")
            self.log_to_console(f"Макс позволен шум: {noise_info['max_noise']}")
            self.log_to_console(f"Макс дължина: {noise_info['max_length']} числа")
            self.log_to_console(f"Резултатът е {correctness_msg}!")

            # Show explanation if incorrect
            if expected_result is not None and not is_correct:
                self.log_to_console("")
                self.log_to_console("ЗАЩО РЕЗУЛТАТЪТ Е ГРЕШЕН:")
                self.log_to_console("   • Шумът в криптограмата е станал твърде висок/дълъг")
                self.log_to_console("   • При декриптиране шумът 'замърсява' правилния резултат")
                self.log_to_console("   • Floating-point грешките се натрупват при много операции")
                self.log_to_console("   • BGV схемата има ограничения за дълбочината на операциите")
                self.log_to_console("")
                self.log_to_console("РЕШЕНИЯ:")
                self.log_to_console("   • Използвайте по-малко последователни умножения")
                self.log_to_console("   • Увеличете параметрите в конфигурацията (λ, n)")
                self.log_to_console("   • Рестартирайте с нови криптограми")
                self.log_to_console("   • Разделете сложните операции на по-малки стъпки")

            self.log_to_console("=" * 45)
            self.log_to_console("")

        except Exception as e:
            DialogFactory.show_error("Грешка", "Грешка при декриптиране", str(e))