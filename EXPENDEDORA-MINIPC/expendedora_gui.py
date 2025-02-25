import tkinter as tk
from tkinter import messagebox
from expendedora_core import obtener_dinero_ingresado, obtener_fichas_disponibles, expender_fichas

class ExpendedoraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expendedora - Control")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f0f0")

        # Diccionario para almacenar las configuraciones de las promociones
        self.promociones = {
            "Promo 1": {"precio": 0, "fichas": 0},
            "Promo 2": {"precio": 0, "fichas": 0},
            "Promo 3": {"precio": 0, "fichas": 0}
        }

        # Valor de cada ficha
        self.valor_ficha = 1.0

        # Contadores de la página principal
        self.contadores = {
            "fichas_expendidas": 0,
            "dinero_ingresado": 0,
            "promo1_contador": 0,
            "promo2_contador": 0,
            "promo3_contador": 0,
            "fichas_restantes": 0
        }

        # Menú lateral
        self.menu_frame = tk.Frame(root, width=200, bg="#333")
        self.menu_frame.pack(side="left", fill="y")

        tk.Label(self.menu_frame, text="Menú", bg="#333", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.menu_frame, text="Inicio", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: self.mostrar_frame(self.main_frame)).pack(pady=5)
        tk.Button(self.menu_frame, text="Configuración", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: self.mostrar_frame(self.config_frame)).pack(pady=5)
        tk.Button(self.menu_frame, text="Cierre y Reportes", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: self.mostrar_frame(self.reportes_frame)).pack(pady=5)
        tk.Button(self.menu_frame, text="Simulación", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: self.mostrar_frame(self.simulacion_frame)).pack(pady=5)

        # Página principal
        self.main_frame = tk.Frame(root, bg="#f4f4f4")
        self.contadores_frame = tk.Frame(self.main_frame, bg="#ddd", bd=2, relief="groove")
        self.contadores_frame.pack(pady=10, fill="x")

        self.contadores_labels = {}
        for key, text in [
            ("fichas_expendidas", "Fichas expendidas"),
            ("dinero_ingresado", "Dinero ingresado"),
            ("promo1_contador", "Promo 1 usadas"),
            ("promo2_contador", "Promo 2 usadas"),
            ("promo3_contador", "Promo 3 usadas"),
            ("fichas_restantes", "Fichas restantes")
        ]:
            label = tk.Label(self.contadores_frame, text=f"{text}: 0", font=("Arial", 14), bg="#ddd")
            label.pack(pady=5)
            self.contadores_labels[key] = label

        self.fichas_restantes_label = self.contadores_labels["fichas_restantes"]

        tk.Button(self.main_frame, text="Expender Fichas", command=self.elegir_fichas, bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=10)

        # Página de simulación
        self.simulacion_frame = tk.Frame(root, bg="#ffffff")
        tk.Label(self.simulacion_frame, text="Simulación de Entradas y Salidas", font=("Arial", 14, "bold"), bg="#fff").pack(pady=10)

        tk.Button(self.simulacion_frame, text="Simular Billetero", command=self.simular_billetero, bg="#007BFF", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Barrera", command=self.simular_barrera, bg="#FF5722", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Entrega de Fichas", command=self.simular_entrega_fichas, bg="#4CAF50", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Salida de Fichas", command=self.simular_salida_fichas, bg="#FFC107", fg="black", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Promo 1", command=lambda: self.simular_promo("Promo 1"), bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Promo 2", command=lambda: self.simular_promo("Promo 2"), bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Promo 3", command=lambda: self.simular_promo("Promo 3"), bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)

        # Página de configuración
        self.config_frame = tk.Frame(root, bg="#ffffff")
        tk.Label(self.config_frame, text="Configuración de Promociones", font=("Arial", 14, "bold"), bg="#fff").pack(pady=10)
        for promo in ["Promo 1", "Promo 2", "Promo 3"]:
            tk.Button(self.config_frame, text=f"Configurar {promo}", command=lambda p=promo: self.configurar_promo(p), bg="#007BFF", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.config_frame, text="Configurar Valor de Ficha", command=self.configurar_valor_ficha, bg="#007BFF", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)

        # Página de reportes y cierre del día
        self.reportes_frame = tk.Frame(root, bg="#ffffff")
        tk.Label(self.reportes_frame, text="Cierre y Reportes", font=("Arial", 14, "bold"), bg="#fff").pack(pady=10)
        tk.Button(self.reportes_frame, text="Realizar Apertura", bg="#007BFF", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.reportes_frame, text="Realizar Cierre", bg="#D32F2F", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)

        self.mostrar_frame(self.main_frame)

    def mostrar_frame(self, frame):
        for f in [self.main_frame, self.config_frame, self.reportes_frame, self.simulacion_frame]:
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    def configurar_promo(self, promo):
        config_window = tk.Toplevel(self.root)
        config_window.title(f"Configurar {promo}")
        config_window.geometry("300x250")
        config_window.configure(bg="#ffffff")
        
        tk.Label(config_window, text="Precio (en $):", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
        precio_entry = tk.Entry(config_window, font=("Arial", 12), bd=2, relief="solid")
        precio_entry.insert(0, self.promociones[promo]["precio"])
        precio_entry.pack(pady=5, padx=10, fill='x')
        
        tk.Label(config_window, text="Fichas entregadas:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
        fichas_entry = tk.Entry(config_window, font=("Arial", 12), bd=2, relief="solid")
        fichas_entry.insert(0, self.promociones[promo]["fichas"])
        fichas_entry.pack(pady=5, padx=10, fill='x')
        
        def guardar_promo():
            try:
                self.promociones[promo]["precio"] = float(precio_entry.get())
                self.promociones[promo]["fichas"] = int(fichas_entry.get())
                config_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        
        tk.Button(config_window, text="Guardar", command=guardar_promo, bg="#4CAF50", fg="white", font=("Arial", 12), bd=0).pack(pady=5)
        tk.Button(config_window, text="Cancelar", command=config_window.destroy, bg="#D32F2F", fg="white", font=("Arial", 12), bd=0).pack(pady=5)

    def configurar_valor_ficha(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Configurar Valor de Ficha")
        config_window.geometry("300x150")
        config_window.configure(bg="#ffffff")
        
        tk.Label(config_window, text="Valor de cada ficha (en $):", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
        valor_entry = tk.Entry(config_window, font=("Arial", 12), bd=2, relief="solid")
        valor_entry.insert(0, self.valor_ficha)
        valor_entry.pack(pady=5, padx=10, fill='x')
        
        def guardar_valor_ficha():
            try:
                self.valor_ficha = float(valor_entry.get())
                config_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un valor numérico válido.")
        
        tk.Button(config_window, text="Guardar", command=guardar_valor_ficha, bg="#4CAF50", fg="white", font=("Arial", 12), bd=0).pack(pady=5)
        tk.Button(config_window, text="Cancelar", command=config_window.destroy, bg="#D32F2F", fg="white", font=("Arial", 12), bd=0).pack(pady=5)

    def elegir_fichas(self):
        fichas_window = tk.Toplevel(self.root)
        fichas_window.title("Elegir cantidad de fichas")
        fichas_window.geometry("300x150")
        fichas_window.configure(bg="#ffffff")
        
        tk.Label(fichas_window, text="Cantidad de fichas a expender:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
        fichas_entry = tk.Entry(fichas_window, font=("Arial", 12), bd=2, relief="solid")
        fichas_entry.pack(pady=5, padx=10, fill='x')
        
        def confirmar_fichas():
            try:
                cantidad_fichas = int(fichas_entry.get())
                self.contadores["fichas_restantes"] = cantidad_fichas
                self.fichas_restantes_label.config(text=f"Fichas restantes: {self.contadores['fichas_restantes']}")
                self.contadores["dinero_ingresado"] += cantidad_fichas * self.valor_ficha
                self.contadores_labels["dinero_ingresado"].config(text=f"Dinero ingresado: ${self.contadores['dinero_ingresado']:.2f}")
                fichas_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un valor numérico válido.")
        
        tk.Button(fichas_window, text="Confirmar", command=confirmar_fichas, bg="#007BFF", fg="white", font=("Arial", 12), bd=0).pack(pady=5)
        tk.Button(fichas_window, text="Cancelar", command=fichas_window.destroy, bg="#D32F2F", fg="white", font=("Arial", 12), bd=0).pack(pady=5)

    def expender_fichas_gui(self):
        if self.contadores["fichas_restantes"] > 0:
            if expender_fichas(1):
                self.contadores["fichas_restantes"] -= 1
                self.fichas_restantes_label.config(text=f"Fichas restantes: {self.contadores['fichas_restantes']}")
                self.contadores["fichas_expendidas"] += 1
                self.contadores_labels["fichas_expendidas"].config(text=f"Fichas expendidas: {self.contadores['fichas_expendidas']}")
        else:
            messagebox.showerror("Error", "No hay suficientes fichas.")

    def simular_billetero(self):
        messagebox.showinfo("Simulación", "Billetero activado: Se ha ingresado dinero.")

    def simular_barrera(self):
        messagebox.showinfo("Simulación", "Barrera activada: Se detectó una ficha.")

    def simular_entrega_fichas(self):
        messagebox.showinfo("Simulación", "Se están entregando fichas.")
        
    def simular_salida_fichas(self):
        if self.contadores["fichas_restantes"] > 0:
            self.contadores["fichas_expendidas"] += 1
            self.contadores["fichas_restantes"] -= 1
            self.contadores_labels["fichas_expendidas"].config(text=f"Fichas expendidas: {self.contadores['fichas_expendidas']}")
            self.fichas_restantes_label.config(text=f"Fichas restantes: {self.contadores['fichas_restantes']}")
        else:
            messagebox.showerror("Error", "No hay suficientes fichas.")
            
    def simular_promo(self, promo):
        self.contadores["fichas_restantes"] += self.promociones[promo]["fichas"]
        self.contadores_labels["fichas_restantes"].config(text=f"Fichas restantes: {self.contadores['fichas_restantes']}")
        self.contadores["dinero_ingresado"] += self.promociones[promo]["precio"]
        self.contadores_labels["dinero_ingresado"].config(text=f"Dinero ingresado: ${self.contadores['dinero_ingresado']:.2f}")
        self.contadores[f"{promo.lower()}_contador"] += 1
        self.contadores_labels[f"{promo.lower()}_contador"].config(text=f"{promo} usadas: {self.contadores[f'{promo.lower()}_contador']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpendedoraGUI(root)
    root.mainloop()
