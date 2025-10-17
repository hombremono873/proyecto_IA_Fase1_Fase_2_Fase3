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
def load_dataset(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_model(path: str):
    return joblib.load(path)

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

def encode_categoricals(X):
    X_encoded = X.copy()
    for col in X_encoded.select_dtypes(include=["object"]).columns:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col])
    return X_encoded

# ------------------------------------------------------------------------------  
def predict_datos_test(modelo, X_test_num):
    y_pred  = modelo.predict(X_test_num)
    y_proba = modelo.predict_proba(X_test_num)[:, 1]
    return y_pred, y_proba

# ------------------------------------------------------------------------------  
# >>> NO SE ELIMINA NINGUNA FUNCIÓN <<<
def generar_submission111(y_pred, ids, ruta_salida="datos/predicciones.txt"):
    submission = pd.DataFrame({"id": ids, "y": y_pred})
    os.makedirs(os.path.dirname(ruta_salida) or ".", exist_ok=True)
    submission.to_csv(ruta_salida, index=False)
    return submission

def generar_submission(y_pred, ids, ruta_salida="/app/datos/predict.csv"):
    os.makedirs(os.path.dirname(ruta_salida) or ".", exist_ok=True)
    submission = pd.DataFrame({"id": ids.astype(str), "y": y_pred})
    submission.to_csv(ruta_salida, index=False)
    print(f"Archivo de submission generado en: {ruta_salida}")
    return submission

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

    # Guardar TXT (como lo tenías)
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

    #  Además, generar SIEMPRE el CSV oficial en /app/datos/predict.csv
    generar_submission(y_pred, ids, ruta_salida="/app/datos/predict.csv")

    # Mostrar primeras predicciones
    for i in range(min(5, len(ids))):
        print(f"id={ids[i]}, y_pred={y_pred[i]}")

if __name__ == "__main__":
    ejecutar_flujo_prediccion()
