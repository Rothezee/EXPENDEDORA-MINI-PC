import threading
import tkinter as tk
from expendedora_gui import ExpendedoraGUI
from expendedora_core import enviar_pulso, init_db
from User_management import UserManagement
def start_gui():
    root = tk.Tk()
    app = ExpendedoraGUI(root)
    root.mainloop()

def main():
    # Inicializar la base de datos
    init_db()
    
    # Iniciar el envío de pulsos al servidor
    threading.Thread(target=enviar_pulso).start()
    
    # Iniciar la interfaz gráfica
    start_gui()

if __name__ == "__main__":
    app = UserManagement()
    app.run()
    main()