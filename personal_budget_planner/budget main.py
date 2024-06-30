import tkinter as tk
from tkinter import messagebox, simpledialog
from database import BudgetDatabase
from datetime import datetime
from tkinter import ttk
from budget_entry_app import IncomeEntryApp, ExpenseEntryApp
import smtplib
from email.mime.text import MIMEText

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kişisel Bütçe Planlayıcı")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"400x300+{int((screen_width-400)/2)}+{int((screen_height-300)/2)}")

        self.db = BudgetDatabase()

        self.create_first_window()
        # self.open_kayit_window()
        # self.open_uyegirisi_window()

    def create_first_window(self):
        tk.Label(self.root, text="Kişisel Bütçe Planlayıcıya Hoşgeldiniz").pack(pady=10)
        tk.Button(self.root, text="Kayıt Ol", command=self.open_kayit_window).pack(pady=5)
        tk.Button(self.root, text="Üye Girişi", command=self.open_uyegirisi_window).pack(pady=5)
    
    def open_kayit_window(self):
        self.root.withdraw()  # Ana pencereyi gizle
        root2 = tk.Toplevel(self.root)  # Yeni pencere oluştur
        app2 = UserRegisterApp(root2, self.db)  # Yeni pencere için kullanıcı kayıt uygulama objesi oluştur
        root2.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root2))  # Yeni pencere kapatılınca ana pencereyi tekrar göster
        
    def open_uyegirisi_window(self):
        self.root.withdraw()  # Ana pencereyi gizle
        root2 = tk.Toplevel(self.root)  # Yeni pencere oluştur
        app2 = UserLoginApp(root2, self.db)  # Yeni pencere için kullanıcı girişi uygulama objesi oluştur
        root2.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root2))  # Yeni pencere kapatılınca ana pencereyi tekrar göster
        
    
    def on_closing(self,window):
        window.destroy()  # Açık olan pencereyi kapat
        self.root.deiconify()  # Ana pencereyi tekrar göster
        self.root.focus_set()  # Ana pencereyi odaklan
    

class UserRegisterApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Kayıt Ol")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"400x200+{int((screen_width-400)/2)}+{int((screen_height-200)/2)}")

        tk.Label(self.root, text="Ad:").pack(pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Soyad:").pack(pady=5)
        self.surname_entry = tk.Entry(self.root)
        self.surname_entry.pack(pady=5)

        tk.Label(self.root, text="Yaş:").pack(pady=5)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.pack(pady=5)

        tk.Label(self.root, text="E-posta:").pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Şifre:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Kayıt Ol", command=self.register_user).pack(pady=10)
    
    def send_email(self, email, subject, message):
        # E-posta gönderenin bilgileri
        sender_email = "your_email@example.com"
        sender_password = "your_password"

        # E-posta mesajını oluştur
        msg = MIMEText(message)
        msg['kişisel bütçe planlayıcısına hoşgeldiniz kaydınızı onaylayın'] = subject
        msg['From kişiselbütçeplanlayıcı'] = sender_email
        msg['To'] = email

        # SMTP sunucusuna bağlan
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()  # Güvenli bağlantı için TLS başlat
            server.login(sender_email, sender_password)  # SMTP sunucusuna giriş yap

            # E-postayı gönder
            server.sendmail(sender_email,email, msg.as_string())

    def register_user(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not name or not email or not password:
            messagebox.showerror("Hata", "Ad, email ve şifre alanları boş bırakılamaz.")
            return

        try:
            password = int(password)
        except ValueError:
            messagebox.showerror("Hata", "Şifre yalnızca sayılardan oluşabilir.")
            return
        
        user = self.db.get_user_by_email(email)
        if user:
            messagebox.showerror("Hata", "Bu e-posta adresi zaten kayıtlı.")
            return

        self.db.add_user(name, surname, age, email, password)
        messagebox.showinfo("Başarılı", "Kullanıcı kaydedildi.")
        self.clear_entries()
        self.send_email(email, "Kaydınızı Onaylayın", f"Merhaba {name}, kaydınız başarıyla tamamlandı!")
        self.root.destroy()  # Kayıt penceresini kapat
        self.root.master.deiconify()  # Ana pencereyi tekrar göster

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.root.destroy()  # Kayıt penceresini kapat
    
class UserLoginApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Üye Girişi")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"400x200+{int((screen_width-400)/2)}+{int((screen_height-200)/2)}")

        tk.Label(self.root, text="E-posta:").pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Şifre:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Giriş Yap", command=self.login_user).pack(pady=10)

    def login_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Hata", "E-posta ve şifre alanları boş bırakılamaz.")
            return

        messagebox.showinfo("Başarılı", "Giriş başarılı.")
        # self.root.destroy()  # Giriş penceresini kapat
        root2 = tk.Tk()  # Ana pencere oluştur
        app3 = BudgetEntryApp(root2, self.db)  # BudgetEntryApp'i aç

class BudgetEntryApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Gelir/Gider Girişi")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"400x300+{int((screen_width-400)/2)}+{int((screen_height-300)/2)}")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Gelir mi Gider mi?").pack(pady=10)
        tk.Button(self.root, text="Gelir Girişi", command=self.income_entry_window).pack()
        tk.Button(self.root, text="Gider Girişi", command=self.expense_entry_window).pack()
        tk.Button(self.root, text="Bütçeyi Hesapla", command=self.calculate_budget).pack(pady=10)

        self.total_income_label = tk.Label(self.root, text="Toplam Gelir: 0")
        self.total_income_label.pack(pady=5)
        self.total_expense_label = tk.Label(self.root, text="Toplam Gider: 0")
        self.total_expense_label.pack(pady=5)

        self.update_total_budget()

    def update_total_budget(self):
        total_income = self.db.get_total_income()
        total_expense = self.db.get_total_expense()

        self.total_income_label.config(text=f"Toplam Gelir: {total_income}")
        self.total_expense_label.config(text=f"Toplam Gider: {total_expense}")
    
    def calculate_budget(self):
        total_income = self.db.get_total_income()
        total_expense = self.db.get_total_expense()
        budget = total_income - total_expense

        messagebox.showinfo("Bütçe Hesabı", f"Mevcut bütçeniz: {budget}")

    def income_entry_window(self):
        root3 = tk.Toplevel(self.root)
        app3 = IncomeEntryApp(root3, self.db)
        root3.protocol("WM_DELETE_WINDOW", self.update_total_budget)  # Gelir penceresi kapatılınca bütçeyi güncelle

    def income_entry_window(self):
        root3 = tk.Toplevel(self.root)
        app3 = IncomeEntryApp(root3, self.db)

    def expense_entry_window(self):
        root3 = tk.Toplevel(self.root)
        app3 = ExpenseEntryApp(root3, self.db)

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()


