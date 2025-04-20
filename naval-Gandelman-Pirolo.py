import random
import os


#* Para ver los comentarios con colores usar la extension Better Comments de Vs Code (Para eso es lo que se agrega al principio de cada comentario)

#* https://docs.python.org/3/library/random.html
#* https://docs.python.org/3/library/os.html#os.system
#* https://docs.python.org/3/tutorial/datastructures.html
#* https://docs.python.org
#* https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
#* https://docs.python.org/3/tutorial/errors.html



#* Declaracion de constantes
N: int = 10
CANTIDAD_BARCOS: int = 5
CANTIDAD_DISPAROS: int = 20
LARGO_BARCOS: list[int] = [5, 4, 3, 3, 2]  

#* Direcciones
DERECHA: tuple[int, int] = (0, 1)
ABAJO: tuple[int, int] = (1, 0)
IZQUIERDA: tuple[int, int] = (0, -1)
ARRIBA: tuple[int, int] = (-1, 0)


def crear_tablero() -> list[list[str]]:
    #* Crea el tablero con N filas y N columnas y lo llena con ~
    return [["~" for _ in range(N)] for _ in range(N)]


def mostrar_tablero(tablero: list[list[str]], ocultar_barcos: bool = False) -> None:
    #* Imprime las columnas
    print("  " + " ".join(str(indice) for indice in range(N)))
    for fila in range(N):
        #? Imprime el número de fila al inicio de cada fila
        print(fila, end=" ")
        for columna in range(N):
            #? Imprime el valor de la celda
            celda:str = tablero[fila][columna]
            #? Si ocultar_barcos es True, muestra ~ en lugar de los barcos para así poder imprimir tanto para los barcos posicionados como cuando ataca el oponente
            if ocultar_barcos and celda == "O":
                print("~", end=" ")
            else:
                print(celda, end=" ")
        print()


def colocar_barco_aleatorio(tablero: list[list[str]], largo: int) -> bool:
    #* Posiciones válidas
    posiciones_posibles: list[tuple[int, int, int]] = []

    #? Generar todas las posiciones horizontales posibles
    for fila in range(N):
        for columna in range(N - largo + 1):
            if all(tablero[fila][columna + i] == "~" for i in range(largo)):
                posiciones_posibles.append((fila, columna, 0))  #? 0 para horizontal

    #? Generar todas las posiciones verticales posibles
    for fila in range(N - largo + 1):
        for columna in range(N):
            if all(tablero[fila + i][columna] == "~" for i in range(largo)):
                posiciones_posibles.append((fila, columna, 1))  #? 1 para vertical

    #! Si ninguna posicion es valida retorna False
    if not posiciones_posibles:
        print(f"No se pudo colocar barco de tamaño {largo}. No hay posiciones disponibles.")
        return False

    #* Elige una posicion valida aleatoria
    fila, columna , orientacion = random.choice(posiciones_posibles) 
    #* Coloca el barco 
    for i in range(largo):
        f:int = fila + (i if orientacion == 1 else 0)
        c:int = columna + (i if orientacion == 0 else 0)
        tablero[f][c] = "O"

    
    return True


def colocar_barco_manual(tablero: list[list[str]], largo: int, numero_jugador: int) -> None:
    #* Coloca un barco manualmente en el tablero
    while True:
        print(f"Jugador {numero_jugador}, coloca tu barco de tamaño {largo}")
        #* Muestra el tablero 
        mostrar_tablero(tablero)
        #? Se le pide al jugador que coloque el barco
        try:
            #? Se le pide al jugador que ingrese la fila, columna y orientacion
            fila: int = int(input("Fila inicial (0-9): "))
            columna: int = int(input("Columna inicial (0-9): "))
            orientacion: str = input("Orientación (h para horizontal, v para vertical): ").lower()
            
            #? Verificar si la orientación es válida
            if orientacion not in ("h", "v"):
                print("Orientación inválida. Usa 'h' o 'v'.")
                continue
                
            #? Verificar si las coordenadas están en el del tablero
            if not (0 <= fila < N and 0 <= columna < N):
                print("Coordenadas fuera del tablero.")
                continue
            
            if orientacion == "h":
                #? Verificar si entra el barco horizontalmente
                if columna + largo > N:
                    print(f"El barco no entra horizontalmente desde la columna {columna}.")
                    continue
                    
                #? Verificar si hay espacio libre
                if any(tablero[fila][columna + i] != "~" for i in range(largo)):
                    print("Hay otro barco en esa posición")
                    continue
                    
                #* Colocar el barco horizontalmente
                for i in range(largo):
                    tablero[fila][columna + i] = "O"
                break
                
            else:  #? orientacion == "v"
                #? Verificar si entra verticalmente
                if fila + largo > N:
                    print(f"El barco no entra verticalmente desde la fila {fila}.")
                    continue
                    
                #? Verificar si hay espacio libre
                if any(tablero[fila + i][columna] != "~" for i in range(largo)):
                    print("Hay otro barco en esa posición")
                    continue
                    
                #* Colocar el barco verticalmente
                for i in range(largo):
                    tablero[fila + i][columna] = "O"
                break
                
        except ValueError:
            #! Si la entrada no es un número entero, se tira un error
            print("Error, Ingresa un número entero")


def realizar_disparo(tablero: list[list[str]], numero_jugador: int, modo_solitario: bool = False) -> tuple[bool, bool]:
    #* Realiza un disparo
    while True:
        try:
            #? Si estas en modo dos jugadores
            if not modo_solitario:
                #? Imprime el jugador que le toca
                print(f"Jugador {numero_jugador}, es tu turno de disparar.")
            
            #? Se le pide al jugador que ingrese la fila y columna
            fila: int = int(input("Fila (0-9): "))
            columna: int = int(input("Columna (0-9): "))
            
            #? Verificar si las coordenadas están dentro del tablero
            if not (0 <= fila < N and 0 <= columna < N):
                print("Las coordenadas no son validas")
                continue
                
            #? Verificar si ya se disparó en esa posición
            if tablero[fila][columna] == "X" or tablero[fila][columna] == "*":
                print("Ya disparaste en esa posición")
                continue
                
            #* Realizar el disparo
            if tablero[fila][columna] == "O":
                print("Le pegaste a un barco")
                tablero[fila][columna] = "X"  #* Marcar como barco impactado
                
                #? Verificar si el barco esta hundido
                barco_hundido: bool = verificar_barco_hundido(tablero, fila, columna)
                if barco_hundido:
                    print("Hundiste un Barco")
                    
                #* Devuelve que acerto y si hundio un barco
                return True, barco_hundido  
                
            else:  
                print("No le diste a ningún barco")
                #* Se marca como disparo fallido
                tablero[fila][columna] = "*"  
                return False, False  
                
        except ValueError:
            #! Si la entrada no es un número entero, se tira un error
            print("Error, Ingresa un número entero")


def verificar_barco_hundido(tablero: list[list[str]], fila_impacto: int, columna_impacto: int) -> bool:
    #* Recorrer todas las direcciones para verificar si el barco está hundido
    for direccion in [DERECHA, ABAJO, IZQUIERDA, ARRIBA]:
        desplazamiento_fila, desplazamiento_columna = direccion
        fila, columna = fila_impacto + desplazamiento_fila, columna_impacto + desplazamiento_columna
        
        #? Buscar en esa dirección mientras este dentro del tablero y hayan partes del barco
        while 0 <= fila < N and 0 <= columna < N and tablero[fila][columna] in ["X", "O"]:
            if tablero[fila][columna] == "O":
                #! No todo el barco se hundio
                return False  
            fila += desplazamiento_fila
            columna += desplazamiento_columna

    #* Todo el barco se hundio
    return True 


def contar_barcos_restantes(tablero: list[list[str]]) -> int:
    #* Cuenta los barcos sin hundir

    #? Guarda las celdas ya visitadas
    celdas_contadas: list[list[bool]] = [[False for _ in range(N)] for _ in range(N)]
    #? Guarda los barcos contados
    contador: int = 0
    
    for fila in range(N):
        for columna in range(N):
            #? Si encuentro un barco sin contar lo sumo
            if tablero[fila][columna] == "O" and not celdas_contadas[fila][columna]:
                contador += 1
                
                #* Marco todo el barco entero como contado
                celdas_pendientes: list[tuple[int, int]] = [(fila, columna)]
                #? Mientras queden celdas sin contar
                while celdas_pendientes:
                    #* Tomo la celda pendiente (el ultimo elemento de la lista y lo borro de esta ) 
                    fila, columna = celdas_pendientes.pop() 
                    if 0 <= fila < N and 0 <= columna < N and tablero[fila][columna] == "O" and not celdas_contadas[fila][columna]:
                        #? Si la celda esta en el tablero, forma parte del barco y no fue contada, la cuento
                        celdas_contadas[fila][columna] = True
                        for desplazamiento_fila, desplazamiento_columna in [DERECHA, ABAJO, IZQUIERDA, ARRIBA]:
                            #? Busco las celdas contiguas al barco y las agrego a la lista de pendientes
                            celdas_pendientes.append((fila + desplazamiento_fila, columna + desplazamiento_columna))
                            
    return contador


def un_jugador() -> None:
    #* Crear tablero y colocar barcos aleatoriamente
    tablero: list[list[str]] = crear_tablero()
    for largo in LARGO_BARCOS:
        #? Para cada barco, colocar aleatoriamente
        colocar_barco_aleatorio(tablero, largo)
        
    #* Declaracion de variables
    disparos_acertados: int = 0
    disparos_realizados: int = 0
    barcos_hundidos: int = 0
    
    # * Prints iniciales
    print("UN JUGADOR")
    print(f"Tienes {CANTIDAD_DISPAROS} disparos para hundir {CANTIDAD_BARCOS} barcos.")
    print(f"Barcos restantes: {CANTIDAD_BARCOS - barcos_hundidos}")
    
    #* Bucle principal de juego
    while disparos_realizados < CANTIDAD_DISPAROS:
        # ? Mientras no se hayan acabado los disparos se imprime el tablero
        print("\nTablero actual:")
        mostrar_tablero(tablero, ocultar_barcos=True)
        
        #* Realizar disparo 
        # ? Se suma o resta dependiendo si el disparo fue acertado o no
        disparo_acertado, barco_hundido = realizar_disparo(tablero, 1, modo_solitario=True)
        disparos_realizados += 1
        if disparo_acertado:
            disparos_acertados += 1
            if barco_hundido:
                barcos_hundidos += 1
                print(f"Hundiste un barco! Quedan: {CANTIDAD_BARCOS - barcos_hundidos} barcos")
            
        #? Verificar victoria
        if barcos_hundidos == CANTIDAD_BARCOS:
            print("\nGanaste!")
            break
            
        print(f"Te quedan: {CANTIDAD_DISPAROS - disparos_realizados} disparos")
        print(f"Quedan: {CANTIDAD_BARCOS - barcos_hundidos} barcos")
        
    #* Fin del juego
    print("\nTablero final:")
    #* Imprimir el tablero final
    mostrar_tablero(tablero)
    
    if barcos_hundidos < CANTIDAD_BARCOS:
        #? Si no se hundieron todos los barcos se imprime que perdio
        print(f"\nPerdiste. Quedan {CANTIDAD_BARCOS - barcos_hundidos} barcos sin hundir.")
        #? Sino se imprime que gano
    else:
        print(f"\nGanaste! En {disparos_realizados} disparos.")


def dos_jugadores() -> None:
    #* Crear tableros para ambos jugadores
    tablero_jugador1: list[list[str]] = crear_tablero()
    tablero_jugador2: list[list[str]] = crear_tablero()
    
    print("DOS JUGADORES")
    
    #* Cada jugador coloca sus barcos
    print("\nJugador 1, pone tus barcos:")
    for largo in LARGO_BARCOS:
        #? Para cada barco, colocar manualmente
        colocar_barco_manual(tablero_jugador1, largo, 1)
    
    #* Limpiar la pantalla 
    # * Lo hago imprimiendo 100 lineas en blanco y tmb
    #* Limpiando ya que limpiar no funciona en terminales integradas en Ides
    print("\n" * 100) 
    os.system('cls' if os.name == 'nt' else 'clear')


    for largo in LARGO_BARCOS:
        colocar_barco_manual(tablero_jugador2, largo, 2)
        
    #* Limpiar la pantalla
    print("\n" * 100) 
    os.system('cls' if os.name == 'nt' else 'clear')    
    
    #* Los jugadores disparan
    jugador_actual: int = 1  #* Empieza el jugador 1
    barcos_hundidos_jugador1: int = 0 
    barcos_hundidos_jugador2: int = 0
    
    while barcos_hundidos_jugador1 < CANTIDAD_BARCOS and barcos_hundidos_jugador2 < CANTIDAD_BARCOS:
        #? Mientras ningun jugador haya ganado se imprime el tablero del oponente
        tablero_objetivo: list[list[str]] = tablero_jugador2 if jugador_actual == 1 else tablero_jugador1
        
        #* Se imprimen los turnos y los barcos restantes y el tablero del oponente
        print(f"\n=Turno del Jugador: {jugador_actual}")
        print(f"Barcos hundidos del oponente: {barcos_hundidos_jugador2 if jugador_actual == 1 else barcos_hundidos_jugador1}")
        print(f"Barcos restantes del oponente: {CANTIDAD_BARCOS - (barcos_hundidos_jugador2 if jugador_actual == 1 else barcos_hundidos_jugador1)}")
        print("Tablero del oponente:")
        mostrar_tablero(tablero_objetivo, ocultar_barcos=True)
        
        #* Disparar
        disparo_acertado, barco_hundido = realizar_disparo(tablero_objetivo, jugador_actual)
        
        #? Actualizar contador de barcos hundidos
        if barco_hundido:
            if jugador_actual == 1:
                barcos_hundidos_jugador2 += 1
                print(f"¡Barco hundido! Quedan: {CANTIDAD_BARCOS - barcos_hundidos_jugador2} barcos del oponente")
            else:
                barcos_hundidos_jugador1 += 1
                print(f"¡Barco hundido! Quedan: {CANTIDAD_BARCOS - barcos_hundidos_jugador1} barcos del oponente")
            
        #? Cambiar turno si el jugador falló
        if not disparo_acertado:
            jugador_actual = 2 if jugador_actual == 1 else 1
            
    #* Fin del juego
    jugador_ganador: int = 1 if barcos_hundidos_jugador2 == CANTIDAD_BARCOS else 2
    print(f"\nGano el jugador: {jugador_ganador}!")
    
    #* Imprimir tableros finales
    print("\nTablero final del Jugador 1:")
    mostrar_tablero(tablero_jugador1)
    print("\nTablero final del Jugador 2:")
    mostrar_tablero(tablero_jugador2)


def main() -> None:    
    # * Bucle principal del juego
    while True:
        print("\nElegi el modo de juego:")
        print("1. Un jugador")
        print("2. Dos jugadores")
        
        modo_juego: str = input("\nOpción: ").strip()
        
        #? Empezar el modo de juego elegido
        if modo_juego == "1":
            un_jugador()
        elif modo_juego == "2":
            dos_jugadores()
        else:
            print("\nOpción invalida. Intenta de nuevo.")



main()

