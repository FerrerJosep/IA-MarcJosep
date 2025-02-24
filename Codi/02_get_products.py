import requests
import concurrent.futures
import json
import os
import time

input_file = "./Data/asins.txt"
output_file = "./Data/products.jsonl"
API_KEYS = [
    "000f8774b5f8782161820d3a038fddc4",
    "e8b3c716e689e349595622c51b62f3a0",
    "bb655963163ffbd205c11ce8ab3ec6a5",
    "1cc04538226f6d7f7ff0492bfb65fb06"
]
current_api_index = 0
processed_count = 0

with open(input_file, "r") as file:
    ASIN_LIST = [line.strip() for line in file.readlines()]

total_asins = len(ASIN_LIST)
progress_interval = max(1, total_asins // 100)

if not os.path.exists(output_file):
    open(output_file, "w").close()

def fetch_product_data(asin):
    global current_api_index
    for attempt in range(len(API_KEYS)):
        api_key = API_KEYS[current_api_index]
        payload = {
            'api_key': api_key,
            'url': f'https://www.amazon.es/dp/{asin}',
            'output_format': 'json',
            'autoparse': 'true',
            'retry_404': 'true'
        }
        response = requests.get('https://api.scraperapi.com/', params=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error con API_KEY {current_api_index + 1}: {api_key} (Código {response.status_code})")
            current_api_index = (current_api_index + 1) % len(API_KEYS)
            print(f"Cambiando a API_KEY {current_api_index + 1}: {API_KEYS[current_api_index]}")
            time.sleep(1)
    print(f"Saltando ASIN {asin} tras fallar con todas las API Keys.")
    return None

def save_to_file(data):
    with open(output_file, "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(fetch_product_data, ASIN_LIST)
    for product_info in results:
        if product_info is not None:
            save_to_file(product_info)
        processed_count += 1
        if processed_count % progress_interval == 0 or processed_count == total_asins:
            progress = (processed_count / total_asins) * 100
            print(f"Progreso: {processed_count}/{total_asins} ({progress:.2f}%)")

print("Proceso completado. Datos guardados en products.jsonl")