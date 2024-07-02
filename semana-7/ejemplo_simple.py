import os  # Importa el módulo os para interactuar con el sistema operativo.
import pandas as pd  # Importa pandas para manipulación y análisis de datos.
from selenium import webdriver  # Importa webdriver de Selenium para controlar el navegador.
from selenium.webdriver.common.by import By  # Importa By para localizar elementos en la página.
from selenium.webdriver.support.ui import WebDriverWait  # Importa WebDriverWait para esperas explícitas.
from selenium.webdriver.support import expected_conditions as EC  # Importa condiciones esperadas para las esperas explícitas.

# Define la URL de la página principal de donde se van a extraer los datos.
PAGINA_PRINCIPAL = "http://books.toscrape.com"

# Inicializa el navegador Firefox.
navegador = webdriver.Firefox()
navegador.get(PAGINA_PRINCIPAL)  # Abre la página web especificada por la URL.
navegador.implicitly_wait(10)  # Establece una espera implícita de 10 segundos para que los elementos se carguen.

datos = []  # Inicializa una lista vacía para almacenar los datos de los libros.
categorias = ["Humor", "Art"]  # Lista de categorías de libros a extraer.

# Itera sobre la lista de categorías proporcionadas.
for categoria in categorias:
    # Encuentra el enlace a la categoría actual usando XPath y hace clic en él.
    enlace_categoria = navegador.find_element(By.XPATH, f'//a[contains(text(),"{categoria}")]')
    enlace_categoria.click()

    try:
        # Espera explícita de hasta 10 segundos para que los elementos con el selector '.product_pod' estén presentes.
        libros = WebDriverWait(navegador, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product_pod'))
        )
    except Exception as e:
        # Si ocurre una excepción durante la espera, la lanza para ser manejada posteriormente.
        raise e

    # Itera sobre cada libro encontrado en la categoría.
    for libro in libros:
        # Encuentra los elementos correspondientes al título, precio y disponibilidad del libro.
        titulo = libro.find_element(By.CSS_SELECTOR, "h3 > a")
        precio = libro.find_element(By.CSS_SELECTOR, ".price_color")
        stock = libro.find_element(By.CSS_SELECTOR, ".instock.availability")
        # Agrega la información del libro a la lista de datos en forma de diccionario.
        datos.append({
            'titulo': titulo.get_attribute("title"),
            'precio': precio.text,
            'stock': stock.text,
            'categoria': categoria
        })

    # Vuelve a la página principal para continuar con la siguiente categoría.
    navegador.get(PAGINA_PRINCIPAL)

navegador.quit()  # Cierra el navegador.

# Convierte la lista de datos en un DataFrame de pandas.
df = pd.DataFrame(datos)
# Obtener la ruta del directorio actual.
directorio_actual = os.getcwd()
# Concatenar la ruta del directorio con el nombre del archivo CSV.
ruta_csv = os.path.join(directorio_actual, "libros_exportados.csv")
# Guarda el DataFrame como un archivo CSV sin incluir el índice.
df.to_csv(ruta_csv, index=False)
print(df)  # Imprime el DataFrame (para propósitos de depuración).

print('LISTO!')  # Imprime un mensaje indicando que el proceso ha finalizado.
