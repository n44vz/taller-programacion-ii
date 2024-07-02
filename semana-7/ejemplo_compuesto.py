import os  # Importa el módulo os para interactuar con el sistema operativo.
import pandas as pd  # Importa pandas para manipulación y análisis de datos.
from selenium import webdriver  # Importa webdriver de Selenium para controlar el navegador.
from selenium.webdriver.common.by import By  # Importa By para localizar elementos en la página.
from selenium.webdriver.support.ui import WebDriverWait  # Importa WebDriverWait para esperas explícitas.
from selenium.webdriver.support import expected_conditions as EC  # Importa condiciones esperadas para las esperas explícitas.

# Define la URL de la página principal de donde se van a extraer los datos.
PAGINA_PRINCIPAL = "http://books.toscrape.com"

def obtener_datos(url, categorias):
    """
    Función para obtener datos de libros de la página especificada por la URL y categorías proporcionadas.

    Args:
    url (str): URL de la página principal.
    categorias (list): Lista de categorías de libros a extraer.

    Returns:
    list: Lista de diccionarios con datos de libros.
    """
    # Configura las opciones del navegador para que se ejecute en modo headless (sin interfaz gráfica).
    opciones_navegador = webdriver.FirefoxOptions()
    opciones_navegador.headless = True

    # Inicializa el navegador Firefox con las opciones configuradas.
    driver = webdriver.Firefox(options=opciones_navegador)
    driver.get(url)  # Abre la página web especificada por la URL.
    driver.implicitly_wait(10)  # Establece una espera implícita de 10 segundos para que los elementos se carguen.

    datos = []  # Inicializa una lista vacía para almacenar los datos de los libros.

    # Itera sobre la lista de categorías proporcionadas.
    for categoria in categorias:
        # Encuentra el enlace a la categoría actual usando XPath y hace clic en él.
        enlace_categoria = driver.find_element(By.XPATH, f'//a[contains(text(),"{categoria}")]')
        enlace_categoria.click()

        try:
            # Espera explícita de hasta 10 segundos para que los elementos con el selector '.product_pod' estén presentes.
            libros = WebDriverWait(driver, 10).until(
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
        driver.get(url)

    driver.quit()  # Cierra el navegador.
    return datos  # Devuelve la lista de datos recopilados.

def exportar_csv(datos):
    """
    Función para exportar los datos recopilados a un archivo CSV.

    Args:
    datos (list): Lista de diccionarios con datos de libros.
    """
    # Convierte la lista de datos en un DataFrame de pandas.
    df = pd.DataFrame(datos)
    # Obtener la ruta del directorio donde se encuentra el script.
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    # Concatenar la ruta del directorio con el nombre del archivo CSV.
    ruta_csv = os.path.join(directorio_script, "libros_exportados.csv")
    # Guarda el DataFrame como un archivo CSV sin incluir el índice.
    df.to_csv(ruta_csv, index=False)
    print(df)  # Imprime el DataFrame (para propósitos de depuración).

def main():
    """
    Función principal para obtener los datos de libros y exportarlos a un archivo CSV.
    """
    # Llama a obtener_datos con la URL de la página principal y las categorías de interés, almacenando los datos devueltos.
    datos = obtener_datos(url=PAGINA_PRINCIPAL, categorias=["Humor", "Art"])
    # Llama a exportar_csv para guardar los datos en un archivo CSV.
    exportar_csv(datos)
    print('LISTO!')  # Imprime un mensaje indicando que el proceso ha finalizado.

if __name__ == '__main__':
    # Comprueba si el script se está ejecutando directamente (no importado como un módulo) y llama a la función principal.
    main()
