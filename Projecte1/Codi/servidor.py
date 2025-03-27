from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Cargar modelo, escalador y columnas
modelo = pickle.load(open("../modelo.pkl", "rb"))
scaler = pickle.load(open("../scaler.pkl", "rb"))
columnas_modelo = pickle.load(open("../columnas.pkl", "rb"))

def procesar_entrada(datos):
    df = pd.DataFrame([datos])

    # Convertir a float los valores numéricos
    df["Memoria"] = df["Memoria"].astype(float)
    df["RAM"] = df["RAM"].astype(float)
    df["Precio"] = df["Precio"].astype(float)
    df["Estrellas"] = df["Estrellas"].astype(float)
    df["Peso"] = df["Peso"].astype(float)

    # Transformar marcas en variables dummy
    df = pd.get_dummies(df, columns=["Marca"], prefix="Marca")

    # Extraer dimensiones (si están disponibles)
    if "Dimensiones" in df.columns:
        df[["Ancho", "Alto", "Profundidad"]] = df["Dimensiones"].str.replace(",", ".").str.extract(r"([\d.]+) x ([\d.]+) x ([\d.]+)").astype(float)
        df.drop(columns=["Dimensiones"], inplace=True)

    # Asegurar que las columnas coincidan con el modelo
    for col in columnas_modelo:
        if col not in df.columns:
            df[col] = 0  

    df = df[columnas_modelo]  # Ordenar columnas
    df_scaled = scaler.transform(df)  # Normalizar datos

    return df_scaled

@app.route("/predecir", methods=["POST"])
def predecir():
    try:
        datos = request.json
        datos_procesados = procesar_entrada(datos)

        prediccion = modelo.predict(datos_procesados)[0]
        
        resultado = "Buena oferta" if prediccion == 1 else "Mala oferta"
        

        return jsonify({"prediccion": resultado})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
