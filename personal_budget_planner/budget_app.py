import tkinter as tk
from tkinter import messagebox
from database import BudgetDatabase

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kişisel Bütçe Planlayıcı")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")

        self.db = BudgetDatabase()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Ad Soyad:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Label(self.root, text="E-posta:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()

        tk.Label(self.root, text="Yaş:").pack()
        self.age_entry = tk.Entry(self.root)
        self.age_entry.pack()

        tk.Button(self.root, text="Kaydet", command=self.save_user).pack()

    def save_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        age = self.age_entry.get()

        if not name or not email or not age:
            messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Hata", "Yaş alanına geçerli bir sayı giriniz.")
            return

        self.db.add_user(name, email, age)
        messagebox.showinfo("Başarılı", "Kullanıcı başarıyla kaydedildi.")
        self.open_transaction_type_window()

    def open_transaction_type_window(self):
        self.transaction_type_window = tk.Toplevel(self.root)
        self.transaction_type_window.title("Gelir/Gider Seçimi")

        tk.Label(self.transaction_type_window, text="Gelir mi Gider mi yapmak istiyorsunuz?").pack()

        tk.Button(self.transaction_type_window, text="Gelir Girişi", command=self.open_income_entry_window).pack()
        tk.Button(self.transaction_type_window, text="Gider Girişi", command=self.open_expense_entry_window).pack()

    def open_income_entry_window(self):
        self.income_entry_window = tk.Toplevel(self.transaction_type_window)
        self.income_entry_window.title("Gelir Girişi")

        tk.Label(self.income_entry_window, text="Tarih (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self.income_entry_window)
        self.date_entry.pack()

        tk.Label(self.income_entry_window, text="Miktar:").pack()
        self.amount_entry = tk.Entry(self.income_entry_window)
        self.amount_entry.pack()

        self.category = tk.StringVar()
        self.category.set("Ev")
        tk.Label(self.income_entry_window, text="Kategori:").pack()
        tk.OptionMenu(self.income_entry_window, self.category, "Ev", "Yemek", "Kıyafet", "Ulaşım", "Diğer").pack()

        tk.Button(self.income_entry_window, text="Kaydet", command=self.save_income).pack()

    def open_expense_entry_window(self):
        self.expense_entry_window = tk.Toplevel(self.transaction_type_window)
        self.expense_entry_window.title("Gider Girişi")

        tk.Label(self.expense_entry_window, text="Tarih (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self.expense_entry_window)
        self.date_entry.pack()

        tk.Label(self.expense_entry_window, text="Miktar:").pack()
        self.amount_entry = tk.Entry(self.expense_entry_window)
        self.amount_entry.pack()

        self.category = tk.StringVar()
        self.category.set("Ev")
        tk.Label(self.expense_entry_window, text="Kategori:").pack()
        tk.OptionMenu(self.expense_entry_window, self.category, "Ev", "Yemek", "Kıyafet", "Ulaşım", "Diğer").pack()

        tk.Button(self.expense_entry_window, text="Kaydet", command=self.save_expense).pack()

    def save_income(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category.get()

        if not date or not amount:
            messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Hata", "Miktar alanına geçerli bir sayı giriniz.")
            return

        self.db.add_transaction("Gelir", amount, category, date)
        messagebox.showinfo("Başarılı", "Gelir kaydedildi.")
        self.transaction_type_window.destroy()

    def save_expense(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category.get()

        if not date or not amount:
            messagebox.showerror("Hata", "Tüm alanları doldurunuz.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Hata", "Miktar alanına geçerli bir sayı giriniz.")
            return

        self.db.add_transaction("Gider", amount, category, date)
        messagebox.showinfo("Başarılı", "Gider kaydedildi.")
        self.transaction_type_window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()