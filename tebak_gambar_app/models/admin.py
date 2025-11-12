# models/admin.py
import hashlib

class Admin:
    """Model admin untuk autentikasi."""
    
    def __init__(self, username: str, password_hash: str):
        if not username or not password_hash:
            raise ValueError("Username dan password hash tidak boleh kosong.")
        self._username = username
        self._password_hash = password_hash

    @property
    def username(self) -> str:
        return self._username

    def verify_password(self, password: str) -> bool:
        """Verifikasi password dengan hashing SHA-256."""
        if not isinstance(password, str):
            return False
        return self._password_hash == hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def hash_password(password: str) -> str:
        """Helper untuk hashing password (digunakan saat registrasi)."""
        return hashlib.sha256(password.encode()).hexdigest()