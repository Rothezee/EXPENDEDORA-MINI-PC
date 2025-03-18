import tkinter as tk
from tkinter import messagebox
from .login import LoginWindow
from .register import RegisterWindow

class UserManagement:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Control de Usuarios")
        self.root.geometry("400x300")
        self.root.configure(bg="#e9ecef")  # Fondo gris claro
        self.root.resizable(False, False)

        self.main_frame = tk.Frame(self.root, bg="#e9ecef")
        self.main_frame.pack(pady=50)

        # Título
        self.title_label = tk.Label(self.main_frame, text="Gestión de Usuarios", bg="#e9ecef", fg="#343a40", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=20)

        # Estilo del botón de Login
        self.login_button = tk.Button(self.main_frame, text="Iniciar Sesión", command=self.open_login, bg="#007BFF", fg="white", font=("Arial", 12, "bold"), bd=0, padx=10, pady=5)
        self.login_button.pack(pady=10)
        self.login_button.bind("<Enter>", lambda e: self.login_button.config(bg="#0056b3"))
        self.login_button.bind("<Leave>", lambda e: self.login_button.config(bg="#007BFF"))

        # Estilo del botón de Register
        self.register_button = tk.Button(self.main_frame, text="Registrar", command=self.open_register, bg="#007BFF", fg="white", font=("Arial", 12, "bold"), bd=0, padx=10, pady=5)
        self.register_button.pack(pady=10)
        self.register_button.bind("<Enter>", lambda e: self.register_button.config(bg="#0056b3"))
        self.register_button.bind("<Leave>", lambda e: self.register_button.config(bg="#007BFF"))

    def open_login(self):
        LoginWindow(self.root)

    def open_register(self):
        RegisterWindow(self.root)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = UserManagement()
    app.run()