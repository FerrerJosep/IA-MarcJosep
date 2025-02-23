import requests
import concurrent.futures
import json

API_KEYS = [
    "000f8774b5f8782161820d3a038fddc4"
]
current_api_index = 0
products_data = []
processed_count = 0
progress_interval = max(1, total_asins // 100)

with open("./Data/asins.txt", "r") as file:
    ASIN_LIST = [line.strip() for line in file.readlines()]
total_asins = len(ASIN_LIST)

def fetch_product_data(asin):
    global current_api_index
    for _ in range(len(API_KEYS)):
        payload = {
            'api_key': API_KEYS[current_api_index],
            'url': f'https://www.amazon.es/dp/{asin}',
            'output_format': 'json',
            'autoparse': 'true',
            'retry_404': 'true'
        }
        response = requests.get('https://api.scraperapi.com/', params=payload) 
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error con API_KEY {current_api_index + 1}: {API_KEYS[current_api_index]}")
            current_api_index = (current_api_index + 1) % len(API_KEYS)
            print(f"Usando API_KEY {current_api_index + 1}: {API_KEYS[current_api_index]}")
    return None

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(fetch_product_data, ASIN_LIST)

    for product_info in results:
        if product_info is not None:
            products_data.append(product_info)

        processed_count += 1
        if processed_count % progress_interval == 0 or processed_count == total_asins:
            progress = (processed_count / total_asins) * 100
            print(f"Progreso: {processed_count}/{total_asins} ({progress:.2f}%)")

with open("./Data/products.json", "w", encoding="utf-8") as f:
    json.dump(products_data, f, ensure_ascii=False, indent=4)

print("Datos guardados en products.json")