import hashlib
import os

class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        # Generate a salt
        salt = os.urandom(16)
        # Derive the key using PBKDF2
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        # Return salt and hash
        return salt + pwdhash

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        # Extract the salt from the stored password
        salt = stored_password[:16]
        stored_pwdhash = stored_password[16:]
        # Hash the provided password with the same salt
        pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
        # Compare the hashes
        return pwdhash == stored_pwdhash
