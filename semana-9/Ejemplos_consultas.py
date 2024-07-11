
# Solicitud de un recurso a un endpoint sin argumentos

import requests
import json

URL = "https://jsonplaceholder.typicode.com/posts"

respuesta = requests.get(URL)

if respuesta.status_code == 200:
    print('Solicitud exitosa')
    print('Datos:', respuesta.json())
else:
    print("Error en la solicitud del recurso. Detalles: \n",
          respuesta.text)

# Solicitud de un recurso a un endpoint con argumentos

URL = "https://jsonplaceholder.typicode.com/posts/1/comments/"

respuesta = requests.get(URL)

if respuesta.status_code == 200:
    print('Solicitud exitosa')
    print('Datos:', respuesta.json())
else:
    print("Error en la solicitud del recurso. Detalles: \n",
          respuesta.text)
    
# Envio de un recurso a un endpoint con argumentos

URL = "https://jsonplaceholder.typicode.com/posts/"

datos = {
    "title": 'titulo ejemplo',
    'body': "parrafo de ejemplo", 
    'id': 1 
    }

headers = {
    'Content-type': 'application/json; charset=UTF-8'
    }

respuesta = requests.post(URL, data = json.dumps(datos), headers = headers)
respuesta_json = respuesta.json()

if respuesta.status_code == 201:
    print('Se ha insertado exitosamente')
    print('Datos:', respuesta_json)
else:
    print("Error en la solicitud del recurso. Detalles: \n",
          respuesta.text)

# Metodo delete

URL = "https://jsonplaceholder.typicode.com/posts/101"

respuesta = requests.delete(URL)
print(respuesta.status_code)