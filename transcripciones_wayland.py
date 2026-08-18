import time
import csv
import subprocess
import os
import re

# ==========================================
#       WRAPPERS PARA WAYLAND (ydotool / wl-clipboard / kdialog)
# ==========================================

def send_keys_text(text):
    subprocess.run(["ydotool", "type", text])

def send_shortcut(keys):
    """
    keys: string como "ctrl+t", "ctrl+shift+End", "ctrl+c", "enter"
    Se asume una versión moderna de ydotool que soporta nombres de teclas.
    Si falla, puede requerir códigos hex (ej. 29:1 20:1 20:0 29:0).
    """
    subprocess.run(["ydotool", "key", keys])

def click_absolute(x, y, button=1):
    """
    Mueve a una posición absoluta y hace click.
    button=1 usa 0x40 (clic izquierdo) como sugirió el usuario.
    """
    subprocess.run(["ydotool", "mousemove", "--absolute", "-x", str(x), "-y", str(y)])
    if button == 1:
        subprocess.run(["ydotool", "click", "0x40"])

def fill_clipboard(text):
    # wl-copy necesita recibir el texto, podemos pasarlo por stdin o como argumento
    # Es más seguro pasarlo por stdin
    process = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE, text=True)
    process.communicate(input=text)

def get_clipboard():
    try:
        return subprocess.check_output(["wl-paste"], text=True)
    except subprocess.CalledProcessError:
        return ""

def error_dialog(title, msg):
    subprocess.run(["kdialog", "--title", title, "--error", msg])


# ==========================================
#       CONFIGURACIÓN UNIVERSAL
# ==========================================

base_dir = os.path.expanduser("~/Documentos/GIT/Mi_Repositorio_Scripts")

# Archivos y carpetas
archivo_log = os.path.join(base_dir, "autokey_Linux", "debug_log_wayland.txt")
archivo_csv = os.path.join(base_dir, "organizador_csv", "csv_maestro_s2.csv")
carpeta_guardado = os.path.join(base_dir, "transcripciones_locales")
script_duplicados = os.path.join(base_dir, "check_duplicates", "check_duplicates.py")
venv_python = os.path.join(base_dir, "venv/bin/python3")

# ==========================================
#       MODO DESARROLLO
# ==========================================
dev_mode = False

# ==========================================
#       COORDENADAS (MODIFICABLES)
# ==========================================
x_iniciar_video = 935
y_iniciar_video = 595

x_pausar_video = x_iniciar_video
y_pausar_video = y_iniciar_video

x_abrir_transcripcion = 153
y_abrir_transcripcion = 203

x_seleccionar_palabra = 1649
y_seleccionar_palabra = 205

# ==========================================
#       TIEMPOS
# ==========================================
esperaLargo = 10
esperaMediolargo = 3
esperaCorto = 2
esperaIntantaneo = 0.5

# Contador
procesados_hoy = 0
errores_hoy = 0

# Crear directorio si no existe
if not os.path.exists(carpeta_guardado):
    os.makedirs(carpeta_guardado)
os.makedirs(os.path.dirname(archivo_log), exist_ok=True)

# Función Log
def log(mensaje):
    with open(archivo_log, "a", encoding="utf-8") as f:
        timestamp = time.strftime("%H:%M:%S")
        f.write(f"[{timestamp}] {mensaje}\n")

log("=== INICIANDO SESIÓN DE BUCLE WAYLAND ===")
log(f"Modo Desarrollo: {dev_mode}")

# ==========================================
#    EL GRAN BUCLE
# ==========================================
while True:
    filas = []
    tarea_actual = None
    indice_fila = -1
    
    # 1. LEER CSV
    try:
        with open(archivo_csv, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            filas = list(reader)
    except Exception as e:
        log(f"ERROR: No se pudo leer el CSV. {str(e)}")
        error_dialog("Error", "Fallo al leer CSV")
        break

    # 2. BUSCAR PENDIENTE
    for i, fila in enumerate(filas):
        if i == 0: continue 
        if len(fila) < 2: continue 
        
        estado = fila[2] if len(fila) > 2 else ""
        
        # Procesar SOLO si el estado está vacío
        if not estado.strip():
            tarea_actual = fila
            indice_fila = i
            break

    # SALIDA DEL BUCLE (Si no hay tareas)
    if not tarea_actual:
        log("No hay más tareas pendientes. Saliendo del bucle.")
        break

    url_video = tarea_actual[0]
    nombre_clase = tarea_actual[1]

    log(f"--- Procesando: {nombre_clase} ---")

    # ==========================================
    #       NAVEGACIÓN Y EXTRACCIÓN
    # ==========================================
    
    try:
        # Limpiar portapapeles
        fill_clipboard("")
        
        # Abrir Video en nueva pestaña
        send_shortcut("ctrl+t")
        time.sleep(esperaIntantaneo) 
        send_keys_text(url_video)
        send_shortcut("enter")
        time.sleep(esperaLargo) 

        # 1. Clic para iniciar el video
        click_absolute(x_iniciar_video, y_iniciar_video, 1)
        time.sleep(esperaCorto)

        # 2. Clic para pausar el video
        click_absolute(x_pausar_video, y_pausar_video, 1)
        time.sleep(esperaCorto)

        # 3. Clic para abrir la transcripción
        click_absolute(x_abrir_transcripcion, y_abrir_transcripcion, 1)
        time.sleep(esperaLargo)

        # 4. Doble clic para seleccionar una palabra de la transcripción
        click_absolute(x_seleccionar_palabra, y_seleccionar_palabra, 1)
        time.sleep(0.1)
        click_absolute(x_seleccionar_palabra, y_seleccionar_palabra, 1)
        time.sleep(esperaCorto)

        # 5. Seleccionar todo el texto hasta el final
        send_shortcut("ctrl+shift+End")
        time.sleep(esperaCorto)

        # 6. Copiar
        send_shortcut("ctrl+c")
        time.sleep(esperaCorto)
        
    except Exception as e:
        log(f"ERROR DURANTE NAVEGACIÓN: {str(e)}")
        errores_hoy += 1
        break

    # ==========================================
    #       GUARDADO Y SUBIDA A DRIVE
    # ==========================================
    
    try:
        log("Procesando transcripción y subiendo a Drive...")
        texto_copiado = get_clipboard()
        
        regex_tiempo = re.compile(r'^\d{1,2}:\d{2}(:\d{2})?$')
        lineas = texto_copiado.split('\n')
        texto_limpio = []
        linea_actual = ""
        cantidad_timestamps = 0
        
        for linea in lineas:
            linea = linea.strip()
            if not linea: continue
            
            if regex_tiempo.match(linea):
                cantidad_timestamps += 1
                if linea_actual: texto_limpio.append(linea_actual)
                linea_actual = linea + " "
            else:
                if cantidad_timestamps > 0:
                    linea_actual += linea + " "
                
        if linea_actual: texto_limpio.append(linea_actual.strip())
        texto_copiado_formateado = "\n".join(texto_limpio)
        
        # --- PRUEBA DE CALIDAD SUPREMA ---
        if cantidad_timestamps < 5:
            log(f"⚠️ PRUEBA DE CALIDAD FALLIDA: No se detectaron suficientes timestamps ({cantidad_timestamps}).")
            filas[indice_fila][2] = "ERROR"
            with open(archivo_csv, 'w', newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(filas)
            errores_hoy += 1
            log(f"Se marcó {nombre_clase} como ERROR. Deteniendo bucle por precaución.")
            break
        # -------------------------
        
        ruta_archivo = os.path.join(carpeta_guardado, f"Transcripcion - {nombre_clase}.txt")
        
        # Preparar texto final
        encabezado = "=========================================\n"
        encabezado += f"Clase: {nombre_clase}\n"
        encabezado += f"Fuente (URL): {url_video}\n"
        encabezado += "Generado Automáticamente en KDE/Wayland\n"
        encabezado += "=========================================\n\n"
        
        texto_final = encabezado + texto_copiado_formateado
        
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(texto_final)
        
        # ACTUALIZAR CSV
        filas[indice_fila][2] = "LISTO"
        with open(archivo_csv, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(filas)
            
        # SUBIR A DRIVE
        script_drive = os.path.join(base_dir, "organizador_csv", "subir_a_drive.py")
        try:
            subprocess.call([venv_python, script_drive, ruta_archivo, nombre_clase])
        except Exception as drive_e:
            log(f"Error al ejecutar script de Drive: {str(drive_e)}")
            
        procesados_hoy += 1
        log(f"Éxito. CSV actualizado y archivo enviado a Drive para: {nombre_clase}")
        
    except Exception as e:
        log(f"ERROR al guardar archivo o actualizar CSV: {str(e)}")
        error_dialog("Error Guardado", str(e))
        errores_hoy += 1
        break

    if dev_mode:
        log("Modo de desarrollo activado. Finalizando ejecución tras el primer ciclo.")
        break

    time.sleep(2)

log("--- BUCLE FINALIZADO ---")

if not dev_mode:
    log("Ejecutando chequeo de duplicados...")
    try:
        subprocess.call([venv_python, script_duplicados])
    except Exception as e:
        log(f"Error al chequear duplicados: {str(e)}")

# AVISO FINAL EN EL NAVEGADOR
try:
    send_shortcut("ctrl+t")
    time.sleep(1)
    if errores_hoy > 0:
        aviso = f"PROCESO_TERMINADO_CON_ERRORES__REVISA_LOS_LOGS__VIDEOS_{procesados_hoy}"
    else:
        aviso = f"PROCESO_TERMINADO_EXITOSAMENTE__VIDEOS_{procesados_hoy}"
    send_keys_text(aviso)
except:
    pass

log("=== FIN DE SESIÓN ===")
