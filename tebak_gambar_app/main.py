# main.py

from tkinter import Tk
from ui.main_menu import MainMenuUI

if __name__ == "__main__":
    root = Tk()
    root.title("Tebak Gambar - OOP Edition")
    root.geometry("600x500")
    MainMenuUI(root)
    root.mainloop()