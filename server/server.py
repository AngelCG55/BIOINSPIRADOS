from flask import Flask, request, jsonify
from flask_cors import CORS
import main as m
import json
import numpy as np
import copy
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

@app.route('/procesar', methods=['POST'])
def procesar():
    datos = request.get_json()

    # Procesar los datos recibidos
    objetos_generados = datos.get('objetos_generados', [])
    print(objetos_generados)
    print("espera")
    n = int(datos.get('n', 0))
    wmax = float(datos.get('wmax', 0))
    MaxIter = int(datos.get('MaxIter', 0))
    woaType = int(datos.get('woaType', 0))
    historial_fitness_aux = []
    best_whales_aux = []
    if n != 0 and wmax != 0:
        objetos_generados, historial_fitness, best_whales, mejor_fitness = m.main(n, wmax, objetos_generados,MaxIter,woaType)
        
        # Convertir a un tipo serializable por JSON
        mejor_fitness = int(mejor_fitness)
        for elemento in historial_fitness:
            historial_fitness_aux.append(int(elemento))
        for fila in best_whales:
            nueva_fila = []
            for elemento in fila:
                nueva_fila.append(int(elemento))
            best_whales_aux.append(nueva_fila)
        print(type(best_whales))
        print(type(best_whales_aux))
        
        respuesta = {
            "objetos_generados": objetos_generados,
            "historial_fitness":  historial_fitness_aux,
            "best_whales": best_whales_aux,
            "mejor_fitness": mejor_fitness
        }
        
        print(respuesta) 
        print(jsonify(respuesta)) 
    else:
        respuesta = {"error": "Parámetros inválidos"}
        print(jsonify(respuesta)) 
    return respuesta

if __name__ == '__main__':
    app.run(debug=True, port=5001)
