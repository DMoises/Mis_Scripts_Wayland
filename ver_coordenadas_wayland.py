#!/usr/bin/env python3
import time
import subprocess
import os

print("========================================")
print(" RASTREADOR DE COORDENADAS PARA KDE WAYLAND ")
print("========================================")
print("Presiona Ctrl+C para salir.\n")

def get_cursor_pos():
    # En KDE Wayland, qdbus nos permite obtener la posición del cursor de forma segura.
    # Intentamos primero con qdbus6 (Plasma 6) y luego con qdbus (Plasma 5).
    commands = [
        ["qdbus-qt6", "org.kde.KWin", "/KWin", "org.kde.KWin.cursorPos"],
        ["qdbus6", "org.kde.KWin", "/KWin", "org.kde.KWin.cursorPos"],
        ["qdbus", "org.kde.KWin", "/KWin", "org.kde.KWin.cursorPos"]
    ]
    
    for cmd in commands:
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
            # La salida suele ser algo como: QPoint(840,520) o similar
            if "QPoint" in output:
                # Extraemos los números
                coords = output.replace("QPoint(", "").replace(")", "").split(",")
                if len(coords) == 2:
                    return f"X: {coords[0].strip()} | Y: {coords[1].strip()}"
            return output
        except FileNotFoundError:
            pass # Si no encuentra qdbus6, intenta con el siguiente
        except subprocess.CalledProcessError:
            pass # Si falla el comando, intenta con el siguiente
            
    return "Error: No se pudo obtener la posición (¿Estás usando KDE Wayland y qdbus está instalado?)"

try:
    while True:
        pos = get_cursor_pos()
        # Borra la línea actual y reescribe (como hace el watch)
        print(f"\rPosición actual: {pos}          ", end="", flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n¡Rastreo finalizado!")
