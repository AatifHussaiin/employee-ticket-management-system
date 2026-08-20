import hashlib


def hash_password(password):
    """
    Convert a plain-text password into a SHA-256 hash.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password, hashed_password):
    """
    Verify whether the entered password matches the stored hash.
    """
    return hash_password(password) == hashed_password