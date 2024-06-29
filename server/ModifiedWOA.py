import funciones_WOA as gD
import numpy as np

def whale_optimization_algorithm(objetos_generados,n, wmax, poblacion_max, MaxIter):
    # INICIALIZAR VARIABLES
    best_whales = []
    poblacion_ballenas = []
    fitness_ballenas = []
    
    # POBLACION INICIAL Y CALCULAR FITNESS
    poblacion_ballenas = gD.generar_poblacion(poblacion_max, objetos_generados)
    fitness_ballenas = gD.poblacion_fitness(poblacion_ballenas, objetos_generados, wmax)

    # MEJOR SOLUCION
    X_best = gD.mejor_solucion(poblacion_ballenas, fitness_ballenas)
    X_best_fitness = gD.calcular_fitness(X_best, objetos_generados, wmax)
    
    best_fitnesses = []
    
    # WOA
    for t in range(1, MaxIter + 1):
        #print(f"Generación: {t}")
        for i in range(poblacion_max):
            #print(f"Ballena: {i}")
            dimension = len(poblacion_ballenas[i])
            a = 2.0 - t * ((2.0 - 1.0) / MaxIter)
            r1 = np.random.random(dimension)
            r2 = np.random.random()
            
            A = 2 * a * r1 - a
            C_coef = 2 * r2
            
            l = np.random.uniform(-1, 1, size=dimension)
            p = np.random.random()
            
            if p < 0.5:
                if abs(C_coef) < 1:
                    # Enjambre alrededor de la mejor solución encontrada
                    D = abs(A * X_best - poblacion_ballenas[i])
                    #MODIFICACIONES
                    poblacion_ballenas[i] = np.round(np.abs(X_best - A * D + l  * 0.01)).astype(int)
                else:
                    # Buscar una nueva solución aleatoriamente
                    X_rand = gD.crear_solucion_aleatoria(objetos_generados)
                    D = np.abs(A * X_rand - poblacion_ballenas[i])
                    #MODIFICACIONES
                    poblacion_ballenas[i] = np.round(np.abs(X_rand - A * D + l  * 0.01)).astype(int)
            else:
                # Simular el comportamiento de burbujeo (movimiento en espiral)
                distance_to_best = np.abs([X_best[j] - poblacion_ballenas[i][j] for j in range(len(X_best))])
                poblacion_ballenas[i] = np.round(np.abs(distance_to_best * np.exp(-a * C_coef) * np.cos(2 * np.pi * C_coef) + X_best + l  * 0.01)).astype(int)
            
            fitness_actual = gD.calcular_fitness(poblacion_ballenas[i], objetos_generados, wmax)
            fitness_ballenas[i] = fitness_actual
        
        # Actualizar mejor ballena
        best_whales = gD.mejores_solucion(poblacion_ballenas, fitness_ballenas)
        current_best = best_whales[-1] #la ultima
        current_best_fitness = gD.calcular_fitness(current_best, objetos_generados, wmax)
        if current_best_fitness < X_best_fitness:
            X_best = current_best
            X_best_fitness = current_best_fitness

        best_fitnesses.append(X_best_fitness)
        
    return objetos_generados,X_best, X_best_fitness, best_fitnesses,best_whales

