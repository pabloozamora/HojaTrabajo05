import simpy
import random

# Constantes

env = simpy.Environment()
RANDOM_SEED = 225
CPU_SPEED = 3

def execute_process(env, name, ram, cpu, arrival, num_instructions, ram_required):
    yield env.timeout(arrival)

    start_time = env.now
    print("[NEW] %s agregado a la cola exitosamente. Tiempo actual: %f RAM requerida: %d" % (name, env.now, ram_required))
    yield ram.get(ram_required)

    while num_instructions > 0:
        print("[READY] %s listo para ejecutar. Tiempo actual: %f Instrucciones pendientes: %d" % (name, env.now, num_instructions))
        with cpu.request() as req:
            yield req

            instructions_done = CPU_SPEED
            num_instructions -= CPU_SPEED
            if num_instructions < 0:
                instructions_done = num_instructions + CPU_SPEED
            yield env.timeout(1)

            print("[RUNNING] %s. El CPU ha ejecutado %d instrucciones exitosamente. Tiempo actual: %f")
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
    total_time += env.now + arrival








