#!/bin/bash

# Script de configuración Kiosk Mode para Raspberry Pi 4 - Cajero Automático
# Ejecutar con: sudo bash setup_kiosk.sh

set -e  # Salir si hay algún error

echo "=========================================="
echo "  CONFIGURACIÓN KIOSK MODE PARA CAJERO   "
echo "=========================================="
echo ""

# Verificar que se ejecute como root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Este script debe ejecutarse como root (usa sudo)"
   exit 1
fi

# Configuración personalizable
CAJERO_USER="cajero"
APP_PATH="/home/$CAJERO_USER/mi_aplicacion.py"

echo "🔧 Iniciando configuración..."
echo "Usuario del cajero: $CAJERO_USER"
echo "Ruta de la aplicación: $APP_PATH"
echo ""

# 1. Actualizar sistema
echo "📦 Actualizando sistema..."
apt update && apt upgrade -y

# 2. Instalar paquetes necesarios
echo "📦 Instalando paquetes necesarios..."
apt install -y openbox xinit xserver-xorg unclutter python3 python3-pip

# 3. Crear usuario cajero
echo "👤 Creando usuario cajero..."
if id "$CAJERO_USER" &>/dev/null; then
    echo "   Usuario $CAJERO_USER ya existe"
else
    adduser --disabled-password --gecos "" $CAJERO_USER
    usermod -a -G gpio,spi,i2c,audio,video $CAJERO_USER
    echo "   Usuario $CAJERO_USER creado"
fi

# 4. Configurar auto-login
echo "🔐 Configurando auto-login..."
mkdir -p /etc/systemd/system/getty@tty1.service.d
cat > /etc/systemd/system/getty@tty1.service.d/override.conf << EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $CAJERO_USER --noclear %I \$TERM
EOF

# 5. Crear script de inicio de la aplicación
echo "🚀 Creando script de inicio..."
cat > /home/$CAJERO_USER/start_cajero.sh << 'EOF'
#!/bin/bash

# Configurar display
export DISPLAY=:0

# Deshabilitar protector de pantalla y gestión de energía
xset s off
xset -dpms
xset s noblank

# Ocultar cursor del mouse después de 0.1 segundos
unclutter -idle 0.1 -root &

# Loop infinito para mantener la aplicación corriendo
while true; do
    echo "Iniciando aplicación del cajero..."
    
    # AQUÍ CAMBIA LA RUTA A TU APLICACIÓN
    # Ejemplo: python3 /home/cajero/mi_aplicacion.py
    # O: /home/cajero/mi_programa_ejecutable
    
    # Por ahora, mostraremos un mensaje de ejemplo
    python3 -c "
import tkinter as tk
import time

root = tk.Tk()
root.title('CAJERO AUTOMÁTICO')
root.configure(bg='black')
root.attributes('-fullscreen', True)

label = tk.Label(root, 
                text='🏧 CAJERO AUTOMÁTICO\\n\\nConfiguración completada\\nReemplaza este mensaje con tu aplicación\\n\\nPresiona ESC para salir (temporal)', 
                font=('Arial', 24), 
                fg='white', 
                bg='black',
                justify='center')
label.pack(expand=True)

def on_escape(event):
    root.destroy()

root.bind('<Escape>', on_escape)
root.mainloop()
"
    
    echo "La aplicación se cerró. Reiniciando en 3 segundos..."
    sleep 3
done
EOF

chmod +x /home/$CAJERO_USER/start_cajero.sh
chown $CAJERO_USER:$CAJERO_USER /home/$CAJERO_USER/start_cajero.sh

# 6. Configurar Openbox
echo "🪟 Configurando Openbox..."
mkdir -p /home/$CAJERO_USER/.config/openbox
chown -R $CAJERO_USER:$CAJERO_USER /home/$CAJERO_USER/.config

# Autostart de Openbox
cat > /home/$CAJERO_USER/.config/openbox/autostart << EOF
#!/bin/bash
/home/$CAJERO_USER/start_cajero.sh &
EOF
chmod +x /home/$CAJERO_USER/.config/openbox/autostart

# Configuración de Openbox (deshabilitar teclas peligrosas)
cat > /home/$CAJERO_USER/.config/openbox/rc.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<openbox_config xmlns="http://openbox.org/3.4/rc" xmlns:xi="http://www.w3.org/2001/XInclude">
  <resistance>
    <strength>10</strength>
    <screen_edge_strength>20</screen_edge_strength>
  </resistance>
  <focus>
    <focusNew>yes</focusNew>
    <followMouse>no</followMouse>
    <focusLast>yes</focusLast>
    <underMouse>no</underMouse>
    <focusDelay>200</focusDelay>
    <raiseOnFocus>no</raiseOnFocus>
  </focus>
  <placement>
    <policy>Smart</policy>
    <center>yes</center>
    <monitor>Primary</monitor>
    <primaryMonitor>1</primaryMonitor>
  </placement>
  <theme>
    <name>Clearlooks</name>
    <titleLayout>NLIMC</titleLayout>
    <keepBorder>yes</keepBorder>
    <animateIconify>yes</animateIconify>
    <font place="ActiveWindow">
      <name>sans</name>
      <size>8</size>
      <weight>bold</weight>
      <slant>normal</slant>
    </font>
    <font place="InactiveWindow">
      <name>sans</name>
      <size>8</size>
      <weight>bold</weight>
      <slant>normal</slant>
    </font>
  </theme>
  <desktops>
    <number>1</number>
    <firstdesk>1</firstdesk>
    <popupTime>875</popupTime>
  </desktops>
  <resize>
    <drawContents>yes</drawContents>
    <popupShow>Nonpixel</popupShow>
    <popupPosition>Center</popupPosition>
    <popupFixedPosition>
      <x>10</x>
      <y>10</y>
    </popupFixedPosition>
  </resize>
  <margins>
    <top>0</top>
    <bottom>0</bottom>
    <left>0</left>
    <right>0</right>
  </margins>
  <dock>
    <position>TopLeft</position>
    <floatingX>0</floatingX>
    <floatingY>0</floatingY>
    <noStrut>no</noStrut>
    <stacking>Above</stacking>
    <direction>Vertical</direction>
    <autoHide>no</autoHide>
    <hideDelay>300</hideDelay>
    <showDelay>300</showDelay>
    <moveButton>Middle</moveButton>
  </dock>
  <keyboard>
    <!-- Deshabilitar combinaciones de teclas peligrosas -->
    <keybind key="A-F4"><action name="Nothing"/></keybind>
    <keybind key="C-A-t"><action name="Nothing"/></keybind>
    <keybind key="C-A-Delete"><action name="Nothing"/></keybind>
    <keybind key="C-A-l"><action name="Nothing"/></keybind>
    <keybind key="A-Tab"><action name="Nothing"/></keybind>
    <keybind key="A-S-Tab"><action name="Nothing"/></keybind>
  </keyboard>
  <mouse>
    <dragThreshold>1</dragThreshold>
    <doubleClickTime>500</doubleClickTime>
    <screenEdgeWarpTime>400</screenEdgeWarpTime>
    <screenEdgeWarpMouse>false</screenEdgeWarpMouse>
  </mouse>
  <applications>
    <application class="*">
      <fullscreen>yes</fullscreen>
      <maximized>yes</maximized>
      <skip_pager>yes</skip_pager>
      <skip_taskbar>yes</skip_taskbar>
    </application>
  </applications>
</openbox_config>
EOF

# 7. Configurar archivos de inicio del usuario
echo "⚙️  Configurando archivos de inicio del usuario..."

# .bash_profile para iniciar X automáticamente
cat > /home/$CAJERO_USER/.bash_profile << EOF
if [ -z "\$DISPLAY" ] && [ "\$XDG_VTNR" = 1 ]; then
    exec startx
fi
EOF

# .xinitrc para iniciar Openbox
cat > /home/$CAJERO_USER/.xinitrc << EOF
#!/bin/bash
exec openbox-session
EOF

chmod +x /home/$CAJERO_USER/.xinitrc

# 8. Asignar permisos correctos
chown -R $CAJERO_USER:$CAJERO_USER /home/$CAJERO_USER/

# 9. Deshabilitar TTYs adicionales
echo "🔒 Deshabilitando TTYs adicionales..."
systemctl mask getty@tty2.service
systemctl mask getty@tty3.service
systemctl mask getty@tty4.service
systemctl mask getty@tty5.service
systemctl mask getty@tty6.service

# 10. Configurar firewall básico
echo "🛡️  Configurando firewall..."
apt install -y ufw
ufw --force enable
ufw default deny incoming
ufw default allow outgoing

# 11. Recargar configuración de systemd
echo "🔄 Recargando configuración de systemd..."
systemctl daemon-reload
systemctl enable getty@tty1.service

# 12. Crear script de aplicación de ejemplo (si no existe)
if [ ! -f "$APP_PATH" ]; then
    echo "📝 Creando aplicación de ejemplo..."
    cat > "$APP_PATH" << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación de ejemplo para cajero automático
Reemplaza este archivo con tu aplicación real
"""

import tkinter as tk
from tkinter import messagebox
import sys

class CajeroApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CAJERO AUTOMÁTICO")
        self.root.configure(bg='#1a1a2e')
        self.root.attributes('-fullscreen', True)
        
        # Crear interfaz
        self.create_interface()
        
        # Bind para salir con ESC (solo para pruebas)
        self.root.bind('<Escape>', self.salir)
        
    def create_interface(self):
        # Título principal
        title_label = tk.Label(
            self.root,
            text="🏧 CAJERO AUTOMÁTICO",
            font=('Arial', 32, 'bold'),
            fg='white',
            bg='#1a1a2e'
        )
        title_label.pack(pady=50)
        
        # Mensaje de estado
        status_label = tk.Label(
            self.root,
            text="Sistema configurado correctamente\nReemplaza este archivo con tu aplicación real",
            font=('Arial', 18),
            fg='#4ade80',
            bg='#1a1a2e',
            justify='center'
        )
        status_label.pack(pady=20)
        
        # Botones de ejemplo
        button_frame = tk.Frame(self.root, bg='#1a1a2e')
        button_frame.pack(pady=50)
        
        tk.Button(
            button_frame,
            text="Consultar Saldo",
            font=('Arial', 16),
            width=20,
            height=2,
            bg='#3b82f6',
            fg='white',
            command=self.consultar_saldo
        ).pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Retirar Dinero",
            font=('Arial', 16),
            width=20,
            height=2,
            bg='#ef4444',
            fg='white',
            command=self.retirar_dinero
        ).pack(pady=10)
        
        # Instrucciones
        instructions_label = tk.Label(
            self.root,
            text="Presiona ESC para salir (solo para pruebas)",
            font=('Arial', 12),
            fg='#6b7280',
            bg='#1a1a2e'
        )
        instructions_label.pack(side='bottom', pady=20)
    
    def consultar_saldo(self):
        messagebox.showinfo("Saldo", "Su saldo actual es: $1,234.56")
    
    def retirar_dinero(self):
        messagebox.showinfo("Retiro", "Funcionalidad de retiro no implementada")
    
    def salir(self, event=None):
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir?"):
            self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CajeroApp()
    app.run()
EOF
    
    chmod +x "$APP_PATH"
    chown $CAJERO_USER:$CAJERO_USER "$APP_PATH"
fi

echo ""
echo "✅ ¡Configuración completada exitosamente!"
echo ""
echo "=========================================="
echo "           PRÓXIMOS PASOS:"
echo "=========================================="
echo ""
echo "1. 📝 EDITA tu aplicación en:"
echo "   $APP_PATH"
echo ""
echo "2. 🔧 O modifica el script de inicio:"
echo "   /home/$CAJERO_USER/start_cajero.sh"
echo ""
echo "3. 🔄 Reinicia el sistema:"
echo "   sudo reboot"
echo ""
echo "4. 🔒 Después del reinicio:"
echo "   - El sistema iniciará automáticamente como '$CAJERO_USER'"
echo "   - Tu aplicación se ejecutará en pantalla completa"
echo "   - ESC estará deshabilitado (excepto en la app de ejemplo)"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - Cambia la contraseña del usuario pi: passwd pi"
echo "   - Cambia la contraseña del usuario cajero: passwd cajero"
echo "   - Deshabilita SSH si no lo necesitas: sudo systemctl disable ssh"
echo ""
echo "🎯 ¡Tu cajero está listo para usar!"
echo "=========================================="
