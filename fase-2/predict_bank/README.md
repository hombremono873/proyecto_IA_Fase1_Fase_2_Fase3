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

Este proyecto implementa un modelo de Machine Learning en Python para predecir el resultado de ciertas actividades bancarias.  
El modelo y el flujo de predicción se ejecutan dentro de un contenedor Docker, lo cual garantiza un entorno limpio y reproducible.

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
Debe ubicarse el archivo kaggle.json a la misma altura del archivo Dockerfile dentro de la carpeta,
predick_bank.

---

## Requisitos previos

- Docker Desktop instalado y ejecutándose
- Sistema operativo Windows con acceso a terminal (CMD o PowerShell)
- Proyecto organizado con la siguiente estructura:

## taller_IA_fase2/ # Carpeta principal del proyecto
## ├── datos/ # Carpeta externa para datasets y modelo entrenado
## │ ├── train.csv # Dataset de entrenamiento (descargado desde Kaggle)
## │ ├── test.csv # Dataset de prueba (descargado desde Kaggle)
## │ ├── sample_submission.csv # Archivo de ejemplo de submission (Kaggle)
## │ └── modelo_entrenado.pkl  # Modelo entrenado guardado
## ├── predict_bank/      # Código fuente del proyecto
## │ ├── app/             # Scripts principales
## │ │ ├── train.py       # Script de entrenamiento del modelo
## │ │ ├── predict.py     # Script de predicción
## │ │ └── init.py        # (opcional) indica que es un paquete Python
## │ ├── Dockerfile       # Configuración del contenedor Docker
## │ ├── requirements.txt # Dependencias del proyecto
## │ └── README.md        #  Documentación del proyecto
## | └──kaggle.json       # Credenciales de la API de Kaggle
## └──



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

Despues de haber construido la imagen del docker, la aplicación queda en modo interactivo,
Si es la primera vez que se ejecuta la aplicación ocurre lo siguiente.
Al ejecutar el train.py se accede a la clave almacenada en json, se descarga automaticamente los datasets
(train.csv, test.csv) almacenados en la carpeta temporal datos. Adicionalmente se genera el archivo modelo_entrenado.pkl y se ubica en la carpeta temporal datos.
Al ejecutar test.csv se prueba el modelo y se genera los archivos test.txt y sumisscion.csv, que se ubicaran en la carpeta temporal datos del docker. Igualmente se imprime en consola algunos resultados de la prediccion.

Entrenamiento del modelo
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
 El siguiente comando ejecuta las predicciones, al finalizar se descarga en la carpata temporal datos el archivo predicciones.txt

# Ejecutar predict.py
```bash
root@4820ed2101ab:/app# python predict.py
```
Despues de ejecutar el comando anterior, ademas de guardarse el archivo con las predicciones se
puede apreciar la siguiente información en consola:

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
  C:\cualquier ruta>docker image prune -a

```

# Gestion de archivos generados

Los archivos modelo_entrenado.pkl, predicciones.txt, predict.csv quedan en la carpeta temporal datos
pueden ser leidos asi: 

```bash
root@6cd540dc7299:/app/datos# head -n 10 /app/datos/predict.csv
root@6cd540dc7299:/app/datos# head -n 10 /app/datos/predicciones.txt

```
# Descarga a mi pc los archivos
Teniendo corriendo el docker abra otra consola y ejecute el comando docker ps para obtener el id del docker
**Nota** las rutas y ID dependen de tu equipo, solo muestro un ejemplo de como lo hice en el mío"

**Formato**
docker cp <ID_CONTENEDOR>:/app/datos/predict.csv "C:\Users\OMAR\Downloads\predict.csv"
```bash
docker ps
Obtuve por ID "ad38969d1f09"
docker cp ad38969d1f09:/app/datos/predict.csv "C:\Users\OMAR TORRES\Downloads\predict.csv"
docker cp ad38969d1f09:/app/datos/predicciones.txt "C:\Users\OMAR TORRES\Downloads\predicciones.txt"
docker cp ad38969d1f09:/app/datos/modelo_entrenado.pkl "C:\Users\OMAR TORRES\Downloads\modelo_entrenado.pkl"
```

## En caso de consulta contactar a:
Omar Alberto Torres
tel: 3043440112
Correo: omar.torresm@udea.edu.co

Nota: En caso de requerir orientación adicional sobre la ejecución o los detalles técnicos del proyecto, puede contactarme al correo institucional o revisar los comentarios en el código fuente.









