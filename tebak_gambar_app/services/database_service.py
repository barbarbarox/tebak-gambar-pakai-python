# services/database_service.py

import mysql.connector
from mysql.connector import Error
from config.db_config import DB_CONFIG

class DatabaseService:
    """Abstraksi koneksi dan operasi database dengan encapsulation."""
    
    def __init__(self):
        self._connection = None

    def _connect(self):
        """Membuat atau mengembalikan koneksi aktif ke database."""
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(**DB_CONFIG)
            except Error as e:
                raise ConnectionError(f"Gagal terhubung ke database: {e}")
        return self._connection

    def execute_query(self, query: str, params=None, fetch=False):
        """
        Menjalankan query SQL.
        - Jika fetch=True, mengembalikan hasil (untuk SELECT).
        - Jika fetch=False, hanya mengeksekusi (untuk INSERT/UPDATE/DELETE).
        """
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Error saat eksekusi query: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        """Menutup koneksi database jika terbuka."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None