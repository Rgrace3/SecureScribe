#Final Project code

import os
import re
from cryptography.fernet import Fernet
import getpass

def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search('[a-z]', password):
        return False
    if not re.search('[A-Z]', password):
        return False
    if not re.search('[0-9].*[0-9]', password):  # At least 2 numbers
        return False
    if not re.search('[!@#$%&*].*[!@#$%&*]', password):  # At least 2 special characters
        return False
    return True

def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

print("Password must meet the following requirements:")
print("- At least 8 characters")
print("- At least one lowercase letter")
print("- At least one uppercase letter")
print("- At least 2 numbers")
print("- At least 2 special characters (!@#$%&*)")

password = getpass.getpass('Please enter a valid password : ')
if not password:
    print("Password cannot be empty")
elif validate_password(password):
    confirm_password = getpass.getpass("Please re-enter your password for verification: ")
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
    else:
        print("Password verified")
        folder_path = r"C:\SecureScribe"
        filename = input("Enter the filename to save the password to (no extension): ")
        if not filename:
            filename = "valid"
        elif not filename.endswith(".txt"):
            filename += ".txt"
        
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        
            file_path = os.path.join(folder_path, filename)
            print("File will be saved to:", file_path)  # Print the file path
            with open(file_path, "w") as file:
                file.write(password)
            key = Fernet.generate_key()
            encrypted_password = encrypt_data(password, key)
            with open(file_path, "wb") as file:
                file.write(encrypted_password)

            print(f"Password saved to {filename}")
            print("Encryption key: ", key.decode())
        except OSError as e:
            print(f"Error: {e}")
            print("Failed to create password file. Please check the folder permissions.")
else:
    print("Invalid password")
