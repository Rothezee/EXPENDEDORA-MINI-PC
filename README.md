# EXPENDEDORA-MINI-PC

Aplicación en Python para gestionar una expendedora de fichas, con interfaz gráfica y sistema de usuarios.

## Descripción

Este proyecto permite controlar una expendedora de fichas a través de una interfaz gráfica desarrollada en `tkinter` y Python. Incluye funcionalidades para el registro e inicio de sesión de usuarios, gestión de promociones, conversión de dinero a fichas, manejo de hardware (dispensador, sensores), reportes y cierre de caja.

## Características principales

- Interfaz gráfica amigable (Tkinter) con menú lateral y diferentes secciones.
- Registro e inicio de sesión de usuarios.
- Conversión automática de dinero a fichas según configuraciones.
- Control y simulación de entrega de fichas (integración con hardware).
- Contadores de fichas expendidas, dinero ingresado y promociones usadas.
- Sección de configuración y reportes.
- Script de inicio automático en Linux (`iniciarExpendedora.sh`).

## Estructura del proyecto

- `main.py`: Archivo principal, gestiona el flujo de inicio de sesión y lanza la GUI.
- `expendedora_gui.py`: Interfaz gráfica principal.
- `expendedora_core.py`: Lógica de negocio y control del hardware (dispensador de fichas).
- `User_management/`: Módulos para registro, login y gestión de usuarios.
- `iniciarExpendedora.sh`: Script para lanzar la aplicación fácilmente en Linux.

## Requisitos

- Python 3.x
- Tkinter (interfaz gráfica)
- [Raspberry Pi GPIO](https://pypi.org/project/RPi.GPIO/) (si se usa hardware real)
- Otros módulos estándar de Python

## Instalación y uso

1. Clona el repositorio:
   ```sh
   git clone https://github.com/Rothezee/EXPENDEDORA-MINI-PC.git
   cd EXPENDEDORA-MINI-PC/EXPENDEDORA-MINIPC
   ```

2. Instala las dependencias necesarias:
   ```sh
   pip install -r requirements.txt
   ```
   (Si no existe el archivo, instala manualmente: `pip install RPi.GPIO` y asegúrate de tener tkinter).

3. Ejecuta el script principal:
   ```sh
   python3 main.py
   ```
   O usa el script de inicio:
   ```sh
   bash iniciarExpendedora.sh
   ```

4. Regístrate o inicia sesión y comienza a usar la expendedora.

## Notas

- El sistema está diseñado para integrarse con hardware real (dispensador de fichas, sensores, etc.), pero incluye funciones de simulación.
- Puedes adaptar la lógica de conversión y promociones modificando los parámetros en el código.
- ¡Contribuciones y sugerencias son bienvenidas!

---

¿Dudas o quieres contribuir? Abre un issue o pull request.
