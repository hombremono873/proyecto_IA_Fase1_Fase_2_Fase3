# Predicciones con el modelo previamente entrenado
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import os

# ------------------------------------------------------------------------------  
# Carpeta de datos
# ------------------------------------------------------------------------------  
DATA_DIR = "datos"   # /app/datos si tu WORKDIR es /app

# ------------------------------------------------------------------------------ 
# ------------------------------------------------------------------------------
# la funcion load_dataset(..) carga los archivos de los datasets *.csv y 
# retorna el dataframe.
#-------------------------------------------------------------------------------
def load_dataset(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

#-------------------------------------------------------------------------------
# la funcion load_model(...) retorna el modelo entrenado
#-------------------------------------------------------------------------------
def load_model(path: str):
    return joblib.load(path)

# ------------------------------------------------------------------------------
# la funcion clean_df(..) elimina columnas o series en el dataframe que no son 
# relevantes para el entrenamiento del modelo.
#-------------------------------------------------------------------------------

def clean_df(df: pd.DataFrame, cols_drop: list, flag: bool):
    df_clean = df.drop(columns=cols_drop, errors="ignore")
    if flag:
        y = df_clean["y"]
        X = df_clean.drop(columns=["y"])
        return X, y
    else:
        return df_clean
#-------------------------------------------------------------------------------
# La función encode_categoricals(....) codifica las columnas categoricas a 
# numeros.
#-------------------------------------------------------------------------------

def encode_categoricals(X):
    X_encoded = X.copy()
    for col in X_encoded.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col])
    return X_encoded

# ------------------------------------------------------------------------------
# la funcion_predict_datos_test(....) solicita predicciones al modelo 
#-------------------------------------------------------------------------------  
def predict_datos_test(modelo, X_test_num):
    y_pred  = modelo.predict(X_test_num)
    y_proba = modelo.predict_proba(X_test_num)[:, 1]
    return y_pred, y_proba

#-------------------------------------------------------------------------------
# La funcion generar_submission(....) construye un archivo con el resultado de 
# las predicciones y lo almacena en la carpeta temporal datos dentro del docker
#-------------------------------------------------------------------------------

def generar_submission(y_pred, ids, ruta_salida="/app/datos/predict.csv"):
    os.makedirs(os.path.dirname(ruta_salida) or ".", exist_ok=True)
    submission = pd.DataFrame({"id": ids.astype(str), "y": y_pred})
    submission.to_csv(ruta_salida, index=False)
    print(f"Archivo de submission generado en: {ruta_salida}")
    return submission

# ------------------------------------------------------------------------------
# la función ejecutar_flujo_prediccion(...) es la responsable de ejecutar todo el
# codigo para ejecutar predicciones.
#-------------------------------------------------------------------------------  
def ejecutar_flujo_prediccion(
    ruta_modelo: str = os.path.join(DATA_DIR, "modelo_entrenado.pkl"),
    ruta_test: str = os.path.join(DATA_DIR, "test.csv"),
    ruta_salida: str = os.path.join(DATA_DIR, "predicciones.txt")
): 
    print(
    "El proceso de predicciones para probar el modelo puede tardar unos segundos, "
    "por favor sea paciente.\n"
   )
    columnas_a_eliminar = ["id", "day", "month", "duration"]
     
    modelo = load_model(ruta_modelo)
    df_test = load_dataset(ruta_test)
    ids = df_test["id"]
    X_test = clean_df(df_test, columnas_a_eliminar, flag=False)
    X_test_encoded = encode_categoricals(X_test)

    y_pred, _ = predict_datos_test(modelo, X_test_encoded)

    # Se guarda *.txt
    os.makedirs(os.path.dirname(ruta_salida) or ".", exist_ok=True)
    if ruta_salida.endswith(".txt"):
        with open(ruta_salida, "w") as f:
            f.write("id y\n")
            for id_val, pred in zip(ids, y_pred):
                f.write(f"{id_val} {pred}\n")
        print(f"Predicciones guardadas en archivo de texto: {ruta_salida}")
    else:
        pd.DataFrame({"id": ids, "y": y_pred}).to_csv(ruta_salida, index=False)
        print(f"Predicciones guardadas en archivo CSV: {ruta_salida}")

    #  Además, generar siempre el CSV oficial en /app/datos/predict.csv
    generar_submission(y_pred, ids, ruta_salida="/app/datos/predict.csv")

    # Mostrar primeras predicciones
    for i in range(min(5, len(ids))):
        print(f"id={ids[i]}, y_pred={y_pred[i]}")
#-------------------------------------------------------------------------------
# El codigo lanza o ejecuta la funcion que maneja el flujo de predicción
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    ejecutar_flujo_prediccion()
