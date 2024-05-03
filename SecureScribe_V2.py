import os
import re
import logging
from cryptography.fernet import Fernet
import getpass

# Configure logging
logging.basicConfig(filename='securescribe.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search('[a-z]', password):
        score += 1 
    if re.search('[A-Z]', password):
        score += 1
    if re.search('[0-9]', password):
        score += 1
    if re.search('[!@#$%&*]', password):
        score += 1
    return score

def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

def log_file_access(file_path, action):
    logging.info("File %s %s", action, file_path)

logging.info("SecureScribe program started.")

print("Welcome to SecureScribe!")
print("Compatible with Windows only.")
print("Thank you for using SecureScribe.")

password = getpass.getpass('Please enter a valid password : ')
logging.info("User entered a password.")

if not password:
    print("Password cannot be empty")
    logging.warning("User entered an empty password.")
elif validate_password(password):
    confirm_password = getpass.getpass("Please re-enter your password for verification: ")
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        logging.warning("Passwords do not match.")
    else:
        print("Password verified")
        logging.info("Password verified.")
        strength = password_strength(password)
        if strength == 5:
            print("Password strength: Strong")
        elif strength >= 3:
            print("Password strength: Moderate")
        else:
            print("Password strength: Weak")
        
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
            logging.info("File will be saved to: %s", file_path)
            with open(file_path, "w") as file:
                file.write(password)
            key = Fernet.generate_key()
            encrypted_password = encrypt_data(password, key)
            with open(file_path, "wb") as file:
                file.write(encrypted_password)

            log_file_access(file_path, "created")
            
            print(f"Password saved to {filename}")
            print("Encryption key: ", key.decode())
            logging.info("Password saved to %s", filename)
            logging.info("Encryption key: %s", key.decode())
        except OSError as e:
            print(f"Error: {e}")
            print("Failed to create password file. Please check the folder permissions.")
            logging.error("Failed to create password file: %s", e)
else:
    print("Invalid password")
    logging.warning("User entered an invalid password.")

# Attempt to read the password file
try:
    with open(file_path, "r") as file:
        password_read = file.read()
    print("Successfully read password from file.")
    logging.info("Successfully read password from file.")
    log_file_access(file_path, "read")
except FileNotFoundError:
    print("Password file not found.")
    logging.warning("Password file not found.")
except Exception as e:
    print(f"Error reading password file: {e}")
    logging.error("Error reading password file: %s", e)

# Attempt to modify the password file
try:
    with open(file_path, "a") as file:
        file.write("\nThis line is an attempt to modify the file.")
    print("Successfully modified password file.")
    logging.info("Successfully modified password file.")
    log_file_access(file_path, "modified")
except Exception as e:
    print(f"Error modifying password file: {e}")
    logging.error("Error modifying password file: %s", e)

logging.info("SecureScribe program ended.")
