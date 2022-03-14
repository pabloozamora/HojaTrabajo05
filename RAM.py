import simpy
import random
import numpy

# Constantes

env = simpy.Environment()
RANDOM_SEED = 225

def execute_process(env, name, ram, cpu, arrival, num_instructions, ram_required, cpu_speed):
    yield env.timeout(arrival)

    start_time = env.now
    yield ram.get(ram_required)
    print("[NEW] %s agregado a la cola exitosamente. Tiempo actual: %f RAM requerida: %d" % (name, env.now, ram_required))

    while num_instructions > 0:
        print("[READY] %s listo para ejecutar. Tiempo actual: %f Instrucciones pendientes: %d" % (name, env.now, num_instructions))
        with cpu.request() as req:
            yield req

            instructions_done = cpu_speed
            num_instructions -= cpu_speed
            if num_instructions < 0:
                instructions_done = num_instructions + cpu_speed
            yield env.timeout(1)

            print("[RUNNING] %s. El CPU ha ejecutado %d instrucciones exitosamente. Tiempo actual: %f" % (name, instructions_done, env.now))
            print("RAM actualmente disponible: %d" % (ram.level))

        if num_instructions > 0:
            waiting_or_ready = random.randint(1,2)
            if waiting_or_ready == 1:
                print("[WAITING] %s esta realizando operaciones I/O. Tiempo actual: %d" % (name, env.now))
                yield env.timeout(1)
    
    yield ram.put(ram_required)
    print("[TERMINATED] %s se ha terminado de ejecutar. Tiempo actual: %f" % (name, env.now))
    print("RAM actualmente disponible: %d" % (ram.level))
    global total_time
    global times
    total_time += env.now + arrival
    times.append(env.now - arrival)

#Ingreso de variables
print("Bienvenido a la simulacion de programas en un sistema operativo de tiempo compartido")
ram_capacity = int(input("Ingrese la capacidad de RAM a utilizar: "))
cpu_capacity = int(input("Ingrese la cantidad de procesadores del CPU a utilizar: "))
cpu_speed = int(input("Ingrese la cantidad de instrucciones que el CPU es capaz de ejecutar a la vez (Velocidad del CPU): "))
intervals = int(input("Ingrese los intervalos de la distribucion exponencial: "))
num_processes = int(input("Ingrese la cantidad de procesos a ejecutar: "))
print("*** Iniciando simulacion ***")

#Creando el ambiente de simulacion
random.seed(RANDOM_SEED)
ram = simpy.Container(env, ram_capacity, init = ram_capacity)
cpu = simpy.Resource(env, capacity = cpu_capacity)
total_time = 0
times = []

#Corriendo la simulacion
for i in range (num_processes):
    arrival = random.expovariate(1.0/intervals)
    num_instructions = random.randint(1,10)
    ram_required = random.randint(1,10)
    env.process(execute_process(env,"Proceso #%s" %(i+1), ram, cpu, arrival, num_instructions, ram_required, cpu_speed))

env.run()
print("\nPromedio del tiempo de ejecucion de cada proceso: %f" %(total_time/num_processes))
print("Desviacion estandar: %f" %(numpy.std(times)))
print("\nGracias por utilizar la simulacion de programas en un sistema operativo de tiempo compartido. Feliz dia\n")










