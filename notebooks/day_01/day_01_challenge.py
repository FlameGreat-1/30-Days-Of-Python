import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Modern Calculator")
        master.geometry("300x400")
        master.resizable(False, False)
        
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        self.create_widgets()
        
    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Result display
        result_frame = ttk.Frame(self.master, padding=(10, 10))
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        result_entry = ttk.Entry(result_frame, textvariable=self.result_var, font=('Arial', 24), justify='right')
        result_entry.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(self.master)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        row, col = 0, 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            ttk.Button(button_frame, text=button, command=cmd, width=5).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        ttk.Button(button_frame, text='C', command=self.clear, width=5).grid(row=row, column=col, padx=5, pady=5)
        
    def click(self, key):
        if key == '=':
            try:
                result = eval(self.result_var.get())
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        else:
            if self.result_var.get() == "0" or self.result_var.get() == "Error":
                self.result_var.set(key)
            else:
                self.result_var.set(self.result_var.get() + key)
    
    def clear(self):
        self.result_var.set("0")

root = tk.Tk()
calculator = Calculator(root)
root.mainloop()