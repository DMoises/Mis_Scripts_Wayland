import time
import subprocess
import os

# ==========================================
#       WRAPPERS PARA WAYLAND
# ==========================================
def send_shortcut(keys):
    subprocess.run(["ydotool", "key", keys])

def fill_clipboard(text):
    process = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=text)

def get_clipboard():
    try:
        return subprocess.check_output(["wl-paste"], text=True)
    except subprocess.CalledProcessError:
        return ""

def notify_os(title, message):
    subprocess.run(["notify-send", title, message])

# ==========================================
#       SCRIPT PRINCIPAL
# ==========================================

# 1. Copiar la URL
send_shortcut("ctrl+c")
time.sleep(0.3)
url_detectada = get_clipboard()

# 2. Pulsar F2 para el nombre del archivo
send_shortcut("F2")
time.sleep(0.4)

# 3. Copiar el nombre
send_shortcut("ctrl+c")
time.sleep(0.3)
nombre_archivo = get_clipboard()

# 4. Salir del modo edición
send_shortcut("esc")
time.sleep(0.1)

# 5. Unir todo y devolverlo al portapapeles
if url_detectada and nombre_archivo:
    resultado = f"{url_detectada},{nombre_archivo}"
    fill_clipboard(resultado)
    notify_os("Wayland Script", "URL y Nombre combinados con éxito")
else:
    notify_os("Wayland Script", "Error: No se pudo capturar el texto")
