from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

driver.get("https://www.redpiso.es")

time.sleep(3)

# Buscar caja de búsqueda (ajustar selector real)
search_box = driver.find_element(By.ID, "pv_id_0_1")
search_box.click()
time.sleep(1)
search_box.send_keys("Madrid")
search_box.send_keys(Keys.ENTER)
time.sleep(2)
search_box.send_keys(Keys.ARROW_DOWN)
time.sleep(1)
search_box.send_keys(Keys.ENTER)

time.sleep(10)

html = driver.page_source

# BeautifulSoup para analizar el HTML
soup = BeautifulSoup(html, "html.parser")

def extraer_pisos(html):
    soup = BeautifulSoup(html, "html.parser")
    resultados = []

    cards = soup.find_all("div", class_="flex flex-1 flex-col py-2")

    for card in cards:
        precio = card.find("p").get_text(strip=True)
        descripcion = card.find("h3").get_text(strip=True)

        resultados.append((precio, descripcion))

    return resultados

# página 1 (la inicial)
wait = WebDriverWait(driver, 10)

# Click en checkbox "Piso"
wait.until(
    EC.element_to_be_clickable((By.XPATH, "//label[.//span[text()='Piso']]"))
).click()

time.sleep(3)


html = driver.page_source
pisos = extraer_pisos(html)

for precio, descripcion in pisos:
    print("[Página 1]", precio, "-", descripcion)


# páginas 2 a 92
for i in range(2, 92):
    boton = driver.find_element(By.XPATH, f"//button[text()='{i}']")
    boton.click()
    
    time.sleep(3)

    html = driver.page_source
    pisos = extraer_pisos(html)

    for precio, descripcion in pisos:
        print(f"[Página {i}]", precio, "-", descripcion)