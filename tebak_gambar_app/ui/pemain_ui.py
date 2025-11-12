# ui/pemain_ui.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os
from models.pemain import Pemain
from services.game_logic import GameLogic

class PemainUI:
    def __init__(self, root, kembali_class):
        self.root = root
        self.kembali_class = kembali_class
        self.root.configure(bg="#e3f2fd")  # Light blue
        self.game_logic = GameLogic()
        self.pemain = None
        self.skor = 0
        self.sisa_soal = 5
        self.soal_sekarang = None
        self.photo = None  # Untuk mencegah garbage collection
        self.input_nama()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def input_nama(self):
        self.clear_window()
        nama = simpledialog.askstring("Nama Pemain", "Masukkan nama Anda:", parent=self.root)
        if not nama:
            self.kembali_ke_menu()
            return
        try:
            self.pemain = Pemain(nama)
            self.mulai_game()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.input_nama()

    def mulai_game(self):
        self.skor = 0
        self.sisa_soal = 5
        self.ambil_soal()

    def ambil_soal(self):
        try:
            self.soal_sekarang = self.game_logic.ambil_soal_acak()
            self.tampilkan_soal()
        except (ValueError, FileNotFoundError) as e:
            messagebox.showerror("Error", str(e))
            self.kembali_ke_menu()

    def tampilkan_soal(self):
        self.clear_window()

        # Judul
        tk.Label(
            self.root, text=f"Soal {6 - self.sisa_soal}/5",
            font=("Arial", 16, "bold"),
            bg="#e3f2fd", fg="#0d47a1"
        ).pack(pady=10)

        # Gambar
        if os.path.exists(self.soal_sekarang.path_gambar):
            img = Image.open(self.soal_sekarang.path_gambar)
            img = img.resize((320, 200), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.root, image=self.photo, bg="#e3f2fd")
            img_label.pack(pady=10)
        else:
            tk.Label(
                self.root, text="🖼️ Gambar tidak tersedia",
                fg="red", bg="#e3f2fd"
            ).pack(pady=10)

        # Input jawaban
        tk.Label(
            self.root, text="Jawaban Anda:",
            font=("Arial", 12), bg="#e3f2fd"
        ).pack()
        self.entry_jawaban = tk.Entry(
            self.root, font=("Arial", 14), width=20, justify="center"
        )
        self.entry_jawaban.pack(pady=10)
        self.entry_jawaban.focus()

        # Tombol
        tk.Button(
            self.root, text="✅ Periksa", command=self.cek_jawaban,
            bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
            relief="flat", padx=15, pady=5
        ).pack(pady=5)

        tk.Button(
            self.root, text="⬅️ Menu Utama", command=self.kembali_ke_menu,
            bg="#9e9e9e", fg="white", font=("Arial", 10),
            relief="flat", padx=10
        ).pack(pady=5)

    def cek_jawaban(self):
        jawaban = self.entry_jawaban.get().strip()
        if not jawaban:
            messagebox.showwarning("Peringatan", "Silakan masukkan jawaban!")
            return

        if jawaban.lower() == self.soal_sekarang.jawaban:
            self.pemain.tambah_skor(20)
            messagebox.showinfo("Benar!", f"✅ Jawaban benar!\n+20 poin\nSkor: {self.pemain.skor}")
        else:
            messagebox.showerror("Salah!", f"❌ Jawaban salah!\nJawaban benar: {self.soal_sekarang.jawaban}")

        self.sisa_soal -= 1
        if self.sisa_soal > 0:
            self.ambil_soal()
        else:
            self.selesai_main()

    def selesai_main(self):
        # Simpan ke leaderboard
        self.game_logic.simpan_ke_leaderboard(self.pemain)

        # Cek apakah masuk top 10
        posisi = self.game_logic.cek_masuk_top_10(self.pemain.skor)

        self.tampilkan_hasil_akhir(posisi)

    def tampilkan_hasil_akhir(self, posisi):
        self.clear_window()
        bg_color = "#e8f5e9" if posisi else "#ffebee"
        fg_color = "#2e7d32" if posisi else "#c62828"
        self.root.configure(bg=bg_color)

        tk.Label(
            self.root, text="🎉 Game Selesai!",
            font=("Arial", 22, "bold"),
            bg=bg_color, fg="#1b5e20" if posisi else "#b71c1c"
        ).pack(pady=20)

        tk.Label(
            self.root, text=f"Nama: {self.pemain.nama}",
            font=("Arial", 14), bg=bg_color
        ).pack()
        tk.Label(
            self.root, text=f"Skor Akhir: {self.pemain.skor}",
            font=("Arial", 16, "bold"), bg=bg_color
        ).pack(pady=10)

        if posisi:
            tk.Label(
                self.root,
                text=f"🏆 SELAMAT! Anda masuk TOP {posisi}!",
                font=("Arial", 16, "bold"),
                fg=fg_color, bg=bg_color
            ).pack(pady=15)
        else:
            tk.Label(
                self.root,
                text="Terus berlatih untuk masuk leaderboard!",
                font=("Arial", 12), bg=bg_color
            ).pack()

        # Tombol
        tk.Button(
            self.root, text="🏆 Lihat Leaderboard",
            command=self.tampilkan_leaderboard,
            bg="#4CAF50", fg="white", font=("Arial", 12)
        ).pack(pady=5)
        tk.Button(
            self.root, text="🔁 Main Lagi",
            command=self.input_nama,
            bg="#2196F3", fg="white", font=("Arial", 12)
        ).pack(pady=5)
        tk.Button(
            self.root, text="⬅️ Menu Utama",
            command=self.kembali_ke_menu,
            bg="#9e9e9e", fg="white", font=("Arial", 12)
        ).pack(pady=5)

    def tampilkan_leaderboard(self):
        self.clear_window()
        self.root.configure(bg="#fff3e0")

        tk.Label(
            self.root, text="🏆 Top 10 Leaderboard",
            font=("Arial", 20, "bold"),
            bg="#fff3e0", fg="#e65100"
        ).pack(pady=20)

        try:
            data = self.game_logic.get_leaderboard(10)
            if data:
                for i, (nama, skor) in enumerate(data, 1):
                    warna = "#ff6f00" if i <= 3 else "#5d4037"
                    tk.Label(
                        self.root,
                        text=f"{i}. {nama} — {skor} poin",
                        font=("Arial", 12, "bold" if i <= 3 else "normal"),
                        fg=warna, bg="#fff3e0"
                    ).pack()
            else:
                tk.Label(self.root, text="Belum ada data pemain.", bg="#fff3e0").pack()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat leaderboard: {e}")

        tk.Button(
            self.root, text="⬅️ Kembali",
            command=self.kembali_ke_menu,
            bg="#9e9e9e", fg="white"
        ).pack(pady=20)

    def kembali_ke_menu(self):
        self.root.configure(bg="#f0f8ff")
        from ui.main_menu import MainMenuUI
        MainMenuUI(self.root)