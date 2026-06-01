import random
import tkinter as tk
from tkinter import scrolledtext

# --- LÓGICA DE LA SIMULACIÓN COMPLETA (3 CAJEROS, 8 HORAS) ---
def run_simulation(sim_time=480.0): 
    prob_retiro = 0.70
    prob_consignacion = 0.30
    
    prob_ret_types = [0.23, 0.40, 0.17, 0.20]
    serv_ret_times = [1.0, 2.0, 3.0, 4.0]
    
    prob_con_types = [0.10, 0.20, 0.30, 0.40]
    serv_con_times = [3.0, 3.0, 5.0, 7.0]
    
    cajeros_libres_en = [0.0, 0.0, 0.0] 
    tiempos_servicio_por_cajero = {0: [], 1: [], 2: []}
    usuarios_atendidos_por_cajero = {0: 0, 1: 0, 2: 0}
    
    conteo_usuarios = {
        'Retiro Rápido': 0, 'Retiro Normal': 0, 'Retiro Lento': 0, 'Retiro Muy Lento': 0,
        'Consig Rápido': 0, 'Consig Normal': 0, 'Consig Lento': 0, 'Consig Muy Lento': 0
    }
    
    time = 0.0
    mean_arrival_time = 1.5 
    
    while True:
        time += random.expovariate(1.0 / mean_arrival_time)
        if time > sim_time:
            break
            
        es_retiro = random.random() < prob_retiro
        
        if es_retiro:
            tipo_idx = random.choices([0, 1, 2, 3], weights=prob_ret_types)[0]
            t_servicio = random.expovariate(1.0 / serv_ret_times[tipo_idx])
            nombres = ['Retiro Rápido', 'Retiro Normal', 'Retiro Lento', 'Retiro Muy Lento']
            conteo_usuarios[nombres[tipo_idx]] += 1
        else:
            tipo_idx = random.choices([0, 1, 2, 3], weights=prob_con_types)[0]
            t_servicio = random.expovariate(1.0 / serv_con_times[tipo_idx])
            nombres = ['Consig Rápido', 'Consig Normal', 'Consig Lento', 'Consig Muy Lento']
            conteo_usuarios[nombres[tipo_idx]] += 1
            
        cajero_elegido = cajeros_libres_en.index(min(cajeros_libres_en))
        inicio_servicio = max(time, cajeros_libres_en[cajero_elegido])
        fin_servicio = inicio_servicio + t_servicio
        
        cajeros_libres_en[cajero_elegido] = fin_servicio
        tiempos_servicio_por_cajero[cajero_elegido].append(t_servicio)
        usuarios_atendidos_por_cajero[cajero_elegido] += 1
        
    promedios_atencion = []
    for i in range(3):
        if len(tiempos_servicio_por_cajero[i]) > 0:
            promedios_atencion.append(sum(tiempos_servicio_por_cajero[i]) / len(tiempos_servicio_por_cajero[i]))
        else:
            promedios_atencion.append(0)
            
    return promedios_atencion, conteo_usuarios, usuarios_atendidos_por_cajero

# --- FUNCIÓN DEL BOTÓN ---
def iniciar_simulacion():
    btn_simular.config(state=tk.DISABLED, text="⏳ Calculando 10 Réplicas...")
    ventana.update()
    txt_resultados.delete(1.0, tk.END)
    
    num_simulations = 10
    todos_promedios_cajeros = {0: [], 1: [], 2: []}
    totales_usuarios_cajeros = {0: 0, 1: 0, 2: 0}
    totales_usuarios_tipos = {k: 0 for k in ['Retiro Rápido', 'Retiro Normal', 'Retiro Lento', 'Retiro Muy Lento',
                                             'Consig Rápido', 'Consig Normal', 'Consig Lento', 'Consig Muy Lento']}
    
    txt_resultados.insert(tk.END, "====== HISTORIAL DETALLADO POR RÉPLICA ======\n")
    txt_resultados.insert(tk.END, "┌──────┬─────────────────────────────┬─────────────────────────────┬──────────────────────────────┐\n")
    txt_resultados.insert(tk.END, "│ RÉP. │ RETIROS (Ráp/Nor/Len/MLen)  │ CONSIG. (Ráp/Nor/Len/MLen)  │ MENOR CANTIDAD EN LA RÉPLICA │\n")
    txt_resultados.insert(tk.END, "├──────┼─────────────────────────────┼─────────────────────────────┼──────────────────────────────┤\n")
    
    for rep in range(1, num_simulations + 1):
        prom_atencion, conteo, usuarios_cajero = run_simulation()
        
        menor_tipo = min(conteo, key=conteo.get)
        menor_cantidad = conteo[menor_tipo]
        
        retiros_str = f"{conteo['Retiro Rápido']:>3}/{conteo['Retiro Normal']:>3}/{conteo['Retiro Lento']:>3}/{conteo['Retiro Muy Lento']:>3}"
        consig_str = f"{conteo['Consig Rápido']:>3}/{conteo['Consig Normal']:>3}/{conteo['Consig Lento']:>3}/{conteo['Consig Muy Lento']:>3}"
        menor_str = f"{menor_tipo} ({menor_cantidad})"
        
        txt_resultados.insert(tk.END, f"│ {rep:^4} │ {retiros_str:^27} │ {consig_str:^27} │ {menor_str:^28} │\n")
        
        for i in range(3):
            todos_promedios_cajeros[i].append(prom_atencion[i])
            totales_usuarios_cajeros[i] += usuarios_cajero[i]
        for k in conteo:
            totales_usuarios_tipos[k] += conteo[k]
            
    txt_resultados.insert(tk.END, "└──────┴─────────────────────────────┴─────────────────────────────┴──────────────────────────────┘\n\n")
    
    final_tiempos_cajeros = [sum(todos_promedios_cajeros[i])/num_simulations for i in range(3)]
    final_usuarios_cajeros = [totales_usuarios_cajeros[i]/num_simulations for i in range(3)]
    
    cajero_menor_tiempo = final_tiempos_cajeros.index(min(final_tiempos_cajeros)) + 1
    cajero_mayor_tiempo = final_tiempos_cajeros.index(max(final_tiempos_cajeros)) + 1
    
    txt_resultados.insert(tk.END, "====== ESTADÍSTICAS FINALES PROMEDIADAS ======\n")
    txt_resultados.insert(tk.END, "\n1. DESEMPEÑO INDIVIDUAL POR CAJERO\n")
    txt_resultados.insert(tk.END, "┌──────────┬───────────────────────────┬─────────────────────────────┐\n")
    txt_resultados.insert(tk.END, "│ CAJERO   │ TIEMPO PROMEDIO (min/usr) │ VOLUMEN TRABAJO (usr/día)   │\n")
    txt_resultados.insert(tk.END, "├──────────┼───────────────────────────┼─────────────────────────────┤\n")
    for i in range(3):
        txt_resultados.insert(tk.END, f"│ Cajero {i+1} │ {final_tiempos_cajeros[i]:^25.2f} │ {final_usuarios_cajeros[i]:^27.1f} │\n")
    txt_resultados.insert(tk.END, "└──────────┴───────────────────────────┴─────────────────────────────┘\n")
    txt_resultados.insert(tk.END, f"▶ CAJERO MÁS RÁPIDO: Cajero {cajero_menor_tiempo} (Menor tiempo de atención)\n")
    txt_resultados.insert(tk.END, f"▶ CAJERO MÁS LENTO : Cajero {cajero_mayor_tiempo} (Mayor tiempo de atención)\n\n")
    
    txt_resultados.insert(tk.END, "\n2. PROMEDIO DE USUARIOS DE CADA TIPO EN LA SUCURSAL\n")
    txt_resultados.insert(tk.END, "┌────────────────────────┬────────────────────────┐\n")
    txt_resultados.insert(tk.END, "│ TIPO DE USUARIO        │ PROMEDIO POR DÍA       │\n")
    txt_resultados.insert(tk.END, "├────────────────────────┼────────────────────────┤\n")
    for k, v in totales_usuarios_tipos.items():
        promedio_por_replica = v / num_simulations
        txt_resultados.insert(tk.END, f"│ {k:<22} │ {promedio_por_replica:>16.1f} usrs │\n")
    txt_resultados.insert(tk.END, "└────────────────────────┴────────────────────────┘\n")
        
    btn_simular.config(state=tk.NORMAL, text="▶ REPETIR SIMULACIÓN")

# --- INTERFAZ GRÁFICA ---
ventana = tk.Tk()
ventana.title("Simulador Bancario - Actividad 2 M3")
# Ampliamos la ventana para que las tablas encajen perfectamente
ventana.geometry("900x750")
ventana.configure(bg="#F4F6F9")

lbl_titulo = tk.Label(ventana, text="🏦 Banco de Colombia - Tablero de Resultados", font=("Arial", 16, "bold"), bg="#F4F6F9")
lbl_titulo.pack(pady=10)

btn_simular = tk.Button(ventana, text="▶ GENERAR TABLAS ESTADÍSTICAS", font=("Arial", 11, "bold"), bg="#0056B3", fg="white", cursor="hand2", command=iniciar_simulacion, padx=15, pady=8)
btn_simular.pack(pady=5)

# Ajustamos el ancho para las tablas
txt_resultados = scrolledtext.ScrolledText(ventana, width=105, height=33, font=("Consolas", 10), bg="white", fg="black")
txt_resultados.pack(pady=10)

ventana.mainloop()