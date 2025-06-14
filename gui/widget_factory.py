import tkinter as tk
from tkinter import scrolledtext, ttk

from gui.styles import ComponentConfig, Icons, LayoutConfig, Spacing


class WidgetFactory:
    #Class for styled UI components
    
    @staticmethod
    def create_label(parent, text="", style_type="normal", **kwargs):
        # Create a label with style.

        style_map = {
            'title': 'Title.TLabel',
            'heading': 'Heading.TLabel', 
            'subheading': 'Subheading.TLabel',
            'normal': 'Normal.TLabel',
            'small': 'Small.TLabel',
            'accent': 'Accent.TLabel',
            'muted': 'Muted.TLabel',
            'success': 'Success.TLabel',
            'error': 'Error.TLabel',
            'warning': 'Warning.TLabel'
        }
        
        style = style_map.get(style_type, 'Normal.TLabel')
        return ttk.Label(parent, text=text, style=style, **kwargs)
    
    @staticmethod
    def create_entry(parent, size="medium", **kwargs):
        # Create entry field
        
        config_map = {
            'small': ComponentConfig.ENTRY_SMALL,
            'medium': ComponentConfig.ENTRY_MEDIUM,
            'large': ComponentConfig.ENTRY_LARGE,
            'values': ComponentConfig.ENTRY_VALUES
        }
        
        config = config_map.get(size, ComponentConfig.ENTRY_MEDIUM)
        final_config = {**config, **kwargs}
        return ttk.Entry(parent, **final_config)
    
    @staticmethod
    def create_combo(parent, values=None, size="medium", **kwargs):
        # Create combobox.
        
        config_map = {
            'small': ComponentConfig.COMBO_SMALL,
            'medium': ComponentConfig.COMBO_MEDIUM,
            'large': ComponentConfig.COMBO_LARGE
        }
        
        config = config_map.get(size, ComponentConfig.COMBO_MEDIUM)
        final_config = {**config, **kwargs}
        
        var = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=var, **final_config)
        
        if values:
            combo['values'] = values
            
        return combo, var
    
    @staticmethod
    def create_button(parent, text="", command=None, style_type="secondary", icon="", **kwargs):
        # Create button
        
        config_map = {
            'primary': ComponentConfig.BUTTON_PRIMARY,
            'secondary': ComponentConfig.BUTTON_SECONDARY,
            'small': ComponentConfig.BUTTON_SMALL,
            'help': ComponentConfig.BUTTON_HELP
        }
        
        config = config_map.get(style_type, ComponentConfig.BUTTON_SECONDARY)
        final_config = {**config, **kwargs}
        
        if style_type == "help" and not text:
            from gui.styles import Icons
            text = Icons.HELP
        
        button_text = f"{icon} {text}".strip() if icon else text
        
        return ttk.Button(parent, text=button_text, command=command, **final_config)
    
    @staticmethod
    def create_listbox(parent, **kwargs):
        # Create listbox
        
        config = {**ComponentConfig.LISTBOX_DEFAULT, **kwargs}
        listbox = tk.Listbox(parent, **config)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        return listbox, scrollbar
    
    @staticmethod
    def create_text_widget(parent, widget_type="results", height=None, **kwargs):
        # Create text widget
        
        config_map = {
            'results': ComponentConfig.TEXT_RESULTS,
            'info': ComponentConfig.TEXT_INFO
        }
        
        config = config_map.get(widget_type, ComponentConfig.TEXT_RESULTS)
        final_config = {**config, **kwargs}
        
        if height:
            final_config['height'] = height
        
        if widget_type == "results":
            return scrolledtext.ScrolledText(parent, **final_config)
        else:
            text_widget = tk.Text(parent, **final_config)
            scrollbar = ttk.Scrollbar(parent, orient='vertical', command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            return text_widget, scrollbar
    
    @staticmethod
    def create_frame(parent, frame_type="normal", **kwargs):
        # Create frame.

        import tkinter as tk
        
        if frame_type == "modern":
            return ttk.Frame(parent, style='Modern.TFrame', **kwargs)
        elif frame_type == "card":
            return ttk.Frame(parent, style='Card.TFrame', **kwargs)
        else:
            return tk.Frame(parent, **kwargs)
    
    @staticmethod
    def create_labelframe(parent, text="", padding=None, **kwargs):
        # Create LabelFrame

        if padding is None:
            padding = LayoutConfig.CARD_PADDING
            
        return ttk.LabelFrame(parent, text=text, style='Card.TLabelframe', 
                             padding=padding, **kwargs)
    
    @staticmethod
    def create_radiobutton(parent, text="", variable=None, value="", **kwargs):
        # Create radio button
        return ttk.Radiobutton(parent, text=text, variable=variable, value=value, **kwargs)
    
    @staticmethod
    def create_treeview(parent, columns=(), show='headings', height=10, **kwargs):
        # Create tree view.
        
        tree = ttk.Treeview(parent, columns=columns, show=show, height=height, **kwargs)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        return tree, scrollbar


class LayoutHelper:
    
    @staticmethod
    def grid_configure(widget, row=0, column=0, sticky='w', padx=None, pady=None, **kwargs):
        if padx is None:
            padx = LayoutConfig.GRID_PADX
        if pady is None:
            pady = LayoutConfig.GRID_PADY
            
        widget.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady, **kwargs)
    
    @staticmethod
    def pack_configure(widget, side='top', fill='none', expand=False, pady=None, padx=0, **kwargs):
        if pady is None:
            pady = LayoutConfig.PACK_PADY_MEDIUM
            
        widget.pack(side=side, fill=fill, expand=expand, pady=pady, padx=padx, **kwargs)
    
    @staticmethod
    def create_grid_row(parent, widgets_config, start_row=0):
        # Create grid row.
        
        widgets = []
        
        for col, config in enumerate(widgets_config):
            widget_type = config.get('type', 'label')
            widget_kwargs = config.get('kwargs', {})
            grid_kwargs = config.get('grid', {})
            
            if widget_type == 'label':
                widget = WidgetFactory.create_label(parent, **widget_kwargs)
            elif widget_type == 'entry':
                widget = WidgetFactory.create_entry(parent, **widget_kwargs)
            elif widget_type == 'button':
                widget = WidgetFactory.create_button(parent, **widget_kwargs)
            elif widget_type == 'combo':
                widget, var = WidgetFactory.create_combo(parent, **widget_kwargs)
                widgets.append(var)
            else:
                continue
            
            LayoutHelper.grid_configure(widget, row=start_row, column=col, **grid_kwargs)
            widgets.append(widget)
            
        return widgets


class DialogFactory:
    # Dialog factory
    
    @staticmethod
    def show_info(title, message, details=None):
        # Shows info dialog.
        
        from tkinter import messagebox
        if details:
            DialogFactory._show_custom_dialog(title, message, details, "info")
        else:
            messagebox.showinfo(title, message)
    
    @staticmethod
    def show_warning(message):
        # Shows warning dialog.
        
        from tkinter import messagebox
        messagebox.showwarning("Внимание", message)
    
    @staticmethod
    def show_error(title, message, details=None):
        # Shows error dialog.

        if details:
            DialogFactory._show_custom_dialog(title, message, details, "error")
        else:
            from tkinter import messagebox
            messagebox.showerror(title, message)
    
    @staticmethod
    def ask_yes_no(message):
        # Shows yes/no dialog.
        
        from tkinter import messagebox
        return messagebox.askyesno("Потвърждение", message)
      
    @staticmethod
    def _show_custom_dialog(title, message, details, dialog_type):
        # Shows custom dialog.
        
        import tkinter as tk
        from tkinter import scrolledtext
        
        dialog = tk.Toplevel()
        dialog.title(title)
        dialog.geometry("500x400")
        dialog.configure(bg='#f0f0f0')
        dialog.transient()
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (250)
        y = (dialog.winfo_screenheight() // 2) - (200)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Icon and message frame
        top_frame = tk.Frame(main_frame, bg='#f0f0f0')
        top_frame.pack(fill='x', pady=(0, 15))
        
        if dialog_type != 'error':
            icon_map = {'info': 'ℹ️', 'warning': '⚠️'}
            icon = icon_map.get(dialog_type, 'ℹ️')
            
            icon_label = tk.Label(top_frame, text=icon, font=('Segoe UI', 16), 
                                 bg='#f0f0f0', fg='#333333')
            icon_label.pack(side='left', padx=(0, 10))
        
        # Main message
        message_label = tk.Label(top_frame, text=message, font=('Segoe UI', 11, 'bold'), 
                                bg='#f0f0f0', fg='#333333', wraplength=400, justify='left')
        message_label.pack(side='left', fill='x', expand=True)
        
        # Details text
        details_text = scrolledtext.ScrolledText(main_frame, height=15, width=60,
                                                font=('Courier', 9), wrap='word',
                                                bg='#ffffff', fg='#333333')
        details_text.pack(fill='both', expand=True, pady=(0, 15))
        details_text.insert('1.0', details)
        details_text.configure(state='disabled')
        
        # OK button
        ok_button = ttk.Button(main_frame, text="OK", command=dialog.destroy,
                              style='Secondary.TButton')
        ok_button.pack()


class StatusFactory:
    # Status factory class
        
    @staticmethod
    def log_message(text_widget, message, message_type="info"):

        from gui.ui_components import log_to_results

        icon_map = {
            'info': Icons.INFO,
            'success': Icons.SUCCESS,
            'error': Icons.ERROR,
            'warning': Icons.WARNING
        }
        
        icon = icon_map.get(message_type, "")
        formatted_message = f"{icon} {message}" if icon else message
        
        log_to_results(text_widget, formatted_message)


# Convenience functions for often used combinations
def create_parameter_row(parent, label_text, entry_size="medium", help_command=None, row=0):
    # Creates a row with label, entry and help button.

    # Label
    label = WidgetFactory.create_label(parent, label_text, "subheading")
    LayoutHelper.grid_configure(label, row=row, column=0, sticky='w')
    
    # Entry
    entry = WidgetFactory.create_entry(parent, entry_size)
    LayoutHelper.grid_configure(entry, row=row, column=1, sticky='w')
    
    # Help button
    help_btn = None
    if help_command:
        help_btn = WidgetFactory.create_button(parent, "", help_command, "help")
        LayoutHelper.grid_configure(help_btn, row=row, column=2)
    
    return entry, help_btn


def create_operation_section(parent, title):
    return WidgetFactory.create_labelframe(parent, title)


def create_button_row(parent, buttons_config):
    # Create a row with buttons.
    
    frame = WidgetFactory.create_frame(parent)
    buttons = []
    
    for i, config in enumerate(buttons_config):
        button_config = {k: v for k, v in config.items() 
                        if k not in ['side', 'padx', 'pady']}
        
        side = config.get('side', 'left')
        padx = config.get('padx', (0, Spacing.PADDING_SMALL))
        pady = config.get('pady', 0)
        
        btn = WidgetFactory.create_button(frame, **button_config)
        btn.pack(side=side, padx=padx, pady=pady)
        
        buttons.append(btn)
    
    return frame, buttons


# Export
__all__ = [
    'WidgetFactory', 'LayoutHelper', 'DialogFactory', 'StatusFactory',
    'create_parameter_row', 'create_operation_section', 'create_button_row'
]