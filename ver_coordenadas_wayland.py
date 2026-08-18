#!/usr/bin/env python3
import tkinter as tk
import subprocess

print("========================================")
print(" RASTREADOR DE COORDENADAS (INTERACTIVO) ")
print("========================================")
print("La pantalla se oscurecerá levemente.")
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
        print("📋 ¡Coordenadas copiadas al portapapeles!")
        
    root.destroy()

root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-alpha', 0.5) # Semitransparente para ver el fondo
root.configure(background='black')
root.config(cursor="crosshair")

label = tk.Label(root, 
                 text="HAZ CLIC EXACTAMENTE DONDE QUIERAS MEDIR\n\n(Presiona la tecla ESC para salir sin medir)", 
                 fg="white", 
                 bg="black", 
                 font=("Arial", 20, "bold"))
label.pack(expand=True)

# Capturar el clic izquierdo
root.bind("<Button-1>", show_coordinates)
# Tecla de escape para salir
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
