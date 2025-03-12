import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pickle



def preprocess_data(df):
    df_copy = df.copy()

    # Calcular el precio medio por características clave
    df_copy["Precio_medio"] = df_copy.groupby(["Memoria", "RAM", "Marca"])["Precio"].transform("mean")

    # Nuevo criterio: se considera "Buena oferta" si el precio es un 10-20% menor que el promedio
    df_copy["target"] = df_copy["Precio"] < df_copy["Precio_medio"] * np.random.uniform(0.80, 0.90)

    # Introducir descuentos realistas (simulados)
    df_copy["Precio_descuento"] = df_copy["Precio"] * (1 - np.random.uniform(0.05, 0.15, size=len(df_copy)))

    # Convertir variables categóricas en dummies
    df_copy = pd.get_dummies(df_copy, columns=["Marca"], prefix="Marca")

    # Extraer dimensiones
    df_copy[["Ancho", "Alto", "Profundidad"]] = df_copy["Dimensiones"].str.replace(",", ".").str.extract(r"([\d.]+) x ([\d.]+) x ([\d.]+)").astype(float)

    df_copy.drop(columns=["Dimensiones", "Unnamed: 0", "Precio Inicial", "Precio_medio"], inplace=True)

    return df_copy


df = pd.read_csv('./Data/mobilsNET.csv')
df_processed = preprocess_data(df)
print(df_processed["target"].value_counts(normalize=True))


X = df_processed.drop(columns=["target", "Precio", "Precio_descuento"])
y = df_processed["target"]



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_split=10, min_samples_leaf=5, random_state=42)
model.fit(X_train, y_train)

def guardar_modelo_pickle():
    with open("modelo.pkl", "wb") as f:
        pickle.dump(model, f)

    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    with open("columnas.pkl", "wb") as f:
        pickle.dump(list(X.columns), f)


# Guardar modelo y escalador
def guardar_modelo(model, scaler, X):
    joblib.dump(model, "modelo.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(X.columns.tolist(), "features.pkl")

guardar_modelo_pickle()
print("✅ Modelo y escalador guardados exitosamente.")
