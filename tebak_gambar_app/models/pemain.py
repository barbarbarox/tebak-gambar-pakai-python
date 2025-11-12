# models/pemain.py

class Pemain:
    """Representasi pemain dalam game Tebak Gambar."""
    
    def __init__(self, nama: str):
        if not isinstance(nama, str) or not nama.strip():
            raise ValueError("Nama pemain harus berupa string non-kosong.")
        self._nama = nama.strip()
        self._skor = 0

    @property
    def nama(self) -> str:
        return self._nama

    @property
    def skor(self) -> int:
        return self._skor

    def tambah_skor(self, nilai: int):
        if not isinstance(nilai, int) or nilai < 0:
            raise ValueError("Nilai skor harus bilangan bulat non-negatif.")
        self._skor += nilai

    def __repr__(self):
        return f"Pemain(nama='{self._nama}', skor={self._skor})"