# ============================================================
# RULETA RUSA DE ARCHIVOS
# Proyecto de consola - Unidad: Estructuras externas (ficheros)
# ============================================================

import os
import os.path
import shutil
import random
from datetime import datetime

# ------------------------------------------------------------
# CONSTANTES: rutas de las carpetas y archivos del proyecto
# ------------------------------------------------------------

CARPETA_JUGADORES = "jugadores"          # Carpeta donde se guardan los jugadores
CARPETA_LOG       = "log"                # Carpeta donde se guarda el log
CARPETA_BACKUP    = "backup"             # Carpeta donde se guardan las copias de seguridad
RUTA_LOG          = os.path.join(CARPETA_LOG, "partida.log")  # Ruta completa al log
MAX_JUGADORES     = 7                    # Máximo de jugadores permitidos

# ¿Por qué os.path.join en vez de "log/partida.log"?
# Porque os.path.join funciona en Windows, Linux y Mac.
# En Windows la barra es "\" y en Linux es "/". join lo resuelve solo.


# ------------------------------------------------------------
# FUNCIONES DE ENTORNO
# ------------------------------------------------------------

def crear_entorno():
    """
    Crea las carpetas necesarias para el proyecto si no existen.
    Se llama siempre al arrancar el programa.
    """
    try:
        # exist_ok=True significa: "si ya existe, no hagas nada, no des error"
        os.makedirs(CARPETA_JUGADORES, exist_ok=True)
        os.makedirs(CARPETA_LOG, exist_ok=True)
        print("Entorno listo.\n")
    except OSError as e:
        print(f"Error al crear las carpetas del entorno: {e}")

# ------------------------------------------------------------
# FUNCIONES DE LOG
# ------------------------------------------------------------

def inicializar_log():
    """
    Crea el archivo de log desde cero (sobrescribe si ya existe).
    Se llama siempre al comenzar una nueva partida.
    """
    try:
        # Modo "w" → write: si el archivo existe lo borra, si no existe lo crea
        with open(RUTA_LOG, "w", encoding="utf-8") as archivo:
            # Escribimos una cabecera para que el log quede bonito y claro
            ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            archivo.write("=" * 45 + "\n")
            archivo.write("   LOG DE PARTIDA - RULETA RUSA DE ARCHIVOS\n")
            archivo.write(f"   Partida iniciada el {ahora}\n")
            archivo.write("=" * 45 + "\n\n")
        print("Log de partida inicializado.\n")
    except OSError as e:
        print(f"Error al inicializar el log: {e}")


def escribir_log(mensaje):
    """
    Añade una línea al archivo de log con fecha, hora y mensaje.
    Se llama cada vez que ocurre algo importante en la partida.
    """
    try:
        # Modo "a" → append: añade al final del archivo sin borrar nada
        with open(RUTA_LOG, "a", encoding="utf-8") as archivo:
            ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Cada línea tendrá este formato:
            # [26/05/2025 10:32:15] El jugador X ha sido eliminado.
            archivo.write(f"[{ahora}] {mensaje}\n")
    except OSError as e:
        print(f"Error al escribir en el log: {e}")

# ------------------------------------------------------------
# FUNCIONES AUXILIARES
# ------------------------------------------------------------

def obtener_jugadores():
    """
    Devuelve una lista con los nombres de los archivos de jugadores.
    Usa os.listdir() para leer el contenido de la carpeta.

    Retorna:
        list: Lista de nombres de archivo (ej: ["jugador_ana.txt"])
              Lista vacía si no hay jugadores o hay un error.
    """
    try:
        # os.listdir() devuelve todos los archivos de una carpeta
        archivos = os.listdir(CARPETA_JUGADORES)

        # Filtramos: solo queremos archivos .txt que empiecen por "jugador_"
        jugadores = [f for f in archivos if f.startswith("jugador_") and f.endswith(".txt")]

        return jugadores

    except OSError as e:
        print(f"Error al leer la carpeta de jugadores: {e}")
        return []


def renombrar_jugador(archivo_actual, nuevo_nombre):
    """
    Renombra el archivo físico del jugador cuando su nombre ha cambiado.
    Se llama automáticamente desde modificar_jugador() si el nombre cambia.
    Usa os.rename() para cambiar el nombre del archivo en disco.

    Parámetros:
        archivo_actual (str): Nombre actual del archivo (ej: "jugador_ana.txt")
        nuevo_nombre   (str): Nuevo nombre del jugador (ej: "Maria")
    """
    # Construimos el nuevo nombre de archivo igual que en crear_jugador()
    nombre_base   = f"jugador_{nuevo_nombre.lower().replace(' ', '_')}"
    nuevo_archivo = f"{nombre_base}.txt"
    ruta_actual   = os.path.join(CARPETA_JUGADORES, archivo_actual)
    ruta_nueva    = os.path.join(CARPETA_JUGADORES, nuevo_archivo)

    # Si ya existe ese nombre de archivo, añadimos contador (_2, _3...)
    contador = 2
    while os.path.exists(ruta_nueva):
        nuevo_archivo = f"{nombre_base}_{contador}.txt"
        ruta_nueva    = os.path.join(CARPETA_JUGADORES, nuevo_archivo)
        contador += 1

    try:
        os.rename(ruta_actual, ruta_nueva)   # os.rename() cambia el nombre en disco
        print(f"  Archivo renombrado a '{nuevo_archivo}'.")
    except OSError as e:
        print(f"Error al renombrar el archivo: {e}")

# ------------------------------------------------------------
# CRUD DE JUGADORES
# ------------------------------------------------------------

def crear_jugador():
    """
    Pide nombre y apellidos al usuario y crea un archivo .txt
    con los datos del jugador en la carpeta de jugadores.
    """
    print("\n--- AÑADIR JUGADOR ---")

    # Comprobamos que no se supere el máximo de jugadores
    jugadores = obtener_jugadores()
    if len(jugadores) >= MAX_JUGADORES:
        print(f"Ya hay {MAX_JUGADORES} jugadores. No se pueden añadir más.\n")
        return  # Salimos de la función sin hacer nada más

    # Pedimos los datos al usuario
    nombre = input("Nombre: ").strip()
    apellidos = input("Apellidos: ").strip()

    # Validación básica: no permitir campos vacíos
    if not nombre or not apellidos:
        print("El nombre y los apellidos no pueden estar vacíos.\n")
        return

    # Construimos el nombre del archivo en minúsculas y sin espacios
    # Ejemplo: "Ana García" → "jugador_ana.txt"
    nombre_base = f"jugador_{nombre.lower().replace(' ', '_')}"
    nombre_archivo = f"{nombre_base}.txt"
    ruta_archivo = os.path.join(CARPETA_JUGADORES, nombre_archivo)

    contador = 2
    while os.path.exists(ruta_archivo):
        nombre_archivo = f"{nombre_base}_{contador}.txt"
        ruta_archivo = os.path.join(CARPETA_JUGADORES, nombre_archivo)
        contador += 1


    # Creamos el archivo con los datos del jugador
    try:
        # Modo "w" → creamos el archivo nuevo
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(f"nombre={nombre}\n")
            archivo.write(f"apellidos={apellidos}\n")

        print(f"Jugador '{nombre} {apellidos}' añadido correctamente.\n")

    except OSError as e:
        print(f"Error al crear el jugador: {e}")

def leer_jugadores():
    """
    Muestra por pantalla todos los jugadores existentes
    leyendo el contenido de cada archivo .txt.
    """
    print("\n--- LISTA DE JUGADORES ---")

    jugadores = obtener_jugadores()

    # Comprobamos si hay jugadores
    if not jugadores:
        print("No hay jugadores registrados.\n")
        return

    # Recorremos cada archivo y mostramos sus datos
    for i, archivo in enumerate(jugadores, start=1):
        ruta_archivo = os.path.join(CARPETA_JUGADORES, archivo)

        try:
            # Modo "r" → solo lectura
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()  # Leemos todas las líneas de golpe

            # Cada línea tiene formato "clave=valor"
            # Usamos un diccionario para guardar los datos
            datos = {}
            for linea in lineas:
                linea = linea.strip()        # Quitamos saltos de línea
                if "=" in linea:             # Comprobamos que la línea es válida
                    clave, valor = linea.split("=", 1)  # Separamos por el primer "="
                    datos[clave] = valor

            # Mostramos los datos del jugador
            nombre    = datos.get("nombre", "Desconocido")
            apellidos = datos.get("apellidos", "Desconocido")
            print(f"  {i}. {nombre} {apellidos}  ({archivo})")

        except OSError as e:
            print(f"Error al leer el archivo {archivo}: {e}")

    print()  # Línea en blanco al final para que quede limpio

def modificar_jugador():
    """
    Permite cambiar el nombre o los apellidos de un jugador existente.
    """
    print("\n--- MODIFICAR JUGADOR ---")

    jugadores = obtener_jugadores()

    if not jugadores:
        print("No hay jugadores registrados.\n")
        return

    # Mostramos la lista para que el usuario elija
    leer_jugadores()

    try:
        opcion = int(input("Elige el número del jugador a modificar: ").strip())

        # Comprobamos que el número esté dentro del rango válido
        if opcion < 1 or opcion > len(jugadores):
            print("Número no válido.\n")
            return

    except ValueError:
        # Si el usuario escribe algo que no es un número
        print("Debes introducir un número.\n")
        return

    # Obtenemos el archivo correspondiente al jugador elegido
    archivo_elegido = jugadores[opcion - 1]  # -1 porque las listas empiezan en 0
    ruta_archivo = os.path.join(CARPETA_JUGADORES, archivo_elegido)

    # Leemos los datos actuales del jugador
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        datos = {}
        for linea in lineas:
            linea = linea.strip()
            if "=" in linea:
                clave, valor = linea.split("=", 1)
                datos[clave] = valor

        # Mostramos los datos actuales
        print(f"\n  Datos actuales:")
        print(f"  Nombre    : {datos.get('nombre', '')}")
        print(f"  Apellidos : {datos.get('apellidos', '')}")
        print()

        # Pedimos los nuevos datos
        # Si el usuario pulsa Enter sin escribir nada, mantenemos el valor actual
        nuevo_nombre = input(f"  Nuevo nombre [{datos.get('nombre', '')}]: ").strip()
        nuevos_apellidos = input(f"  Nuevos apellidos [{datos.get('apellidos', '')}]: ").strip()

        if not nuevo_nombre:
            nuevo_nombre = datos.get("nombre", "")
        if not nuevos_apellidos:
            nuevos_apellidos = datos.get("apellidos", "")

        # Sobreescribimos el archivo con los datos actualizados
        # Modo "w" → borra el contenido anterior y escribe el nuevo
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(f"nombre={nuevo_nombre}\n")
            f.write(f"apellidos={nuevos_apellidos}\n")

        print(f"\n Jugador actualizado: '{nuevo_nombre} {nuevos_apellidos}'.")

        # Si el nombre cambió, renombramos también el archivo físico
        nombre_original = datos.get("nombre", "")
        if nuevo_nombre.lower() != nombre_original.lower():
            renombrar_jugador(archivo_elegido, nuevo_nombre)

        print()

    except OSError as e:
        print(f"Error al modificar el jugador: {e}")

def eliminar_jugador():
    """
    Elimina el archivo de un jugador elegido por el usuario.
    Pide confirmación antes de borrar.
    """
    print("\n--- ELIMINAR JUGADOR ---")

    jugadores = obtener_jugadores()

    if not jugadores:
        print("No hay jugadores registrados.\n")
        return

    # Mostramos la lista para que el usuario elija
    leer_jugadores()

    try:
        opcion = int(input("Elige el número del jugador a eliminar: ").strip())

        if opcion < 1 or opcion > len(jugadores):
            print("Número no válido.\n")
            return

    except ValueError:
        print("Debes introducir un número.\n")
        return

    archivo_elegido = jugadores[opcion - 1]
    ruta_archivo = os.path.join(CARPETA_JUGADORES, archivo_elegido)

    # Pedimos confirmación antes de borrar
    confirmacion = input(f"¿Seguro que quieres eliminar '{archivo_elegido}'? (s/n): ").strip().lower()

    if confirmacion != "s":
        print("Operación cancelada.\n")
        return

    try:
        os.remove(ruta_archivo)  # os.remove() borra un archivo
        print(f"Jugador '{archivo_elegido}' eliminado correctamente.\n")

    except OSError as e:
        print(f"Error al eliminar el jugador: {e}")

# ------------------------------------------------------------
# MOTOR DEL JUEGO
# ------------------------------------------------------------

def hay_suficientes_jugadores():
    """
    Comprueba si el número de jugadores está entre 2 y el máximo permitido.

    Retorna:
        bool: True si hay suficientes jugadores, False si no.
    """
    jugadores = obtener_jugadores()
    total = len(jugadores)

    if total < 2:
        print(f"Necesitas al menos 2 jugadores para jugar. Ahora hay {total}.\n")
        return False

    if total > MAX_JUGADORES:
        print(f"Hay demasiados jugadores ({total}). El máximo es {MAX_JUGADORES}.\n")
        return False

    return True  # Todo correcto

def eliminar_jugador_aleatorio():
    """
    Elige un jugador al azar de la carpeta y borra su archivo.

    Retorna:
        str: El nombre completo del jugador eliminado.
             None si ocurrió algún error.
    """
    jugadores = obtener_jugadores()

    if not jugadores:
        return None

    # random.choice() elige un elemento aleatorio de una lista
    archivo_elegido = random.choice(jugadores)
    ruta_archivo = os.path.join(CARPETA_JUGADORES, archivo_elegido)

    # Leemos el nombre del jugador antes de borrarlo
    # (para poder mostrarlo y escribirlo en el log)
    nombre_completo = archivo_elegido  # valor por defecto si falla la lectura

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        datos = {}
        for linea in lineas:
            linea = linea.strip()
            if "=" in linea:
                clave, valor = linea.split("=", 1)
                datos[clave] = valor

        nombre_completo = f"{datos.get('nombre', '?')} {datos.get('apellidos', '?')}"

    except OSError as e:
        print(f"Error al leer el archivo del jugador: {e}")

    # Borramos el archivo del jugador eliminado
    try:
        os.remove(ruta_archivo)
        return nombre_completo

    except OSError as e:
        print(f"Error al eliminar el jugador: {e}")
        return None

def iniciar_partida():
    """
    Controla el flujo completo de la partida.
    Elimina jugadores aleatoriamente hasta que quede uno solo.
    """
    print("\n--- INICIAR PARTIDA ---\n")

    # Paso 1: Comprobamos que haya suficientes jugadores
    if not hay_suficientes_jugadores():
        return  # Salimos si no hay suficientes jugadores

    # Paso 2: Copia de seguridad automática antes de que la partida borre jugadores
    hacer_copia_seguridad()

    # Paso 3: Inicializamos el log (se sobrescribe el anterior)
    inicializar_log()

    # Paso 3: Mostramos y registramos los jugadores que participan
    jugadores_iniciales = obtener_jugadores()
    total_inicial = len(jugadores_iniciales)

    print(f"¡Comienza la partida con {total_inicial} jugadores!\n")
    escribir_log(f"Partida iniciada con {total_inicial} jugadores.")
    escribir_log("-" * 35)

    # Registramos en el log quiénes participan
    for archivo in jugadores_iniciales:
        ruta = os.path.join(CARPETA_JUGADORES, archivo)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                lineas = f.readlines()
            datos = {}
            for linea in lineas:
                linea = linea.strip()
                if "=" in linea:
                    clave, valor = linea.split("=", 1)
                    datos[clave] = valor
            nombre_completo = f"{datos.get('nombre', '?')} {datos.get('apellidos', '?')}"
            escribir_log(f"Jugador registrado: {nombre_completo}")
        except OSError:
            escribir_log(f"Jugador registrado: {archivo}")

    escribir_log("-" * 35)
    print("Pulsa Enter para girar la ruleta...")
    print("=" * 40)

    # -------------------------------------------------------
    # BUCLE PRINCIPAL DE LA PARTIDA
    # -------------------------------------------------------
    ronda = 1

    while True:

        # Comprobamos cuántos jugadores quedan
        jugadores_restantes = obtener_jugadores()
        total_restantes = len(jugadores_restantes)

        # ¿Ha terminado la partida?
        if total_restantes == 1:
            # Leemos el nombre del ganador desde su archivo
            archivo_ganador = jugadores_restantes[0]
            ruta_ganador = os.path.join(CARPETA_JUGADORES, archivo_ganador)

            try:
                with open(ruta_ganador, "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                datos = {}
                for linea in lineas:
                    linea = linea.strip()
                    if "=" in linea:
                        clave, valor = linea.split("=", 1)
                        datos[clave] = valor
                nombre_ganador = f"{datos.get('nombre', '?')} {datos.get('apellidos', '?')}"
            except OSError:
                nombre_ganador = archivo_ganador

            # Mostramos y registramos al ganador
            print("\n" + "=" * 40)
            print(f"¡GANADOR: {nombre_ganador}!")
            print("=" * 40 + "\n")
            escribir_log("-" * 35)
            escribir_log(f"GANADOR: {nombre_ganador}")
            escribir_log("Partida finalizada.")
            print(f"Resultado guardado en '{RUTA_LOG}'.\n")

            # Copiamos el log al backup para que exportar_estadisticas() pueda leerlo
            try:
                ultima_backup = sorted(os.listdir(CARPETA_BACKUP))[-1]
                shutil.copy(RUTA_LOG, os.path.join(CARPETA_BACKUP, ultima_backup))
            except OSError:
                pass  # Si falla el copiado del log no interrumpimos el programa

            # Eliminamos todos los jugadores automáticamente al terminar la partida
            try:
                shutil.rmtree(CARPETA_JUGADORES)
                os.makedirs(CARPETA_JUGADORES, exist_ok=True)
                print("Jugadores eliminados. ¡Listo para una nueva partida!\n")
                escribir_log("Jugadores eliminados. Tablero limpio.")
            except OSError as e:
                print(f"Error al limpiar jugadores tras la partida: {e}")

            break  # Salimos del bucle → partida terminada

        # Mostramos los jugadores que siguen vivos
        print(f"\n  Ronda {ronda} — Jugadores restantes: {total_restantes}")
        print("  " + "-" * 30)
        for i, archivo in enumerate(jugadores_restantes, start=1):
            ruta = os.path.join(CARPETA_JUGADORES, archivo)
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                datos = {}
                for linea in lineas:
                    linea = linea.strip()
                    if "=" in linea:
                        clave, valor = linea.split("=", 1)
                        datos[clave] = valor
                print(f"  {i}. {datos.get('nombre','?')} {datos.get('apellidos','?')}")
            except OSError:
                print(f"  {i}. {archivo}")

        print()
        input("Pulsa Enter para girar la ruleta...")

        # Eliminamos un jugador al azar
        eliminado = eliminar_jugador_aleatorio()

        if eliminado:
            print(f"\n¡{eliminado} ha sido eliminado!\n")
            escribir_log(f"Ronda {ronda}: '{eliminado}' ha sido eliminado.")
        else:
            print("\nError al eliminar un jugador.\n")

        ronda += 1
        print("=" * 40)

# ------------------------------------------------------------
# FUNCIONES DE SISTEMA OPERATIVO
# ------------------------------------------------------------

def mostrar_info_sistema():
    """
    Muestra información del entorno del proyecto usando os y os.path.
    Útil para comprobar que todo está en su sitio.
    """
    print("\n--- INFORMACIÓN DEL SISTEMA ---\n")

    try:
        # os.getcwd() → devuelve la carpeta actual de trabajo
        carpeta_actual = os.getcwd()
        print(f"  Directorio de trabajo : {carpeta_actual}")

        # os.path.abspath() → convierte ruta relativa en ruta absoluta
        ruta_jugadores = os.path.abspath(CARPETA_JUGADORES)
        ruta_log       = os.path.abspath(RUTA_LOG)
        print(f"  Carpeta jugadores     : {ruta_jugadores}")
        print(f"  Archivo log           : {ruta_log}")

        # os.path.isdir() → comprueba si una ruta es una carpeta
        existe_jugadores = os.path.isdir(CARPETA_JUGADORES)
        existe_log       = os.path.isdir(CARPETA_LOG)
        print(f"\n  ¿Existe carpeta jugadores? : {'Sí' if existe_jugadores else 'No'}")
        print(f"  ¿Existe carpeta log?       : {'Sí' if existe_log else 'No'}")

        # os.path.isfile() → comprueba si el log existe como archivo
        existe_archivo_log = os.path.isfile(RUTA_LOG)
        print(f"  ¿Existe archivo log?       : {'Sí' if existe_archivo_log else 'No'}")

        # Tamaño del log si existe
        if existe_archivo_log:
            # os.path.getsize() → tamaño en bytes
            tamanio = os.path.getsize(RUTA_LOG)
            print(f"  Tamaño del log             : {tamanio} bytes")

        # Número de jugadores actuales
        jugadores = obtener_jugadores()
        print(f"\n  Jugadores registrados   : {len(jugadores)} / {MAX_JUGADORES}")

        # Listamos los archivos de jugadores con su tamaño
        if jugadores:
            print("\n  Archivos de jugadores:")
            for archivo in jugadores:
                ruta = os.path.join(CARPETA_JUGADORES, archivo)
                # os.path.isfile() para asegurarnos de que es un archivo
                if os.path.isfile(ruta):
                    tamanio = os.path.getsize(ruta)
                    print(f"    · {archivo}  ({tamanio} bytes)")

    except OSError as e:
        print(f"Error al obtener información del sistema: {e}")

    print()

def limpiar_jugadores():
    """
    Borra todos los archivos de jugadores de la carpeta.
    Usa shutil para borrar la carpeta entera y la vuelve a crear vacía.
    Pide confirmación antes de actuar.
    """
    print("\n--- LIMPIAR TODOS LOS JUGADORES ---\n")

    jugadores = obtener_jugadores()

    if not jugadores:
        print("No hay jugadores que eliminar.\n")
        return

    print(f"  Esto eliminará {len(jugadores)} jugador/es permanentemente.")
    confirmacion = input("  ¿Estás seguro? (s/n): ").strip().lower()

    if confirmacion != "s":
        print("Operación cancelada.\n")
        return

    try:
        # shutil.rmtree() → borra la carpeta ENTERA con todo su contenido
        # Es más directo que borrar archivo por archivo con os.remove()
        shutil.rmtree(CARPETA_JUGADORES)

        # Volvemos a crear la carpeta vacía
        # (la necesitamos para que el programa siga funcionando)
        os.makedirs(CARPETA_JUGADORES, exist_ok=True)

        print(f"Todos los jugadores han sido eliminados.\n")

    except OSError as e:
        print(f"Error al limpiar los jugadores: {e}")

