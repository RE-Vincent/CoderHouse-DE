import requests
from psycopg2 import connect, Error
from psycopg2.extras import execute_batch
from datetime import datetime
import os
import numpy as np

# Credenciales de autenticación
USERNAME = os.getenv("username_ch")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
DATABASE = os.getenv("database")
PORT = os.getenv("port")
API_KEY = os.getenv("api_key")


# Varibale de tiempo
today = datetime.now()

# Endpoint
url = 'https://financialmodelingprep.com/api/v3/'

def get_data(fund: str) -> list:
    """Función que lee los datos"""
    # Obtener datos de la API
    response = requests.get(f'{url}/{fund}/list?apikey={API_KEY}')
    
    # Verificar si la solicitud fue exitosa
    if response.status_code != 200:
        print(f"Error al obtener datos: {response.status_code}")
        return []
    
    stocks_data = response.json()
    
    # Eliminar registros con valores nulos
    data = [dictionary for dictionary in stocks_data if all(value is not None for value in dictionary.values())]
    
    # Eliminar registros duplicados basados en la clave 'symbol'
    unique_data = [dict(t) for t in {tuple(d.items()) for d in data}]
    
    # Agregar el registro de la fecha del request
    for dictionary in unique_data:
        dictionary['date'] = today
    
    # Obtener los precios de las acciones
    prices = [d.get('price', 0) for d in unique_data]

    # Manejamos los valores atipicos de acuerdo a la distribución de los datos
    # Calcular el rango intercuartílico (IQR)
    q1 = np.percentile(prices, 25)
    q3 = np.percentile(prices, 75)
    iqr = q3 - q1
    
    # Establecer los límites para los valores atípicos
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # Filtrar los datos basados en los límites
    filtered_data = [d for d in unique_data if lower_bound < d.get('price', 0) < upper_bound]
    print("Datos obtenidos exitosamente")
    
    return filtered_data

def api_to_aws(data):
    try:
        # Conexión persistente a la base de datos
        conn = connect(
            host=HOST,
            database=DATABASE,
            port=PORT,
            user=USERNAME,
            password=PASSWORD,
        )
        
        cursor = conn.cursor()

        # Creación de la tabla con clave primaria compuesta
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rmorenocueva_coderhouse.ETF_list (
                symbol VARCHAR(50) NOT NULL,
                name VARCHAR(200) NOT NULL,
                price DOUBLE PRECISION,
                exchange VARCHAR(50),
                exchangeShortName VARCHAR(50),
                type VARCHAR(20),
                date TIMESTAMP,
                PRIMARY KEY (symbol, date)
            )
        """)
        
        conn.commit()

        # Ingesta de los datos por lotes
        ingesta_batch = """
            INSERT INTO rmorenocueva_coderhouse.ETF_list (
                symbol, name, price, exchange, exchangeShortName, type, date
            )
            VALUES (
                %(symbol)s, %(name)s, %(price)s, %(exchange)s, %(exchangeShortName)s, %(type)s, %(date)s
            )
        """
        execute_batch(cursor, ingesta_batch, data)

        conn.commit()
        print("Datos insertados correctamente.")
    except (Exception, Error) as error:
        print("Error al insertar datos:", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Conexión cerrada.")

# if __name__ == '__main__':
#     data = get_data('etf')
#     api_to_aws(data)
