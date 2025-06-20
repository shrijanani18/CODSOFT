import customtkinter as ctk
import tkinter as tk
import random, string, re, pyperclip, datetime, os

# --- Strength Check ---
def assess_strength(pw):
    score = sum(bool(re.search(p, pw)) for p in [
        r".{8,}", r"[A-Z]", r"[a-z]", r"[0-9]", r"[!@#$%^&*]"
    ])
    labels = ["Too Short", "Weak", "Fair", "Good", "Strong", "Excellent"]
    return score, labels[score]

# --- Generate Password ---
def generate():
    length = length_var.get()
    pool = ""
    if upper_var.get(): pool += string.ascii_uppercase
    if lower_var.get(): pool += string.ascii_lowercase
    if digit_var.get(): pool += string.digits
    if symbol_var.get(): pool += string.punctuation
    if exclude_amb_var.get():
        pool = pool.translate(str.maketrans('', '', 'l1IO0'))
    if not pool or length < 4:
        return
    pwd = "".join(random.choice(pool) for _ in range(length))
    result_var.set(pwd)
    score, label = assess_strength(pwd)
    strength_label.configure(text=label, fg=["red","orange","yellow","cyan","green"][score-1])
    pyperclip.copy(pwd)
    status_label.configure(text="Copied to clipboard ✅")
    if save_var.get():
        with open("passwords.txt","a") as f:
            f.write(f"{datetime.datetime.now()}\t{pwd}\n")

# --- Toggle Visibility ---
def toggle_mask():
    result_entry.configure(show="" if show_var.get() else "•")

# --- Theme Switch ---
def toggle_theme():
    ctk.set_appearance_mode("dark" if theme_var.get() else "light")

# --- GUI Setup ---
app = ctk.CTk()
app.geometry("450x500")
app.title("Advanced Password Generator")

theme_var = tk.BooleanVar(value=False)
show_var = tk.BooleanVar(value=False)
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)
exclude_amb_var = tk.BooleanVar(value=False)
save_var = tk.BooleanVar(value=True)
length_var = tk.IntVar(value=16)
result_var = tk.StringVar()

# Layout
ctk.CTkCheckBox(app, text="Dark Mode", variable=theme_var, command=toggle_theme).pack(anchor="ne", padx=10, pady=5)
ctk.CTkLabel(app, text="Password Length").pack(pady=(10,0))
ctk.CTkSlider(app, from_=4, to=64, number_of_steps=60, variable=length_var).pack(fill="x", padx=20)

for var, text in [(upper_var,"Uppercase"),(lower_var,"Lowercase"),(digit_var,"Digits"),(symbol_var,"Symbols"),(exclude_amb_var,"Exclude Ambiguous"),(save_var,"Save to File")]:
    ctk.CTkCheckBox(app, text=text, variable=var).pack(anchor="w", padx=20, pady=2)

ctk.CTkButton(app, text="Generate Password", command=generate).pack(pady=10)

strength_label = ctk.CTkLabel(app, text="Strength: ")
strength_label.pack()
result_entry = ctk.CTkEntry(app, textvariable=result_var, show="•", width=300)
result_entry.pack(pady=10)

ctk.CTkCheckBox(app, text="Show Password", variable=show_var, command=toggle_mask).pack()
status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=5)

app.mainloop()
