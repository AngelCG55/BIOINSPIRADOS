function validarForm() {
    var inputJSON = document.getElementById("inputJSON");
    var boton =  document.getElementById("modalGraficas");
    var inputWMax = document.getElementById("inputWMax").value.trim();
    var inputNObj = document.getElementById("inputNObj").value.trim();
    var inputMaxIter = document.getElementById("inputMaxIter").value.trim();
    var selectElement = document.getElementById('selectWOA');
    var file = inputJSON.files[0];
    var json = null;
    woaType = selectElement.value;
    if (inputWMax === "") {
        alert("Complete los datos necesarios: Peso Máximo");
        return;
    }

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            try {
                json = JSON.parse(e.target.result).datos;
                //console.log('Contenido del archivo JSON:');
                //console.log(json);

                if (inputMaxIter !== "") {
                    datos = {
                        objetos_generados: json,
                        n: json.length,
                        wmax: inputWMax,
                        MaxIter: inputMaxIter,
                        woaType: woaType
                    }
                    boton.click()
                    enviarJSON(datos)
                    console.log("JSON File: ", json);
                    console.log("Peso Máximo: ", inputWMax);
                    console.log("Iteraciones Máximas: ", inputMaxIter);
                } else {
                    datos = {
                        objetos_generados: json,
                        n: json.length,
                        wmax: inputWMax,
                        woaType: woaType
                    }
                    boton.click()
                    enviarJSON(datos)
                    
                    console.log("Solo JSON File: ", json);
                    console.log("Peso Máximo: ", inputWMax);
                }
            } catch (error) {
                console.error('Error al parsear el archivo JSON:', error);
            }
        };

        reader.readAsText(file);
    } else {
        if (inputNObj === "") {
            alert("Complete los datos necesarios: #Objetos");
            return;
        }

        if (inputMaxIter !== "") {
            console.log("#Objetos: ", inputNObj);
            console.log("Iteraciones Máximas: ", inputMaxIter);
            datos = {
                n: inputNObj,
                wmax: inputWMax,
                MaxIter: inputMaxIter,
                woaType: woaType
            }
            boton.click()
            enviarJSON(datos)
        } else {
            console.log("#Objetos: ", inputNObj);
            console.log("Peso Máximo: ", inputWMax);
            datos = {
                n: inputNObj,
                wmax: inputWMax,
                woaType: woaType
            }
            boton.click()
            enviarJSON(datos)
        }
    }
}
function resetForm() {
    var inputJSON = document.getElementById("inputJSON");
    var inputWMax = document.getElementById("inputWMax");
    var inputNObj = document.getElementById("inputNObj");
    var inputMaxIter = document.getElementById("inputMaxIter");

    inputJSON.value = "";
    inputWMax.value = "";
    inputNObj.value = "";
    inputMaxIter.value = "";
}
async function enviarJSON(datos) {
    // const datos = {
    //     //objetos_generados: [{'id': 0, 'peso': 0.37}, {'id': 1, 'peso': 0.03}, {'id': 2, 'peso': 0.86}, {'id': 3, 'peso': 0.9}, {'id': 4, 'peso': 0.99}, {'id': 5, 'peso': 0.5}, {'id': 6, 'peso': 0.1}, {'id': 7, 'peso': 0.05}, {'id': 8, 'peso': 0.09}, {'id': 9, 'peso': 0.33}],
    //     objetos_generados: [],
    //     n: 15,
    //     wmax: 1.0
    //     //MaxIter:2000
    // };
    resetForm()
    try {
        const respuesta = await fetch('http://localhost:5001/procesar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });

        if (respuesta.ok) {
            const datosProcesados = await respuesta.json();
            console.log('Respuesta del servidor:', datosProcesados);
            mostrarDatos(datosProcesados)
        } else {
            console.error('Error en la respuesta del servidor');
        }
    } catch (error) {
        console.error('Error al enviar los datos:', error);
    }
}
function graficaConvergencia(fitnessData){
    // Crear etiquetas para los ejes x
    const labels = fitnessData.map((_, index) => index + 1);

    // Configuración de la gráfica
    const data = {
        labels: labels,
        datasets: [{
            label: 'Fitness',
            data: fitnessData,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: false,
            tension: 0.1,
            pointRadius: 1, // Tamaño de los puntos
            borderWidth: 2 // Grosor de la línea
        }]
    };

    // Configuración del Chart.js
    const config = {
        type: 'line',
        data: data,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Gráfica de Convergencia',
                    font: {
                        size: 16
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Generación'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Valor de Fitness'
                    }
                }
            }
        }
    };

    // Renderizar la gráfica en el canvas
    const ctx = document.getElementById('fitnessChart').getContext('2d');
    new Chart(ctx, config);
}
function graficaSolucion(objetos,solucion,idDiv,i){
console.log(objetos)
console.log(solucion)

// Función para crear la gráfica
function imprimirAsignacionContenedores(asignacionContenedores, objetos,idDiv,i) {
    const contenedores = {};
    asignacionContenedores.forEach((contenedor, obj_id) => {
        if (!contenedores[contenedor]) {
            contenedores[contenedor] = [];
        }
        contenedores[contenedor].push(obj_id);
    });
6
    const contenedorIndices = Object.keys(contenedores);
    const pesosContenedores = contenedorIndices.map(contenedor =>
        contenedores[contenedor].reduce((totalPeso, obj_id) => totalPeso + objetos[obj_id].peso, 0)
    );

    // Generar colores aleatorios
    const generarColoresAleatorios = (cantidad) => {
        const colores = [];
        for (let i = 0; i < cantidad; i++) {
            const color = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.7)`;
            colores.push(color);
        }
        return colores;
    };

    const labels = contenedorIndices.map(contenedor => `Contenedor ${contenedor}`);

    // Obtener colores aleatorios para cada objeto
    const colores = generarColoresAleatorios(objetos.length);

    // Configurar datos para la gráfica de barras
    const datasets = objetos.map((objeto, index) => {
        const data = contenedorIndices.map(contenedor =>
            contenedores[contenedor].includes(objeto.id) ? objetos[objeto.id].peso : 0
        );
        return {
            label: `O:${objeto.id} W:${objeto.peso}`,
            backgroundColor: colores[index % colores.length], // Usar colores aleatorios
            data: data
        };
    });

    // Configurar opciones de la gráfica
    const config = {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            scales: {
                x: {
                    stacked: true,
                    title: {
                        display: true,
                        text: 'Contenedor'
                    }
                },
                y: {
                    stacked: true,
                    title: {
                        display: true,
                        text: 'Peso'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: `Asignación de Objetos a Contenedores ${i}`,
                    font: {
                        size: 16
                    }
                }
            }
        }
    };

    // Crear la instancia de la gráfica
    const ctx = document.getElementById(idDiv).getContext('2d');
    new Chart(ctx, config);
}
// Llamar a la función para mostrar la gráfica
imprimirAsignacionContenedores(solucion, objetos,idDiv,i);

}
function mostrarDatos(datosProcesados){
    formatearModalGraficos()
    graficaConvergencia(datosProcesados.historial_fitness)
    
    //graficaSolucion()
    agregarGraficos(datosProcesados.objetos_generados,datosProcesados.best_whales)

}
function agregarGraficos(objetos_generados, best_whales) {
    let carrusel = document.getElementById('carousel-inner');

    // Itera sobre el arreglo best_whales
    for (let i = 0; i < best_whales.length; i++) {
        // Crea un nuevo elemento <div> con la clase "carousel-item"
        let nuevoDiv = document.createElement('div');
        nuevoDiv.classList.add('carousel-item');

        // Crea un nuevo elemento <canvas> con un ID único basado en el índice i
        let nuevoCanvas = document.createElement('canvas');
        nuevoCanvas.id = `fitnessChart${i}`;

        // Agrega el canvas como hijo del <div> creado
        nuevoDiv.appendChild(nuevoCanvas);
        console.log(nuevoCanvas)
        console.log(nuevoDiv)
        // Agrega el <div> como hijo del carrusel
        carrusel.appendChild(nuevoDiv);

        graficaSolucion(objetos_generados,best_whales[i],`fitnessChart${i}`,i+1)
    }
}

function formatearModalGraficos(){
    // Datos de fitness proporcionados
    let carrusel = document.getElementById('carousel-inner');
    while (carrusel.firstChild) {
        carrusel.removeChild(carrusel.firstChild);
    }
    let nuevoDiv = document.createElement('div');
    nuevoDiv.classList.add('carousel-item');
    nuevoDiv.classList.add('active');

    // Crea un nuevo elemento <canvas> con un ID único basado en el índice i
    let nuevoCanvas = document.createElement('canvas');
    nuevoCanvas.id = `fitnessChart`;
    nuevoCanvas.width = `400`;
    nuevoCanvas.height = `200`;

    // Agrega el canvas como hijo del <div> creado
    nuevoDiv.appendChild(nuevoCanvas);
    console.log(nuevoCanvas)
    console.log(nuevoDiv)
    // Agrega el <div> como hijo del carrusel
    carrusel.appendChild(nuevoDiv);
}