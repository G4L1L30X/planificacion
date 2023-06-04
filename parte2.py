from queue import PriorityQueue
from threading import Thread, Lock
import random
import time

class Cliente:
    def __init__(self, tipo, tiempo_llegada):
        self.tipo = tipo
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_atencion = 0

    def __str__(self):
        return f"Cliente {self.tipo} (Tiempo de llegada: {self.tiempo_llegada}), (Tiempo de atención: {self.tiempo_atencion:} minutos)"

    def __lt__(self, other):
        if self.tipo == other.tipo:
            return self.tiempo_llegada < other.tiempo_llegada
        else:
            return self.tipo < other.tipo

prioridad_tarjeta = 2
prioridad_sin_tarjeta = 2
prioridad_preferencial = 1

num_clientes = 10  # Número de clientes a simular
N = int(input("Ingrese el número de ventanillas: "))  # Número de ventanillas/procesadores

cola_clientes = PriorityQueue()
atencion_terminada = False
lock = Lock()

def simular_llegada_clientes():
    for tiempo in range(1, num_clientes + 1):
        tipo_cliente = ""

        if random.random() < 0.5:
            tipo_cliente = "Cliente con tarjeta"
            prioridad = prioridad_tarjeta
        else:
            tipo_cliente = "Cliente sin tarjeta"
            prioridad = prioridad_sin_tarjeta

        if random.random() < 0.1:
            tipo_cliente += " (Preferencial)"
            prioridad = prioridad_preferencial

        cliente = Cliente(tipo_cliente, tiempo)
        cola_clientes.put((prioridad, cliente))

class Ventanilla(Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id + 1
        self.tiempo_total_atencion = 0
        self.clientes_atendidos = 0

    def run(self):
        while True:
            if atencion_terminada:
                break

            lock.acquire()
            if not cola_clientes.empty():
                cliente = cola_clientes.get()[1]
                lock.release()

                tiempo_ráfaga = random.randint(1, 20)
                cliente.tiempo_atencion = tiempo_ráfaga  # Actualizar el tiempo de atención del cliente
                print(f"Ventanilla {self.id} atendiendo a: {cliente}")

                time.sleep(tiempo_ráfaga)

                lock.acquire()
                self.tiempo_total_atencion += tiempo_ráfaga
                self.clientes_atendidos += 1
                lock.release()

                cola_clientes.task_done()
            else:
                lock.release()
                time.sleep(0.1)  # Esperar antes de verificar la cola de clientes nuevamente

ventanillas = []
for i in range(N):
    ventanilla = Ventanilla(i)
    ventanilla.start()
    ventanillas.append(ventanilla)

simular_llegada_clientes()

cola_clientes.join()
atencion_terminada = True

for ventanilla in ventanillas:
    ventanilla.join()

total_clientes_atendidos = sum(ventanilla.clientes_atendidos for ventanilla in ventanillas)
tiempo_total_atencion = sum(ventanilla.tiempo_total_atencion for ventanilla in ventanillas)

print("\n--- Resultados ---")
print(f"Clientes atendidos: {total_clientes_atendidos}")
print(f"Tiempo total de atención: {tiempo_total_atencion:} minutos")
print(f"Tiempo promedio de atención: {tiempo_total_atencion / total_clientes_atendidos:.2f} minutos")