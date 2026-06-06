import random
from datetime import datetime

# ---------------- INICIO ----------------

while True:
    input("\n🧨 BUSCAMINAS TERMINAL\nPresiona ENTER para continuar...")

    print("\n1. Iniciar sesión")
    print("2. Crear usuario")
    print("3. Salir")

    opcion_inicio = input("> ")

    # ---------------- CREAR USUARIO ----------------
    if opcion_inicio == "2":
        try:
            archivo = open("usuarios.txt", "r")
            usuarios = [linea.strip() for linea in archivo]
            archivo.close()
        except:
            usuarios = []

        nombre = input("Ingrese nombre de usuario: ")

        if nombre in usuarios:
            print("❌ Usuario ya existe")
        else:
            archivo = open("usuarios.txt", "a")
            archivo.write(nombre + "\n")
            archivo.close()
            print("✅ Usuario creado")

    # ---------------- LOGIN ----------------
    elif opcion_inicio == "1":
        try:
            archivo = open("usuarios.txt", "r")
            usuarios = [linea.strip() for linea in archivo]
            archivo.close()
        except:
            usuarios = []

        logueado = False

        while not logueado:
            nombre = input("Ingrese su usuario: ")

            if nombre in usuarios:
                print(f"\n✅ Bienvenido {nombre}")
                logueado = True
            else:
                print("❌ Usuario no encontrado")
                op = input("1. Intentar de nuevo\n2. Volver\n> ")

                if op == "2":
                    break

        # ---------------- MENÚ PRINCIPAL ----------------
        while logueado:
            print(f"\n🎮 Usuario: {nombre}")
            print("1. Campaña")
            print("2. Desafío")
            print("3. Ranking")
            print("4. Historial")
            print("5. Cerrar sesión")

            op_menu = input("> ")

            # ---------------- MODO CAMPAÑA ----------------
            if op_menu == "1":
                nivel = 1
                continuar = True

                while nivel <= 12 and continuar:
                    print(f"\n🧠 Nivel {nivel}")

                    casillas = list(range(1, 20))
                    minas = random.sample(casillas, nivel)
                    usadas = []
                    puntaje = 0

                    jugando = True

                    while jugando:
                        disponibles = [x for x in casillas if x not in usadas]
                        print("Disponibles:", disponibles)

                        eleccion = input("Elige un número: ")

                        if not eleccion.isdigit():
                            print("❌ Ingresa un número válido")
                            continue

                        eleccion = int(eleccion)

                        if eleccion not in casillas:
                            print("❌ Número fuera de rango")
                            continue

                        if eleccion in usadas:
                            print("⚠️ Ya elegiste ese número")
                            continue

                        usadas.append(eleccion)

                        if eleccion in minas:
                            print("💥 PERDISTE en nivel", nivel)
                            jugando = False
                            continuar = False
                        else:
                            puntaje += 10 * nivel
                            print("✅ Seguro. Puntaje:", puntaje)

                    # Guardar partida
                    fecha = datetime.now().strftime("%Y-%m-%d")
                    archivo = open("partidas.txt", "a")
                    archivo.write(f"{nombre},{puntaje},Campaña,{fecha}\n")
                    archivo.close()

                    if continuar:
                        nivel += 1
                    else:
                        print("📊 Llegaste hasta el nivel:", nivel)

            # ---------------- DESAFÍO ----------------
            elif op_menu == "2":
                minas_cantidad = input("Cantidad de minas (max 24): ")

                if not minas_cantidad.isdigit():
                    print("❌ Número inválido")
                    continue

                minas_cantidad = int(minas_cantidad)

                if minas_cantidad > 24:
                    minas_cantidad = 24

                casillas = list(range(1, 20))
                minas = random.sample(casillas, minas_cantidad)
                usadas = []
                puntaje = 0

                jugando = True

                while jugando:
                    disponibles = [x for x in casillas if x not in usadas]
                    print("Disponibles:", disponibles)

                    eleccion = input("Elige un número: ")

                    if not eleccion.isdigit():
                        print("❌ Ingresa un número válido")
                        continue

                    eleccion = int(eleccion)

                    if eleccion not in casillas:
                        print("❌ Número fuera de rango")
                        continue

                    if eleccion in usadas:
                        print("⚠️ Ya elegiste ese número")
                        continue

                    usadas.append(eleccion)

                    if eleccion in minas:
                        print("💥 PERDISTE")
                        jugando = False
                    else:
                        puntaje += 10 * minas_cantidad
                        print("✅ Seguro. Puntaje:", puntaje)

                # Guardar
                fecha = datetime.now().strftime("%Y-%m-%d")
                archivo = open("partidas.txt", "a")
                archivo.write(f"{nombre},{puntaje},Desafio,{fecha}\n")
                archivo.close()

            # ---------------- RANKING ----------------
            elif op_menu == "3":
                try:
                    archivo = open("partidas.txt", "r")
                    lineas = archivo.readlines()
                    archivo.close()

                    ranking_campana = []
                    ranking_desafio = []

                    for linea in lineas:
                        datos = linea.strip().split(",")
                        usuario = datos[0]
                        puntos = int(datos[1])
                        modo = datos[2]

                        if modo == "Campaña":
                            ranking_campana.append((usuario, puntos))
                        else:
                            ranking_desafio.append((usuario, puntos))

                    ranking_campana.sort(key=lambda x: x[1], reverse=True)
                    ranking_desafio.sort(key=lambda x: x[1], reverse=True)

                    print("\n🏆 RANKING CAMPAÑA")
                    for i in range(min(5, len(ranking_campana))):
                        print(i+1, ranking_campana[i][0], "-", ranking_campana[i][1])

                    print("\n🔥 RANKING DESAFÍO")
                    for i in range(min(5, len(ranking_desafio))):
                        print(i+1, ranking_desafio[i][0], "-", ranking_desafio[i][1])

                except:
                    print("No hay partidas registradas.")
            # ---------------- HISTORIAL ----------------
            elif op_menu == "4":
                try:
                    archivo = open("partidas.txt", "r")
                    lineas = archivo.readlines()
                    archivo.close()

                    print(f"\n📜 HISTORIAL DE {nombre}")

                    encontrado = False

                    for linea in lineas:
                        datos = linea.strip().split(",")
                        usuario = datos[0]
                        puntos = datos[1]
                        modo = datos[2]
                        fecha = datos[3]

                        if usuario == nombre:
                            print(f"Modo: {modo} | Puntaje: {puntos} | Fecha: {fecha}")
                            encontrado = True

                    if not encontrado:
                        print("No tienes partidas registradas.")

                except:
                    print("No hay historial disponible.")

            elif op_menu == "5":
                logueado = False

    elif opcion_inicio == "3":
        break