import random
from datetime import datetime 

while True:
    input("Presiona Enter para iniciar el juego...")
    print("Seleccione una de las 3 opciones: ")
    print("1. Iniciar secion")
    print("2. Crar Usuario")
    print("3. Salir") 
    opcion = input("> ")
    if opcion == "2":
        try:
            archivo = open("usuarios.txt", "r")
            usuarios = [linea.strip() for linea in archivo]
            archivo.close()
        except:
            usuarios = []
        nombre = input("Ingrese su nombre de ususario:")
        if nombre in usuarios:
            print("El nombre de usuario ya existe, porfavor elija otro.")
        else:
            archivo = open("usuarios.txt", "a")
            archivo.write(nombre + "\n")
            archivo.close()
            print("Usuario creado exitosamente.")
    elif opcion == "1":
        try:
            archivo = open("usuarios.txt", "r")
            usuarios = [linea.strip() for linea in archivo]
            archivo.close()
        except:
            usuarios = []

        logueado = False

        while not logueado:
            nombre = input("Ingrese su nombre de usuario: ")
            if nombre in usuarios:
                print("Bienvenido, " + nombre + "!")
                logueado = True
            else:
                print("EL nombre de usuario no existe, porfavor intente de nuevo o cree un nuevo usuario.")
                nuevo_usuario = input("Desea crear un nuevo usuario? (s/n): ")
                if nuevo_usuario.lower() == "s":
                    archivo = open("usuarios.txt", "a")
                    archivo.write(nombre + "\n")
                    archivo.close()
                    print("Usuario creado exitosamente. Porfavor inicie sesion nuevamente.")
                    logueado = True
        while logueado:
            print(f"\n Usuario: {nombre}")
            print("1. Campaña ")
            print("2. Desafio")
            print("3. Ranking")
            print("4. Historial")
            print("5. Eliminar usuario")
            print("6. Cerrar sesión")
            op_juego = input ("> ")
            match op_juego:
                case "1":
                    print("Modo Campaña seleccionado.")
                    nivel = 1
                    continuar = True
                    puntaje = 0  
                    nivel_final = 0

                    while nivel <= 12 and continuar:
                        print(f"\nNivel {nivel}")
                        
                        casillas = list(range(1,17))
                        minas = random.sample(casillas, nivel)
                        usadas = []
                        jugando = True
                        while jugando:
                            disponible = [x for x in casillas if x not in usadas]
                            print(f"Casillas disponibles: {disponible}")
                            seleccion  = input("Elige un número: ")
                            if not seleccion.isdigit():
                                print("Por favor, ingrese un número válido.")
                                continue
                            seleccion = int(seleccion)
                            if seleccion not in casillas:
                                print("Número fuera de rango por favor elija un número entre 1 y 16.")
                                continue

                            if seleccion in usadas:
                                print("Ya has seleccionado esa casilla, por favor elige otra.")
                                continue
                            usadas.append(seleccion)
                            if seleccion in minas:
                                print("¡BOOM! Has perdido.")
                                jugando = False
                                continuar = False
                                nivel_final = nivel
                            else:
                                puntaje += 10 * nivel
                                print(f"¡Bien hecho! Has ganado {puntaje} puntos.")
                                if len(usadas) == len(casillas) - len(minas):
                                    print("¡Has despejado todas las casillas seguras del nivel!")
                                    jugando = False
                                    nivel_final = nivel

                        if continuar:
                            nivel += 1   

                    if nivel_final == 0:
                        nivel_final = nivel - 1
                    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    archivo = open ("partidas.txt", "a")
                    archivo.write(f"{nombre},Campaña,{puntaje},{nivel_final},{fecha}\n")  
                    archivo.close()

                    if not continuar:
                        print("Felicidades llegaste hasta el nivel " + str(nivel_final))
                    else:
                        print("¡Felicidades! Completaste los 12 niveles de la campaña.")

                case "2":
                    minas_cantidad = input("Ingrese la cantidad de minas (1-24):")
                    if not minas_cantidad.isdigit() or not (1 <= int(minas_cantidad) <= 24):
                        print("Por favor, ingrese un número válido entre 1 y 24.")
                        continue
                    minas_cantidad = int(minas_cantidad)
                    casillas = list(range(1, 26))
                    minas = random.sample(casillas, minas_cantidad)
                    usadas = []
                    puntaje = 0
                    jugando = True
                    while jugando:
                        disponible = [x for x in casillas if x not in usadas]
                        print(f"Casillas disponibles: {disponible}")
                        seleccion  = input("Elige un número: ")
                        if not seleccion.isdigit():
                            print("Por favor, ingrese un número válido.")
                            continue
                        seleccion = int(seleccion)
                        if seleccion not in casillas:
                            print("Número fuera de rango por favor elija un número entre 1 y 25.")
                            continue

                        if seleccion in usadas:
                            print("Ya has seleccionado esa casilla, por favor elige otra.")
                            continue
                        usadas.append(seleccion)
                        if seleccion in minas:
                            print("¡BOOM! Has perdido.")
                            jugando = False
                        else:
                            puntaje += 10
                            print(f"¡Bien hecho! Has ganado {puntaje} puntos.")
                    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    archivo = open ("partidas.txt", "a")
                    archivo.write(f"{nombre},Desafio,{puntaje},{minas_cantidad},{fecha}\n")  
                    archivo.close()

                case "3":
                    try:
                        archivo = open("partidas.txt", "r")
                        lineas = archivo.readlines()
                        archivo.close()

                        ranking_campana = []
                        ranking_desafio = []
                        
                        for linea in lineas:
                            datos = linea.strip().split(",")
                            usuario = datos[0]        
                            modo = datos[1]           
                            puntos = int(datos[2])    

                            if modo == "Campaña":
                                ranking_campana.append((usuario, puntos))
                            else:
                                ranking_desafio.append((usuario, puntos))

                        ranking_campana.sort(key = lambda x: x[1], reverse= True)
                        ranking_desafio.sort(key = lambda x: x[1], reverse = True)

                        print("\n Ranking de jugadores de modo Campaña:")
                        for i in range(min(5, len(ranking_campana))):
                            print(f"Campaña - {i+1}. {ranking_campana[i][0]}: {ranking_campana[i][1]} puntos")

                        print("\n Ranking de jugadores de modo Desafío:" )
                        for i in range(min(5, len(ranking_desafio))):
                            print(f"Desafío - {i+1}. {ranking_desafio[i][0]}: {ranking_desafio[i][1]} puntos")
                    except:
                        print("NO hay partidas registradas")

                case "4":
                    try:
                        archivo = open("partidas.txt", "r")
                        lineas = archivo.readlines()
                        archivo.close()

                        print(f"\n Historial de partidas de {nombre}:")

                        encontrado = False
                        for linea in lineas:
                            datos = linea.strip().split(",")
                            usuario = datos[0]
                            modo = datos[1]       
                            puntos = datos[2]     
                            fecha = datos[4]      
                            
                            if usuario == nombre:
                                print(f"{modo} , puntaje: {puntos},  fecha: {fecha}")
                                encontrado = True

                        if not encontrado:
                            print("No tienes partidas registradas. ")
                    except:
                        print("No hay historial disponible.")

                case "5":
                    confirmacion = input("Esta seguro de que desea eliminar su usuario? Esta accion no se puede deshacer. (s/n): ")
                    if confirmacion.lower() == "s":
                        try:
                            usuarios.remove(nombre)
                            archivo = open("usuarios.txt", "w")
                            for usuario in usuarios:
                                archivo.write(usuario + "\n")
                            archivo.close()
                            print("Usuario eliminado exitosamente. Cerrando sesión...")
                            logueado = False
                        except:
                            print("Error al eliminar el usuario.")
                    else:
                        print("Eliminación de usuario cancelada.")

                case "6":
                    print("Cerrando sesión....")
                    logueado = False
    elif opcion == "3":
        print("Saliendo del juego.........")
        break