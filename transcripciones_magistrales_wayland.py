import time
import csv
import subprocess
import os

# ==========================================
#       WRAPPERS PARA WAYLAND
# ==========================================
def send_keys_text(text):
    subprocess.run(["ydotool", "type", text])

def send_shortcut(keys):
    subprocess.run(["ydotool", "key", keys])

def click_relative(x, y, button=1):
    # NOTA: ydotool en Wayland a veces no soporta relative movement perfecto.
    # Si falla, se recomienda usar click_absolute. 
    # Aquí se hace un wrapper simple que asume que el comando relative existe.
    subprocess.run(["ydotool", "mousemove", "-x", str(x), "-y", str(y)])
    if button == 1:
        subprocess.run(["ydotool", "click", "0x40"])

def error_dialog(title, msg):
    subprocess.run(["kdialog", "--title", title, "--error", msg])

# ==========================================
#       CONFIGURACIÓN UNIVERSAL
# ==========================================

base_dir = os.path.expanduser("~/Documentos/GIT/Mi_Repositorio_Scripts")

venv_python = os.path.join(base_dir, "venv/bin/python3") 
script_cleaner = os.path.join(base_dir, "cleaner_clipboard", "cleaner_clipboard.py")
script_duplicados = os.path.join(base_dir, "check_duplicates", "check_duplicates.py")
archivo_log = os.path.join(base_dir, "autokey_Linux", "debug_log_magistrales_wayland.txt")
archivo_csv = os.path.join(base_dir, "organizador_csv", "csv_maestro_s2.csv")

# Tiempos
esperaLargo = 10
esperaMediolargo = 3
esperaCorto = 2
esperaIntantaneo = 0.5

# Contador
procesados_hoy = 0

os.makedirs(os.path.dirname(archivo_log), exist_ok=True)

def log(mensaje):
    with open(archivo_log, "a", encoding="utf-8") as f:
        timestamp = time.strftime("%H:%M:%S")
        f.write(f"[{timestamp}] {mensaje}\n")

log("=== INICIANDO SESIÓN DE BUCLE MAGISTRALES WAYLAND ===")

# ==========================================
#    EL GRAN BUCLE
# ==========================================
while True:
    filas = []
    tarea_actual = None
    indice_fila = -1
    
    try:
        with open(archivo_csv, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            filas = list(reader)
    except Exception as e:
        log(f"ERROR: No se pudo leer el CSV. {str(e)}")
        error_dialog("Error", "Fallo al leer CSV")
        break

    for i, fila in enumerate(filas):
        if i == 0: continue 
        if len(fila) < 2: continue 
        
        estado = fila[2] if len(fila) > 2 else ""
        
        if estado.strip() != "LISTO":
            tarea_actual = fila
            indice_fila = i
            break

    if not tarea_actual:
        log("No hay más tareas pendientes. Saliendo del bucle.")
        break

    url_video = tarea_actual[0]
    nombre_clase = tarea_actual[1]

    log(f"--- Procesando: {nombre_clase} ---")

    # ==========================================
    #       NAVEGACIÓN
    # ==========================================
    try:
        send_shortcut("ctrl+t")
        time.sleep(esperaIntantaneo) 
        send_keys_text(url_video)
        send_shortcut("enter")
        time.sleep(esperaLargo) 

        send_shortcut("F12")
        time.sleep(esperaMediolargo) 

        click_relative(500, 580, 1)
        time.sleep(esperaCorto)
        click_relative(500, 580, 1)
        time.sleep(esperaCorto)

        for i in range(2):
            send_shortcut("shift+tab")
            time.sleep(esperaIntantaneo)
            
        send_shortcut("enter")
        time.sleep(esperaCorto)

        click_relative(1270, 315, 1)
        time.sleep(esperaCorto)
        send_shortcut("tab")
        time.sleep(esperaCorto)
        send_shortcut("shift+tab")
        time.sleep(esperaCorto)
        
        send_shortcut("enter")
        time.sleep(esperaCorto)

        send_shortcut("down")
        time.sleep(esperaIntantaneo)
        send_shortcut("right")
        time.sleep(esperaIntantaneo)
        send_shortcut("menu")
        time.sleep(esperaIntantaneo)

        send_shortcut("down")   
        time.sleep(esperaIntantaneo)
        send_shortcut("enter")  

        time.sleep(esperaLargo) 

        send_shortcut("ctrl+a") 
        time.sleep(esperaCorto)
        send_shortcut("ctrl+c") 
        time.sleep(esperaCorto)

        send_shortcut("ctrl+w") 
        time.sleep(esperaCorto)
        
    except Exception as e:
        log(f"ERROR DURANTE NAVEGACIÓN: {str(e)}")
        break

    # ==========================================
    #       PROCESAMIENTO
    # ==========================================
    try:
        log("Ejecutando script cleaner...")
        
        # Ojo: aquí asumimos que wl-clipboard está disponible y el cleaner_clipboard ya fue migrado
        subprocess.check_output(
            ["python3", script_cleaner, nombre_clase], # Usamos python3 por si el venv falla
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        filas[indice_fila][2] = "LISTO"
        with open(archivo_csv, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(filas)
            
        procesados_hoy += 1
        log(f"Éxito. CSV actualizado para: {nombre_clase}")
        
    except subprocess.CalledProcessError as e:
        log(f"ERROR CRÍTICO en script Python: {e.output}")
        error_dialog("Error Script", str(e.output))
        break

    time.sleep(2)

log("--- BUCLE FINALIZADO ---")
log("Ejecutando chequeo de duplicados...")

try:
    subprocess.call(["python3", script_duplicados])
except Exception as e:
    log(f"Error al chequear duplicados: {str(e)}")

send_shortcut("ctrl+t")
time.sleep(1)
aviso = f"PROCESO_TERMINADO__VIDEOS_PROCESADOS_{procesados_hoy}"
send_keys_text(aviso)

log("=== FIN DE SESIÓN ===")
