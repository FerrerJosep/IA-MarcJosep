from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configurar Selenium con Chrome en modo headless
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # No abrir ventana del navegador
options.add_argument("--disable-blink-features=AutomationControlled")  # Evitar detección de bot
options.add_argument("start-maximized")  
options.add_argument("disable-infobars")

# Inicializar el driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL de búsqueda en Amazon España
url = "https://www.amazon.es/s?k=mobil&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=18LZTS0F1Q8I7&sprefix=mobil%2Caps%2C125&ref=nb_sb_noss_1"

# Cargar la página
driver.get(url)

# Esperar a que se cargue el contenido dinámico
driver.implicitly_wait(5)

# Extraer todos los elementos con data-asin
productos = driver.find_elements(By.CSS_SELECTOR, 'div[data-asin]')

# Obtener los valores de data-asin (filtrando los vacíos)
data_asins = [p.get_attribute("data-asin") for p in productos if p.get_attribute("data-asin")]

# Imprimir los resultados
print(data_asins)

# guardar los resultados en un archivo
with open("asins.txt", "w") as f:
    f.write("\n".join(data_asins))
    
# Cerrar el navegador
driver.quit()
