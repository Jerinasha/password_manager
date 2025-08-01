import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet
import base64
import hashlib
import json
import os

# Utility functions (load, save, encrypt, decrypt)

def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

def get_key(master_password):
    hash = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(hash)

def encrypt_password(password, master_password):
    key = get_key(master_password)
    f = Fernet(key)
    encrypted = f.encrypt(password.encode()).decode()
    return encrypted

def decrypt_password(encrypted, master_password):
    key = get_key(master_password)
    f = Fernet(key)
    try:
        decrypted = f.decrypt(encrypted.encode()).decode()
        return decrypted
    except:
        return None

# Main GUI class
class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager GUI")
        self.root.geometry("400x350")

        self.master_password = None
        self.data = {}

        self.create_widgets()
        self.ask_master_password()

    def ask_master_password(self):
        self.master_password = simpledialog.askstring("Master Password", "Enter your master password:", show='*')
        if not self.master_password:
            messagebox.showerror("Error", "Master password is required!")
            self.root.destroy()
        else:
            self.data = load_data()

    def create_widgets(self):
        # Site name
        tk.Label(self.root, text="Site Name:").pack(pady=5)
        self.site_entry = tk.Entry(self.root, width=40)
        self.site_entry.pack()

        # Username
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=40)
        self.username_entry.pack()

        # Password
        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=40, show="*")
        self.password_entry.pack()

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)

        save_btn = tk.Button(btn_frame, text="Save Password", command=self.save_password)
        save_btn.grid(row=0, column=0, padx=10)

        retrieve_btn = tk.Button(btn_frame, text="Retrieve Password", command=self.retrieve_password)
        retrieve_btn.grid(row=0, column=1, padx=10)

    def save_password(self):
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not site or not username or not password:
            messagebox.showwarning("Warning", "Please fill in all fields!")
            return

        encrypted = encrypt_password(password, self.master_password)
        self.data[site] = {"username": username, "password": encrypted}
        save_data(self.data)
        messagebox.showinfo("Success", f"Password for '{site}' saved successfully!")

        # Clear entries
        self.site_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def retrieve_password(self):
        site = self.site_entry.get().strip()
        if not site:
            messagebox.showwarning("Warning", "Please enter the site name!")
            return

        if site in self.data:
            decrypted = decrypt_password(self.data[site]["password"], self.master_password)
            if decrypted is None:
                messagebox.showerror("Error", "Incorrect master password or corrupted data.")
            else:
                username = self.data[site]["username"]
                messagebox.showinfo(f"Password for {site}",
                                    f"Username: {username}\nPassword: {decrypted}")
        else:
            messagebox.showerror("Error", f"No data found for site '{site}'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
