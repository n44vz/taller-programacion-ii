import pandas as pd
import sqlite3
from flask import Flask, jsonify
import os

app = Flask(__name__)

def inicializar_bd():
    """
    Inicializa la base de datos leyendo un archivo CSV y creando una tabla SQL.
    """
    try:
        directorio_actual = os.getcwd()
        os.chdir(directorio_actual)
        # Lee el archivo CSV
        df = pd.read_excel('Superstore.xlsx')
        # Conecta a la base de datos SQLite
        conn = sqlite3.connect('ventas.db')
        # Crea la tabla 'pedidos' a partir del DataFrame
        df.to_sql('pedidos', conn, if_exists='replace', index=False)
        conn.close()
        print("Base de datos inicializada exitosamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")

# Inicializa la base de datos al inicio
inicializar_bd()

def obtener_conexion_bd():
    """
    Establece y retorna una conexión a la base de datos.
    """
    return sqlite3.connect('ventas.db')

@app.route('/pedidos/<order_id>', methods=['GET'])
def obtener_pedido(order_id):
    """
    Maneja la solicitud GET para obtener un pedido específico.
    """
    conn = obtener_conexion_bd()
    cursor = conn.cursor()
    # Ejecuta la consulta SQL para obtener el pedido
    cursor.execute("SELECT * FROM pedidos WHERE [Order ID] = ?", (order_id,))
    pedido = cursor.fetchone()
    conn.close()

    if pedido:
        # Convierte el resultado a un diccionario
        columnas = [column[0] for column in cursor.description]
        resultado = dict(zip(columnas, pedido))
        return jsonify(resultado)
    else:
        return jsonify({"error": "Pedido no encontrado"}), 404

if __name__ == '__main__':
    # Inicia la aplicación Flask
    app.run(debug=False, port=5000)