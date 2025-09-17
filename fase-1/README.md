# Proyecto de Inteligencia Artificial: Predictor en Actividades Bancarias

**Fecha de entrega:** 21 de agosto de 2025  
**Asignatura:** Técnicas en Inteligencia Artificial  
**Estudiante:** Omar Alberto Torres  
**Docentes:** Raúl Ramos Pollán, Jonathan Granda  
**Universidad:** Universidad de Antioquia  

## Descripción del Proyecto
Este proyecto implementa un modelo de **Machine Learning supervisado** para predecir si un cliente bancario aceptará una oferta de **depósito a plazo** tras una campaña de marketing.  

El objetivo es apoyar la toma de decisiones en estrategias comerciales, priorizando clientes con mayor probabilidad de conversión y reduciendo costos de campañas ineficientes.

## Fuente de Datos
- **Dataset:** Binary Classification with a Bank Dataset  
- **Plataforma:** Kaggle  
- **Competencia:** Tabular Playground Series - Season 5, Episode 8  
- **Enlace:** [Kaggle - Playground Series S5E8](https://www.kaggle.com/competitions/playground-series-s5e8/overview)  

El dataset incluye variables demográficas y económicas de clientes, y la variable `y` que indica aceptación (`1`) o rechazo (`0`) del producto.

## Requisitos del Sistema

### Hardware mínimo sugerido
- Procesador de 64 bits  
- 8 GB de RAM  
- 2 GB de espacio libre en disco  

### Software
- Python 3.11.4  
- Entorno recomendado: **Google Colab** (no requiere instalación adicional)  

### Librerías utilizadas
- pandas  
- numpy  
- scikit-learn  
- matplotlib  
- joblib  

Estas librerías ya vienen instaladas en Google Colab. Si deseas ejecutar en local, instálalas con:

```bash
pip install pandas numpy scikit-learn matplotlib joblib
```
# funcionamiento del codigo
1. El notebook realiza los siguientes pasos:
2. Carga los datos desde train.csv y test.csv.
3. Exploración preliminar de los datos.
4. Limpieza y codificación de variables categóricas.
5. Entrenamiento de un modelo de clasificación con Random Forest.
6. Evaluación con métricas: Accuracy, ROC-AUC y PR-AUC.
7. Exportación del modelo entrenado (modelo_entrenado.pkl).
8. Generación del archivo submission.csv con predicciones sobre el conjunto de prueba.
9. Limitaciones actuales
10. No incluye validación cruzada ni optimización de hiperparámetros.
11. No incorpora técnicas avanzadas de ingeniería de características.
12. No está dockerizado ni expuesto como servicio web (fase futura).

# Cómo Ejecutar el Proyecto

## Opción recomendada: Google Colab

1. Obtener el token de API de Kaggle:  
   - Ir a https://www.kaggle.com/account  
   - En la sección API → hacer clic en "Create New Token"  
   - Se descargará un archivo llamado `kaggle.json`.

2. Inscribirse en la competencia de Kaggle y acceder a los datos:  
   - Competencia: https://www.kaggle.com/competitions/playground-series-s5e8/overview  
   - Datos: https://www.kaggle.com/competitions/playground-series-s5e8/data  

   Nota: estos mismos enlaces también están disponibles directamente en el notebook de Colab.

3. Al ejecutar el código en Colab, se abrirá una ventana para subir el archivo `kaggle.json`.  
   Este paso es obligatorio para poder autenticar la descarga del dataset.

4. Una vez configurado, ejecutar las celdas del notebook en orden:
   1. Descarga y carga de datos  
   2. Exploración preliminar  
   3. Preprocesamiento  
   4. Entrenamiento del modelo  
   5. Evaluación  
   6. Exportación del modelo (`modelo_entrenado.pkl`)  
   7. Generación del archivo `submission.csv` con las predicciones  

---

# Anexo: Código de configuración en Colab

```bash python
# Subir kaggle.json (abrirá una ventana para seleccionar el archivo)

files.upload()

# Configurar Kaggle
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# Descargar y descomprimir el dataset en la carpeta ./datos
!mkdir -p ./datos
!kaggle competitions download -c playground-series-s5e8 -p ./datos
!unzip -o ./datos/*.zip -d ./datos

Los datos quedaran disponibles en:
./datos/train.csv
./datos/test.csv
./datos/sample_submission.csv

```

# Contacto
Para dudas o contribuciones:
Omar Alberto Torres
Correo: omara.torres@udea.edu.co
Cel: 3043440112