import random
import numpy as np
import matplotlib.pyplot as plt
def generar_objetos(n):
    objetos = [{'id': i, 'peso': round(random.uniform(0.0001, 1.0), 2)} for i in range(n)]
    return objetos

# def crear_solucion_aleatoria(objetos, wmax):
#     contenedores = [[]]  # Iniciar con al menos un contenedor vacío
#     objetos_restantes = objetos[:]  # Copiar la lista de objetos para no alterar la original
    
#     while objetos_restantes:
#         objeto = random.choice(objetos_restantes)  # Escoger un objeto aleatorio
#         objeto_agregado = False
        
#         # Intentar agregar el objeto al último contenedor creado
#         ultimo_contenedor = contenedores[-1]
#         peso_contenedor = sum(obj['peso'] for obj_id in ultimo_contenedor for obj in objetos if obj['id'] == obj_id)
        
#         if peso_contenedor + objeto['peso'] <= wmax:
#             ultimo_contenedor.append(objeto['id'])
#             objeto_agregado = True
        
#         # Si no cabe en el último contenedor, crear uno nuevo
#         if not objeto_agregado:
#             contenedores.append([objeto['id']])
        
#         # Remover el objeto de la lista de objetos restantes
#         objetos_restantes = [obj for obj in objetos_restantes if obj['id'] != objeto['id']]
    
#     return contenedores

# def crear_solucion_aleatoria(objetos, wmax):
#     contenedores = [[]]  # Iniciar con al menos un contenedor vacío
#     pesos_contenedores = [0]  # Peso inicial del primer contenedor
#     objetos_restantes = objetos[:]  # Copiar la lista de objetos para no alterar la original
#     asignacion_contenedores = [-1] * len(objetos)  # Lista para guardar la asignación de contenedores
    
#     while objetos_restantes:
#         objeto = random.choice(objetos_restantes)  # Escoger un objeto aleatorio
#         objeto_agregado = False
        
#         # Intentar agregar el objeto a uno de los contenedores existentes
#         for i in range(len(contenedores)):
#             if pesos_contenedores[i] + objeto['peso'] <= wmax:
#                 contenedores[i].append(objeto['id'])
#                 pesos_contenedores[i] += objeto['peso']
#                 asignacion_contenedores[objeto['id']] = i + 1  # Guardar el número del contenedor (1-indexado)
#                 objeto_agregado = True
#                 break
        
#         # Si no cabe en ninguno de los contenedores existentes, crear uno nuevo
#         if not objeto_agregado:
#             contenedores.append([objeto['id']])
#             pesos_contenedores.append(objeto['peso'])
#             asignacion_contenedores[objeto['id']] = len(contenedores)  # Guardar el número del nuevo contenedor (1-indexado)
        
#         # Remover el objeto de la lista de objetos restantes
#         objetos_restantes = [obj for obj in objetos_restantes if obj['id'] != objeto['id']]
    
#     return asignacion_contenedores

def crear_solucion_aleatoria(objetos):
    asignacion_contenedores = [-1] * len(objetos)  # Lista para guardar la asignación de contenedores
    
    for objeto in objetos:
        # Asignar cada objeto a un contenedor aleatorio
        contenedor_aleatorio = random.randint(1, random.randint(1, len(objetos)))
        asignacion_contenedores[objeto['id']] = contenedor_aleatorio  # Guardar el número del contenedor (1-indexado)
    
    return asignacion_contenedores

def calcular_fitness(asignacion_contenedores, objetos, wmax):
    # Encontrar el número máximo de contenedor (fitness inicial)
    fitness = max(asignacion_contenedores)+1
    
    # Crear una lista para guardar la suma de pesos de cada contenedor
    pesos_contenedores = [0] * fitness
    
    # Calcular la suma de pesos de cada contenedor
    for i, contenedor in enumerate(asignacion_contenedores):
        pesos_contenedores[contenedor - 1] += objetos[i]['peso']
    
    # Verificar si algún contenedor excede el peso máximo permitido
    for peso in pesos_contenedores:
        if peso > wmax:
            fitness += (len(objetos)+1)*2
    
    return fitness

def imprimir_solucion(solucion):
    for i, contenedor in enumerate(solucion):
        print(f"Contenedor {i+1}:")
        for objeto in contenedor:
            print(f"  ID: {objeto['id']}, Peso: {objeto['peso']}")
        print(f"  Peso total del contenedor: {sum(item['peso'] for item in contenedor)}")
        
def imprimir_soluciones(poblacion_ballenas, fitness_ballenas):      
    print("Fitness de las soluciones generadas:")
    for i, (ballena, fitness) in enumerate(zip(poblacion_ballenas, fitness_ballenas)):
        print(f"Solución {i+1}: Ballena = {ballena}, Fitness = {fitness}")
def imprimir_soluciones_best(poblacion_ballenas,mejor_fitness):      
    print("Fitness de las soluciones generadas:")
    for i, (ballena) in enumerate(zip(poblacion_ballenas)):
        print(f"Solución {i+1}: Ballena = {ballena}, Fitness = {mejor_fitness}")        

def generar_poblacion(poblacion_max,objetos_generados):
    poblacion_ballenas = []
    for _ in range(poblacion_max):
        solucion = crear_solucion_aleatoria(objetos_generados)
        poblacion_ballenas.append(solucion)
    return poblacion_ballenas
        
def poblacion_fitness(poblacion_ballenas,objetos_generados,wmax):
    fitness_ballenas = []
    for ballena in poblacion_ballenas:
        fitness = calcular_fitness(ballena,objetos_generados,wmax)
        fitness_ballenas.append(fitness)
    return fitness_ballenas

def mejor_solucion(poblacion_ballenas, fitness_ballenas):
    mejor_fitness = min(fitness_ballenas)  # Encontrar el mínimo fitness de la población
    indice_mejor = fitness_ballenas.index(mejor_fitness)  # Obtener el índice del mejor fitness
    
    mejor_solucion = poblacion_ballenas[indice_mejor]  # Obtener la mejor solución según el índice

    return mejor_solucion

def mejores_solucion(poblacion_ballenas, fitness_ballenas):
    mejor_fitness = min(fitness_ballenas)  # Encontrar el mínimo fitness de la población
    
    # Obtener todas las ballenas que tienen el mejor fitness y convertirlas en listas
    mejores_solutions = [list(poblacion_ballenas[i]) for i in range(len(fitness_ballenas)) if fitness_ballenas[i] == mejor_fitness]

    return mejores_solutions

#WOA
def actualizar_coeficientes(t, MaxIter,dimension):
    a = 2 - t * (2 / MaxIter)  # a disminuye linealmente de 2 a 0
    A = 2 * np.random.random(size=dimension) - 1  # A en el rango [-a, a]
    C = 2 * np.random.random()  # C en el rango [0, 2]
    return a, A, C

def encontrar_mejor_contenedor(ballena, objetos_generados):
    mejor_contenedor = None
    mejor_peso_total = -float('inf')  # Inicializar con un valor muy bajo para encontrar el máximo
    
    for contenedor in ballena:
        peso_total_contenedor = sum(obj['peso'] for obj in objetos_generados if obj['id'] in contenedor)
        
        if peso_total_contenedor > mejor_peso_total:
            mejor_peso_total = peso_total_contenedor
            mejor_contenedor = contenedor
    
    return mejor_contenedor, mejor_peso_total

def graficar_fitness(historial_fitness):
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(len(historial_fitness)), historial_fitness, label='Mejor fitness de cada iteración', color='b')
    plt.xlabel('Iteración')
    plt.ylabel('Fitness')
    plt.title('Evolución del fitness durante la optimización con WOA')
    plt.legend()
    plt.grid(True)
    plt.show()
    
def imprimir_asignacion_contenedores(asignacion_contenedores, objetos):
    # Crear una estructura para almacenar los objetos por contenedor
    contenedores = {}

    # Llenar la estructura con los objetos asignados a cada contenedor
    for obj_id, contenedor in enumerate(asignacion_contenedores):
        if contenedor not in contenedores:
            contenedores[contenedor] = []
        contenedores[contenedor].append(obj_id)

    # Iterar sobre los contenedores e imprimir la información
    for contenedor, objetos_en_contenedor in contenedores.items():
        print(f"Contenedor {contenedor} - Peso {sum(objetos[obj_id]['peso'] for obj_id in objetos_en_contenedor)}")
        for obj_id in objetos_en_contenedor:
            print(f"  - Objeto: {obj_id} Peso: {objetos[obj_id]['peso']}")
    

