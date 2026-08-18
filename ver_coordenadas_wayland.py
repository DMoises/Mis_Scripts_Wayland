#!/usr/bin/env python3
import subprocess
import os

print("==================================================")
print(" 🚀 ABRIENDO CONSOLA DE DEPURACIÓN KDE (WAYLAND) ")
print("==================================================")
print("INSTRUCCIONES:")
print("1. En la ventana que se acaba de abrir, ve a la pestaña 'Input Events'.")
print("2. Mueve tu ratón por la pantalla.")
print("3. Las coordenadas absolutas (X, Y) aparecerán actualizándose en vivo.\n")
print("Comando original guardado:")
print("qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.showDebugConsole\n")

try:
    subprocess.run(["qdbus-qt6", "org.kde.KWin", "/KWin", "org.kde.KWin.showDebugConsole"])
except FileNotFoundError:
    print("❌ Error: No se encontró 'qdbus-qt6'. ¿Estás seguro de estar en Fedora KDE?")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
