import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import math

class ScientificCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Scientific Calculator")
        master.geometry("400x550")
        style = Style(theme='superhero')  # choose from ttkbootstrap themes

        # Notebook for tabs
        nb = ttk.Notebook(master)
        nb.pack(fill='both', expand=True, padx=5, pady=5)

        # Basic tab
        self.basic_frame = ttk.Frame(nb)
        nb.add(self.basic_frame, text="Basic")
        self.make_basic(self.basic_frame)

        # Scientific tab
        self.sci_frame = ttk.Frame(nb)
        nb.add(self.sci_frame, text="Scientific")
        self.make_scientific(self.sci_frame)

    def make_basic(self, parent):
        self.basic_disp = ttk.Entry(parent, font=("Helvetica", 20), justify="right")
        self.basic_disp.pack(fill='x', padx=5, pady=5, ipady=10)
        buttons = [
            '7','8','9','/',
            '4','5','6','*',
            '1','2','3','-',
            '0','.','C','+'
        ]
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        for i, text in enumerate(buttons):
            cmd = lambda x=text: self.click(x, self.basic_disp)
            ttk.Button(frame, text=text, command=cmd).grid(row=i//4, column=i%4, sticky="nsew", padx=2, pady=2)
        ttk.Button(frame, text="=", command=lambda: self.calc(self.basic_disp)).grid(row=4, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)
        for r in range(5):
            frame.rowconfigure(r, weight=1)
        for c in range(4):
            frame.columnconfigure(c, weight=1)

    def make_scientific(self, parent):
        self.sci_disp = ttk.Entry(parent, font=("Helvetica", 20), justify="right")
        self.sci_disp.pack(fill='x', padx=5, pady=5, ipady=10)
        buttons = [
            'sin','cos','tan','log',
            '(' ,')' ,'exp','sqrt',
            '7','8','9','/',
            '4','5','6','*',
            '1','2','3','-',
            '0','.','C','+'
        ]
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        for i, text in enumerate(buttons):
            cmd = lambda x=text: self.click(x, self.sci_disp)
            style = 'info.TButton' if text.isalpha() or text in ('sqrt','log','exp') else ''
            ttk.Button(frame, text=text, command=cmd, style=style).grid(row=i//4, column=i%4, sticky="nsew", padx=2, pady=2)
        ttk.Button(frame, text="=", command=lambda: self.calc(self.sci_disp)).grid(row=6, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)
        for r in range(7):
            frame.rowconfigure(r, weight=1)
        for c in range(4):
            frame.columnconfigure(c, weight=1)

    def click(self, val, entry):
        if val == 'C':
            entry.delete(0, tk.END)
        elif val in ('sin','cos','tan','log','exp','sqrt'):
            entry.insert(tk.END, val + "(")
        else:
            entry.insert(tk.END, val)

    def calc(self, entry):
        expr = entry.get()
        try:
            # safe environment
            result = eval(expr, {"__builtins__":None, "math":math, **math.__dict__})
            entry.delete(0, tk.END)
            entry.insert(0, str(result))
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(0, "Error")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
