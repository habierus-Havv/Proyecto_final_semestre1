import tkinter as tk
import random

def inicializar_juego():
    global n, turnos_totales, matriz, matriz_usada, jugador1, jugador2
    global turno_actual, ronda_actual, puntos1, puntos2, seleccion_bloqueada
    
    jugador1 = entrada_j1.get()
    jugador2 = entrada_j2.get()
    n = int(entrada_n.get())
    turnos_totales = int(entrada_turnos.get())
    
    if not jugador1: jugador1 = "jugador 1"
    if not jugador2: jugador2 = "jugador 2"
    if n < 3: n = 3
    
    matriz = [[random.randint(0, 11) for _ in range(n)] for _ in range(n)]
    matriz_usada = [[False for _ in range(n)] for _ in range(n)]
    
    turno_actual = 1
    ronda_actual = 1
    puntos1 = 0
    puntos2 = 0
    seleccion_bloqueada = False
    
    panel_config.pack_forget()
    panel_juego.pack()
    crear_tablero()
    actualizar_interfaz()

def crear_tablero():
    for widget in panel_tablero.winfo_children():
        widget.destroy()
    
    global botones
    botones = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            btn = tk.Button(panel_tablero, text="", width=6, height=3, font=("Arial", 12, "bold"),
                            command=lambda r=i, c=j: seleccionar_celda(r, c))
            btn.grid(row=i, column=j, padx=2, pady=2)
            botones[i][j] = btn

def actualizar_interfaz():
    nombre_act = jugador1 if turno_actual == 1 else jugador2
    lbl_estado.config(text=f"ronda: {ronda_actual}/{turnos_totales} - turno de: {nombre_act}")
    lbl_puntos.config(text=f"puntos - {jugador1}: {puntos1} | {jugador2}: {puntos2}")
    
    for i in range(n):
        for j in range(n):
            if matriz_usada[i][j]:
                botones[i][j].config(text="x", state="disabled", bg="lightgrey")
            else:
                botones[i][j].config(text="", state="normal", bg="white")

def contar_tiempo():
    global tiempo_restante, temporizador
    if tiempo_restante > 0:
        tiempo_restante -= 1
        lbl_tiempo.config(text=f"tiempo: {tiempo_restante}s")
        temporizador = raiz.after(1000, contar_tiempo)
    else:
        lbl_tiempo.config(text="tiempo agotado")
        finalizar_turno(0)

def seleccionar_celda(r, c):
    global tiempo_restante, temporizador, fila_sel, col_sel, seleccion_bloqueada, respuesta_correcta
    if seleccion_bloqueada or matriz_usada[r][c]:
        return
        
    seleccion_bloqueada = True
    fila_sel = r
    col_sel = c
    
    suma_vecinos = 0
    for i in range(r - 1, r + 2):
        for j in range(c - 1, c + 2):
            if 0 <= i < n and 0 <= j < n:
                if i == r and j == c:
                    botones[i][j].config(text=str(matriz[i][j]), bg="red")
                else:
                    botones[i][j].config(text=str(matriz[i][j]), bg="lightblue")
                    suma_vecinos += matriz[i][j]
                    
    respuesta_correcta = suma_vecinos * matriz[r][c]
    
    opciones = [respuesta_correcta]
    while len(opciones) < 4:
        falso = respuesta_correcta + random.randint(-20, 20)
        if falso != respuesta_correcta and falso >= 0 and falso not in opciones:
            opciones.append(falso)
    random.shuffle(opciones)
    
    for i in range(4):
        botones_opciones[i].config(text=str(opciones[i]), state="normal", 
                                   command=lambda v=opciones[i]: verificar_respuesta(v))
        
    tiempo_restante = 25
    lbl_tiempo.config(text=f"tiempo: {tiempo_restante}s")
    contar_tiempo()

def verificar_respuesta(valor_elegido):
    global puntos1, puntos2, temporizador
    raiz.after_cancel(temporizador)
    
    puntos_ganados = 3 if valor_elegido == respuesta_correcta else 0
    if turno_actual == 1:
        puntos1 += puntos_ganados
    else:
        puntos2 += puntos_ganados
        
    finalizar_turno(puntos_ganados)

def finalizar_turno(puntos):
    global turno_actual, ronda_actual, seleccion_bloqueada
    
    matriz_usada[fila_sel][col_sel] = True
    
    for btn in botones_opciones:
        btn.config(text="", state="disabled")
        
    if turno_actual == 1:
        turno_actual = 2
    else:
        turno_actual = 1
        ronda_actual += 1
        
    if ronda_actual > turnos_totales:
        mostrar_ganador()
    else:
        seleccion_bloqueada = False
        actualizar_interfaz()

def mostrar_ganador():
    panel_juego.pack_forget()
    panel_final.pack()
    
    if puntos1 > puntos2:
        txt = f"el ganador es {jugador1}"
    elif puntos2 > puntos1:
        txt = f"el ganador es {jugador2}"
    else:
        txt = "empate"
        
    lbl_ganador.config(text=f"{txt}\n\nresultados finales:\n{jugador1}: {puntos1} puntos\n{jugador2}: {puntos2} puntos")

raiz = tk.Tk()
raiz.title("matriz aritmetica")
raiz.geometry("600x650")

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

botones_opciones = []
for _ in range(4):
    b = tk.Button(panel_opciones, text="", width=10, height=2, font=("Arial", 10, "bold"), state="disabled")
    b.pack(side="left", padx=5)
    botones_opciones.append(b)

panel_final = tk.Frame(raiz)
lbl_ganador = tk.Label(panel_final, font=("Arial", 16, "bold"), justify="center")
lbl_ganador.pack(pady=50)

raiz.mainloop()