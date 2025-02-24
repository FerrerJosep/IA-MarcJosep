import csv
import json
import os
import re

input_file = "./Data/products.jsonl"
output_file = "./Data/mobils.csv"

def find_value_by_keywords(data_dict, keywords, pattern=None, default="null"):
    for key, value in data_dict.items():
        if any(keyword.lower() in key.lower() for keyword in keywords):
            if pattern is None or re.search(pattern, str(value)):
                return value
    return default

def safe_get(value, default="null"):
    return str(value).replace("€", "").strip() if value else default

def infer_ram(title):
    match = re.search(r"\b(\d+)\s?(GB|MB)\b", title, re.IGNORECASE)
    if match:
        ram = match.group(1) + " " + match.group(2).upper()
        return ram
    return "null"

def infer_memory(title):
    match = re.search(r"\b(\d+)\s?(GB|TB)\b", title, re.IGNORECASE)
    if match:
        memory = match.group(1) + " " + match.group(2).upper()
        return memory
    return "null"

def infer_screen_size(title):
    match = re.search(r"\b(\d+\.?\d*)\s?(pulgadas|''|in)\b", title, re.IGNORECASE)
    if match:
        return match.group(1) + " pulgadas"
    return "null"

def infer_processor(description):
    processors = ["MediaTek", "Snapdragon", "Exynos", "Helio", "Dimensity"]
    for processor in processors:
        if processor.lower() in description.lower():
            return processor
    return "null"

if not os.path.exists(input_file):
    print("El archivo JSONL no existe.")
    exit()

with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Asin", "Precio", "Precio Inicial", "Título", "Estrellas", "Opiniones", "Marca", "Modelo", "Año del modelo", "Dimensiones",
                     "RAM", "Memoria", "Sistema operativo", "Resolución pantalla", "Tamaño pantalla", "Relación aspecto", "Peso", "Tecnología conectividad", 
                     "Batería", "Cámara principal", "Cámara frontal", "Procesador", "Color"])

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                product = json.loads(line.strip())
                product_information = product.get("product_information", {})
                full_description = product.get("full_description", "")

                asin = product_information.get("ASIN", "null")
                url = product.get("brand_url", "null")
                product_price = safe_get(product.get("pricing", "null"))
                product_original_price = safe_get(product.get("list_price", product_price))
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
                resolucion_pantalla = find_value_by_keywords(product_information, ["resolucion", "resolución"], r"\d+\s?x\s?\d+")
                tamano_pantalla = find_value_by_keywords(product_information, ["pantalla", "pulgadas"], r"\d+\.?\d*\s?pulgadas")
                relacion_aspecto = find_value_by_keywords(product_information, ["relacion", "aspecto"], r"\d+:\d+")
                peso = find_value_by_keywords(product_information, ["peso", "masa"], r"\b\d+\s?g\b")
                tecnologia_conectividad = find_value_by_keywords(product_information, ["tecnología", "conectividad"], r"\b(2G|3G|4G|5G|Wi-Fi|Bluetooth)\b")
                bateria = find_value_by_keywords(product_information, ["batería", "capacidad batería"], r"\b\d+\s?mAh\b")
                camara_principal = find_value_by_keywords(product_information, ["cámara", "principal"], r"\b\d+\s?MP\b")
                camara_frontal = find_value_by_keywords(product_information, ["cámara", "frontal"], r"\b\d+\s?MP\b")
                procesador = find_value_by_keywords(product_information, ["procesador", "chipset"], r"\b(MediaTek|Snapdragon|Exynos|Helio|Dimensity)\b")
                color = find_value_by_keywords(product_information, ["color"])
                
                if ram == "null":
                    ram = infer_ram(product_title)
                if memoria == "null":
                    memoria = infer_memory(product_title)
                if tamano_pantalla == "null":
                    tamano_pantalla = infer_screen_size(product_title)
                if procesador == "null":
                    procesador = infer_processor(full_description)
                    
                writer.writerow([
                    url, asin, product_price, product_original_price, product_title, product_star_rating, product_num_ratings,
                    marca, modelo, ano, dimensiones, ram, memoria, sistema_operativo, resolucion_pantalla, tamano_pantalla, 
                    relacion_aspecto, peso, tecnologia_conectividad, bateria, camara_principal, camara_frontal, procesador, color
                ])
            except json.JSONDecodeError:
                print(f"Error al leer la línea JSON: {line.strip()}")
            except Exception as e:
                print(f"Error procesando producto: {e}")

print("Proceso completado. Datos guardados en mobils.csv")