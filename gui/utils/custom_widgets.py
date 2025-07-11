from tkinter import Toplevel, Button, Entry, Frame, Label, Text

class CustomAlert(Toplevel):
    """
    A custom alert dialog that looks more modern than standard messagebox
    
    Usage:
    CustomAlert(parent_window, "Title", "Message", "error|success|info")
    """
    def __init__(self, parent, title, message, alert_type="error"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Configure the window appearance based on alert type
        bg_colors = {
            "error": "#FF5252", 
            "success": "#4CAF50",
            "info": "#2196F3",
            "warning": "#FFC107"
        }
        
        bg_color = bg_colors.get(alert_type, "#FF5252")
        
        # Create frame for the alert
        self.configure(bg="#FFFFFF")
        
        # Add alert icon and header
        icons = {
            "error": "❌", 
            "success": "✓",
            "info": "ℹ️",
            "warning": "⚠️"
        }
        
        icon_text = icons.get(alert_type, "❌")
        
        Label(self, text=icon_text, font=("Montserrat Bold", 30), bg="#FFFFFF", fg=bg_color).pack(pady=(20, 0))
        
        # Add title
        Label(self, text=title, font=("Montserrat Bold", 14), bg="#FFFFFF", fg="#333333").pack(pady=(10, 5))
        
        # Add message
        Label(self, text=message, font=("Montserrat", 12), bg="#FFFFFF", fg="#555555", wraplength=350).pack(pady=(0, 15))
        
        # Add OK button
        ok_button = Button(
            self,
            text="OK",
            font=("Montserrat Bold", 12),
            bg=bg_color,
            fg="#FFFFFF",
            relief="flat",
            command=self.destroy,
            width=10,
            cursor="hand2"
        )
        ok_button.pack(pady=10)
        
        # Center the window on parent
        self.transient(parent)
        self.grab_set()
        
        # Bind escape key to close
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind("<Return>", lambda event: self.destroy())


class HoverButton(Button):
    """
    A button that changes color on hover
    """
    def __init__(self, master, hover_bg="#4A85F0", **kw):
        super().__init__(master=master, cursor="hand2", **kw)
        self.defaultBackground = self.cget("background")
        self.hover_bg = hover_bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(background=self.hover_bg)

    def on_leave(self, e):
        self.config(background=self.defaultBackground)


class StyledEntry(Entry):
    """
    An entry widget with placeholder text that disappears on focus
    """
    def __init__(self, master, placeholder="", **kw):
        self.placeholder = placeholder
        self.placeholder_color = "#AAAAAA"
        self.default_fg_color = kw.pop('fg', '#333333')
        
        super().__init__(master, **kw)
        
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)
        
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)

    def focus_in(self, *args):
        if self.get() == self.placeholder:
            self.delete('0', 'end')
            self.config(fg=self.default_fg_color)

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()
            
    def get_value(self):
        """Get the actual value, not the placeholder"""
        if self.get() == self.placeholder:
            return ""
        return self.get()


class StyledTable(Frame):
    """
    A custom table widget with better styling than standard tkinter
    """
    def __init__(self, master, columns, data=None, **kwargs):
        super().__init__(master, **kwargs)
        self.columns = columns
        self.data = data or []
        
        # Create header row
        self.header_frame = Frame(self, bg="#5E95FF")
        self.header_frame.pack(fill="x")
        
        col_width = 1 / len(columns)
        
        for i, col in enumerate(columns):
            header_cell = Label(
                self.header_frame, 
                text=col, 
                bg="#5E95FF", 
                fg="white",
                font=("Montserrat Bold", 12),
                padx=10, 
                pady=8
            )
            header_cell.grid(row=0, column=i, sticky="nsew")
            self.header_frame.grid_columnconfigure(i, weight=1)
            
        # Create data rows
        self.data_frame = Frame(self)
        self.data_frame.pack(fill="both", expand=True)
        
        self.populate_data()
    
    def populate_data(self):
        # Clear existing data rows
        for widget in self.data_frame.winfo_children():
            widget.destroy()
            
        # Add data rows
        for i, row in enumerate(self.data):
            row_bg = "#F5F5F5" if i % 2 == 0 else "#FFFFFF"
            
            for j, cell_value in enumerate(row):
                cell = Label(
                    self.data_frame,
                    text=str(cell_value),
                    bg=row_bg,
                    fg="#333333",
                    font=("Montserrat", 10),
                    padx=10,
                    pady=8,
                    borderwidth=1,
                    relief="ridge"
                )
                cell.grid(row=i, column=j, sticky="nsew")
                self.data_frame.grid_columnconfigure(j, weight=1)
                
    def update_data(self, new_data):
        self.data = new_data
        self.populate_data()
