import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from tkcalendar import Calendar  # tkcalendar kütüphanesini için terminale pip install tkcalender yazın 
from datetime import datetime

class IncomeEntryApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Gelir Girişi")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"400x300+{int((screen_width-400)/2)}+{int((screen_height-300)/2)}")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Tutar:").pack(pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        tk.Label(self.root, text="Tarih:").pack(pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack(pady=5)
        tk.Button(self.root, text="Tarih Seç", command=self.pick_date).pack(pady=5)  # Tarih seçmek için buton

        tk.Button(self.root, text="Kaydet", command=self.save_income).pack(pady=10)

    def pick_date(self):
        date_str = simpledialog.askstring("Tarih Seç", "Lütfen tarihi giriniz (YYYY-MM-DD):")
        if date_str:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, date_str)

    def save_income(self):
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        if not amount or not date:
            messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Hata", "Tutar alanına geçerli bir sayı giriniz.")
            return

        self.db.add_transaction("Gelir", amount, "", "", date)
        messagebox.showinfo("Başarılı", "Gelir kaydedildi.")
        self.clear_entries()

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        
class ExpenseEntryApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Gider Girişi")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"400x300+{int((screen_width-400)/2)}+{int((screen_height-300)/2)}")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Tutar:").pack(pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        tk.Label(self.root, text="Tarih:").pack(pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack(pady=5)
        tk.Button(self.root, text="Tarih Seç", command=self.pick_date).pack(pady=5)  # Tarih seçmek için buton

        tk.Label(self.root, text="Kategori:").pack(pady=5)
        self.category_var = tk.StringVar()
        self.category_var.set("Ev")  # Default kategori değeri
        categories = ["Ev", "Ulaşım", "Yemek", "Giysi", "Diğer"]  # Kategori seçenekleri
        self.category_menu = tk.OptionMenu(self.root, self.category_var, *categories)
        self.category_menu.pack(pady=5)

        tk.Button(self.root, text="Kaydet", command=self.save_expense).pack(pady=10)

    def pick_date(self):
        date_str = simpledialog.askstring("Tarih Seç", "Lütfen tarihi giriniz (YYYY-MM-DD):")
        if date_str:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, date_str)

    def save_expense(self):
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        category = self.category_var.get()

        if not amount or not date:
            messagebox.showerror("Hata", "Tutar ve tarih alanlarını doldurunuz.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Hata", "Tutar alanına geçerli bir sayı giriniz.")
            return

        self.db.add_transaction("Gider", amount, category, "", date)
        messagebox.showinfo("Başarılı", "Gider kaydedildi.")
        self.clear_entries()

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseEntryApp(root, None)  # None, db'yi temsil ediyor, kodda bir veritabanı objesi olmadığı için None geçildi
    root.mainloop()