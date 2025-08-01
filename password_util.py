import json
import os
from cryptography.fernet import Fernet
import base64
import hashlib

# Load saved data from the JSON file
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {}

# Save data to the JSON file
def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

# Generate a key using the master password
def get_key(master_password):
    hash = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(hash)

# Add a new password entry
def add_password(site, username, password, master_password):
    key = get_key(master_password)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode()).decode()

    data = load_data()
    data[site] = {"username": username, "password": encrypted}
    save_data(data)
    print(f"✅ Password for '{site}' has been saved.")

# Retrieve and decrypt a saved password
def get_password(site, master_password):
    data = load_data()
    if site in data:
        key = get_key(master_password)
        fernet = Fernet(key)
        try:
            decrypted = fernet.decrypt(data[site]["password"].encode()).decode()
            print(f"🔓 Username: {data[site]['username']}")
            print(f"🔓 Password: {decrypted}")
        except:
            print("❌ Incorrect master password.")
    else:
        print("❌ Site not found in saved records.")
