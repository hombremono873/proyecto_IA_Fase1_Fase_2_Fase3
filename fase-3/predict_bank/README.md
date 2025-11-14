# Predicción con Modelo de Machine Learning (Dockerizado)

> **Proyecto:** Predictor en Actividades Bancarias  
> **Autor:** Omar Torres — Estudiante de Ingeniería de Sistemas  
> **Entregado a:** Raúl Ramos Pollán, Jonathan Granda – Facultad de Ingeniería, Universidad de Antioquia  
> **Fecha de entrega:** 23 de noviembre de 2025

## Resumen
Este proyecto implementa un flujo completo de Machine Learning orientado a la predicción de resultados en campañas bancarias mediante un modelo Random Forest.

La aplicación está contenedorizada con Docker y expone una API REST desarrollada en Flask, que permite interactuar con el modelo de manera sencilla y automatizada.
A través de esta API, el usuario puede:

1. Entrenar el modelo a partir del conjunto de datos de Kaggle.
2. Probar el modelo utilizando el archivo test.csv.
3. Realizar una predicción individual enviando un registro en formato JSON.

El uso de Docker garantiza un entorno reproducible, limpio y portátil, facilitando la ejecución del sistema en cualquier entorno sin conflictos de dependencias.

---
**Acceso a los datos de Kaggle**

El proyecto utiliza los datasets de la competencia **[Playground Series – Season 5, Episode 8](https://www.kaggle.com/competitions/playground-series-s5e8/overview)**.  

Para que el contenedor pueda descargar automáticamente los datos al momento de entrenar el modelo, es necesario configurar tus credenciales de Kaggle.

### Pasos para configurar el acceso
1. Únete a la competencia en los enlaces oficiales:
   - [Competencia (overview)](https://www.kaggle.com/competitions/playground-series-s5e8/overview)
   - [Datos (data)](https://www.kaggle.com/competitions/playground-series-s5e8/data)
2. En tu perfil de Kaggle, ve a:  
   **Account → Create New API Token**  
   Esto descargará un archivo llamado `kaggle.json`.
3. Coloca `kaggle.json` **en la raíz del proyecto**, al mismo nivel del `Dockerfile`.  
   
---
**Estructura del proyecto**
```text

taller_IA_fase3/
├──  predict_bank/                   # Proyecto principal
    ├── app/                        # Código fuente principal
    │   ├── apirest.py              # API REST con endpoints (train, predict_file, predict_one)
    │   |     
    │   ├── predict.py              # Lógica de predicción
    │   └── train.py                # Lógica de entrenamiento
    │
    ├── .dockerignore               # Archivos a ignorar por Docker
    ├──datos/ se llena con archivos generados en el train, si no existe se crea
    ├── Dockerfile                  # Imagen de Docker para la app
    ├── doker                       # (posible archivo auxiliar, revisar si es necesario)
    ├── kaggle.json                 # > Sin este archivo, el modelo no podrá descargar ni entrenar los datos.
    ├── prueba.txt                  # Archivo de prueba (auxiliar)
    ├── README.md                   # Documentación del proyecto
    └── requirements.txt            # Dependencias de Python
```
---
## Endpoints de la API 
## /train — Entrenamiento del modelo

**Método: POST**
Descripción:
Descarga los datos desde Kaggle (si no existen localmente), ejecuta el flujo de entrenamiento completo, evalúa el modelo y guarda el archivo modelo_entrenado.pkl dentro del contenedor (/app/datos).

**Flujo interno:**

1. Descarga o verifica los datasets (train.csv, test.csv, sample_submission.csv).
2. Limpia los datos eliminando columnas innecesarias (id, day, month, duration).
3. Codifica las variables categóricas con LabelEncoder.
4. Entrena un modelo RandomForestClassifier.
5. Calcula métricas (Accuracy, F1-Score, AUC).
6. Guarda el modelo en disco.

**Respuesta exitosa (200):**

```bash
{
  "mensaje": "Entrenamiento completado",
  "metrics": {
    "accuracy": 0.912,
    "f1_score": 0.87,
    "auc": 0.935
  }
}
```
---
## /predict_file — Predicción desde archivo CSV
Método: GET
Descripción:
Carga el modelo entrenado y el archivo test.csv ubicado en /app/datos.
Genera las predicciones y guarda los resultados en:

/app/datos/predicciones.txt

**Flujo interno:**

1. Carga el modelo modelo_entrenado.pkl.
2. Lee el archivo test.csv.
3. Limpia y codifica las variables.
4. Realiza las predicciones (y_pred).
5. Guarda los resultados en formato texto y CSV.

**Respuesta exitosa (200):**
 ```bash
{
  "mensaje": "Predicción realizada con éxito",
  "preview": [
    {"id": 1, "y": 0},
    {"id": 2, "y": 1},
    {"id": 3, "y": 0}
  ]
}
 ```
---
## /predict_one — Predicción individual con JSON

**Método: POST**
Descripción:
Permite realizar una predicción para un solo registro recibido en formato JSON.

**Entrada esperada:**

```bash
{
  "age": 45,
  "job": "admin.",
  "marital": "married",
  "education": "secondary",
  "balance": 1200,
  "housing": "yes",
  "loan": "no",
  "campaign": 3,
  "pdays": 999,
  "previous": 0,
  "poutcome": "unknown"
}

```
**Respuesta exitosa (200):**
```bash
{
  "pred": 1,
  "proba": 0.84
}

```
---
# Notas importantes

La carpeta **`datos`** (externa al contenedor Docker) está diseñada para mantener todos los archivos generados durante la ejecución del proyecto. si no existe se crea en automático 

1. El archivo **`kaggle.json`** debe ser actualizado por el profesor con un token válido de Kaggle.  
   Sin esta clave de acceso, el programa **no podrá descargar los datasets**.

2. Durante la etapa de **entrenamiento**, el programa descarga los datasets desde Kaggle, los copia a la carpeta temporal dentro del contenedor y, además, los deja disponibles en la carpeta externa `datos`.

3. Una vez **entrenado el modelo**, el archivo `modelo_entrenado.pkl` se guarda automáticamente en la carpeta externa `datos`.

4. Al ejecutar la **predicción con `test.csv`**, los resultados (`predicciones.txt` y `predicciones.csv`) se generan dentro del contenedor y se guardan también en la carpeta externa `datos`.

5. En caso de ser necesario, puedo suministrar mi archivo `kaggle.json` con las credenciales configuradas para facilitar la ejecución.

---
## Ejecución del proyecto

### Construcción de la imagen Docker

1. Asegúrese de tener **Docker Desktop** instalado y en ejecución.  
2. Abra una terminal (**CMD** o **PowerShell**) en su sistema.  
3. Ubíquese en la **raíz del proyecto `predict_bank`**, es decir, en el mismo nivel donde se encuentra el archivo **`Dockerfile`**.

**Ejemplo (en Windows):**

```bash
   cd C:\Users\OMAR TORRES\Desktop\taller_IA_fase3\predict_bank
```

---
## Construcción de la imagen Docker

1. Ubíquese en la raíz del proyecto, a la altura del archivo Dockerfile. 
2. Por ejemplo (en mi caso): cd C:\Users\OMAR TORRES\Desktop\taller_IA_fase3\predict_bank

# Construir la imagen Docker
```bash
docker build -t predict_bank .

```
---
## Ejecución del contenedor Docker

1. Para correr la API REST dentro de un contenedor Docker 
2. y montar la carpeta de datos externa al proyecto, utilice el siguiente comando:

# El siguiente comando ejecuta la imagen y coordina el dialogo entre puertos
```bash
docker run -p 5001:5000 predict_bank
```
---

Para correr la API REST dentro de un contenedor Docker y montar la carpeta de datos externa, se utiliza el siguiente comando:
```bash
docker run -it --rm -v "%cd%\datos:/app/datos" -p 5001:5000 predict_bank
```
---

El comando anterior ejecuta el contenedor a partir de la imagen predict_bank,
expone el puerto 5000 del contenedor en el puerto 5001 de tu máquina local,
y monta la carpeta datos como volumen compartido entre tu sistema y el contenedor,
permitiendo guardar los modelos y resultados fuera del entorno Docker.

---

## Eliminación y administración rápida de Docker

```bash
#  Detener contenedores en ejecución
docker stop $(docker ps -q)

#  Eliminar contenedores detenidos o en ejecución
docker rm -f $(docker ps -aq)

#  Eliminar imágenes específicas o todas
docker rmi <nombre_o_id_imagen>
for /f %i in ('docker images -q') do docker rmi -f %i

#  Limpieza automática con Docker Prune
docker system prune          # elimina contenedores, redes y caché no usados
docker system prune -a       # incluye imágenes no utilizadas
```

## Ruta de datos y endpoints

En mi caso, la ruta del volumen de datos es:
**"C:/Users/OMAR TORRES/Desktop/taller_IA_fase3/datos"**.  
La carpeta **datos** es externa al proyecto Docker y se usa para **guardar el modelo entrenado** y las **predicciones** durante las pruebas.

---
# Nota 1 muy importante
Los endpoints pueden ser ejecutados con postman o usando la aplicacion cliente.py que corre en un contenedor
independiente.

**Pruebas con Postman**
```bash
- http://localhost:5001/train  
- http://localhost:5001/predict_file  
- http://localhost:5001/predict_one
```
---

## Uso del cliente Python (cliente.py)

Además de herramientas como Postman o cURL, el proyecto incluye un script auxiliar llamado cliente.py,
que permite interactuar directamente con la API REST desde la línea de comandos utilizando Python.

Este cliente fue diseñado para consumir los tres endpoints principales expuestos por el servidor Flask:

1. /train → Entrena el modelo.
2. /predict_file → Genera predicciones a partir del archivo test.csv.
3. /predict_one → Realiza una predicción individual enviando un registro en formato JSON.

El propósito del cliente es automatizar las pruebas de la API y facilitar el trabajo con los endpoints sin necesidad de herramientas externas.

### Nota 2

Asegúrese de que el contenedor Docker esté corriendo (la API activa en el puerto **5001**)  
---
## Contacto
Omar Alberto Torres  
Tel: 304 344 0112  
Correo: omar.torresm@udea.edu.co

**Nota:** Si requiere orientación adicional sobre la ejecución o detalles técnicos, puede escribir al correo institucional o revisar los comentarios en el código fuente.






