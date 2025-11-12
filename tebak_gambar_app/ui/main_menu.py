# ui/main_menu.py

import tkinter as tk
from tkinter import font as tkfont

class MainMenuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Tebak Gambar")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f8ff")  # AliceBlue
        self.setup_ui()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def fade_in(self, widget, alpha=0):
        """Animasi fade-in sederhana (simulasi via background)."""
        if alpha < 1.0:
            # Tidak ada opacity di tkinter, jadi kita pakai warna transisi
            # Alternatif: tampilkan setelah delay
            self.root.after(30, lambda: self.fade_in(widget, alpha + 0.1))
        # Untuk demo, kita langsung tampilkan
        widget.pack(pady=12)

    def create_button(self, text, command):
        btn = tk.Button(
            self.root, text=text, command=command,
            font=("Arial", 14, "bold"),
            bg="#4CAF50", fg="white",
            activebackground="#45a049", activeforeground="white",
            relief="flat", padx=20, pady=10,
            cursor="hand2"
        )
        # Efek hover
        btn.bind("<Enter>", lambda e: btn.config(bg="#66BB6A"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#4CAF50"))
        return btn

    def setup_ui(self):
        self.clear_window()

        # Judul
        title_font = tkfont.Font(family="Arial", size=28, weight="bold")
        title = tk.Label(
            self.root, text="🎮 TEBAK GAMBAR",
            font=title_font,
            bg="#f0f8ff", fg="#2c3e50"
        )
        title.pack(pady=40)

        # Tombol
        btn_pemain = self.create_button("👤 Main sebagai Pemain", self.go_to_pemain)
        btn_admin = self.create_button("🔑 Masuk sebagai Admin", self.go_to_admin)
        btn_leaderboard = self.create_button("🏆 Lihat Leaderboard", self.go_to_leaderboard)
        btn_keluar = self.create_button("❌ Keluar", self.root.quit)

        for btn in [btn_pemain, btn_admin, btn_leaderboard, btn_keluar]:
            self.fade_in(btn)

    # Placeholder navigasi (akan diisi setelah class lain dibuat)
    def go_to_pemain(self):
        from ui.pemain_ui import PemainUI
        PemainUI(self.root, self.__class__)

    def go_to_admin(self):
        from ui.admin_ui import AdminUI
        AdminUI(self.root, self.__class__)

    def go_to_leaderboard(self):
        from ui.pemain_ui import PemainUI
        # Gunakan method di PemainUI untuk tampilkan leaderboard
        ui = PemainUI(self.root, self.__class__)
        ui.tampilkan_leaderboard()