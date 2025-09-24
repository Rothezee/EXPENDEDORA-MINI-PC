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
APP_PATH="/home/admin/EXPENDEDORA-MINI-PC/EXPENDEDORA-MINIPC/main.py"

echo "🔧 Iniciando configuración..."
echo "Usuario del cajero: $CAJERO_USER"
echo "Ruta de la aplicación: $APP_PATH"
echo ""

# Verificar que la aplicación existe
if [ ! -f "$APP_PATH" ]; then
    echo "❌ ERROR: No se encontró la aplicación en $APP_PATH"
    echo "   Verifica que la ruta sea correcta y que el archivo exista."
    exit 1
fi

echo "✅ Aplicación encontrada: $APP_PATH"
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

# 5. Dar permisos al usuario cajero para ejecutar la aplicación
echo "🔑 Configurando permisos para la aplicación..."
# Dar permisos de ejecución al directorio /home/admin
chmod o+x /home/admin
chmod o+x /home/admin/EXPENDEDORA-MINI-PC
chmod o+x /home/admin/EXPENDEDORA-MINI-PC/EXPENDEDORA-MINIPC
# Dar permisos de lectura al archivo
chmod o+r /home/admin/EXPENDEDORA-MINI-PC/EXPENDEDORA-MINIPC/main.py

# También agregar cajero al grupo admin si existe
if getent group admin > /dev/null 2>&1; then
    usermod -a -G admin $CAJERO_USER
    echo "   Usuario $CAJERO_USER agregado al grupo admin"
fi

# 6. Crear script de inicio de la aplicación
echo "🚀 Creando script de inicio..."
cat > /home/$CAJERO_USER/start_cajero.sh << EOF
#!/bin/bash

# Configurar display
export DISPLAY=:0

# Deshabilitar protector de pantalla y gestión de energía
xset s off
xset -dpms
xset s noblank

# Ocultar cursor del mouse después de 0.1 segundos
unclutter -idle 0.1 -root &

# Cambiar al directorio de la aplicación para que funcionen las rutas relativas
cd /home/admin/EXPENDEDORA-MINI-PC/EXPENDEDORA-MINIPC

# Loop infinito para mantener la aplicación corriendo
while true; do
    echo "Iniciando aplicación del cajero..."
    echo "Ejecutando: python3 $APP_PATH"
    
    # Ejecutar la aplicación
    python3 $APP_PATH
    
    # Si la aplicación se cierra, registrar el evento y reiniciar
    echo "La aplicación se cerró en \$(date). Reiniciando en 3 segundos..."
    sleep 3
done
EOF

chmod +x /home/$CAJERO_USER/start_cajero.sh
chown $CAJERO_USER:$CAJERO_USER /home/$CAJERO_USER/start_cajero.sh

# 7. Configurar Openbox
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
    <n>Clearlooks</n>
    <titleLayout>NLIMC</titleLayout>
    <keepBorder>yes</keepBorder>
    <animateIconify>yes</animateIconify>
    <font place="ActiveWindow">
      <n>sans</n>
      <size>8</size>
      <weight>bold</weight>
      <slant>normal</slant>
    </font>
    <font place="InactiveWindow">
      <n>sans</n>
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
    <keybind key="C-A-F1"><action name="Nothing"/></keybind>
    <keybind key="C-A-F2"><action name="Nothing"/></keybind>
    <keybind key="C-A-F3"><action name="Nothing"/></keybind>
    <keybind key="C-A-F4"><action name="Nothing"/></keybind>
    <keybind key="C-A-F5"><action name="Nothing"/></keybind>
    <keybind key="C-A-F6"><action name="Nothing"/></keybind>
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
      <decor>no</decor>
    </application>
  </applications>
</openbox_config>
EOF

# 8. Configurar archivos de inicio del usuario
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

# 9. Asignar permisos correctos
chown -R $CAJERO_USER:$CAJERO_USER /home/$CAJERO_USER/

# 10. Deshabilitar TTYs adicionales
echo "🔒 Deshabilitando TTYs adicionales..."
systemctl mask getty@tty2.service
systemctl mask getty@tty3.service
systemctl mask getty@tty4.service
systemctl mask getty@tty5.service
systemctl mask getty@tty6.service

# 11. Configurar firewall básico
echo "🛡️  Configurando firewall..."
apt install -y ufw
ufw --force enable
ufw default deny incoming
ufw default allow outgoing

# 12. Configurar sudoers para permitir que cajero ejecute la aplicación como admin (opcional)
echo "🔐 Configurando permisos sudo (opcional)..."
cat > /etc/sudoers.d/cajero << EOF
# Permitir que cajero ejecute la aplicación como admin sin contraseña
$CAJERO_USER ALL=(admin) NOPASSWD: /usr/bin/python3 /home/admin/EXPENDEDORA-MINI-PC/EXPENDEDORA-MINIPC/main.py
# Permitir reinicio y apagado
$CAJERO_USER ALL=(ALL) NOPASSWD: /sbin/shutdown, /sbin/reboot
EOF

# 13. Instalar dependencias de Python que pueda necesitar tu aplicación
echo "🐍 Instalando dependencias Python comunes..."
pip3 install --upgrade pip
# Agrega aquí las dependencias específicas de tu aplicación
# pip3 install tkinter pygame requests etc.

# 14. Recargar configuración de systemd
echo "🔄 Recargando configuración de systemd..."
systemctl daemon-reload
systemctl enable getty@tty1.service

# 15. Crear un log para la aplicación
echo "📝 Configurando logging..."
mkdir -p /var/log/cajero
touch /var/log/cajero/aplicacion.log
chown $CAJERO_USER:$CAJERO_USER /var/log/cajero/aplicacion.log

# Modificar el script para incluir logging
cat > /home/$CAJERO_USER/start_cajero_with_log.sh << EOF
#!/bin/bash

# Configurar display
export DISPLAY=:0

# Archivo de log
LOG_FILE="/var/log/cajero/aplicacion.log"

# Función para logging
log_message() {
    echo "\$(date '+%Y-%m-%d %H:%M:%S') - \$1" >> "\$LOG_FILE"
    echo "\$1"
}

# Deshabilitar protector de pantalla y gestión de energía
xset s off
xset -dpms
xset s noblank

# Ocultar cursor del mouse después de 0.1 segundos
unclutter -idle 0.1 -root &

# Cambiar al directorio de la aplicación para que funcionen las rutas relativas
cd /home/admin/EXPENDEDORA-MINI-PC/EXPENDEDORA-MINIPC

# Loop infinito para mantener la aplicación corriendo
while true; do
    log_message "Iniciando aplicación del cajero..."
    log_message "Ejecutando: python3 $APP_PATH"
    
    # Ejecutar la aplicación y capturar errores
    python3 $APP_PATH 2>> "\$LOG_FILE"
    EXIT_CODE=\$?
    
    # Registrar la salida
    if [ \$EXIT_CODE -eq 0 ]; then
        log_message "La aplicación se cerró normalmente."
    else
        log_message "La aplicación se cerró con error (código: \$EXIT_CODE)."
    fi
    
    log_message "Reiniciando en 3 segundos..."
    sleep 3
done
EOF

chmod +x /home/$CAJERO_USER/start_cajero_with_log.sh
chown $CAJERO_USER:$CAJERO_USER /home/$CAJERO_USER/start_cajero_with_log.sh

# Actualizar autostart para usar el script con logging
cat > /home/$CAJERO_USER/.config/openbox/autostart << EOF
#!/bin/bash
/home/$CAJERO_USER/start_cajero_with_log.sh &
EOF

echo ""
echo "✅ ¡Configuración completada exitosamente!"
echo ""
echo "=========================================="
echo "           INFORMACIÓN IMPORTANTE:"
echo "=========================================="
echo ""
echo "📍 APLICACIÓN CONFIGURADA:"
echo "   $APP_PATH"
echo ""
echo "👤 USUARIO DEL SISTEMA:"
echo "   $CAJERO_USER"
echo ""
echo "📋 ARCHIVOS IMPORTANTES:"
echo "   • Script de inicio: /home/$CAJERO_USER/start_cajero_with_log.sh"
echo "   • Configuración Openbox: /home/$CAJERO_USER/.config/openbox/"
echo "   • Log de aplicación: /var/log/cajero/aplicacion.log"
echo ""
echo "=========================================="
echo "           PRÓXIMOS PASOS:"
echo "=========================================="
echo ""
echo "1. 🔄 Reinicia el sistema:"
echo "   sudo reboot"
echo ""
echo "2. 📊 Después del reinicio:"
echo "   - El sistema iniciará automáticamente como '$CAJERO_USER'"
echo "   - Tu aplicación se ejecutará en pantalla completa"
echo "   - Los logs se guardarán en /var/log/cajero/aplicacion.log"
echo ""
echo "3. 🔍 Para ver los logs en tiempo real:"
echo "   sudo tail -f /var/log/cajero/aplicacion.log"
echo ""
echo "4. 🛠️  Para hacer mantenimiento:"
echo "   - Cambiar a TTY2: Ctrl+Alt+F2 (si está habilitado)"
echo "   - O conectarse por SSH si está habilitado"
echo ""
echo "⚠️  IMPORTANTE - SEGURIDAD:"
echo "   - Cambia la contraseña del usuario pi: sudo passwd pi"
echo "   - Cambia la contraseña del usuario admin: sudo passwd admin"
echo "   - Configura contraseña para cajero: sudo passwd cajero"
echo "   - Deshabilita SSH si no lo necesitas: sudo systemctl disable ssh"
echo ""
echo "🎯 ¡Tu cajero está listo para usar!"
echo "   La aplicación se ejecutará automáticamente al reiniciar."
echo "=========================================="
