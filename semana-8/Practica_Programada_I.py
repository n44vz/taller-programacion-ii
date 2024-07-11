# Paso 1: Importar bibliotecas
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Paso 2: Inicializar driver
driver = webdriver.Chrome()

# Paso 3: Definir URL para el scraping
url = "https://www.scrapethissite.com/pages/forms"

# Paso 4: Navegamos a la página
driver.get(url)  

# Paso 5: Inicializar lista vacia
datos = []

# Paso 6: Función para extraer datos
def extraer_datos():
    equipos = driver.find_elements(By.CLASS_NAME, "team")
    for equipo in equipos:
        nombre = equipo.find_element(By.CLASS_NAME, "name").text
        anio = equipo.find_element(By.CLASS_NAME, "year").text
        victorias = equipo.find_element(By.CLASS_NAME, "wins").text
        derrotas = equipo.find_element(By.CLASS_NAME, "losses").text
        derrotas_tiempo_extra = equipo.find_element(By.CLASS_NAME, "ot-losses").text
        porcentaje_victorias = equipo.find_element(By.CLASS_NAME, "pct").text
        goles_favor = equipo.find_element(By.CLASS_NAME, "gf").text
        goles_contra = equipo.find_element(By.CLASS_NAME, "ga").text
        gol_diferencia = equipo.find_element(By.CLASS_NAME, "diff").text
        
        datos.append({
        "Nombre": nombre,
        "Año": anio,
        "Victorias": victorias,
        "Derrotas": derrotas,
        "Derrotas Tiempo Extra": derrotas_tiempo_extra,
        "% Victorias": porcentaje_victorias,
        "Goles a favor": goles_favor,
        "Goles en contra": goles_contra,
        "Gol diferencia": gol_diferencia
        })   

# Extraer datos de todas las páginas
while True:
    # Esperar a que la tabla se cargue
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "team")))
    
    # Extraer datos de la página actual
    extraer_datos()
    
    # Intentar ir a la siguiente página
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']"))
        )
        if "disabled" in next_button.get_attribute("class"):
            break
        next_button.click()
        time.sleep(2)  # Esperar a que la página se cargue
    except:
        break  # Si no hay botón "Next", hemos terminado

df = pd.DataFrame(datos)

# Obtener la ruta del directorio del script actual
script_dir = os.getcwd()

# Crear la ruta completa del archivo CSV
csv_path = os.path.join(script_dir, "hockey_teams_data.csv")

# Guardar el DataFrame como CSV en el directorio del script
df.to_csv(csv_path, index=False)

# Cerrar el navegador
driver.quit()

print(f"Los datos se han guardado en: {csv_path}")