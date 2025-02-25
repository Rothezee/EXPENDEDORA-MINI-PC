from gpio_sim import GPIO
import time
import requests
import sqlite3
import threading
import time
import tkinter as tk
import json
import os
from datetime import datetime

config_file = "config.json"
registro_file = "registro.json"

# --- CONFIGURACIÓN DE PINES ---
ECOIN = 35  
SALIDA = 13  
AC = 16  
BOTON_ENTREGA = 26  
TEST = 4
TEST1 = 34
TEST2 = 35
ENTHOPER = 32  
SALHOPER = 12  
BOTON = 36  
SAL1 = 0  
BARRERA = 34  

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_FILE = "expendedora.db"

# --- CONFIGURACIÓN DE SERVIDORES ---
SERVER_HEARTBEAT = "https://www.maquinasbonus.com/esp32_project/insert_heartbeat.php"
SERVER_CIERRE = "https://www.maquinasbonus.com/esp32_project/insert_close_expendedora.php"

# --- VARIABLES DEL SISTEMA ---
cuenta = 0
fichas = 0
r_cuenta = 0
r_sal = 0
promo1_count = 0
promo2_count = 0
promo3_count = 0

# ----------CONEXION CON GUI Y LOGICA PARA GUARDAR REGISTROS---------------
def cargar_configuracion():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        return {"promociones": {}, "valor_ficha": 1.0}

def guardar_configuracion(config):
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

def iniciar_apertura():
    registro = {
        "apertura": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "fichas_expendidas": 0,
        "dinero_ingresado": 0,
        "promociones_usadas": {
            "Promo 1": 0,
            "Promo 2": 0,
            "Promo 3": 0
        }
    }
    guardar_registro(registro)
    return registro

def cargar_registro():
    if os.path.exists(registro_file):
        with open(registro_file, 'r') as f:
            return json.load(f)
    else:
        return iniciar_apertura()

def guardar_registro(registro):
    with open(registro_file, 'w') as f:
        json.dump(registro, f, indent=4)

def actualizar_registro(tipo, cantidad):
    registro = cargar_registro()
    if tipo == "ficha":
        registro["fichas_expendidas"] += cantidad
        registro["dinero_ingresado"] += cantidad * cargar_configuracion()["valor_ficha"]
    elif tipo in ["Promo 1", "Promo 2", "Promo 3"]:
        registro["promociones_usadas"][tipo] += 1
        registro["dinero_ingresado"] += cargar_configuracion()["promociones"][tipo]["precio"]
    guardar_registro(registro)

def realizar_cierre():
    registro = cargar_registro()
    registro["cierre"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    guardar_registro(registro)
    return registro

# --- CONFIGURACIÓN GPIO ---
GPIO.setmode(GPIO.BCM)
for pin in [ECOIN, AC, TEST, TEST1, TEST2, BOTON, BARRERA, ENTHOPER]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for pin in [SALIDA, SALHOPER, SAL1]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# --- CONFIGURACIÓN DE BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS config (clave TEXT PRIMARY KEY, valor INTEGER)''')
    conn.commit()
    conn.close()

def get_config(clave, default=0):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM config WHERE clave=?", (clave,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default

def set_config(clave, valor):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO config (clave, valor) VALUES (?, ?) ON CONFLICT(clave) DO UPDATE SET valor=?", (clave, valor, valor))
    conn.commit()
    conn.close()

# --- ENVÍO DE DATOS AL SERVIDOR ---
def enviar_pulso():
    data = {"device_id": "EXPENDEDORA_1"}
    try:
        response = requests.post(SERVER_HEARTBEAT, json=data)
        print("Heartbeat enviado:", response.text)
    except requests.RequestException as e:
        print("Error enviando heartbeat:", e)

    threading.Timer(60, enviar_pulso).start()  

def enviar_cierre_diario():
    global r_cuenta, r_sal, promo1_count, promo2_count, promo3_count

    data = {
        "device_id": "EXPENDEDORA_1",
        "dato1": promo3_count,
        "dato2": r_cuenta,
        "dato3": promo1_count,
        "dato4": promo2_count,
        "dato5": r_sal
    }
    
    try:
        response = requests.post(SERVER_CIERRE, json=data)
        print("Cierre enviado:", response.text)
    except requests.RequestException as e:
        print("Error enviando cierre:", e)

    r_cuenta = r_sal = promo1_count = promo2_count = promo3_count = 0  

# --- MANEJO DE INTERFAZ GRÁFICA (TKINTER) ---
class ExpendedoraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expendedora de Fichas")
        self.root.geometry("400x300")

        # Etiquetas para mostrar los datos
        self.label_cuenta = tk.Label(root, text="Dinero ingresado: 0", font=("Arial", 14))
        self.label_cuenta.pack(pady=10)

        self.label_fichas = tk.Label(root, text="Fichas disponibles: 0", font=("Arial", 14))
        self.label_fichas.pack(pady=10)

        self.boton_convertir = tk.Button(root, text="Convertir Dinero a Fichas", command=convertir_fichas, font=("Arial", 12))
        self.boton_convertir.pack(pady=10)

        self.boton_cierre = tk.Button(root, text="Enviar Cierre Diario", command=enviar_cierre_diario, font=("Arial", 12))
        self.boton_cierre.pack(pady=10)

        # Actualizar la interfaz cada 1 segundo
        self.actualizar_pantalla()

    def actualizar_pantalla(self):
        self.label_cuenta.config(text=f"Dinero ingresado: {cuenta}")
        self.label_fichas.config(text=f"Fichas disponibles: {fichas}")
        self.root.after(1000, self.actualizar_pantalla)  # Se actualiza cada segundo

# --- CONVERSIÓN DE DINERO A FICHAS ---
def convertir_fichas():
    global cuenta, fichas, r_sal

    valor1 = get_config("VALOR1", 1000)
    valor2 = get_config("VALOR2", 5000)
    valor3 = get_config("VALOR3", 10000)
    fichas1 = get_config("FICHAS1", 1)
    fichas2 = get_config("FICHAS2", 2)
    fichas3 = get_config("FICHAS3", 5)

    if cuenta >= valor1 and cuenta < valor2:
        fichas += fichas1
        cuenta -= valor1
    elif cuenta >= valor2 and cuenta < valor3:
        fichas += fichas2
        cuenta -= valor2
    elif cuenta >= valor3:
        fichas += fichas3
        cuenta -= valor3

    r_sal += fichas

# --- MANEJO DE HOPPER Y ENTREGA DE FICHAS ---
def entregar_fichas():
    global fichas

    while fichas > 0:
        GPIO.output(SALIDA, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(SALIDA, GPIO.LOW)
        fichas -= 1
        time.sleep(0.4)

# --- FUNCIONES PARA LA GUI ---
def obtener_dinero_ingresado():
    return cuenta

def obtener_fichas_disponibles():
    return fichas

def expender_fichas(cantidad):
    global fichas, cuenta
    if fichas >= cantidad:
        fichas -= cantidad
        return True
    return False

# --- PROGRAMA PRINCIPAL ---
def main():
    init_db()
    enviar_pulso()

    # Iniciar la interfaz gráfica
    root = tk.Tk()
    app = ExpendedoraGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
