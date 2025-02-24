import tkinter as tk
from tkinter import messagebox

# Diccionario para almacenar las configuraciones de las promociones
promociones = {
    "Promo 1": {"precio": "", "fichas": ""},
    "Promo 2": {"precio": "", "fichas": ""},
    "Promo 3": {"precio": "", "fichas": ""}
}

# Contadores de la página principal
contadores = {
    "fichas_expendidas": 0,
    "dinero_ingresado": 0,
    "promo1_contador": 0,
    "promo2_contador": 0,
    "promo3_contador": 0,
    "fichas_restantes": 0
}

def configurar_promo(promo):
    config_window = tk.Toplevel(root)
    config_window.title(f"Configurar {promo}")
    config_window.geometry("300x200")
    config_window.configure(bg="#ffffff")
    
    tk.Label(config_window, text="Precio (en $):", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
    precio_entry = tk.Entry(config_window, font=("Arial", 12), bd=2, relief="solid")
    precio_entry.insert(0, promociones[promo]["precio"])
    precio_entry.pack(pady=5, padx=10, fill='x')
    
    tk.Label(config_window, text="Fichas entregadas:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
    fichas_entry = tk.Entry(config_window, font=("Arial", 12), bd=2, relief="solid")
    fichas_entry.insert(0, promociones[promo]["fichas"])
    fichas_entry.pack(pady=5, padx=10, fill='x')
    
    def guardar_promo():
        try:
            promociones[promo]["precio"] = float(precio_entry.get())
            promociones[promo]["fichas"] = int(fichas_entry.get())
            config_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
    
    tk.Button(config_window, text="Guardar", command=guardar_promo, bg="#4CAF50", fg="white", font=("Arial", 12), bd=0).pack(pady=5)
    tk.Button(config_window, text="Cancelar", command=config_window.destroy, bg="#D32F2F", fg="white", font=("Arial", 12), bd=0).pack(pady=5)

def actualizar_contador_fichas():
    if contadores["fichas_restantes"] > 0:
        contadores["fichas_restantes"] -= 1
        fichas_restantes_label.config(text=f"Fichas restantes: {contadores['fichas_restantes']}")
        root.after(1000, actualizar_contador_fichas)
    elif contadores["fichas_restantes"] == 0:
        messagebox.showinfo("Fichas Entregadas", "Todas las fichas han sido entregadas.")

def elegir_fichas():
    fichas_window = tk.Toplevel(root)
    fichas_window.title("Elegir cantidad de fichas")
    fichas_window.geometry("300x150")
    fichas_window.configure(bg="#ffffff")
    
    tk.Label(fichas_window, text="Cantidad de fichas a expender:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
    fichas_entry = tk.Entry(fichas_window, font=("Arial", 12), bd=2, relief="solid")
    fichas_entry.pack(pady=5, padx=10, fill='x')
    
    def confirmar_fichas():
        try:
            contadores["fichas_restantes"] = int(fichas_entry.get())
            fichas_restantes_label.config(text=f"Fichas restantes: {contadores['fichas_restantes']}")
            actualizar_contador_fichas()
            fichas_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido.")
    
    tk.Button(fichas_window, text="Confirmar", command=confirmar_fichas, bg="#007BFF", fg="white", font=("Arial", 12), bd=0).pack(pady=5)
    tk.Button(fichas_window, text="Cancelar", command=fichas_window.destroy, bg="#D32F2F", fg="white", font=("Arial", 12), bd=0).pack(pady=5)

def mostrar_frame(frame):
    for f in [main_frame, config_frame, reportes_frame]:
        f.pack_forget()
    frame.pack(fill="both", expand=True)

def actualizar_contadores():
    for key, label in contadores_labels.items():
        label.config(text=f"{key.replace('_', ' ').title()}: {contadores[key]}")

root = tk.Tk()
root.title("Expendedora - Control")
root.geometry("800x500")
root.configure(bg="#f0f0f0")

# Menú lateral
menu_frame = tk.Frame(root, width=200, bg="#333")
menu_frame.pack(side="left", fill="y")

tk.Label(menu_frame, text="Menú", bg="#333", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(menu_frame, text="Inicio", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: mostrar_frame(main_frame)).pack(pady=5)
tk.Button(menu_frame, text="Configuración", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: mostrar_frame(config_frame)).pack(pady=5)
tk.Button(menu_frame, text="Cierre y Reportes", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: mostrar_frame(reportes_frame)).pack(pady=5)

# Página principal
main_frame = tk.Frame(root, bg="#f4f4f4")
contadores_frame = tk.Frame(main_frame, bg="#ddd", bd=2, relief="groove")
contadores_frame.pack(pady=10, fill="x")

contadores_labels = {}
for key, text in [
    ("fichas_expendidas", "Fichas expendidas"),
    ("dinero_ingresado", "Dinero ingresado"),
    ("promo1_contador", "Promo 1 usadas"),
    ("promo2_contador", "Promo 2 usadas"),
    ("promo3_contador", "Promo 3 usadas"),
    ("fichas_restantes", "Fichas restantes")
]:
    label = tk.Label(contadores_frame, text=f"{text}: 0", font=("Arial", 14), bg="#ddd")
    label.pack(pady=5)
    contadores_labels[key] = label

fichas_restantes_label = contadores_labels["fichas_restantes"]

tk.Button(main_frame, text="Expender Fichas", command=elegir_fichas, bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=10)

# Páginas de configuración y reportes
config_frame = tk.Frame(root, bg="#ffffff")
reportes_frame = tk.Frame(root, bg="#ffffff")

tk.Label(config_frame, text="Configuración de Promociones", font=("Arial", 14, "bold"), bg="#fff").pack(pady=10)
for promo in ["Promo 1", "Promo 2", "Promo 3"]:
    tk.Button(config_frame, text=f"Configurar {promo}", command=lambda p=promo: configurar_promo(p), bg="#007BFF", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)

tk.Label(reportes_frame, text="Cierre y Reportes", font=("Arial", 14, "bold"), bg="#fff").pack(pady=10)
tk.Button(reportes_frame, text="Realizar Apertura", bg="#007BFF", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
tk.Button(reportes_frame, text="Realizar Cierre", bg="#D32F2F", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)

mostrar_frame(main_frame)
root.mainloop()