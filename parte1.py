from operator import attrgetter
from collections import deque

class Proceso:
    def __init__(self, numeroProceso, tiempoLlegada, tiempoRafaga):
        self.numeroProceso = numeroProceso
        self.tiempoLlegada = tiempoLlegada
        self.tiempoRafaga = tiempoRafaga
        self.tiempoRestante = tiempoRafaga

def simular_FCFS(procesos):
    colaListos = deque()
    tiempoActual = 0
    tiempoPromedio = 0

    for proceso in procesos:
        while tiempoActual < proceso.tiempoLlegada:
            print("Inactivo-", tiempoActual)
            tiempoActual += 1

        print("|P{}|-{}".format(proceso.numeroProceso, tiempoActual))

        tiempoActual += proceso.tiempoRafaga
        tiempoPromedio += tiempoActual - proceso.tiempoLlegada

    tiempoPromedio -= tiempoActual
    print("\n{}/{}".format(tiempoPromedio, len(procesos)))
    tiempoPromedio /= len(procesos)
    print("Tiempo promedio de ejecución:", tiempoPromedio)

def simular_SJF(procesos):
    procesosOrdenados = sorted(procesos, key=attrgetter('tiempoRafaga'))
    tiempoActual = 0
    tiempoPromedio = 0

    for proceso in procesosOrdenados:
        while tiempoActual < proceso.tiempoLlegada:
            print("Inactivo-", tiempoActual)
            tiempoActual += 1

        print("|P{}|-{}".format(proceso.numeroProceso, tiempoActual))

        tiempoActual += proceso.tiempoRafaga
        tiempoPromedio += tiempoActual - proceso.tiempoLlegada

    tiempoPromedio -= tiempoActual
    print("\n{}/{}".format(tiempoPromedio, len(procesosOrdenados)))
    tiempoPromedio /= len(procesos)
    print("Tiempo promedio de ejecución:", tiempoPromedio)

def simular_SRTF(procesos):
    tiempoActual = 0
    tiempoPromedio = 0
    procesosRestantes = len(procesos)
    procesosOrdenados = []

    while procesosRestantes > 0:
        for proceso in procesos:
            if proceso.tiempoLlegada <= tiempoActual and proceso not in procesosOrdenados:
                procesosOrdenados.append(proceso)

        if not procesosOrdenados:
            print("Inactivo-", tiempoActual)
            tiempoActual += 1
            continue

        procesoActual = min(procesosOrdenados, key=attrgetter('tiempoRestante'))

        print("|P{}|-{}".format(procesoActual.numeroProceso, tiempoActual))

        procesoActual.tiempoRestante -= 1
        tiempoActual += 1

        if procesoActual.tiempoRestante == 0:
            procesosOrdenados.remove(procesoActual)
            procesosRestantes -= 1

    for proceso in procesos:
        tiempoPromedio += proceso.tiempoRafaga

    tiempoPromedio -= tiempoActual
    print("\n{}/{}".format(tiempoPromedio, len(procesos)))
    tiempoPromedio /= len(procesos)
    print("Tiempo promedio de ejecución:", tiempoPromedio)

def simular_RoundRobin(procesos, quantumTiempo):
    colaListos = deque()
    tiempoActual = 0
    tiempoPromedio = 0
    procesosRestantes = len(procesos)

    for proceso in procesos:
        if proceso.tiempoLlegada <= tiempoActual:
            colaListos.append(proceso)

    while procesosRestantes > 0:
        if not colaListos:
            print("Inactivo-", tiempoActual)
            tiempoActual += 1
            continue

        procesoActual = colaListos.popleft()

        print("|P{}|-{}".format(procesoActual.numeroProceso, tiempoActual))

        tiempoEjecucion = min(quantumTiempo, procesoActual.tiempoRestante)
        procesoActual.tiempoRestante -= tiempoEjecucion
        tiempoActual += tiempoEjecucion

        if procesoActual.tiempoRestante > 0:
            colaListos.append(procesoActual)
        else:
            procesosRestantes -= 1

    for proceso in procesos:
        tiempoPromedio += proceso.tiempoRafaga

    print("\n{}/{}".format(tiempoPromedio, len(procesos)))
    tiempoPromedio /= len(procesos)
    print("Tiempo promedio de ejecución:", tiempoPromedio)

def main():
    eleccion = int(input("Selecciona el planificador:\n"
                         "1. First-Come, First-Served\n"
                         "2. Shortest-Job-First\n"
                         "3. Shortest-Remaining-Time-First\n"
                         "4. Round Robin\n"
                         "Ingresa tu elección: "))

    numProcesos = int(input("Ingresa el número de procesos: "))

    procesos = []

    for i in range(numProcesos):
        print("Proceso {}:".format(i + 1))
        numeroProceso = int(input("  Número de proceso: "))
        tiempoLlegada = int(input("  Tiempo de llegada: "))
        tiempoRafaga = int(input("  Tiempo de ráfaga: "))
        procesos.append(Proceso(numeroProceso, tiempoLlegada, tiempoRafaga))

    if eleccion == 1:
        simular_FCFS(procesos)
    elif eleccion == 2:
        simular_SJF(procesos)
    elif eleccion == 3:
        simular_SRTF(procesos)
    elif eleccion == 4:
        quantumTiempo = int(input("Ingresa el quantum de tiempo para Round Robin: "))
        simular_RoundRobin(procesos, quantumTiempo)
    else:
        print("Selección inválida.")

if __name__ == '__main__':
    main()