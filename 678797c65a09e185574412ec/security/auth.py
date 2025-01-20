
import hashlib
import os
import base64
from cryptography.fernet import Fernet

# Generate a key for encryption/decryption
def generate_key():
    return base64.urlsafe_b64encode(os.urandom(32))

# Encrypt a password
def encrypt_password(password):
    key = generate_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return key, encrypted_password

# Decrypt a password
def decrypt_password(key, encrypted_password):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Hash a password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to store password securely
def store_password(event_id, password):
    key, encrypted_password = encrypt_password(password)
    # Save `event_id`, `key` and `encrypted_password` to the database
    # Database handling code goes here

# Function to verify password
def verify_password(event_id, input_password):
    # Retrieve `key` and `encrypted_password` from the database
    key, encrypted_password = retrieve_password(event_id)
    decrypted_password = decrypt_password(key, encrypted_password)
    return hash_password(input_password) == hash_password(decrypted_password)

# Example function to retrieve password (this should access your actual database)
def retrieve_password(event_id):
    # Replace this with actual database retrieval logic
    return (b'your_base64_encoded_key', b'your_encrypted_password')

# Sample usage
if __name__ == "__main__":
    # event_id = example_event_id
    # password = 'your_secure_password'
    # store_password(event_id, password)
    pass
