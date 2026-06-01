# 🏦 Simulador de Colas Bancarias - Banco de Colombia

**Actividad didáctica 2-M3: Solución de un problema bancario** **Autor:** [Tu Nombre y Apellido]  
**Institución:** [Nombre de tu Universidad/Institución]  

---

##  Descripción del Proyecto
Este repositorio contiene un modelo de simulación de eventos discretos desarrollado en Python. El objetivo principal es evaluar el desempeño operativo de una sucursal del Banco de Colombia mediante la teoría de colas (Modelo M/M/1), analizando los tiempos de espera y el volumen de usuarios atendidos por tres (3) cajeros humanos durante jornadas laborales de 8 horas.

El sistema simula 10 réplicas (días) consecutivos y genera estadísticas precisas para determinar la viabilidad de implementar cajas de atención exclusivas o instalar un nuevo cajero electrónico (ATM).

##  Características Técnicas
* **Lenguaje:** Python 3.x
* **Librerías:** `random` (lógica estocástica), `tkinter` (interfaz gráfica GUI). No requiere librerías externas de terceros.
* **Modelo Matemático:** M/M/1 con tiempos de llegada basados en una distribución exponencial y asignación dinámica al cajero más pronto a desocuparse.
* **Interfaz Visual:** Tablero de resultados interactivo que despliega el historial por réplica y las estadísticas finales promediadas en formato de tablas ASCII.

##  Metodología y Parámetros del Modelo
La simulación contempla los siguientes flujos de usuarios reales:
* **Llegadas:** Los usuarios llegan de forma continua a la sucursal.
* **Tipos de Transacciones:**
  * **Retiros (70%):** Subdivididos en Rápidos (23%), Normales (40%), Lentos (17%) y Muy Lentos (20%), con tiempos de servicio exponenciales de 1 a 4 minutos.
  * **Consignaciones/Pagos (30%):** Subdivididos en Rápidos (10%), Normales (20%), Lentos (30%) y Muy Lentos (40%), con tiempos de servicio exponenciales de 3 a 7 minutos.

##  Instrucciones de Ejecución
Para correr este simulador en tu máquina local, sigue estos pasos:

1. Clona este repositorio en tu computadora:
   ```bash
   git clone [https://github.com/](https://github.com/)[TuUsuario]/[NombreDelRepositorio].git
