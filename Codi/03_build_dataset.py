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
    match = re.search(r"\b(\d+)\s?GB\b", title, re.IGNORECASE)
    return int(match.group(1)) if match else "null"

def infer_memory(title):
    match = re.search(r"\b(\d+)\s?(GB|TB)\b", title, re.IGNORECASE)
    if match:
        size = int(match.group(1))
        unit = match.group(2).upper()
        return size * 1024 if unit == "TB" else size
    return "null"

def extract_ram_and_memory(title):
    pattern = r"(\d+)\s?[+/]\s?(\d+)\s?(GB|TB)"
    match = re.search(pattern, title, re.IGNORECASE)
    if match:
        ram = int(match.group(1))
        memory_size = int(match.group(2))
        memory_unit = match.group(3).upper() #Siempre era en GB
        return ram, memory_size
    return "null", "null"

def remove_gb(value):
    if value != "null":
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            match = re.match(r"^(\d+)\s?GB$", value.strip())
            if match:
                return int(match.group(1))
    return "null"

def infer_screen_size(title):
    match = re.search(r"\b(\d+\.?\d*)\s?(''|\"|pulgadas|in)\b", title, re.IGNORECASE)
    if match:
        return match.group(1)
    return "null"

def infer_processor(description):
    processors = ["MediaTek", "Snapdragon", "Exynos", "Helio", "Dimensity"]
    for processor in processors:
        if processor.lower() in description.lower():
            return processor
    return "null"

def extract_dimensions(text):
    pattern = r"(\d+,\d+|\d+)\s?x\s?(\d+,\d+|\d+)\s?x\s?(\d+,\d+|\d+)"
    match = re.search(pattern, text)
    if match:
        dimensions = f"{match.group(1)} x {match.group(2)} x {match.group(3)}"
        return dimensions
    return "null"

def limit_length(value, max_length, default="null"):
    return str(value).strip()[:max_length] if value else default

def format_resolution(resolution):
    if not resolution:
        return "null"
    pattern = r"(\d+)\s?x\s?(\d+)"
    match = re.search(pattern, str(resolution)) 
    if match:
        return f"{match.group(1)} x {match.group(2)}"
    return "null"

if not os.path.exists(input_file):
    print("El archivo JSONL no existe.")
    exit()
if os.path.exists(output_file):
    os.remove(output_file)
    print(f"Archivo existente {output_file} eliminado.")

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

                marca = limit_length(find_value_by_keywords(product_information, ["fabricante", "marca"]), 25)
                marca = marca.replace('\u200e', '').strip().lower() if marca != "null" else "null"
                modelo = limit_length(find_value_by_keywords(product_information, ["modelo"]), 70)
                ano = find_value_by_keywords(product_information, ["año"], r"\b\d{4}\b")
                dimensiones = extract_dimensions(str(product_information))
                ram = find_value_by_keywords(product_information, ["RAM", "memoria RAM"], r"\d+")
                memoria = find_value_by_keywords(product_information, ["ROM", "memoria", "capacidad"], r"\b(\d+)\s?(GB|TB)\b")
                if ram == "null":
                    ram = infer_ram(product_title)
                if memoria == "null":
                    memoria = infer_memory(product_title)
                if ram == "null" or memoria == "null":
                    extracted_ram, extracted_memory = extract_ram_and_memory(product_title)
                    ram = ram if ram != "null" else extracted_ram
                    memoria = memoria if memoria != "null" else extracted_memory
                ram = remove_gb(ram)
                memoria = remove_gb(memoria)
                sistema_operativo = product_information.get("Sistema operativo", "null")
                resolucion_pantalla = format_resolution(find_value_by_keywords(product_information, ["resolucion", "resolución"]))
                tamano_pantalla = find_value_by_keywords(product_information, ["pantalla", "pulgadas"], r"\b(\d+\.?\d*)\s?(''|\"|pulgadas|in)\b")
                relacion_aspecto = find_value_by_keywords(product_information, ["relacion", "aspecto"], r"\d+:\d+")
                peso = find_value_by_keywords(product_information, ["peso", "masa"], r"\b\d+\s?g\b")
                if peso != "null":
                    peso = re.search(r"\b(\d+)\s?g\b", str(peso)).group(1)
                tecnologia_conectividad = find_value_by_keywords(product_information, ["tecnología", "conectividad"], r"\b(2G|3G|4G|5G|Wi-Fi|Bluetooth)\b")
                bateria = find_value_by_keywords(product_information, ["batería", "capacidad batería"], r"\b\d+\s?mAh\b")
                camara_principal = find_value_by_keywords(product_information, ["cámara", "principal"], r"\b\d+\s?MP\b")
                camara_frontal = find_value_by_keywords(product_information, ["cámara", "frontal"], r"\b\d+\s?MP\b")
                procesador = find_value_by_keywords(product_information, ["procesador", "chipset"], r"\b(MediaTek|Snapdragon|Exynos|Helio|Dimensity)\b")
                color = find_value_by_keywords(product_information, ["color"])

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