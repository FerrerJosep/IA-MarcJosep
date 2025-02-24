from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import threading
import time
import random
import os
import concurrent.futures

os.environ['GH_TOKEN'] = 'MARC LO TIENE'
terminos_busqueda = ["moviles", "phones", "moviles baratos", "movil iphones", "movil xiaomi", "movil samsung", "moviles españa", "moviles top", "moviles buenos"]
asins = set()
lock = threading.Lock()
output_file = "./Data/asins.txt"

def scrape_termino(termino):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    try:
        base_url = f"https://www.amazon.es/s?k={termino.replace(' ', '+')}&page="
        page = 1
        while page <= 7:
            url = f"{base_url}{page}"
            print(f"Scrapeando término '{termino}', página {page}: {url}")
            max_reintentos = 3
            reintentos = 0
            while reintentos < max_reintentos:
                try:
                    driver.get(url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-asin]')))
                    productos = driver.find_elements(By.CSS_SELECTOR, 'div[data-asin]')
                    data_asins = set()
                    for p in productos:
                        try:
                            asin = p.get_attribute("data-asin")
                            if asin:
                                data_asins.add(asin)
                        except Exception as e:
                            print(f"Error al obtener 'data-asin': {e}")
                            continue
                    with lock:
                        tamaño_anterior = len(asins)
                        asins.update(data_asins)
                        nuevos_asins = len(asins) - tamaño_anterior
                    print(f"Recogidos {len(data_asins)} ASINs en la página {page}, de los cuales {nuevos_asins} son nuevos.")
                    break
                except Exception as e:
                    reintentos += 1
                    print(f"Error en la página {page} del término '{termino}': {e}. Reintento {reintentos}/{max_reintentos}")
                    if reintentos == max_reintentos:
                        print(f"Se agotaron los reintentos para la página {page} del término '{termino}'.")
                        continue
            time.sleep(random.uniform(1, 3))
            page += 1
    finally:
        driver.quit()
        
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(scrape_termino, terminos_busqueda)

with open(output_file, "w") as f:
    f.write("\n".join(asins))
    
print(f"Scraping completado. Total ASINs únicos guardados: {len(asins)}")