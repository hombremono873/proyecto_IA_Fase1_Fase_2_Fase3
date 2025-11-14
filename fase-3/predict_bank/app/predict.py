# Predicciones con el modelo previamente entrenado
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import os

# ------------------------------------------------------------------------------  
# Carpeta de datos externa (montada en Docker en /app/datos)
# ------------------------------------------------------------------------------  

DATA_DIR = "/app/datos"
MODEL_PATH = os.path.join(DATA_DIR, "modelo_entrenado.pkl")
# ------------------------------------------------------------------------------  
# Leer conjunto de datos
# ------------------------------------------------------------------------------  
def load_dataset(path: str) -> pd.DataFrame:
    """Carga un archivo CSV y lo retorna como DataFrame."""
    return pd.read_csv(path)

# ------------------------------------------------------------------------------  
# Leer modelo entrenado
# ------------------------------------------------------------------------------  
def load_model(path: str):
    """Carga un modelo previamente entrenado desde un archivo."""
    return joblib.load(path)

# ------------------------------------------------------------------------------  
# Limpiar conjunto de datos
# ------------------------------------------------------------------------------  
def clean_df(df: pd.DataFrame, cols_drop: list, flag: bool):
    #df_clean = df.drop(columns=cols_drop)
    df_clean = df.drop(columns=cols_drop, errors="ignore")
    if flag:
        y = df_clean["y"]
        X = df_clean.drop(columns=["y"])
        return X, y
    else:
        return df_clean

# ------------------------------------------------------------------------------  
# Codificar variables categóricas
# ------------------------------------------------------------------------------  
def encode_categoricals(X):
    X_encoded = X.copy()
    for col in X_encoded.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col])
    return X_encoded

# ------------------------------------------------------------------------------  
# Hacer predicciones
# ------------------------------------------------------------------------------  
def predict_datos_test(modelo, X_test_num):
    y_pred  = modelo.predict(X_test_num)
    y_proba = modelo.predict_proba(X_test_num)[:, 1]
    return y_pred, y_proba

# ------------------------------------------------------------------------------  
# Generar archivo de salida
# ------------------------------------------------------------------------------  
def generar_submission(y_pred, ids, ruta_salida="datos/predicciones.txt"):
    submission = pd.DataFrame({"id": ids, "y": y_pred})
    submission.to_csv(ruta_salida, index=False)
    return submission

# ------------------------------------------------------------------------------  
# Ejecutar flujo completo de predicción
# ------------------------------------------------------------------------------  
def ejecutar_flujo_prediccion(
    ruta_modelo: str = os.path.join(DATA_DIR, "modelo_entrenado.pkl"),
    ruta_test: str = os.path.join(DATA_DIR, "test.csv"),
    ruta_salida: str = os.path.join(DATA_DIR, "predicciones.txt")
):
    columnas_a_eliminar = ["id", "day", "month", "duration"]

    modelo = load_model(ruta_modelo)
    df_test = load_dataset(ruta_test)
    ids = df_test["id"]
    X_test = clean_df(df_test, columnas_a_eliminar, flag=False)
    X_test_encoded = encode_categoricals(X_test)

    y_pred, _ = predict_datos_test(modelo, X_test_encoded)

    # Guardar archivo
    os.makedirs(os.path.dirname(ruta_salida) or ".", exist_ok=True)
    df_pred = pd.DataFrame({"id": ids, "y": y_pred})

    if ruta_salida.endswith(".txt"):
        with open(ruta_salida, "w") as f:
            f.write("id y\n")
            for id_val, pred in zip(ids, y_pred):
                f.write(f"{id_val} {pred}\n")
        csv_path = os.path.join(DATA_DIR, "predicciones.csv")
        df_pred.to_csv(csv_path, index=False)        
    else:
        df_pred.to_csv(ruta_salida, index=False)

    print(f" Predicciones guardadas en {ruta_salida}")

    return df_pred

if __name__ == "__main__":
    ejecutar_flujo_prediccion()
