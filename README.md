# Mis Scripts (Versión Wayland / Fedora KDE)

Este repositorio contiene la migración de los scripts de AutoKey a un entorno nativo Wayland en KDE Plasma, utilizando `ydotool` y `wl-clipboard`.

## Requisitos previos

Para que estos scripts funcionen correctamente, necesitas tener instalados los siguientes paquetes en Fedora:

```bash
sudo dnf install ydotool wl-clipboard kdialog
```

**Importante sobre ydotool:**
`ydotool` funciona a nivel del sistema y requiere que su servicio esté activo para que los scripts tengan permisos de crear el teclado y ratón virtuales. Actívalo con:
```bash
sudo systemctl enable --now ydotool
```
*(Si no quieres usar `sudo` cada vez, asegúrate de que tu usuario esté en el grupo `ydotool` o configura el demonio a nivel de usuario).*

## Cómo configurar los atajos en KDE Plasma 6

Dado que en Plasma 6 ya no existe el antiguo módulo de "Accesos rápidos personalizados", los scripts ahora se configuran directamente desde la sección principal de Atajos:

1. Abre las **Preferencias del sistema**.
2. Dirígete a la sección **Teclado** y luego a **Atajos** (Shortcuts).
3. Haz clic en el botón **Añadir nuevo** (Add New) -> **Orden/Comando** (Command).
4. En el campo de comando, escribe la ruta a tu script, precedida por `python3`. Ejemplo:
   `python3 /home/voupi/Documentos/GIT/Mis_Scripts_Wayland/transcripciones_wayland.py`
5. Finalmente, asigna la combinación de teclas que desees (ej: `Ctrl + Alt + T`).

¡Listo! Cuando presiones esas teclas, KDE ejecutará el script de fondo y `ydotool` realizará los movimientos y clics sin ser bloqueado por Wayland.

## Obtener coordenadas en Wayland

En Wayland (KDE), la forma de obtener las coordenadas del cursor ya no es con `xdotool`. Puedes usar el script `ver_coordenadas_wayland.py` incluido en este repositorio para ver en tiempo real las coordenadas (X, Y) y poder configurar tus variables `x_iniciar_video`, `y_abrir_transcripcion`, etc.
