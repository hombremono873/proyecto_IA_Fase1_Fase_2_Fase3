from flask import Flask, request, jsonify, send_file
import os
import pandas as pd
from app.train import train_model
from app.predict import ejecutar_flujo_prediccion, load_model, clean_df, encode_categoricals


app = Flask(__name__)

#DATA_DIR = "./datos"
#MODEL_PATH = os.path.join(DATA_DIR, "modelo_entrenado.pkl")

DATA_DIR = "/app/datos"
MODEL_PATH = os.path.join(DATA_DIR, "modelo_entrenado.pkl")
# ------------------------------------------------------------------------------
# 1. Entrenamiento del modelo
# ------------------------------------------------------------------------------
@app.route("/train", methods=["POST"])
def train_endpoint():
    try:
        metrics = train_model()
        return jsonify({"mensaje": "Entrenamiento completado", "metrics": metrics}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------------------------
# 2. Predicción por archivo (test.csv)
# ------------------------------------------------------------------------------
#@app.route("/predict_file", methods=["GET"])
@app.route("/predict_file", methods=["GET"])
def predict_file():
    try:
        submission = ejecutar_flujo_prediccion(
            ruta_modelo=MODEL_PATH,
            ruta_test=os.path.join(DATA_DIR, "test.csv"),
            ruta_salida=os.path.join(DATA_DIR, "predicciones.txt") 
        )
        return jsonify({
            "mensaje": "Predicción realizada con éxito",
            "preview": submission.head().to_dict(orient="records")
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------------------------------
# 3. Predicción de un registro JSON
# ------------------------------------------------------------------------------
@app.route("/predict_one", methods=["POST"])
def predict_one():
    try:
        modelo = load_model(MODEL_PATH)
        data = request.get_json()  
        df = pd.DataFrame([data])

        columnas_a_eliminar = ["id", "day", "month", "duration"]
        X = clean_df(df, columnas_a_eliminar, flag=False)
        X_encoded = encode_categoricals(X)

        pred = int(modelo.predict(X_encoded)[0])
        proba = float(modelo.predict_proba(X_encoded)[0, 1])

        return jsonify({"pred": pred, "proba": proba}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------------------------------
# Arranque servidor
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
