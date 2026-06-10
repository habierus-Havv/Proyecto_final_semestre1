import tkinter as tk
import random

n = 5
turnos_totales = 3
matriz = []
matriz_usada = []
jugador1 = ""
jugador2 = ""
turno_actual = 1
ronda_actual = 1
puntos1 = 0
puntos2 = 0
seleccion_bloqueada = False
fila_sel = 0
col_sel = 0
respuesta_correcta = 0
tiempo_restante = 25
temporizador = None
botones = []
nombre_act = ""

# esta funcion empieza el juego con los datos que puso el usuario
def inicializar_juego():
    global n, turnos_totales, matriz, matriz_usada, jugador1, jugador2
    global turno_actual, ronda_actual, puntos1, puntos2, seleccion_bloqueada

    # agarro lo que escribio el usuario
    jugador1 = entrada_j1.get()
    jugador2 = entrada_j2.get()
    n = int(entrada_n.get())
    turnos_totales = int(entrada_turnos.get())

    # si no pusieron nombre le pongo uno yo
    if jugador1 == "":
        jugador1 = "Jugador 1"
    if jugador2 == "":
        jugador2 = "Jugador 2"

    # la matriz minimo tiene que ser 3x3 sino no funciona bien
    if n < 3:
        n = 3

    # creo la matriz con numeros al azar entre 0 y 11
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            numero = random.randint(0, 11)
            fila.append(numero)
        matriz.append(fila)

    # esta matriz me dice cuales celdas ya se usaron
    matriz_usada = []
    for i in range(n):
        fila_falsa = []
        for j in range(n):
            fila_falsa.append(False)
        matriz_usada.append(fila_falsa)

    # reinicio todo para empezar bien
    turno_actual = 1
    ronda_actual = 1
    puntos1 = 0
    puntos2 = 0
    seleccion_bloqueada = False

    # escondo la pantalla de configuracion y muestro el juego
    panel_config.pack_forget()
    panel_juego.pack()
    crear_tablero()
    actualizar_interfaz()


# aqui creo todos los botones del tablero
def crear_tablero():
    # borro lo que habia antes por si acaso
    for widget in panel_tablero.winfo_children():
        widget.destroy()

    global botones
    botones = []
    for i in range(n):
        fila_botones = []
        for j in range(n):
            # cada boton llama a seleccionar_celda con su posicion
            btn = tk.Button(panel_tablero, text="", width=6, height=3,
                            font=("Arial", 12, "bold"),
                            command=lambda r=i, c=j: seleccionar_celda(r, c))
            btn.grid(row=i, column=j, padx=2, pady=2)
            fila_botones.append(btn)
        botones.append(fila_botones)


# actualiza los textos y colores de la pantalla
def actualizar_interfaz():
    global nombre_act

    # veo de quien es el turno
    if turno_actual == 1:
        nombre_act = jugador1
    else:
        nombre_act = jugador2

    lbl_estado.config(text="ronda: " + str(ronda_actual) + "/" + str(turnos_totales) + "  -  turno de: " + nombre_act)
    lbl_puntos.config(text="puntos  -  " + jugador1 + ": " + str(puntos1) + "  |  " + jugador2 + ": " + str(puntos2))

    # pinto cada boton segun si ya fue usado o no
    for i in range(n):
        for j in range(n):
            if matriz_usada[i][j] == True:
                botones[i][j].config(text="x", state="disabled", bg="lightgrey")
            else:
                botones[i][j].config(text="", state="normal", bg="white")


# el temporizador que cuenta hacia atras
def contar_tiempo():
    global tiempo_restante, temporizador
    if tiempo_restante > 0:
        tiempo_restante = tiempo_restante - 1
        lbl_tiempo.config(text="tiempo: " + str(tiempo_restante) + "s")
        # se llama a si misma cada segundo, lo vi en youtube
        temporizador = raiz.after(1000, contar_tiempo)
    else:
        lbl_tiempo.config(text="tiempo agotado")
        finalizar_turno(0)  # si se acaba el tiempo no gana puntos


# cuando el jugador hace click en una celda
def seleccionar_celda(r, c):
    global tiempo_restante, temporizador, fila_sel, col_sel
    global seleccion_bloqueada, respuesta_correcta

    # si ya esta bloqueado o la celda ya se uso no hago nada
    if seleccion_bloqueada == True:
        return
    if matriz_usada[r][c] == True:
        return

    seleccion_bloqueada = True
    fila_sel = r
    col_sel = c

    # sumo todos los vecinos de la celda seleccionada
    suma_vecinos = 0
    for i in range(r - 1, r + 2):
        for j in range(c - 1, c + 2):
            if i >= 0 and i < n and j >= 0 and j < n:
                if i == r and j == c:
                    # la celda central la pinto de rojo
                    botones[i][j].config(text=str(matriz[i][j]), bg="red")
                else:
                    # los vecinos de celeste
                    botones[i][j].config(text=str(matriz[i][j]), bg="lightblue")
                    suma_vecinos = suma_vecinos + matriz[i][j]

    # la respuesta es la suma de vecinos multiplicada por el valor central
    respuesta_correcta = suma_vecinos * matriz[r][c]

    # genero 4 opciones, una correcta y tres falsas
    opciones = []
    opciones.append(respuesta_correcta)

    intentos = 0  # para no quedarme en bucle infinito
    while len(opciones) < 4:
        numero_falso = respuesta_correcta + random.randint(-20, 20)
        if numero_falso != respuesta_correcta and numero_falso >= 0:
            # verifico que no este repetido
            repetido = False
            for op in opciones:
                if op == numero_falso:
                    repetido = True
            if repetido == False:
                opciones.append(numero_falso)
        intentos = intentos + 1
        if intentos > 100:
            break  # por si algo sale mal

    random.shuffle(opciones)

    # muestro las opciones en los botones de abajo
    for i in range(4):
        botones_opciones[i].config(
            text=str(opciones[i]),
            state="normal",
            command=lambda v=opciones[i]: verificar_respuesta(v)
        )

    # arranco el temporizador
    tiempo_restante = 25
    lbl_tiempo.config(text="tiempo: " + str(tiempo_restante) + "s")
    contar_tiempo()


# revisa si la respuesta que eligio el jugador es correcta
def verificar_respuesta(valor_elegido):
    global puntos1, puntos2, temporizador

    # cancelo el temporizador porque ya respondio
    raiz.after_cancel(temporizador)

    puntos_ganados = 0
    if valor_elegido == respuesta_correcta:
        puntos_ganados = 3  # solo si acerto gana puntos

    if turno_actual == 1:
        puntos1 = puntos1 + puntos_ganados
    else:
        puntos2 = puntos2 + puntos_ganados

    finalizar_turno(puntos_ganados)


# termina el turno y pasa al siguiente jugador
def finalizar_turno(puntos):
    global turno_actual, ronda_actual, seleccion_bloqueada

    # marco la celda como usada
    matriz_usada[fila_sel][col_sel] = True

    # desactivo los botones de opciones
    for btn in botones_opciones:
        btn.config(text="", state="disabled")

    # cambio de turno
    if turno_actual == 1:
        turno_actual = 2
    else:
        turno_actual = 1
        ronda_actual = ronda_actual + 1  # nueva ronda cuando los dos jugaron

    # si se acabaron las rondas muestro quien gano
    if ronda_actual > turnos_totales:
        mostrar_ganador()
    else:
        seleccion_bloqueada = False
        actualizar_interfaz()


# pantalla final con el resultado
def mostrar_ganador():
    panel_juego.pack_forget()
    panel_final.pack()

    # comparo puntos para saber quien gano
    if puntos1 > puntos2:
        txt = "el ganador es " + jugador1
    elif puntos2 > puntos1:
        txt = "el ganador es " + jugador2
    else:
        txt = "empate!"

    mensaje = txt + "\n\nresultados finales:\n"
    mensaje = mensaje + jugador1 + ": " + str(puntos1) + " puntos\n"
    mensaje = mensaje + jugador2 + ": " + str(puntos2) + " puntos"

    lbl_ganador.config(text=mensaje)


# ---- aqui empieza la ventana y todo lo visual ----

raiz = tk.Tk()
raiz.title("matriz aritmetica")
raiz.geometry("600x650")

# pantalla de configuracion inicial
panel_config = tk.Frame(raiz)
panel_config.pack(pady=20)
tk.Label(panel_config, text="nombre jugador 1:").pack()
entrada_j1 = tk.Entry(panel_config)
entrada_j1.pack()
tk.Label(panel_config, text="nombre jugador 2:").pack()
entrada_j2 = tk.Entry(panel_config)
entrada_j2.pack()
tk.Label(panel_config, text="tamano de la matriz (n >= 3):").pack()
entrada_n = tk.Entry(panel_config)
entrada_n.insert(0, "5")
entrada_n.pack()
tk.Label(panel_config, text="cantidad de turnos por jugador:").pack()
entrada_turnos = tk.Entry(panel_config)
entrada_turnos.insert(0, "3")
entrada_turnos.pack()
btn_iniciar = tk.Button(panel_config, text="iniciar juego", command=inicializar_juego)
btn_iniciar.pack(pady=10)

# pantalla del juego
panel_juego = tk.Frame(raiz)
lbl_estado = tk.Label(panel_juego, font=("Arial", 12))
lbl_estado.pack(pady=5)
lbl_puntos = tk.Label(panel_juego, font=("Arial", 10))
lbl_puntos.pack(pady=5)
lbl_tiempo = tk.Label(panel_juego, text="tiempo: 25s", font=("Arial", 12, "bold"), fg="red")
lbl_tiempo.pack(pady=5)
panel_tablero = tk.Frame(panel_juego)
panel_tablero.pack(pady=10)
panel_opciones = tk.Frame(panel_juego)
panel_opciones.pack(pady=10)

# los 4 botones de respuesta
botones_opciones = []
for _ in range(4):
    b = tk.Button(panel_opciones, text="", width=10, height=2,
                  font=("Arial", 10, "bold"), state="disabled")
    b.pack(side="left", padx=5)
    botones_opciones.append(b)

# pantalla final
panel_final = tk.Frame(raiz)
lbl_ganador = tk.Label(panel_final, font=("Arial", 16, "bold"), justify="center")
lbl_ganador.pack(pady=50)

raiz.mainloop()