import os
import importlib

"""
    Este archivo se encarga de:
    - Buscar archivos .py dentro de carpetas (y subcarpetas)
    - Cargar esos archivos como comandos y eventos de Discord
    - Mostrar por consola qué comandos y eventos se cargaron y cuáles fallaron

    Parámetros:
    bot       → instancia de commands.Bot
    base_path → carpeta donde están los comandos (por defecto: "commands")
"""

async def load_events(bot):

    # Variables de contadores de eventos y asignacion de eventos
    base_path = "events"
    loaded_events = 0

    # bucle for para asignar el algoritmo en cargado de buscar entre archivos
    for file in os.listdir(base_path):

        # Condicional: Si el archivo.terminaCon .py y el archivo 
        if file.endswith(".py") and file != "__init__.py":

            #Construye la ruta del módulo en formato Python
            #Ejemplo: events/ready.py → events.ready
            module = f"{base_path}.{file[:-3]}"
            # Espera que el bot cargue las extensiones de los modulos
            await bot.load_extension(module)
            # Suma uno a los eventos cargados
            loaded_events += 1

    # Si los eventos cargados son igual a 0
    if loaded_events == 0:
        # Entonces imprimira esto
        print("No se han encontrado Eventos")
    # Si no
    else:
        # Entonces imprimira esto
        print(f"{loaded_events} eventos cargados correctamente")


async def load_commands(bot, base_path = "cogs"):

    # variables de contadores de comandos
    loaded_commands = 0
    failed_commands = 0

    """
    os.walk recorre una carpeta y TODAS sus subcarpetas
    root  → ruta actual (ej: commands/fun)
    _     → lista de subcarpetas (no la usamos aquí)
    files → lista de archivos dentro de la carpeta
    """

    for root, _, files in os.walk(base_path):

        for file in files:

            # Solo cargan archivos .py válidos
            if file.endswith(".py") and file != "__init__.py":

                # Convierte la ruta del archivo en un módulo Python
                path = os.path.join(root, file)
                module = path.replace("\\", ".").replace("/", ".")[:-3]
                
                # Intenta cargar el comando
                try:
                    # Esto ejecuta la función setup(bot) dentro del archivo
                    await bot.load_extension(module)
                    # Si todo va bien, suma uno a los comandos cargados
                    loaded_commands += 1

                # Si hay un error al cargar el comando
                except Exception as error:
                    # Imprime esto
                    print(f"Error al cargar {module}: {error}")
                    # Suma uno a los comandos fallidos
                    failed_commands += 1

    # Si los comandos cargados son igual a 0 y lo mismo con los comandos fallidos
    if loaded_commands == 0 and failed_commands == 0:
        # Entonces imprimira esto retornando
        print("No se han encontrado comandos")
        return

    # Resumen final
    print(f"Comandos cargados correctamente: {loaded_commands}")
    print(f"Comandos con error: {failed_commands}\n")
