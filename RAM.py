'''Programa que simula la ejecucion de procesos en un sistema operativo de tiempo compartido mediante el uso de las
clases Resource y Container del modulo simpy, para el CPU y la memoria RAM, respectivamente.
Realizado por Pablo Andres Zamora Vasquez - 21780, el 13 de marzo de 2022'''

import simpy
import random
import numpy

# Se definen las constantes

env = simpy.Environment()
RANDOM_SEED = 225

def execute_process(env, name, ram, cpu, arrival, num_instructions, ram_required, cpu_speed):
    yield env.timeout(arrival) #Se espera la llegada del proceso

    start_time = env.now #Se almacena el tiempo de la simulacion en la que ingresa el proceso
    yield ram.get(ram_required) #Se retira de la memoria RAM la cantidad de memoria que requiere el proceso
    print("[NEW] %s agregado a la cola exitosamente. Tiempo actual: %f RAM requerida: %d" % (name, env.now, ram_required))

    while num_instructions > 0: #Mientras el proceso tenga instrucciones pendientes

        #READY
        print("[READY] %s listo para ejecutar. Tiempo actual: %f Instrucciones pendientes: %d" % (name, env.now, num_instructions)) #Se despliega el nombre del proceso, el tiempo actual y la cantidad de instrucciones a realizar
        with cpu.request() as req:
            yield req

            instructions_done = cpu_speed
            num_instructions -= cpu_speed #Se restan las instrucciones que pueda realizar el CPU de las instrucciones pendientes
            if num_instructions < 0:
                instructions_done = num_instructions + cpu_speed #Se calculan las instrucciones realizadas por el CPU
            yield env.timeout(1) #Avanza un ciclo de reloj

            #RUNNING
            print("[RUNNING] %s. El CPU ha ejecutado %d instrucciones exitosamente. Tiempo actual: %f" % (name, instructions_done, env.now)) #Se despliegan las instrucciones realizadas y el tiempo actual
            print("RAM actualmente disponible: %d" % (ram.level)) #Se despliega la RAM disponible

        if num_instructions > 0: #Si aun hay instrucciones pendientes
            waiting_or_ready = random.randint(1,2) #Se determina al azar si el proceso ingresa a WAITING
            if waiting_or_ready == 1:

                #WAITING
                print("[WAITING] %s esta realizando operaciones I/O. Tiempo actual: %d" % (name, env.now))
                yield env.timeout(1) #Se avanza un ciclo de reloj antes de regresar a READY
    
    #TERMINATED
    yield ram.put(ram_required) #Se devuelve a la memoria RAM la cantidad de memoria que necesitaba el proceso
    print("[TERMINATED] %s se ha terminado de ejecutar. Tiempo actual: %f" % (name, env.now)) #Se despliega el proceso finalizado y el tiempo actual
    print("RAM actualmente disponible: %d" % (ram.level)) #Se despliega la cantidad de memoria disponible
    global total_time
    global times
    total_time += env.now - arrival #Se agrega el tiempo que tardo el proceso al tiempo total
    times.append(env.now - arrival) #Se agrega a un arreglo el tiempo que tardo en completarse el proceso

#Ingreso de variables
print("Bienvenido a la simulacion de programas en un sistema operativo de tiempo compartido")
ram_capacity = int(input("Ingrese la capacidad de RAM a utilizar: ")) #Se determina la capacidad de la RAM
cpu_capacity = int(input("Ingrese la cantidad de procesadores del CPU a utilizar: ")) #Se determina la capacidad del CPU (Procesadores)
cpu_speed = int(input("Ingrese la cantidad de instrucciones que el CPU es capaz de ejecutar a la vez (Velocidad del CPU): ")) #Se determina la cantidad de instrucciones que puede realizar de un proceso a la vez
intervals = int(input("Ingrese los intervalos de la distribucion exponencial: ")) #Se determina la cantidad de intervalos de la distribucion exponencial
num_processes = int(input("Ingrese la cantidad de procesos a ejecutar: ")) #Se determina la cantidad de procesos a ejecutar
print("*** Iniciando simulacion ***")

#Creando el ambiente de simulacion
random.seed(RANDOM_SEED)
ram = simpy.Container(env, ram_capacity, init = ram_capacity) #Se crea la RAM
cpu = simpy.Resource(env, capacity = cpu_capacity) #Se crea el CPU
total_time = 0
times = []

#Corriendo la simulacion
for i in range (num_processes): #Por cada proceso
    arrival = random.expovariate(1.0/intervals)
    num_instructions = random.randint(1,10) #Se selecciona al azar la cantidad de instrucciones del proceso
    ram_required = random.randint(1,10) #Se selecciona al azar la cantidad de RAM que requiere el proceso
    env.process(execute_process(env,"Proceso #%s" %(i+1), ram, cpu, arrival, num_instructions, ram_required, cpu_speed))

env.run() #Se inicia la simulacion
print("\nPromedio del tiempo de ejecucion de cada proceso: %f" %(total_time/num_processes)) #Se despliega el promedio del tiempo
print("Desviacion estandar: %f" %(numpy.std(times))) #Se despliega la desviacion estandar de los tiempos obtenidos
print("\nGracias por utilizar la simulacion de programas en un sistema operativo de tiempo compartido. Feliz dia\n")










