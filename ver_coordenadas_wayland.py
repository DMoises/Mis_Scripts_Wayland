#!/usr/bin/env python3
import tkinter as tk
import subprocess
import os

print("========================================")
print(" RASTREADOR DE COORDENADAS (INTERACTIVO) ")
print("========================================")
print("Tomando captura de pantalla temporal (congelando imagen)...")

# 1. Tomar captura de pantalla silenciosa con Spectacle
img_path = "/tmp/wayland_coord_screen.png"
if os.path.exists(img_path):
    os.remove(img_path)
    
subprocess.run(["spectacle", "-b", "-n", "-o", img_path])

if not os.path.exists(img_path):
    print("Error: No se pudo tomar la captura con Spectacle. ¿Está instalado?")
    exit(1)

print("Haz clic en el punto exacto del que quieres obtener las coordenadas.")
print("Presiona ESC si quieres cancelar.\n")

def show_coordinates(event):
    x = event.x_root
    y = event.y_root
    print(f"✅ ¡Clic detectado!")
    print(f"📍 Coordenadas absolutas: X = {x} | Y = {y}")
    
    # Intentar copiar al portapapeles nativo de Wayland usando wl-copy
    try:
        process = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE, text=True)
        process.communicate(input=f"{x}, {y}")
        print("📋 ¡Coordenadas copiadas a tu portapapeles de Wayland automáticamente!")
    except Exception:
        # Fallback al portapapeles de tkinter
        root.clipboard_clear()
        root.clipboard_append(f"{x}, {y}")
        print("📋 ¡Coordenadas copiadas al portapapeles (alternativo)!")
        
    root.destroy()

root = tk.Tk()
root.attributes('-fullscreen', True)
root.config(cursor="crosshair")

# Cargar la imagen y ponerla de fondo
img = tk.PhotoImage(file=img_path)
canvas = tk.Canvas(root, width=img.width(), height=img.height(), highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=img, anchor="nw")

# Añadir un texto flotante arriba
canvas.create_text(img.width()//2, 50, 
                   text="HAZ CLIC EXACTAMENTE DONDE QUIERAS MEDIR (Presiona ESC para salir)", 
                   fill="red", font=("Arial", 20, "bold"))

# Capturar el clic izquierdo
root.bind("<Button-1>", show_coordinates)
# Tecla de escape para salir
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()

# Limpiar
if os.path.exists(img_path):
    os.remove(img_path)
