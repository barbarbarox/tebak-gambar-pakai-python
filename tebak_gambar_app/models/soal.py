# models/soal.py

class Soal:
    """Representasi soal tebak gambar."""
    
    def __init__(self, id_soal: int, jawaban: str, path_gambar: str):
        if not isinstance(id_soal, int) or id_soal <= 0:
            raise ValueError("ID soal harus bilangan bulat positif.")
        if not isinstance(jawaban, str) or not jawaban.strip():
            raise ValueError("Jawaban tidak boleh kosong.")
        if not isinstance(path_gambar, str) or not path_gambar:
            raise ValueError("Path gambar tidak boleh kosong.")
        
        self._id = id_soal
        self._jawaban = jawaban.strip().lower()
        self._path_gambar = path_gambar

    @property
    def id(self) -> int:
        return self._id

    @property
    def jawaban(self) -> str:
        return self._jawaban

    @property
    def path_gambar(self) -> str:
        return self._path_gambar

    def __repr__(self):
        return f"Soal(id={self._id}, jawaban='{self._jawaban}', path='{self._path_gambar}')"