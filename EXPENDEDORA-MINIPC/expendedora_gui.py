import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import requests
from User_management import UserManagement

url = "http://192.168.1.33/esp32_project/expendedora/insert_close_expendedora.php"  # URL DE CIERRES y subcierres
urlDatos = "http://192.168.1.33/esp32_project/expendedora/insert_data_expendedora.php"  # URL DE REPORTES
urlSubcierre = "http://192.168.1.33/esp32_project/expendedora/insert_subcierre_expendedora.php"  # URL DE SUBCIERRES


class ExpendedoraGUI:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Expendedora - Control")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f0f0")

        # Inicializar variables de configuración
        self.promociones = {
            "Promo 1": {"precio": 0, "fichas": 0},
            "Promo 2": {"precio": 0, "fichas": 0},
            "Promo 3": {"precio": 0, "fichas": 0}
        }
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

        # Contadores de apertura
        self.contadores_apertura = {
            "fichas_expendidas": 0,
            "dinero_ingresado": 0,
            "promo1_contador": 0,
            "promo2_contador": 0,
            "promo3_contador": 0,
            "fichas_restantes": 0
        }

        # Contadores parciales
        self.contadores_parciales = {
            "fichas_expendidas": 0,
            "dinero_ingresado": 0,
            "promo1_contador": 0,
            "promo2_contador": 0,
            "promo3_contador": 0,
            "fichas_restantes": 0
        }

        # Archivo de configuración
        self.config_file = "config.json"
        self.cargar_configuracion()

        # Header
        self.header_frame = tk.Frame(root, bg="#333")
        self.header_frame.pack(side="top", fill="x")

        tk.Label(self.header_frame, text="Expendedora - Control", bg="#333", fg="white", font=("Arial", 16, "bold")).pack(side="left", padx=10)
        tk.Label(self.header_frame, text=f"{username}", bg="#333", fg="white", font=("Arial", 12)).pack(side="right", padx=10)
        

        # Menú lateral
        self.menu_frame = tk.Frame(root, width=200, bg="#333")
        self.menu_frame.pack(side="left", fill="y")

        tk.Label(self.menu_frame, text="Menú", bg="#333", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.menu_frame, text="Inicio", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: self.mostrar_frame(self.main_frame)).pack(pady=5)
        tk.Button(self.menu_frame, text="Configuración", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: self.mostrar_frame(self.config_frame)).pack(pady=5)
        tk.Button(self.menu_frame, text="Cierre y Reportes", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: self.mostrar_frame(self.reportes_frame)).pack(pady=5)
        tk.Button(self.menu_frame, text="Simulación", bg="#444", fg="white", font=("Arial", 12), width=20, command=lambda: self.mostrar_frame(self.simulacion_frame)).pack(pady=5)
        tk.Button(self.menu_frame, text="Cerrar Sesión", bg="#D32F2F", fg="white", font=("Arial", 12), width=20, command=self.cerrar_sesion).pack(pady=(50, 5))

        # Página principal
        self.main_frame = tk.Frame(root, bg="#f4f4f4")
        self.main_frame.pack(fill="both", expand=True)

        # Frame para contadores
        self.contadores_frame = tk.Frame(self.main_frame, bg="#ddd", bd=2, relief="groove")
        self.contadores_frame.pack(side="left", padx=10, pady=10, fill="y")

        self.contadores_labels = {}
        for key, text in [
            ("fichas_expendidas", "Fichas expendidas"),
            ("dinero_ingresado", "Dinero ingresado"),
            ("promo1_contador", "Promo 1 usadas"),
            ("promo2_contador", "Promo 2 usadas"),
            ("promo3_contador", "Promo 3 usadas"),
            ("fichas_restantes", "Fichas restantes")
        ]:
            label = tk.Label(self.contadores_frame, text=f"{text}: {self.contadores[key]}", font=("Arial", 14), bg="#ddd")
            label.pack(pady=5)
            self.contadores_labels[key] = label

        self.fichas_restantes_label = self.contadores_labels["fichas_restantes"]

        # Frame para botones de acción
        self.botones_frame = tk.Frame(self.main_frame, bg="#f4f4f4")
        self.botones_frame.pack(side="right", padx=10, pady=10, fill="y")

        # Botones de acción en la página principal
        tk.Button(self.botones_frame, text="Expender Fichas", command=self.elegir_fichas, bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.botones_frame, text="Simular Promo 1", command=lambda: self.simular_promo("Promo 1"), bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.botones_frame, text="Simular Promo 2", command=lambda: self.simular_promo("Promo 2"), bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.botones_frame, text="Simular Promo 3", command=lambda: self.simular_promo("Promo 3"), bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.botones_frame, text="Simular Salida de Fichas", command=self.simular_salida_fichas, bg="#FFC107", fg="black", font=("Arial", 12), width=20, bd=0).pack(pady=5)

        # Página de simulación
        self.simulacion_frame = tk.Frame(root, bg="#ffffff")
        tk.Label(self.simulacion_frame, text="Simulación de Entradas y Salidas", font=("Arial", 14, "bold"), bg="#fff").pack(pady=10)

        tk.Button(self.simulacion_frame, text="Simular Billetero", command=self.simular_billetero, bg="#007BFF", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Barrera", command=self.simular_barrera, bg="#FF5722", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Promo 1", command=lambda: self.simular_promo("Promo 1"), bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Promo 2", command=lambda: self.simular_promo("Promo 2"), bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Promo 3", command=lambda: self.simular_promo("Promo 3"), bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.simulacion_frame, text="Simular Entrega de Fichas", command=self.simular_entrega_fichas, bg="#4CAF50", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)

        # Página de configuración
        self.config_frame = tk.Frame(root, bg="#ffffff")
        tk.Label(self.config_frame, text="Configuración de Promociones", font=("Arial", 14, "bold"), bg="#fff").pack(pady=10)
        for promo in ["Promo 1", "Promo 2", "Promo 3"]:
            tk.Button(self.config_frame, text=f"Configurar {promo}", command=lambda p=promo: self.configurar_promo(p), bg="#007BFF", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.config_frame, text="Configurar Valor de Ficha", command=self.configurar_valor_ficha, bg="#007BFF", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)

        # Página de reportes y cierre del día
        self.reportes_frame = tk.Frame(root, bg="#ffffff")
        tk.Label(self.reportes_frame, text="Cierre y Reportes", font=("Arial", 14, "bold"), bg="#fff").pack(pady=10)
        tk.Button(self.reportes_frame, text="Realizar Apertura", command=self.realizar_apertura, bg="#007BFF", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.reportes_frame, text="Realizar Cierre", command=self.realizar_cierre, bg="#D32F2F", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)
        tk.Button(self.reportes_frame, text="Realizar Cierre Parcial", command=self.realizar_cierre_parcial, bg="#FF9800", fg="white", font=("Arial", 12), width=20, bd=0).pack(pady=5)  # Botón de Cierre Parcial

        # Footer
        self.footer_frame = tk.Frame(root, bg="#333")
        self.footer_frame.pack(side="bottom", fill="x")

        self.footer_label = tk.Label(self.footer_frame, text="", bg="#333", fg="white", font=("Arial", 12))
        self.footer_label.pack(pady=5)

        self.actualizar_fecha_hora()  # Llamar a la función para mostrar la fecha y hora

        self.mostrar_frame(self.main_frame)

    def enviar_datos_al_servidor(self):
        datos = {
            "device_id": "EXPENDEDORA_1",
            "dato1": self.contadores['fichas_expendidas'],
            "dato2": self.contadores['dinero_ingresado'],
        }

        try:
            response = requests.post(urlDatos, json=datos)
            if response.status_code == 200:
                print("Datos enviados con éxito")
            else:
                print(f"Error al enviar datos: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servidor: {e}")

    def mostrar_frame(self, frame):
        for f in [self.main_frame, self.config_frame, self.reportes_frame, self.simulacion_frame]:
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    def cargar_configuracion(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.promociones = config.get("promociones", self.promociones)
                self.valor_ficha = config.get("valor_ficha", self.valor_ficha)
                self.contadores = config.get("contadores", self.contadores)
                self.contadores_apertura = config.get("contadores_apertura", self.contadores_apertura)
                self.contadores_parciales = config.get("contadores_parciales", self.contadores_parciales)
        else:
            self.guardar_configuracion()

    def guardar_configuracion(self):
        config = {
            "promociones": self.promociones,
            "valor_ficha": self.valor_ficha,
            "contadores": self.contadores,
            "contadores_apertura": self.contadores_apertura,
            "contadores_parciales": self.contadores_parciales
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

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
                self.guardar_configuracion()
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
                self.guardar_configuracion()
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
                self.contadores["fichas_restantes"] += cantidad_fichas  # Sumar fichas en lugar de asignar
                self.contadores_apertura["fichas_restantes"] += cantidad_fichas  # Actualizar el contador de apertura
                self.contadores_parciales["fichas_restantes"] += cantidad_fichas  # Actualizar el contador parcial
                self.fichas_restantes_label.config(text=f"Fichas restantes: {self.contadores['fichas_restantes']}")
                self.contadores["dinero_ingresado"] += cantidad_fichas * self.valor_ficha
                self.contadores_apertura["dinero_ingresado"] += cantidad_fichas * self.valor_ficha  # Actualizar el contador de apertura
                self.contadores_parciales["dinero_ingresado"] += cantidad_fichas * self.valor_ficha  # Actualizar el
                self.contadores_parciales["dinero_ingresado"] += cantidad_fichas * self.valor_ficha  # Actualizar el contador parcial
                self.fichas_restantes_label.config(text=f"Fichas restantes: {self.contadores['fichas_restantes']}")
                self.contadores["dinero_ingresado"] += cantidad_fichas * self.valor_ficha
                self.contadores_apertura["dinero_ingresado"] += cantidad_fichas * self.valor_ficha  # Actualizar el contador de apertura
                self.contadores_parciales["dinero_ingresado"] += cantidad_fichas * self.valor_ficha  # Actualizar el contador parcial
                self.contadores_labels["dinero_ingresado"].config(text=f"Dinero ingresado: ${self.contadores['dinero_ingresado']:.2f}")
                self.guardar_configuracion()  # Guardar los contadores actualizados
                self.actualizar_contadores_gui()
                fichas_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un valor numérico válido.")
        
        tk.Button(fichas_window, text="Confirmar", command=confirmar_fichas, bg="#007BFF", fg="white", font=("Arial", 12), bd=0).pack(pady=5)
        tk.Button(fichas_window, text="Cancelar", command=fichas_window.destroy, bg="#D32F2F", fg="white", font=("Arial", 12), bd=0).pack(pady=5)

    def realizar_apertura(self):
        # Inicia la apertura del día
        self.contadores_apertura = {
            "fichas_expendidas": 0,
            "dinero_ingresado": 0,
            "promo1_contador": 0,
            "promo2_contador": 0,
            "promo3_contador": 0,
            "fichas_restantes": 0
        }
        self.contadores_parciales = {
            "fichas_expendidas": 0,
            "dinero_ingresado": 0,
            "promo1_contador": 0,
            "promo2_contador": 0,
            "promo3_contador": 0,
            "fichas_restantes": 0
        }
        self.actualizar_contadores_gui()
        self.guardar_configuracion()
        messagebox.showinfo("Apertura", "Apertura del día realizada con éxito.")

    def realizar_cierre(self):
        # Realiza el cierre del día
        cierre_info = {
            "device_id": "EXPENDEDORA_1",
            "fichas_expendidas": self.contadores_apertura['fichas_expendidas'],
            "dinero_ingresado": self.contadores_apertura['dinero_ingresado'],
            "promo1_contador": self.contadores_apertura['promo1_contador'],
            "promo2_contador": self.contadores_apertura['promo2_contador'],
            "promo3_contador": self.contadores_apertura['promo3_contador'],
            "fichas_restantes": self.contadores_apertura['fichas_restantes']
        }
        info = {
            "id_expendedora": "EXPENDEDORA_1",
            "fichas": self.contadores_apertura['fichas_expendidas'],
            "dinero": self.contadores_apertura['dinero_ingresado'],
            "p1": self.contadores_apertura['promo1_contador'],
            "p2": self.contadores_apertura['promo2_contador'],
            "p3": self.contadores_apertura['promo3_contador']
        }
        mensaje_cierre = (
            f"Fichas expendidas: {cierre_info['fichas_expendidas']}\n"
            f"Dinero ingresado: ${cierre_info['dinero_ingresado']:.2f}\n"
            f"Promo 1 usadas: {cierre_info['promo1_contador']}\n"
            f"Promo 2 usadas: {cierre_info['promo2_contador']}\n"
            f"Promo 3 usadas: {cierre_info['promo3_contador']}\n"
            f"Fichas restantes: {cierre_info['fichas_restantes']}"
        )
        messagebox.showinfo("Cierre", f"Cierre del día realizado:\n{mensaje_cierre}")
        
        # Enviar datos al servidor
        try:
            response = requests.post(url, json=info)
            if response.status_code == 200:
                print("Datos de cierre enviados con éxito")
            else:
                print(f"Error al enviar datos de cierre: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servidor: {e}")
        
        self.contadores_apertura = {
            "fichas_expendidas": 0,
            "dinero_ingresado": 0,
            "promo1_contador": 0,
            "promo2_contador": 0,
            "promo3_contador": 0,
            "fichas_restantes": 0
        }
        self.contadores_parciales = {
            "fichas_expendidas": 0,
            "dinero_ingresado": 0,
            "promo1_contador": 0,
            "promo2_contador": 0,
            "promo3_contador": 0,
            "fichas_restantes": 0
        }
        self.guardar_configuracion()

    def realizar_cierre_parcial(self):
        # Realiza el cierre parcial
        subcierre_info = {
            "device_id": "EXPENDEDORA_1",
            "partial_fichas": self.contadores_parciales['fichas_expendidas'],
            "partial_dinero": self.contadores_parciales['dinero_ingresado'],
            "partial_p1": self.contadores_parciales['promo1_contador'],
            "partial_p2": self.contadores_parciales['promo2_contador'],
            "partial_p3": self.contadores_parciales['promo3_contador'],
            "employee_id": self.username  # Reemplazar con el ID del empleado actual
        }
        
        mensaje_subcierre = (
            f"Fichas expendidas: {subcierre_info['partial_fichas']}\n"
            f"Dinero ingresado: ${subcierre_info['partial_dinero']:.2f}\n"
            f"Promo 1 usadas: {subcierre_info['partial_p1']}\n"
            f"Promo 2 usadas: {subcierre_info['partial_p2']}\n"
            f"Promo 3 usadas: {subcierre_info['partial_p3']}"
        )
        messagebox.showinfo("Cierre Parcial", f"Cierre parcial realizado:\n{mensaje_subcierre}")
        
        # Enviar datos al servidor
        try:
            response = requests.post(urlSubcierre, json=subcierre_info)
            if response.status_code == 200:
                print("Datos de cierre parcial enviados con éxito")
            else:
                print(f"Error al enviar datos de cierre parcial: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servidor: {e}")

        # Reiniciar los contadores parciales
        self.contadores_parciales = {
            "fichas_expendidas": 0,
            "dinero_ingresado": 0,
            "promo1_contador": 0,
            "promo2_contador": 0,
            "promo3_contador": 0,
            "fichas_restantes": 0
        }
        self.guardar_configuracion()

    def cerrar_sesion(self):
        # Realizar cierre parcial antes de cerrar sesión
        messagebox.showinfo("Cerrar Sesión", "La sesión ha sido cerrada.")
        self.root.destroy()
        user_management = UserManagement(self.root)
        user_management.run()  # No se pasa ningún argumento aquí

    def actualizar_contadores_gui(self):
        for key in self.contadores_labels:
            self.contadores_labels[key].config(text=f"{key.replace('_', ' ').title()}: {self.contadores[key]}")

    def expender_fichas_gui(self):
        if self.contadores["fichas_restantes"] > 0:
            self.contadores["fichas_restantes"] -= 1
            self.contadores_apertura["fichas_restantes"] -= 1  # Actualizar el contador de apertura
            self.contadores_parciales["fichas_restantes"] -= 1  # Actualizar el contador parcial
            self.contadores["fichas_expendidas"] += 1
            self.contadores_apertura["fichas_expendidas"] += 1  # Actualizar el contador de apertura
            self.contadores_parciales["fichas_expendidas"] += 1  # Actualizar el contador parcial
            self.actualizar_contadores_gui()
            self.guardar_configuracion()
            if self.contadores["fichas_restantes"] == 0:
                self.enviar_datos_al_servidor()
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
            self.contadores_apertura["fichas_expendidas"] += 1  # Actualizar el contador de apertura
            self.contadores_parciales["fichas_expendidas"] += 1  # Actualizar el contador parcial
            self.contadores["fichas_restantes"] -= 1
            self.contadores_apertura["fichas_restantes"] -= 1  # Actualizar el contador de apertura
            self.contadores_parciales["fichas_restantes"] -= 1  # Actualizar el contador parcial
            self.actualizar_contadores_gui()
            self.guardar_configuracion()
            if self.contadores["fichas_restantes"] == 0:
                self.enviar_datos_al_servidor()
        else:
            messagebox.showerror("Error", "No hay suficientes fichas.")
            
    def simular_promo(self, promo):
        # Aumentar el número de fichas restantes según la promoción
        self.contadores["fichas_restantes"] += self.promociones[promo]["fichas"]  # Sumar fichas en lugar de asignar
        self.contadores_apertura["fichas_restantes"] += self.promociones[promo]["fichas"]  # Actualizar el contador de apertura
        self.contadores_parciales["fichas_restantes"] += self.promociones[promo]["fichas"]  # Actualizar el contador parcial
        self.contadores_labels["fichas_restantes"].config(text=f"Fichas restantes: {self.contadores['fichas_restantes']}")
        
        # Aumentar el dinero ingresado según el precio de la promoción
        self.contadores["dinero_ingresado"] += self.promociones[promo]["precio"]
        self.contadores_apertura["dinero_ingresado"] += self.promociones[promo]["precio"]  # Actualizar el contador de apertura
        self.contadores_parciales["dinero_ingresado"] += self.promociones[promo]["precio"]  # Actualizar el contador parcial
        self.contadores_labels["dinero_ingresado"].config(text=f"Dinero ingresado: ${self.contadores['dinero_ingresado']:.2f}")

        # Diccionario para simular el switch
        promo_contadores = {
            "Promo 1": "promo1_contador",
            "Promo 2": "promo2_contador",
            "Promo 3": "promo3_contador"
        }

        # Incrementar el contador de la promoción correspondiente
        if promo in promo_contadores:
            self.contadores[promo_contadores[promo]] += 1
            self.contadores_apertura[promo_contadores[promo]] += 1  # Actualizar el contador de apertura
            self.contadores_parciales[promo_contadores[promo]] += 1  # Actualizar el contador parcial
            self.contadores_labels[promo_contadores[promo]].config(text=f"{promo} usadas: {self.contadores[promo_contadores[promo]]}")
        else:
            messagebox.showerror("Error", "Promoción no válida.")
        
        self.guardar_configuracion()  # Guardar los contadores actualizados

    def actualizar_fecha_hora(self):
        # Obtener la fecha y hora actual
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.footer_label.config(text=current_time)  # Actualizar el label del footer
        self.footer_label.after(1000, self.actualizar_fecha_hora)  # Llamar a esta función cada segundo

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpendedoraGUI(root, "username")  # Reemplazar "username" con el nombre de usuario actual
    root.mainloop()