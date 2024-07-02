# Importar WebDriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd


# Crear objeto WebDriver
driver = webdriver.Firefox()

# Ingresar a la página
driver.get("https://es.wikipedia.org")


barra_busqueda = driver.find_element(
    By.CSS_SELECTOR, 
    ".cdx-text-input__input")

barra_busqueda.send_keys("Eurocopa")

barra_busqueda.send_keys(Keys.RETURN)

tabla = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/center/table")

# Encuentra las filas de la tabla
filas = tabla.find_elements(By.TAG_NAME, "tr")

# Extraer los encabezados
encabezados = [th.text.strip() for th in filas[0].find_elements(By.TAG_NAME, "th")]

# Cierra el navegador.
driver.quit()  

# Extraer los datos
datos = []
for fila in filas[1:]:
    fila_datos = []
    celdas = fila.find_elements(By.XPATH, ".//th | .//td")
    for celda in celdas:
        # Si la celda contiene enlaces <a>, extraer el texto del primer enlace que tenga contenido no vacío
        enlaces = celda.find_elements(By.TAG_NAME, "a")
        if enlaces:
            texto = next((enlace.text.strip() for enlace in enlaces if enlace.text.strip()), celda.text.strip())
        else:
            texto = celda.text.strip()
        
        # Añadir el texto limpio a la lista de datos de la fila
        fila_datos.append(texto)
    datos.append(fila_datos)

# Crear el DataFrame
df = pd.DataFrame(datos, columns=encabezados)

# Mostrar el DataFrame
print(df)