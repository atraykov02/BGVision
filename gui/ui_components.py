import tkinter as tk
from tkinter import ttk

import numpy as np

from core.bgv import decrypt
from crypto.noise_management import check_noise_level
from crypto.operation_handler import calculate_expected_result_for_name


def center_window(window, width, height):
    # Center a window on the screen
    
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


def bind_mousewheel(widget, canvas):
    # Bind mousewheel events to canvas for scrolling
    
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
    
    widget.bind('<Enter>', _bind_to_mousewheel)
    widget.bind('<Leave>', _unbind_from_mousewheel)


def show_cryptogram_details(parent, cryptogram_name, encrypted_values, original_values, 
                           sk, plaintext_modulus, operation_history=None, coef_modulus=None,
                           poly_modulus=None):
    # Show detailed cryptogram information in a scrollable popup window
    details_window = tk.Toplevel(parent)
    details_window.title(f"Преглед на криптограма: {cryptogram_name}")
    details_window.geometry("700x550")
    details_window.configure(bg='#f0f0f0')
    
    # Create scrollable canvas
    canvas = tk.Canvas(details_window, bg='#f0f0f0', highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
    
    def scrollbar_command(*args):
        if len(args) >= 2:
            action = args[0]
            if action == "moveto":
                pos = max(0.0, float(args[1]))
                canvas.yview("moveto", pos)
                return
            elif action == "scroll":
                try:
                    current_view = canvas.yview()
                    current_top = current_view[0]
                    
                    if current_top <= 0 and float(args[1]) < 0:
                        return
                    
                    if current_view[1] >= 1.0 and float(args[1]) > 0:
                        return
                        
                except:
                    pass
        
        canvas.yview(*args)
    
    # Vertical scrollbar
    scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=scrollbar_command)
    scrollbar.pack(side="right", fill="y", pady=20, padx=(0, 20))
    
    # Update the scrollbar
    def update_scrollbar(*args):
        scrollbar.set(*args)
    
    canvas.configure(yscrollcommand=update_scrollbar)
    
    # Frame inside canvas for content
    main_frame = tk.Frame(canvas, bg='#f0f0f0')
    canvas_window = canvas.create_window((0, 0), window=main_frame, anchor='nw')
    
    # Auto-resize main_frame with canvas
    def configure_main_frame(event):
        canvas.itemconfig(canvas_window, width=event.width - 40)  # Account for padding
    
    canvas.bind("<Configure>", configure_main_frame)
    
    # Title
    title_label = tk.Label(main_frame, text=f"🔐 Криптограма: {cryptogram_name}",
                          font=('Segoe UI', 16, 'bold'), bg='#f0f0f0')
    title_label.pack(pady=(0, 20))
    
    # Show original values if available
    if cryptogram_name in original_values:
        original_vals = original_values[cryptogram_name]
        
        values_label = tk.Label(main_frame, text="Елементи на криптограмата:",
                               font=('Segoe UI', 12, 'bold'), bg='#f0f0f0')
        values_label.pack(pady=(0, 10))
        
        # Create grid display for values
        grid_frame = tk.Frame(main_frame, bg='#f0f0f0')
        grid_frame.pack(pady=10)
        
        # Display values in a grid (8 per row)
        cols = 8
        for i, val in enumerate(original_vals):
            row = i // cols
            col = i % cols
            value_label = tk.Label(grid_frame, text=f"{val}",
                                  font=('Courier', 12, 'bold'),
                                  relief='solid', 
                                  bg='#e3f2fd',
                                  padx=8, pady=8)
            value_label.grid(row=row, column=col, padx=2, pady=2)
    
    else:
        # If no original values, show that it's a computed result
        result_label = tk.Label(main_frame, text="Тази криптограма е резултат от операция.",
                               font=('Segoe UI', 12), bg='#f0f0f0')
        result_label.pack(pady=(20, 10))
        
        # Show operation history if available
        if operation_history:
            for hist in operation_history:
                if (hist.get('result') == cryptogram_name and 'Успешно' in hist.get('status', '')):
                    op_text = f"Операция: {hist.get('operation', 'Неизвестна')}"
                    
                    operation_label = tk.Label(main_frame, text=op_text,
                                              font=('Segoe UI', 12, 'bold'),
                                              bg='#f0f0f0',
                                              wraplength=600)
                    operation_label.pack(pady=5)
                    break
    
    # Decrypt button and result area
    decrypt_button = ttk.Button(main_frame, text="🔓 Декриптирай",
                               command=lambda: decrypt_and_show_in_details(
                                   cryptogram_name, encrypted_values, sk, plaintext_modulus,
                                   result_frame, operation_history, original_values,
                                   coef_modulus, poly_modulus
                               ))
    decrypt_button.pack(pady=10)
    
    # Frame for decrypt results
    result_frame = tk.Frame(main_frame, bg='#f0f0f0')
    result_frame.pack(fill='both', expand=True, pady=10)
    
    # Close button
    ttk.Button(main_frame, text="Затвори", 
               command=details_window.destroy).pack(pady=(20, 0))
    
    # Update scroll region when content changes
    def configure_scroll_region(event=None):
        canvas.update_idletasks()
        bbox = canvas.bbox("all")
        if bbox:
            canvas.configure(scrollregion=bbox)
    
    main_frame.bind("<Configure>", configure_scroll_region)
    
    def safe_mousewheel(event):
        # Checks if scrolling is needed before allowing the operation
        bbox = canvas.bbox("all")
        if not bbox:
            return "break"
        
        canvas_height = canvas.winfo_height()
        content_height = bbox[3] - bbox[1]
        
        if content_height <= canvas_height:
            return "break"
        
        try:
            current_view = canvas.yview()
            current_top = current_view[0]
        except:
            return "break"
        
        scroll_direction = -1 * (event.delta / 120)
        if scroll_direction < 0 and current_top <= 0:
            return "break"
        
        if scroll_direction > 0 and current_view[1] >= 1.0:
            return "break"
        
        canvas.yview_scroll(int(scroll_direction), "units")
        return "break"
    
    # Binding for mousewheel
    def bind_safe_mousewheel(widget):
        def on_enter(event):
            canvas.bind_all("<MouseWheel>", safe_mousewheel)
        
        def on_leave(event):
            canvas.unbind_all("<MouseWheel>")
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    # Apply mousewheel
    bind_safe_mousewheel(canvas)
    bind_safe_mousewheel(main_frame)
    
    original_yview = canvas.yview
    
    def safe_yview(*args):
        if len(args) == 0:
            return original_yview()
        
        if args[0] == 'moveto':
            pos = max(0.0, float(args[1]))
            return original_yview('moveto', pos)
        elif args[0] == 'scroll':
            try:
                current_view = original_yview()
                current_top = current_view[0]
                
                if current_top <= 0.001 and float(args[1]) < 0:
                    return original_yview()
                
                if current_view[1] >= 0.999 and float(args[1]) > 0:
                    return original_yview()
                    
            except:
                pass
            
            return original_yview(*args)
        else:
            return original_yview(*args)
    
    canvas.yview = safe_yview
    
    def initial_setup():
        # Update all
        details_window.update_idletasks()
        main_frame.update_idletasks()
        canvas.update_idletasks()
        
        bbox = canvas.bbox("all")
        if bbox:
            canvas.configure(scrollregion=bbox)
        
        canvas.yview('moveto', 0.0)
    
    details_window.after(1, initial_setup)


def decrypt_and_show_in_details(cryptogram_name, encrypted_values, sk, plaintext_modulus,
                               result_frame, operation_history=None, original_values=None,
                               coef_modulus=None, poly_modulus=None):
    # Decrypt and show results in the details window
    
    try:
        # Clear previous results
        for widget in result_frame.winfo_children():
            widget.destroy()
        
        if cryptogram_name not in encrypted_values:
            error_label = tk.Label(result_frame, text="Грешка: Криптограмата не съществува",
                                  font=('Segoe UI', 10), fg='red', bg='#f0f0f0')
            error_label.pack()
            return
        
        c0, c1 = encrypted_values[cryptogram_name]
        
        # Check current modulus and use appropriate secret key
        current_modulus = c0.coef_modulus
        
        if current_modulus != sk.coef_modulus:
            decrypt_sk = sk.copy()
            decrypt_sk.coef_modulus = current_modulus
        else:
            decrypt_sk = sk
        
        # Decrypt
        decrypted_poly, noise = decrypt(c0, c1, decrypt_sk, plaintext_modulus, return_noise=True)
        decrypted_values = decrypted_poly.coef.astype(int)
        
        # Show title
        title_label = tk.Label(result_frame, text="Декриптирани елементи:",
                              font=('Segoe UI', 12, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=(10, 10))
        
        # Create grid display for decrypted values
        grid_frame = tk.Frame(result_frame, bg='#f0f0f0')
        grid_frame.pack(pady=10)
        
        # Display values in a grid (8 per row)
        cols = 8
        for i, val in enumerate(decrypted_values):
            row = i // cols
            col = i % cols
            value_label = tk.Label(grid_frame, text=f"{val}",
                                  font=('Courier', 12, 'bold'),
                                  relief='solid',
                                  bg='#e8f5e8',
                                  padx=8, pady=8)
            value_label.grid(row=row, column=col, padx=2, pady=2)
        
        # Check for correctness
        try:
            if operation_history and original_values and coef_modulus and poly_modulus:
                expected_result = calculate_expected_result_for_name(
                    cryptogram_name, operation_history, original_values,
                    plaintext_modulus, poly_modulus, coef_modulus
                )
                
                if expected_result is not None:
                    try:
                        # Ensure both are numpy arrays with same shape
                        expected_array = np.array(expected_result, dtype=int)
                        decrypted_array = np.array(decrypted_values, dtype=int)
                        
                        # Safe comparison
                        is_correct = np.array_equal(expected_array, decrypted_array)
                        correctness_color = '#28a745' if is_correct else '#dc3545'
                        correctness_text = "✅ ПРАВИЛЕН" if is_correct else "❌ ГРЕШЕН"
                        
                        correctness_label = tk.Label(result_frame, 
                                                    text=f"Резултатът е {correctness_text}",
                                                    font=('Segoe UI', 11, 'bold'),
                                                    fg=correctness_color, bg='#f0f0f0')
                        correctness_label.pack(pady=(10, 5))
                    except Exception as comparison_error:      
                        print(f"Грешка при сравнение: {comparison_error}")
                        pass
        except Exception as correctness_error:
            pass
        
        # Show noise info
        try:
            noise_info = check_noise_level(c0, c1, sk, plaintext_modulus)
            
            noise_text = f"Ниво на шума: {noise} ({noise_info['noise_length']} цифри)"
            noise_label = tk.Label(result_frame, text=noise_text,
                                  font=('Segoe UI', 9), fg='gray', bg='#f0f0f0')
            noise_label.pack(pady=(15, 0))
        except Exception as noise_error:
            noise_digits = len(str(abs(int(noise))))
            noise_text = f"Ниво на шума: {noise} ({noise_digits} цифри)"
            noise_label = tk.Label(result_frame, text=noise_text,
                                  font=('Segoe UI', 9), fg='gray', bg='#f0f0f0')
            noise_label.pack(pady=(15, 0))
        
        # Update scroll region after adding a content
        def update_parent_scroll():
            parent = result_frame
            while parent and not isinstance(parent, tk.Canvas):
                parent = parent.master
            
            if isinstance(parent, tk.Canvas):
                parent.update_idletasks()
                bbox = parent.bbox("all")
                if bbox:
                    parent.configure(scrollregion=bbox)
        
        result_frame.after(10, update_parent_scroll)
        
    except Exception as e:
        error_label = tk.Label(result_frame, text=f"Грешка при декриптиране: {str(e)}",
                              font=('Segoe UI', 10), fg='red', bg='#f0f0f0')
        error_label.pack()


def update_operation_history_tree(tree, operation_history):
    # Update the operation history tree with new data
    
    # Clear existing items
    for item in tree.get_children():
        tree.delete(item)
    
    # Add history items
    for hist in operation_history:
        tree.insert('', 'end', values=(
            hist.get('step', ''),
            hist.get('operation', ''),
            hist.get('result', ''),
            hist.get('status', '')
        ))


def log_to_results(results_text, message):
    # Log message to results text widget
    results_text.insert(tk.END, message + "\n")
    results_text.see(tk.END)