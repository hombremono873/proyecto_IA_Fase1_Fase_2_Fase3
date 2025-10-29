# Predicción con Modelo de Machine Learning – Dockerizado

## Presentado por
**Omar Torres**  
Estudiante de Ingeniería de Sistemas  
Proyecto Machine Learning: *Predictor en Actividades Bancarias*

## Entregado a
**Raul Ramos Pollan, Jonathan Granda**  
Facultad de Ingeniería  
Universidad de Antioquia

## Fecha de entrega
Noviembre 2 2025

---

## Descripción del proyecto

Este proyecto implementa un modelo de Machine Learning en Python para predecir el resultado de determinadas actividades bancarias.  
El modelo y el flujo de predicción se ejecutan dentro de un contenedor Docker, lo que garantiza un entorno limpio, controlado y reproducible. 
El codigo esta diseñado para ejecutarse en modo interactivo y ofrece dos operaciones principales: entrenar el modelo y probar el modelo. 
Adicionalmente, los archivos de entrenamiento, prueba y el modelo entrenado se almacenan en la carpeta temporal datos/, lo que facilita su gestión y reutilización.

## Nota 1
El profesor debe descargar el repositorio ubicado en la siguiente dirección
```bash
https://github.com/hombremono873/entrega_fase_2_con_descarga_kaggle.git

```
## Nota 2
```bash
El profesor debe unirse a la competencia de Kaggle fuente de este trabajo en los enlaces,

https://www.kaggle.com/competitions/playground-series-s5e8/overview
https://www.kaggle.com/competitions/playground-series-s5e8/data

```
El profesor debe obtener un token de acceso "kaggle.json" para acceder a los datasets 
train.csv, test.csv.

## Nota muy importante
Debe ubicarse, el archivo kaggle.json a la misma altura del archivo Dockerfile dentro de la carpeta,
predick_bank.

---

## Requisitos previos

- Docker Desktop instalado y ejecutándose
- Sistema operativo Windows con acceso a terminal (CMD o PowerShell)
- Proyecto organizado con la siguiente estructura:

```text
taller_IA_fase2/
├── predict_bank/ # Carpeta principal del código fuente
│ ├── app/ # Código de la aplicación
│ │ ├── train.py # Script de entrenamiento del modelo
│ │ ├── predict.py # Script de predicción
│ │ └── init.py # (opcional) indica que es un paquete Python
│ ├── Dockerfile # Definición del contenedor Docker
│ ├── requirements.txt # Dependencias de Python del proyecto
│ ├── kaggle.json # Credenciales para la API de Kaggle
│ └── README.md # Documentación del proyecto (este archivo)
│
└── datos/ (temporal) # Carpeta interna dentro del contenedor
├── train.csv # Dataset de entrenamiento descargado (Kaggle)
├── test.csv # Dataset de prueba (Kaggle)
├── sample_submission.csv # Archivo de ejemplo de submission (Kaggle)
└── modelo_entrenado.pkl # Modelo entrenado generado en ejecución
---
```
---
## Ejecución del proyecto
Construcción de la imagen Docker
1. Inicie la aplicación docker desktop
2. Ubíquese en la raíz del proyecto predict_bank


## Construcción de la imagen Docker

```bash
# Ubíquese en la raíz del proyecto a la altura de Dokerfile. Por ejemplo (Mi caso):
cd C:\Users\OMAR TORRES\Desktop\taller_IA_fase2\predict_bank

## Construir la imagen Docker

docker build -t predict_bank_app .
```
# Ejecutar el docker en modo interactivo
```bash
docker run -it --rm predict_bank_app

```

Despues de haber construido la imagen del docker, la aplicación queda en modo interactivo.

Si es la primera vez que se ejecuta la aplicación ocurre lo siguiente:
- Al ejecutar el train.py se accede a la   clave almacenada en json, se descarga automaticamente los datasets
(train.csv, test.csv) que se guardan en la carpeta temporal datos datos/. 

- Adicionalmente se genera el archivo  modelo_entrenado.pkl y se ubica en la carpeta temporal datos/.

- Posteriormente, al ejecutar el script de prueba (predict.py) se evalúa el modelo utilizando del archivo test.csv . Como  resultado final se generan los archivos test.txt y submission.csv, que se almacenaran en la carpeta temporal datos/ del contenedor docker. Asimismo, en la consola se muestranalgunos resultados de la prediccion durante la prueba.

# Entrenamiento del modelo
## Ejecutar predict.py
```bash
root@4820ed2101ab:/app# python train.py
```
**Nota_1:**
  El entrenamiento puede demorar algunos minutos, por favor sea paciente.
  Se accede a los datasets (train.csv y test.csv), se realiza el entrenamiento, el modelo entrenado
  se almacena en la carpeta datos;  temporal en el docker

  Finalizado el entrenamiento se puede ver información como esta:
  100%|███████████████████████████████████████████████████████████████████████████████████████████| 14.7M/14.7M [00:08<00:00, 1.93MB/s]
  Archive:  ./datos/playground-series-s5e8.zip
    inflating: ./datos/sample_submission.csv
    inflating: ./datos/test.csv
    inflating: ./datos/train.csv

   Accuracy: 0.7755
   F1-score: 0.4282
   AUC: 0.8218
   OOB Score (fuera de bolsa): 0.7728
   Modelo guardado en ./datos/modelo_entrenado.pkl
   root@977914e97cec:/app#
 
## Ejecutando predicciones con el archivo test.csv
 El siguiente comando ejecuta las predicciones. 
 Al finalizar, se genera el archivo 'predicciones.txt', que se descarga automáticamente en la carpeta temporal 'datos/'.

# Ejecutar predict.py
```bash
root@4820ed2101ab:/app# python predict.py
```
Despues de ejecutar el comando anterior, además de guardarse el archivo con las predicciones se puede observar la siguiente salida en consola:

root@977914e97cec:/app# python predict.py

Predicciones guardadas en archivo de texto: datos/predicciones.txt
Archivo de submission generado en: /app/datos/predict.csv

id=750000, y_pred=0
id=750001, y_pred=0
id=750002, y_pred=0
id=750003, y_pred=0
id=750004, y_pred=1
root@977914e97cec:/app#

**Nota**

```bash
# Gestión cierre de imagenes y docker

# Ver contenedores activos
 C:\cualquier ruta>docker ps
 # Ver contenedores activos y detenidos
 C:\cualquier ruta>docker ps -a
 # Elimna contenedores detenidos
 C:\cualquier ruta>docker container prune
 # Elimina todas las imagenes 
 C:\cualquier ruta>docker images 
 C:\cualquier ruta>docker image prune -a
  

```

# Gestion de archivos generados

Los archivos 'modelo_entrenado.pkl', 'predicciones.txt', '*.csv' se almacenan en la carpeta temporal 'datos/'
Estos archivos pueden ser leidos odescargados directamente desde el contenedor.
Por ejemplo, alejecutar los siguientes comandos:
```bash
root@4f0889525bcf:/app# cd datos
root@4f0889525bcf:/app/datos# dir
```
Despues de ejecutar los comandoa anteriores podemos observar el contenido de la carpeta 'datos/'.

- modelo_entrenado.pkl  
- playground-series-s5e8.zip  
- predicciones.txt  
- predict.csv  
- sample_submission.csv  
- test.csv  
- train.csv

# Inspeccion rápida de resultados
Si desean revisar una muestra del contenido de los archivos generados, pueden usar el comando 'head'.
Este comando muestra las primeras líneas de un archivo de texto directamente en la consola.

Por ejemplo:

```bash
root@6cd540dc7299:/app/datos# head -n 10 /app/datos/predict.csv
root@6cd540dc7299:/app/datos# head -n 10 /app/datos/predicciones.txt

```
# Descarga de los archivos a mi pc

Con el contenedor Docker en ejecución abre **otra consola** y ejecute el comando para obtener el ID del contenedor activo:

**Nota** las rutas  ID varían segun tu equipo. A continuación se muestra un ejemplo de como realizar la descarga en Windows.

**Formato**
docker cp <ID_CONTENEDOR>:/app/datos/predict.csv "C:\Users\OMAR\Downloads\predict.csv"

```bash
docker ps
Obtuve por ID "ad38969d1f09"
docker cp ad38969d1f09:/app/datos/predict.csv "C:\Users\OMAR TORRES\Downloads\predict.csv"
docker cp ad38969d1f09:/app/datos/predicciones.txt "C:\Users\OMAR TORRES\Downloads\predicciones.txt"
docker cp ad38969d1f09:/app/datos/modelo_entrenado.pkl "C:\Users\OMAR TORRES\Downloads\modelo_entrenado.pkl"
```
---
## Eliminar imagenes
```bash
for /F "tokens=*" %i in ('docker images -q') do docker rmi -f %i
```
---

## En caso de consulta contactar a:

**Omar Alberto Torres**
**Tel:** [+57 304 344 0112](tel:+573043440112)

**Correo:** [omara.torres@udea.edu.co](mailto:omara.torres@udea.edu.co)

>**Nota:** Si necesitan información adicional sobre la ejecución o detalles técnicos del proyecto, escribemen al correo institucional.
> Tambien pueden revisar los comentarios en el código fuente para aclaraciones rápidas.

---








