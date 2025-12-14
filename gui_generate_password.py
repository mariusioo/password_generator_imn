import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime
from password_gen import generate_password
from pathlib import Path


def has_upper(password: str) -> bool:
        return any(ch.isupper() for ch in password)

def has_lower(password: str) -> bool:
        return any(ch.islower() for ch in password)

def has_digits(password: str) -> bool:
        return any(ch.isdigit() for ch in password)

def has_symbols(password: str) -> bool:
    symbols = "!@#$%&_?"
    has_symbols = False
    for ch in password:
        if ch in symbols:
            has_symbols = True
            break
    return has_symbols

def password_strength_from_pwd(pwd: str) ->str:
    categories = 0
    categories += any(ch.isupper() for ch in pwd)
    categories += any(ch.islower() for ch in pwd)
    categories += any(ch.isdigit() for ch in pwd)
    categories += any(ch in "!@#$%&_?" for ch in pwd)
    if categories >= 3:
        return "Strong"
    if categories >= 2:
        return "Moderate"
    return "Weak" 

def save_dialog():
    pwd = password_var.get()
    if not pwd:        
        password_var.set("Generate a password first")
        password_entry.configure(fg="red")
        return
    path = filedialog.asksaveasfilename(
        title="Save password",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        initialfile="saved_passwords.txt"
    )
    if not path:
        return
    with open(path, "a") as file:
        file.write(f"{pwd}\n")

def copy_to_clipboard():
    """Copy text to the system clipboard if requested."""
    pwd = password_var.get()
    if not pwd:        
        password_var.set("Generate a password first")
        password_entry.configure(fg="red")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    root.update_idletasks()

def on_generate():
    try:
        length = int(length_var.get())
    except ValueError:
        password_var.set("Enter a number for length")
        return
    if length < 8:
        password_var.set("Length must be at least 8 characters")
        return
    if not (upper_var.get() or lower_var.get() or digits_var.get() or symbols_var.get()):
        password_var.set("Select at least one type of character")
        return

    pwd = generate_password(
        length=length,
        chose_upper=upper_var.get() == 1,
        chose_lower=lower_var.get() == 1,
        chose_digits=digits_var.get() == 1,
        chose_symbols=symbols_var.get() == 1,
        pronounceable=pronounce_var.get() == 1,
        
    )
    BASE_DIR = Path(__file__).resolve().parent #points to where the py file lives
    hist_path = BASE_DIR / "historical_passwords.txt"
    #print("About to write:", repr(password))
    with open(hist_path, "a") as file:
        timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        file.write(f"{pwd}    was generated on: {timestamp}\n")


    password_var.set(pwd)
    password_entry.config(fg="white")
    has_upper_var.set(1 if has_upper(pwd) else 0)
    has_lower_var.set(1 if has_lower(pwd) else 0)
    has_digits_var.set(1 if has_digits(pwd) else 0)
    has_symbols_var.set(1 if has_symbols(pwd) else 0)
    
    
    pwd_strength_var.set(password_strength_from_pwd(pwd))
    update_status_upper(pwd)
    update_status_lower(pwd)
    update_status_digits(pwd)
    update_status_symbols(pwd)

root = tk.Tk()
root.lift()
root.attributes("-topmost", True)
root.after(150, root.focus_force)
root.after(200, lambda: root.attributes("-topmost", False))
root.title("Password generator")
window_width = 400
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# img_path = Path(__file__).resolve().parent / "image.png"
# root.bg_img = tk.PhotoImage(file=img_path)
# bg_label = tk.Label(root, image=root.bg_img)
# bg_label.place(x=0, y=0, relwidth=1, relheight=1)

length_var = tk.StringVar(value=16)
upper_var = tk.IntVar(value=1)
lower_var = tk.IntVar(value=1)
digits_var = tk.IntVar(value=1) 
symbols_var = tk.IntVar(value=1)
pronounce_var = tk.IntVar(value=0)
password_var = tk.StringVar()
#save_var = tk.IntVar(value=0)
ctc_var = tk.IntVar(value=0)
has_upper_var = tk.IntVar(value=0)
has_lower_var = tk.IntVar(value=0)
has_digits_var = tk.IntVar(value=0)
has_symbols_var = tk.IntVar(value=0)
pwd_strength_var = tk.StringVar()


#build the label and default value for pass length
ttk.Label(root, text="Length:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
ttk.Entry(root, textvariable=length_var, width=5).grid(row=0, column=1, columnspan=2, sticky="w", padx=8)
#build checkbox for include upper case
ttk.Checkbutton(root, text="Uppercase", variable=upper_var).grid(row=1, column=0, columnspan=2, sticky="w", padx=10)
#build checkbox to include lower case
ttk.Checkbutton(root, text="Lowercase", variable=lower_var).grid(row=2, column=0, columnspan=2, sticky="w", padx=10)
#build checkbox to include digits
ttk.Checkbutton(root, text="Digits", variable=digits_var).grid(row=3, column=0, columnspan=2, sticky="w", padx=10)
#build checkbox to include symbols
ttk.Checkbutton(root, text="Symbols", variable=symbols_var).grid(row=4, column=0, columnspan=2, sticky="w", padx=10)
#build a checkbox to generate a pronounceable pass
ttk.Checkbutton(root, text="Pronounceable", variable=pronounce_var).grid(row=5, column=0, columnspan=2, sticky="w", padx=10)
#build a checkbox to save the pass
#ttk.Checkbutton(root, text="Save password", variable=save_var).grid(row=6, column=0, columnspan=2,sticky="w", padx=10)

#generate pass button
ttk.Button(root, text="Generate password", command=on_generate).grid(row=8, column=0, columnspan=2, sticky="w", padx=10)
#generate entry box for created pass
password_entry = tk.Entry(root, textvariable=password_var, width=30)
password_entry.grid(row=9, column=0, columnspan=2, padx=10, pady=(0, 20))

#check for different chars in pwd and check/uncheck the box or generate a green or red label for existent or nonexistent chars

#ttk.Checkbutton(root, text="Has uppercase", variable=has_upper_var, state="disabled", style="Status.TCheckbutton").grid(row=10, column=0, columnspan=1, sticky="w", padx=10)
has_upper_label = tk.Label(root, text="Has uppercase")
has_upper_label.grid(row=10,column=0, columnspan=1, sticky="w", padx=8)
def update_status_upper(pwd: str):
    has_upper_label.configure(
        bg="#c8f7c5" if any(ch.isupper() for ch in pwd) else "#f7c5c5",
        fg="#000000" if any(ch.isupper() for ch in pwd) else "#b00020"
)
#ttk.Checkbutton(root, text="Has lowercase", variable=has_lower_var, state="disabled").grid(row=10, column=1, columnspan=1, sticky="w", padx=10)
has_lower_label = tk.Label(root, text="Has lowercase")
has_lower_label.grid(row=10,column=1, columnspan=1, sticky="w", padx=8, pady=(2, 2))

def update_status_lower(pwd: str):
    has_lower_label.configure(
        bg="#c8f7c5" if any(ch.islower() for ch in pwd) else "#f7c5c5",
        fg="#000000" if any(ch.islower() for ch in pwd) else "#b00020"
)
#ttk.Checkbutton(root, text="Has digits", variable=has_digits_var, state="disabled").grid(row=11, column=0, columnspan=1, sticky="w", padx=10)
has_digits_label = tk.Label(root, text="Has digits")
has_digits_label.grid(row=11,column=0, columnspan=1, sticky="w", padx=8)
def update_status_digits(pwd: str):
    has_digits_label.configure(
        bg="#c8f7c5" if any(ch.isdigit() for ch in pwd) else "#f7c5c5",
        fg="#000000" if any(ch.isdigit() for ch in pwd) else "#b00020"
)
#ttk.Checkbutton(root, text="Has symbols", variable=has_symbols_var, state="disabled").grid(row=11, column=1, columnspan=1, sticky="w", padx=10)
has_symbols_label = tk.Label(root, text="Has symbols")
has_symbols_label.grid(row=11,column=1, columnspan=1, sticky="w", padx=8, pady=(2, 2))
def update_status_symbols(pwd: str):
    symbols = "!@#$%&_?"
    has_symbols_label.configure(
        bg="#c8f7c5" if any(ch in symbols for ch in pwd) else "#f7c5c5",
        fg="#000000" if any(ch in symbols for ch in pwd) else "#b00020"
)

ttk.Label(root, text="Password Strength:").grid(row=12, column=0, sticky="w", padx=8, pady=4)
ttk.Entry(root, textvariable=pwd_strength_var, state="disabled", width=8).grid(row=12, column=1, columnspan=1, sticky="w", padx=8)


#built save to file button
ttk.Button(root, text="Save password", command=save_dialog).grid(row=14, column=0, columnspan=1, sticky="w", padx=10, pady=(0, 8))
#build a button for copy to clipboard
ttk.Button(root, text="Copy to clipboard", command=copy_to_clipboard).grid(row=14, column=1, columnspan=2, sticky="w", padx=10, pady=(0, 8))

#built close the app button
ttk.Button(root, text="Close", style="Tight.TButton", command=root.destroy).grid(row=15, column=0, columnspan=2, sticky="w", padx=10, pady=0)
root.mainloop()
