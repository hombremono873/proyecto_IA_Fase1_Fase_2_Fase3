# Entrenamiento del modelo Random Forest desde cero
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import subprocess
import os

# ------------------------------------------------------------------------------  
# Carpeta de datos externa (montada en Docker en /app/datos)
# ------------------------------------------------------------------------------  
#DATA_DIR = "datos"

#------------------------------------------------------------------------------

def ensure_kaggle_data(competition="playground-series-s5e8", data_dir="./datos"):
    os.makedirs(data_dir, exist_ok=True)
    train_path = os.path.join(data_dir, "train.csv")
    test_path = os.path.join(data_dir, "test.csv")
    sample_path = os.path.join(data_dir, "sample_submission.csv")

    if not (os.path.exists(train_path) and os.path.exists(test_path) and os.path.exists(sample_path)):
        print(" Archivos no encontrados, descargando desde Kaggle...")
        subprocess.run(
            ["kaggle", "competitions", "download", "-c", competition, "-p", data_dir],
            check=True
        )
        subprocess.run(
            f"unzip -o {data_dir}/*.zip -d {data_dir}",
            shell=True,
            check=True
        )
    else:
        print(" Archivos ya existen, se omite descarga.")

    return train_path, test_path, sample_path


# ------------------------------------------------------------------------------  
# Funciones de preprocesamiento
# ------------------------------------------------------------------------------  
def clean_df(df: pd.DataFrame, cols_drop: list, flag: bool):
    df_clean = df.drop(columns=cols_drop)

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
# Definición del modelo Random Forest
# ------------------------------------------------------------------------------  
def modelo_random_forest(X_train, y_train):
    modelo = RandomForestClassifier(
        n_estimators=300,
        max_depth=20,
        n_jobs=-1,
        random_state=42,
        class_weight="balanced_subsample",
        min_samples_leaf=20,
        min_samples_split=10,
        bootstrap=True,
        max_samples=0.7,
        oob_score=True
    )
    modelo.fit(X_train, y_train)
    return modelo

# ------------------------------------------------------------------------------  
# Flujo principal de entrenamiento
# ------------------------------------------------------------------------------  

DATA_DIR = "./datos"

def train_model():
    train_path, _, _ = ensure_kaggle_data(data_dir=DATA_DIR)  # Asegurar que los datos estén disponibles
    df_train = pd.read_csv(train_path)   # Cargar dataset de entrenamiento       
    columnas_a_eliminar = ["id", "day", "month", "duration"] # Columnas a eliminar (coherente con predict.py)

    X, y = clean_df(df_train, columnas_a_eliminar, flag=True)  # Preprocesamiento
    X_encoded = encode_categoricals(X)
    
   # División train/validación
    X_train, X_val, y_train, y_val = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42
    )

    modelo = modelo_random_forest(X_train, y_train)   # Entrenar modelo

    y_pred = modelo.predict(X_val)                    # Evaluar
    y_proba = modelo.predict_proba(X_val)[:, 1]

    acc = accuracy_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred)
    auc = roc_auc_score(y_val, y_proba)

    print(f" Accuracy: {acc:.4f}")
    print(f" F1-score: {f1:.4f}")
    print(f" AUC: {auc:.4f}")
    print(f" OOB Score (fuera de bolsa): {modelo.oob_score_:.4f}")

    # Guardar modelo entrenado
    path_modelo = os.path.join(DATA_DIR, "modelo_entrenado.pkl")
    joblib.dump(modelo, path_modelo)
    print(f" Modelo guardado en {path_modelo}")

# ------------------------------------------------------------------------------  
# Punto de entrada
# ------------------------------------------------------------------------------  
if __name__ == "__main__":
    train_model()
