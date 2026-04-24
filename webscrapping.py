from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

# Encontrar Card con informacion
cards = soup.find_all("div", class_="flex flex-1 flex-col py-2")

for card in cards:
    precio = card.find("p").get_text(strip=True)
    descripcion = card.find("h3").get_text(strip=True)

    print("Precio:", precio)
    print("Texto:", descripcion)
    print("-" * 30)