import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from tkinter import Tk, filedialog, Label, Button, messagebox, simpledialog

# Pad/unpad functions
def pad(data):
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

# Encrypt file
def encrypt_file(file_path, password):
    key = hashlib.sha256(password.encode()).digest()
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(pad(plaintext))
    enc_file = file_path + ".enc"

    with open(enc_file, 'wb') as f:
        f.write(iv + ciphertext)

    messagebox.showinfo("Success", f"File encrypted:\n{enc_file}")

# Decrypt file
def decrypt_file(file_path, password):
    key = hashlib.sha256(password.encode()).digest()

    with open(file_path, 'rb') as f:
        iv = f.read(AES.block_size)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))
    dec_file = file_path.replace(".enc", "_decrypted")

    with open(dec_file, 'wb') as f:
        f.write(plaintext)

    messagebox.showinfo("Success", f"File decrypted:\n{dec_file}")

# GUI
def select_encrypt():
    file_path = filedialog.askopenfilename(title="Select File to Encrypt")
    if not file_path:
        return
    password = simpledialog.askstring("Password", "Enter password:", show='*')
    if password:
        encrypt_file(file_path, password)

def select_decrypt():
    file_path = filedialog.askopenfilename(title="Select File to Decrypt")
    if not file_path:
        return
    password = simpledialog.askstring("Password", "Enter password:", show='*')
    if password:
        decrypt_file(file_path, password)

# Main UI
root = Tk()
root.title("Advanced Encryption Tool - AES256")
root.geometry("400x200")
Label(root, text="Advanced Encryption Tool (AES-256)", font=("Arial", 14, "bold")).pack(pady=10)
Button(root, text="Encrypt File", command=select_encrypt, width=20, bg="#4CAF50", fg="white").pack(pady=10)
Button(root, text="Decrypt File", command=select_decrypt, width=20, bg="#2196F3", fg="white").pack(pady=10)
Button(root, text="Exit", command=root.quit, width=20, bg="#f44336", fg="white").pack(pady=10)
root.mainloop()
