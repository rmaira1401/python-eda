import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import string
import random
import pyperclip


def generate_password():
    try:
        length_input = length_pass.get()
        if not length_input.isdigit():
            raise ValueError("Please Enter a valid number for the password length")
        else:
            length =int(length_input)
            upper = uppercase_var.get()
            lower = lowercase_var.get()
            digit = digits_var.get()
            special = special_var.get()

            characters = ""
            if upper:
                characters += string.ascii_uppercase
            if lower:
                characters += string.ascii_lowercase
            if digit:
                characters += string.digits
            if special:
                characters += string.punctuation

            if not characters:
                raise ValueError("At least one character set must be selected.")
            password =''.join(random.sample(characters,length))
            pass_entry.delete(0, tk.END)
            pass_entry.insert(0, password)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def copy_pass():
    password = pass_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard")
    else:
        messagebox.showwarning("Warning", "No password to copy")


root=tk.Tk()
root.title("Password Generator")
icon = PhotoImage(file="D:\Internship\Python\project1\lock.png")
root.iconphoto(True, icon)

main_frame=tk.Frame(root, padx=30,pady=15)
main_frame.grid(row=0,column=0,sticky="nsew")
tk.Label(main_frame, text="Password length:").grid(row=0,column=0,sticky="w")
length_pass = tk.Entry(main_frame)
length_pass.insert(0,"12")
length_pass.grid(row=0,column=1)
uppercase_var=tk.BooleanVar(value=True)
tk.Checkbutton(main_frame, text="Include Uppercase", variable=uppercase_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=(10,0))
lowercase_var=tk.BooleanVar(value=True)
tk.Checkbutton(main_frame, text="Include Lowercase", variable=lowercase_var).grid(row=2, column=0, columnspan=2, sticky="w")
digits_var=tk.BooleanVar(value=True)
tk.Checkbutton(main_frame, text="Include digits", variable=digits_var).grid(row=3, column=0, columnspan=2, sticky="w")
special_var=tk.BooleanVar(value=True)
tk.Checkbutton(main_frame, text="Include special characters", variable=special_var).grid(row=4, column=0, columnspan=2, sticky="w", pady=(0,10))

btnGenerate = tk.Button(main_frame, text="Generate Password", command = generate_password)
btnGenerate.grid(row=5, column=0, columnspan=2, pady=5)
pass_entry = tk.Entry(main_frame, width=30, justify='center', bd=0)
pass_entry.grid(row=6, column=0, columnspan=2, pady=5)
pass_entry.configure(bg=root.cget("bg"))
btnCopy = tk.Button(main_frame, text="Copy to Clipboard", command = copy_pass)
btnCopy.grid(row=7, column=0, columnspan=2, pady=5)

root.mainloop()


