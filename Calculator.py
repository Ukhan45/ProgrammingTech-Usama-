import tkinter as tk
import math
class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("400x600")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")  
        self._create_widgets()
    def _create_widgets(self):
        self.display = tk.Entry(self, font=("Arial", 24), borderwidth=0, relief=tk.FLAT, justify='right')
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=20)
        self.display.insert(0, "0")
        buttons = [
            ('C', 1, 0), ('←', 1, 1), ('/', 1, 2), ('*', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('-', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('+', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('√', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2, 1, 2)
        ]
        self.button_colors = {} 
        for (text, row, col, *opt) in buttons:
            rowspan = colspan = 1
            if opt:
                rowspan, colspan = opt
            if text.isdigit() or text == '.':
                button_color = "#4285f4"  
            elif text in ('=', '+', '-', '*', '/'):
                button_color = "#ff8c00"  
            elif text == '√':
                button_color = "#4caf50"  
            elif text == 'C' or text == '←':
                button_color = "#e53935"  
            else:
                button_color = "#000000" 
            button = tk.Button(self, text=text, font=("Arial", 18), borderwidth=0, relief=tk.FLAT, command=lambda t=text: self._on_button_click(t), bg=button_color, fg="#ffffff")
            button.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky="nsew", padx=10, pady=10)
            button.bind("<Enter>", lambda event, b=button: self._on_enter(event, b))
            button.bind("<Leave>", lambda event, b=button: self._on_leave(event, b))
            self.button_colors[button] = button_color  
        for i in range(1, 6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
    def _on_enter(self, event, button):
        original_color = self.button_colors[button]
        hover_color = self._get_hover_color(original_color)
        button.config(bg=hover_color)
    def _on_leave(self, event, button):
        original_color = self.button_colors[button]
        button.config(bg=original_color)
    def _get_hover_color(self, color):
        hover_color = "#"+''.join([format(min(int(c, 16) + 32, 255), '02x') for c in (color[1:3], color[3:5], color[5:7])])
        return hover_color
    def _on_button_click(self, char):
        if char == 'C':
            self.display.delete(0, tk.END)
            self.display.insert(0, "0")
        elif char == '←':
            current_text = self.display.get()
            if len(current_text) > 1:
                self.display.delete(len(current_text)-1, tk.END)
            else:
                self.display.delete(0, tk.END)
                self.display.insert(0, "0")
        elif char == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        elif char == '√':
            try:
                number = float(self.display.get())
                result = math.sqrt(number)
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
            except ValueError:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        else:
            current_text = self.display.get()
            if current_text == "0":
                self.display.delete(0, tk.END)
                self.display.insert(0, char)
            else:
                self.display.insert(tk.END, char) 
if __name__ == "__main__":
    calculator = Calculator()
    calculator.mainloop()
