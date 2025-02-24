import csv
import json
import os
import re

input_file = "./Data/products.jsonl"
output_file = "./Data/moviles.csv"

def find_value_by_keywords(data_dict, keywords, pattern=None, default="null"):
    for key, value in data_dict.items():
        if any(keyword.lower() in key.lower() for keyword in keywords):
            if pattern is None or re.search(pattern, str(value)):
                return value
    return default

def safe_get(value, default="null"):
    return str(value).replace("€", "").strip() if value else default

if not os.path.exists(input_file):
    print("El archivo JSONL no existe.")
    exit()

with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Asin", "Precio", "Precio Inicial", "Título", "Estrellas", "Opiniones", "Marca", "Modelo", "Año del modelo", "Dimensiones",
                     "RAM", "Memoria", "Sistema operativo", "Resolución pantalla", "Tamaño pantalla", "Relación aspecto", "Peso", "Tecnología conectividad", "Batería"])

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                product = json.loads(line.strip())  # Convertir la línea en un diccionario
                product_information = product.get("product_information", {})

                asin = product_information.get("ASIN", "null")
                url = product.get("brand_url", "null")
                product_price = product.get("pricing", "null")
                product_original_price = product.get("list_price", product_price)
                product_title = product.get("name", "null")
                product_star_rating = product.get("average_rating", "null")
                product_num_ratings = product.get("total_reviews", "null")

                marca = find_value_by_keywords(product_information, ["fabricante", "marca"])
                modelo = find_value_by_keywords(product_information, ["modelo"])
                ano = find_value_by_keywords(product_information, ["año"], r"\b\d{4}\b")
                dimensiones = find_value_by_keywords(product_information, ["dimensiones", "tamaño", "medidas"], r"\d+")
                ram = find_value_by_keywords(product_information, ["RAM", "memoria RAM"], r"\b(1|2|4|8|16|32|64)\s?GB\b")
                memoria = find_value_by_keywords(product_information, ["ROM", "memoria", "capacidad"], r"\b(32|64|128|256|512|1024)\s?(GB|TB)\b")
                sistema_operativo = product_information.get("Sistema operativo", "null")
                resolucion_pantalla = find_value_by_keywords(product_information, ["resolucion", "resolución"], r"\d+")
                tamano_pantalla = find_value_by_keywords(product_information, ["pantalla", "pulgadas"], r"\d+")
                relacion_aspecto = find_value_by_keywords(product_information, ["relacion", "aspecto"], r"\d+:\d+")
                peso = find_value_by_keywords(product_information, ["peso", "masa"], r"\b\d+\s?g\b")
                tecnologia_conectividad = find_value_by_keywords(product_information, ["tecnología", "conectividad"], r"\b(2G|3G|4G|5G)\b")
                bateria = find_value_by_keywords(product_information, ["batería", "capacidad batería"], r"\b\d+\s?mAh\b")

                writer.writerow([
                    url, asin, product_price, product_original_price, product_title, product_star_rating, product_num_ratings,
                    marca, modelo, ano, dimensiones, ram, memoria, sistema_operativo, resolucion_pantalla, tamano_pantalla, relacion_aspecto, peso, tecnologia_conectividad, bateria
                ])
            except json.JSONDecodeError:
                print(f"Error al leer la línea JSON: {line.strip()}")
            except Exception as e:
                print(f"Error procesando producto: {e}")

print("Proceso completado. Datos guardados en products.csv")