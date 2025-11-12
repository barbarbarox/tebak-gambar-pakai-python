# ui/admin_ui.py

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from models.admin import Admin
from services.database_service import DatabaseService
import os
import shutil

class AdminUI:
    def __init__(self, root, kembali_class):
        self.root = root
        self.kembali_class = kembali_class
        self.db = DatabaseService()
        self.root.configure(bg="#f5f5f5")
        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        tk.Label(
            self.root, text="🔐 Login Admin",
            font=("Arial", 18, "bold"), bg="#f5f5f5"
        ).pack(pady=30)

        tk.Label(self.root, text="Username:", bg="#f5f5f5").pack()
        self.entry_user = tk.Entry(self.root, font=("Arial", 12), width=25)
        self.entry_user.pack(pady=5)

        tk.Label(self.root, text="Password:", bg="#f5f5f5").pack()
        self.entry_pass = tk.Entry(self.root, font=("Arial", 12), width=25, show="*")
        self.entry_pass.pack(pady=5)

        tk.Button(
            self.root, text="Login", command=self.login,
            bg="#00796b", fg="white", font=("Arial", 12)
        ).pack(pady=15)
        tk.Button(
            self.root, text="⬅️ Batal", command=self.kembali_ke_menu,
            bg="#9e9e9e", fg="white"
        ).pack()

    def login(self):
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get()
        if not user or not pwd:
            messagebox.showwarning("Peringatan", "Username dan password wajib diisi!")
            return

        # Ambil hash dari DB
        try:
            result = self.db.execute_query(
                "SELECT username, password FROM admin WHERE username = %s",
                (user,), fetch=True
            )
            if result:
                db_user, db_hash = result[0]
                admin = Admin(db_user, db_hash)
                if admin.verify_password(pwd):
                    self.show_dashboard()
                    return
        except Exception as e:
            messagebox.showerror("Error", f"Login gagal: {e}")
            return

        messagebox.showerror("Error", "Username atau password salah!")

    def show_dashboard(self):
        self.clear_window()
        self.root.configure(bg="#e0f7fa")

        tk.Label(
            self.root, text="🛠️ Panel Admin",
            font=("Arial", 20, "bold"), bg="#e0f7fa", fg="#006064"
        ).pack(pady=20)

        tk.Button(
            self.root, text="➕ Tambah Soal", command=self.tambah_soal,
            bg="#00796b", fg="white", font=("Arial", 12), width=20
        ).pack(pady=8)
        tk.Button(
            self.root, text="👁️ Kelola Soal", command=self.kelola_soal,
            bg="#00796b", fg="white", font=("Arial", 12), width=20
        ).pack(pady=8)
        tk.Button(
            self.root, text="⬅️ Logout", command=self.kembali_ke_menu,
            bg="#9e9e9e", fg="white", font=("Arial", 12), width=20
        ).pack(pady=20)

    def tambah_soal(self):
        self.clear_window()
        self.root.configure(bg="#e0f7fa")

        tk.Label(self.root, text="➕ Tambah Soal", font=("Arial", 16, "bold"), bg="#e0f7fa").pack(pady=15)

        tk.Label(self.root, text="Jawaban:", bg="#e0f7fa").pack()
        self.jawaban_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        self.jawaban_entry.pack(pady=5)

        self.gambar_path = None
        self.gambar_label = tk.Label(self.root, text="Belum ada gambar", bg="#e0f7fa", fg="gray")
        self.gambar_label.pack(pady=5)

        tk.Button(
            self.root, text="📁 Pilih Gambar", command=self.pilih_gambar,
            bg="#00796b", fg="white"
        ).pack(pady=5)
        tk.Button(
            self.root, text="💾 Simpan", command=self.simpan_soal,
            bg="#388e3c", fg="white"
        ).pack(pady=10)
        tk.Button(
            self.root, text="⬅️ Batal", command=self.show_dashboard,
            bg="#9e9e9e", fg="white"
        ).pack()

    def pilih_gambar(self):
        file = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if file:
            self.gambar_path = file
            self.gambar_label.config(text=f"File: {os.path.basename(file)}", fg="black")

    def simpan_soal(self):
        jawaban = self.jawaban_entry.get().strip()
        if not jawaban or not self.gambar_path:
            messagebox.showwarning("Peringatan", "Lengkapi jawaban dan pilih gambar!")
            return

        # Simpan gambar ke folder gambar/
        folder = "gambar"
        os.makedirs(folder, exist_ok=True)
        nama_file = os.path.basename(self.gambar_path)
        dest_path = os.path.join(folder, nama_file)

        # Hindari overwrite dengan nama unik
        counter = 1
        base, ext = os.path.splitext(nama_file)
        while os.path.exists(dest_path):
            nama_file = f"{base}_{counter}{ext}"
            dest_path = os.path.join(folder, nama_file)
            counter += 1

        shutil.copy2(self.gambar_path, dest_path)

        # Simpan ke DB
        try:
            self.db.execute_query(
                "INSERT INTO soal (jawaban, path_gambar) VALUES (%s, %s)",
                (jawaban, dest_path)
            )
            messagebox.showinfo("Sukses", "Soal berhasil ditambahkan!")
            self.show_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan soal: {e}")

    def kelola_soal(self):
        self.clear_window()
        self.root.configure(bg="#e0f7fa")

        tk.Label(self.root, text="👁️ Daftar Soal", font=("Arial", 16, "bold"), bg="#e0f7fa").pack(pady=10)

        try:
            soal_list = self.db.execute_query("SELECT id, jawaban, path_gambar FROM soal", fetch=True)
            if not soal_list:
                tk.Label(self.root, text="Belum ada soal.", bg="#e0f7fa").pack()
            else:
                frame = tk.Frame(self.root, bg="#e0f7fa")
                frame.pack(fill="both", expand=True)

                canvas = tk.Canvas(frame, bg="#e0f7fa")
                scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
                scroll_frame = tk.Frame(canvas, bg="#e0f7fa")

                scroll_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )

                canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
                canvas.configure(yscrollcommand=scroll_y.set)

                for soal in soal_list:
                    id_soal, jawaban, path = soal
                    row = tk.Frame(scroll_frame, bg="#ffffff", relief="groove", bd=1)
                    row.pack(fill="x", padx=5, pady=3)

                    tk.Label(
                        row, text=f"ID: {id_soal} | Jawaban: {jawaban} | {os.path.basename(path)}",
                        font=("Arial", 10), bg="#ffffff", anchor="w"
                    ).pack(side="left", fill="x", expand=True, padx=5, pady=3)

                    tk.Button(
                        row, text="🗑️ Hapus", command=lambda id=id_soal: self.hapus_soal(id),
                        bg="#d32f2f", fg="white", font=("Arial", 8)
                    ).pack(side="right", padx=3)
                    tk.Button(
                        row, text="✏️ Edit", command=lambda s=soal: self.edit_soal(s),
                        bg="#1976d2", fg="white", font=("Arial", 8)
                    ).pack(side="right", padx=3)

                canvas.pack(side="left", fill="both", expand=True)
                scroll_y.pack(side="right", fill="y")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat soal: {e}")

        tk.Button(
            self.root, text="⬅️ Kembali", command=self.show_dashboard,
            bg="#9e9e9e", fg="white"
        ).pack(pady=10)

    def hapus_soal(self, id_soal):
        if messagebox.askyesno("Konfirmasi", "Hapus soal ini?"):
            try:
                self.db.execute_query("DELETE FROM soal WHERE id = %s", (id_soal,))
                self.kelola_soal()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus: {e}")

    def edit_soal(self, soal):
        id_soal, jawaban_lama, path_lama = soal
        new_jawaban = simpledialog.askstring("Edit Jawaban", "Jawaban baru:", initialvalue=jawaban_lama)
        if new_jawaban is None:
            return

        ganti_gambar = messagebox.askyesno("Ganti Gambar?", "Ingin ganti gambar soal?")
        new_path = path_lama
        if ganti_gambar:
            file = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
            if file:
                folder = "gambar"
                os.makedirs(folder, exist_ok=True)
                nama_file = os.path.basename(file)
                dest = os.path.join(folder, nama_file)
                counter = 1
                base, ext = os.path.splitext(nama_file)
                while os.path.exists(dest):
                    nama_file = f"{base}_{counter}{ext}"
                    dest = os.path.join(folder, nama_file)
                    counter += 1
                shutil.copy2(file, dest)
                new_path = dest

        try:
            self.db.execute_query(
                "UPDATE soal SET jawaban = %s, path_gambar = %s WHERE id = %s",
                (new_jawaban, new_path, id_soal)
            )
            messagebox.showinfo("Sukses", "Soal berhasil diupdate!")
            self.kelola_soal()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengupdate: {e}")

    def kembali_ke_menu(self):
        self.root.configure(bg="#f0f8ff")
        from ui.main_menu import MainMenuUI
        MainMenuUI(self.root)