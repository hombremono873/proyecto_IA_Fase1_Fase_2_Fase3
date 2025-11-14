# Cliente Python para la API de Predicción – Dockerizado

## Presentado por
**Omar Alberto Torres**  
Estudiante de Ingeniería de Sistemas  
Proyecto Machine Learning: *Predictor en Actividades Bancarias*

## Entregado a
**Raúl Ramos Pollán, Jonathan Granda**  
Facultad de Ingeniería  
Universidad de Antioquia

## Fecha de entrega
Noviembre 23 de 2025

---

Este proyecto complementa la API principal Predict Bank, desarrollada con Flask, mediante la incorporación de un cliente Python interactivo que se ejecuta dentro de su propio contenedor Docker.

El cliente actúa como una interfaz de consola que permite interactuar con la API REST de predicción de manera sencilla, sin necesidad de herramientas externas como Postman o cURL.

A través de un menú intuitivo, el usuario puede:

1. Entrenar el modelo de Machine Learning, activando el endpoint /train y generando el archivo modelo_entrenado.pkl.
2. Ejecutar predicciones por archivo, usando el endpoint /predict_file con los datos de test.csv.

3. Realizar predicciones individuales, consumiendo el endpoint /predict_one a partir de un registro JSON (data.json) o ingresando los datos manualmente.

De esta manera, el cliente y la API trabajan de forma conjunta para ofrecer un entorno modular, automatizado y reproducible, ideal para pruebas, demostraciones o despliegues controlados en Docker.

---
## Estructura del proyecto completo

El sistema se organiza en dos contenedores principales que trabajan de forma complementaria:

**predict_bank/** , Contiene el servidor Flask (API REST) donde se entrena y ejecuta el modelo de Machine Learning.

**cliente/** , Incluye el cliente Python interactivo, que permite consumir los endpoints de la API desde la consola.

La carpeta raíz **fase-3/** sirve como entorno de trabajo, e incluye además una carpeta datos/ compartida entre ambos contenedores para almacenar datasets, modelos y resultados.

```text
fase-3/
├── datos/ # Carpeta externa (inicialmente vacía)
│ # Se llenará con datasets, modelo y resultados
│
├── predict_bank/ # Contenedor del servidor Flask (API REST)
│ ├── app/
│ │ ├── apirest.py # API con endpoints /train, /predict_file, /predict_one
│ │ ├── train.py # Entrenamiento del modelo
│ │ ├── predict.py # Lógica de predicción
│ ├── Dockerfile # Imagen del servidor Flask
│ ├── requirements.txt # Dependencias del servidor
│ └── README.md # Documentación del API
│
└── cliente/ # Contenedor del cliente Python
├── cliente.py # Menú interactivo para consumir la API
├── Dockerfile # Imagen del cliente
└── README_cliente.md # Documentación del cliente
```
---
## Arquitectura del sistema
El sistema se compone de dos contenedores Docker complementarios, diseñados para separar las responsabilidades entre el entrenamiento del modelo y la interacción del usuario.

**predict_bank/** Contiene el servidor Flask (API REST), responsable de entrenar el modelo de Machine Learning, procesar las predicciones y exponer los endpoints /train, /predict_file y /predict_one.

**cliente/ ** Incluye el cliente Python interactivo, encargado de consumir la API REST mediante un menú en consola que permite al usuario entrenar el modelo, generar predicciones o probar entradas manuales.

La carpeta **raíz fase-3/** actúa como entorno principal del proyecto e incluye una carpeta datos/ compartida entre ambos contenedores, donde se almacenan los archivos generados durante el proceso:

**train.csv** ,**test.csv** datasets descargados desde Kaggle

**modelo_entrenado.pkl** modelo serializado tras el entrenamiento

**predicciones.csv**, **predicciones.txt** ,resultados generados durante las pruebas

---
## Ejecución en modo interactivo

El cliente Python (cliente.py) se ejecuta en modo interactivo dentro de su contenedor, iniciando un menú de opciones en consola.
Desde este menú, el usuario puede seleccionar la acción que desea realizar:

**--- CLIENTE ML ---**

1. Entrenar modelo
2. Predecir usando test.csv para probar el modelo
3. Predecir registro individual (usando data.json)
4. Predecir con entrada dinámica (el usuario digita los datos)
5. Salir
**Seleccione una opción:**

Cada opción del menú invoca internamente una función que se comunica con el servidor Flask a través de solicitudes HTTP (requests.post o requests.get), mostrando los resultados directamente en la terminal.

Cada opción corresponde a una acción sobre la API REST:

**Opcion 1**
Entrena el modelo de Machine Learning: POST /train

**Opcion 2**
Genera predicciones masivas desde test.csv (prueba del modelo): GET /predict_file

**Opcion 3**
Realiza una predicción individual a partir de un archivo JSON (data.json): POST /predict_one

**Opcion 4**
Permite ingresar los datos manualmente desde consola y envía la solicitud dinámica al modelo: POST /predict_one

**Opcion 5**
Finañliza la ejecución del cliente

---
##  Construcción de la imagen Docker

Ubíquese en la raíz del proyecto del cliente (donde se encuentra el archivo `Dockerfile`) y ejecute el siguiente comando:

# Imagen
```bash
docker build -t predict_bank_client .
```

# ejecutando el cliente
Para ejecutar el cliente en modo interactivo, use
```bash
docker run -it --rm predict_bank_client
```

Debe salir un menu como el siguiente:
--- CLIENTE ML ---
1. Entrenar modelo
2. Predecir usando test.csv para probar el modelo
3. Predecir registro individual, entrada previamente configurada en json
4. Predecir , entrada dinámica usuario digita datos de entrada
5. Salir 

# Al seleccionar
Seleccione una opción: 1
El proceso de entrenamiento del modelo puede demorar algunos minutos.

Entrenamiento completado
{'mensaje': 'Entrenamiento completado', 'metrics': None}

Seleccione una opción: 2
El proceso de predict, evalua el modelo con test.csv, al finalizar muestra algo como esto:

Predicción por archivo lista
{'mensaje': 'Predicción realizada con éxito', 'preview': [{'id': 750000, 'y': 0}, {'id': 750001, 'y': 0}, {'id': 750002, 'y': 0}, {'id': 750003, 'y': 0}, {'id': 750004, 'y': 1}]}

Se muestra algunas de las predicciones durante la prueb del modelo.

Seleccione una opcion: 3
Predicción individual
{'pred': 1, 'proba': 0.6749939364047577}

el modelo recibe una entrada en formato json, el modelo procesa la entrada y retorna la predicción

# Salir 
Seleccione una opción: 4
## Presenta un nuevo menu:
1: Hacer prediccion usando el contenido del archivo data.json, se retorna la prediccion.
2: Permite que el usuario digite los campos de entrada y se retorna la predicción.

Seleccione una opción: 5
## Sale esto 
Saliendo del cliente...

# Gestion
Ver imagenes

docker ps -a

parar todos los docker

for /f "tokens=*" %i in ('docker ps -aq') do docker rm -f %i
```
---
Autor

Omar Alberto Torres
Proyecto: Predict Bank – Cliente Python
Universidad de Antioquia – Facultad de Ingeniería
Correo: omar.torresm@udea.edu.co

Teléfono: 304 344 0112



