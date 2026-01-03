import os  # Módulo estándar de Python para trabajar con archivos y carpetas

async def load_commands(bot, base_path = "commands"):
    """
    Esta función se encarga de:
    - Buscar archivos .py dentro de una carpeta (y subcarpetas)
    - Cargar esos archivos como comandos de Discord
    - Mostrar por consola qué comandos se cargaron y cuáles fallaron

    Parámetros:
    bot       → instancia de commands.Bot
    base_path → carpeta donde están los comandos (por defecto: "commands")
    """

    # Contadores para saber cuántos comandos se cargaron correctamente
    loaded = 0
    failed = 0

    # os.walk recorre una carpeta y TODAS sus subcarpetas
    # root  → ruta actual (ej: commands/fun)
    # _     → lista de subcarpetas (no la usamos aquí)
    # files → lista de archivos dentro de la carpeta
    for root, _, files in os.walk(base_path):

        # Recorremos todos los archivos encontrados
        for file in files:

            # Solo nos interesan archivos .py
            # y evitamos __init__.py porque no es un comando
            if file.endswith(".py") and file != "__init__.py":

                # Construimos la ruta completa del archivo
                # Ejemplo: commands/fun/ping.py
                path = os.path.join(root, file)

                # Convertimos la ruta del archivo en un módulo Python
                # commands/fun/ping.py → commands.fun.ping
                module = path.replace("\\", ".").replace("/", ".")
                module = module[:-3]  # Quitamos el ".py"

                try:
                    # Intentamos cargar el archivo como extensión
                    # Esto ejecuta la función setup(bot) dentro del archivo
                    await bot.load_extension(module)

                    # Si no hay errores, mostramos que se cargó correctamente
                    print(f"✅ Comando cargado: {module}")
                    loaded += 1

                except Exception as e:
                    # Si ocurre un error, lo mostramos en consola
                    print(f"❌ Error al cargar {module}: {e}")
                    failed += 1

    # Si NO se encontró ningún comando válido
    if loaded == 0 and failed == 0:
        print("⚠️ No se han encontrado comandos")
        return

    # Resumen final
    print("\n📊 Resumen de carga de comandos")
    print(f"✅ Comandos cargados correctamente: {loaded}")
    print(f"❌ Comandos con error: {failed}\n")
