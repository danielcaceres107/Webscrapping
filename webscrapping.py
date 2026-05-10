import csv
import json
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


URL_RED_PISO = "https://www.redpiso.es"
URL_TASA_CAMBIO = "https://api.exchangerate-api.com/v4/latest/EUR"
ARCHIVO_JSON = "pisos.json"
ARCHIVO_CSV = "pisos.csv"


def obtener_tasa_usd():
    respuesta = requests.get(URL_TASA_CAMBIO, timeout=15)
    respuesta.raise_for_status()
    data = respuesta.json()
    return data["rates"]["USD"]


def convertir_precio_a_usd(precio, tasa_usd):
    precio_limpio = re.sub(r"[^\d,.]", "", precio)

    if not precio_limpio:
        return None

    precio_num = float(
        precio_limpio
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )

    return round(precio_num * tasa_usd, 2)


def extraer_pisos(html, pagina, tasa_usd):
    soup = BeautifulSoup(html, "html.parser")
    resultados = []
    cards = soup.find_all("div", class_="flex flex-1 flex-col py-2")

    for card in cards:
        precio_elemento = card.find("p")
        descripcion_elemento = card.find("h3")

        if precio_elemento is None or descripcion_elemento is None:
            continue

        precio = precio_elemento.get_text(strip=True)
        descripcion = descripcion_elemento.get_text(strip=True)

        resultados.append({
            "pagina": pagina,
            "precio": precio,
            "precio_usd": convertir_precio_a_usd(precio, tasa_usd),
            "descripcion": descripcion,
        })

    return resultados


def guardar_json(pisos, ruta=ARCHIVO_JSON):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(pisos, archivo, ensure_ascii=False, indent=2)


def guardar_csv(pisos, ruta=ARCHIVO_CSV):
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        columnas = ["pagina", "precio", "precio_usd", "descripcion"]
        writer = csv.DictWriter(archivo, fieldnames=columnas, delimiter=";")
        writer.writeheader()
        writer.writerows(pisos)


def buscar_madrid(driver):
    driver.get(URL_RED_PISO)
    time.sleep(3)

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


def seleccionar_tipo_piso(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[.//span[text()='Piso']]"))
    ).click()
    time.sleep(3)


def main():
    tasa_usd = obtener_tasa_usd()
    print("Tasa EUR a USD:", tasa_usd)

    driver = webdriver.Chrome()
    pisos = []

    try:
        buscar_madrid(driver)
        seleccionar_tipo_piso(driver)

        pisos_pagina = extraer_pisos(driver.page_source, pagina=1, tasa_usd=tasa_usd)
        pisos.extend(pisos_pagina)

        for piso in pisos_pagina:
            print(
                f"[Pagina {piso['pagina']}] {piso['precio']} "
                f"({piso['precio_usd']} USD) - {piso['descripcion']}"
            )

        for pagina in range(2, 3):
            boton = driver.find_element(By.XPATH, f"//button[text()='{pagina}']")
            boton.click()
            time.sleep(3)

            pisos_pagina = extraer_pisos(
                driver.page_source,
                pagina=pagina,
                tasa_usd=tasa_usd,
            )
            pisos.extend(pisos_pagina)

            for piso in pisos_pagina:
                print(
                    f"[Pagina {piso['pagina']}] {piso['precio']} "
                    f"({piso['precio_usd']} USD) - {piso['descripcion']}"
                )

    finally:
        driver.quit()

    guardar_json(pisos)
    guardar_csv(pisos)
    print(f"{len(pisos)} pisos guardados en {ARCHIVO_JSON} y {ARCHIVO_CSV}")


if __name__ == "__main__":
    main()
