import time
import subprocess

# ==========================================
#       WRAPPERS PARA WAYLAND
# ==========================================
def send_shortcut(keys):
    subprocess.run(["ydotool", "key", keys])

def click_absolute(x, y, button=1):
    subprocess.run(["ydotool", "mousemove", "--absolute", "-x", str(x), "-y", str(y)])
    if button == 1:
        subprocess.run(["ydotool", "click", "0x40"])

# ==========================================
#       SCRIPT PRINCIPAL
# ==========================================

# Este script asume que ya has copiado el texto que quieres pegar en el portapapeles.
# Asegúrate de ajustar las coordenadas de los clics según tus necesidades.
# En este script se utilizó para enviar texto a dos ventanas separadas en el mismo monitor.

# 1. Primera ubicación
click_absolute(400, 1015, 1) 
time.sleep(0.3)
send_shortcut("ctrl+v")
time.sleep(0.2)
send_shortcut("enter")

time.sleep(0.5)

# 2. Segunda ubicación
click_absolute(1200, 945, 1)
time.sleep(0.3)
send_shortcut("ctrl+v")
time.sleep(0.2)
send_shortcut("enter")
