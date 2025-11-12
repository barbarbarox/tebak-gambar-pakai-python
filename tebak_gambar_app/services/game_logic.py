# services/game_logic.py

import os
import random
from models.soal import Soal
from models.pemain import Pemain
from services.database_service import DatabaseService

class GameLogic:
    """Logika inti game: ambil soal, hitung skor, kelola leaderboard."""
    
    def __init__(self):
        self._db = DatabaseService()

    def ambil_soal_acak(self) -> Soal:
        """Mengambil satu soal acak dari database."""
        hasil = self._db.execute_query(
            "SELECT id, jawaban, path_gambar FROM soal ORDER BY RAND() LIMIT 1",
            fetch=True
        )
        if not hasil:
            raise ValueError("Belum ada soal di database. Silakan tambahkan via admin.")
        
        id_soal, jawaban, path_gambar = hasil[0]
        
        # Validasi keberadaan file gambar
        if not os.path.isfile(path_gambar):
            raise FileNotFoundError(f"File gambar tidak ditemukan: {path_gambar}")
        
        return Soal(id_soal, jawaban, path_gambar)

    def simpan_ke_leaderboard(self, pemain: Pemain):
        """Menyimpan skor pemain ke tabel leaderboard."""
        if not isinstance(pemain, Pemain):
            raise TypeError("Argumen harus berupa instance dari class Pemain.")
        self._db.execute_query(
            "INSERT INTO leaderboard (nama_pemain, skor) VALUES (%s, %s)",
            (pemain.nama, pemain.skor)
        )

    def cek_masuk_top_10(self, skor: int) -> int | None:
        """
        Memeriksa apakah skor masuk top 10.
        Mengembalikan peringkat (1-based) jika masuk, None jika tidak.
        """
        if not isinstance(skor, int) or skor < 0:
            raise ValueError("Skor harus bilangan bulat non-negatif.")
        
        # Ambil 10 skor tertinggi
        hasil = self._db.execute_query(
            "SELECT skor FROM leaderboard ORDER BY skor DESC LIMIT 10",
            fetch=True
        )
        top_scores = [row[0] for row in hasil]

        # Jika kurang dari 10 data, pasti masuk
        if len(top_scores) < 10:
            # Hitung peringkat sebenarnya
            count = self._db.execute_query(
                "SELECT COUNT(*) FROM leaderboard WHERE skor > %s",
                (skor,), fetch=True
            )
            return count[0][0] + 1

        # Jika skor >= skor terendah di top 10, cek peringkat
        if skor >= min(top_scores):
            count = self._db.execute_query(
                "SELECT COUNT(*) FROM leaderboard WHERE skor > %s",
                (skor,), fetch=True
            )
            return count[0][0] + 1
        
        return None

    def get_leaderboard(self, limit: int = 10):
        """Mengambil daftar leaderboard (untuk ditampilkan di UI)."""
        return self._db.execute_query(
            "SELECT nama_pemain, skor FROM leaderboard ORDER BY skor DESC LIMIT %s",
            (limit,), fetch=True
        )