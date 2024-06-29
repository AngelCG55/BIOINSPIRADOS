import WOA as WOA
import IWOA as IWOA
import ModifiedWOA as ModifiedWOA
import numpy as np
import funciones_WOA as gD

def main(n, wmax, objetos_generados,MaxIter,woaType=0):
    if MaxIter == 0:
        if n < 15:
            poblacion_max = 10
            MaxIter = 500
        elif n < 25:
            poblacion_max = 25
            MaxIter = 1500
        elif n < 80:
            poblacion_max = 25
            MaxIter = 3500
        else:
            poblacion_max = 50        
            MaxIter = 5000
    else:
        if n < 15:
            poblacion_max = 10
        elif n < 25:
            poblacion_max = 25
        elif n < 80:
            poblacion_max = 25
        else:
            poblacion_max = 50 
    if objetos_generados == []:
        objetos_generados = gD.generar_objetos(n)
    if woaType == 0:    
        objetos_generados, mejor_solucion, mejor_fitness, historial_fitness, best_whales = WOA.whale_optimization_algorithm(objetos_generados, n, wmax, poblacion_max, MaxIter)
    elif woaType == 1:    
        objetos_generados, mejor_solucion, mejor_fitness, historial_fitness, best_whales = IWOA.whale_optimization_algorithm(objetos_generados, n, wmax, poblacion_max, MaxIter)
    else :
        objetos_generados, mejor_solucion, mejor_fitness, historial_fitness, best_whales = ModifiedWOA.whale_optimization_algorithm(objetos_generados, n, wmax, poblacion_max, MaxIter)
    
    #print(f"La mejor solución encontrada: {mejor_solucion}")
    print(f"Tipo WOA: {woaType}")
    print(f"Con un fitness de: {mejor_fitness}")
    print(f"Contenedores Knapsack: {len(WOA.bin_packing_first_fit(wmax, objetos_generados))}")
    # print(f"Objetos Generados: {objetos_generados}")
    #print(best_whales)
    #gD.imprimir_soluciones_best(best_whales, mejor_fitness)
    gD.imprimir_asignacion_contenedores(best_whales[0], objetos_generados)
    #gD.graficar_fitness(historial_fitness) 
    
    return  objetos_generados,historial_fitness,best_whales,mejor_fitness

