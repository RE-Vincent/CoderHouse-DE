import requests
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime
from dotenv import load_dotenv
import os
import json

load_dotenv()

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

def get_data(fund: str) -> json:
    response = requests.get(f'{url}/{fund}/list?apikey={API_KEY}')
    stocks_data = response.json()
    
    data = [dictionary for dictionary in stocks_data if not any(value is None for value in dictionary.values())]
    for dictionary in data:
        dictionary['date'] = today
    return data

def api_to_aws(data):
    #Conexion y creacion de la tabla
    conn = psycopg2.connect(
                            host = HOST,
                            database = DATABASE,
                            port = PORT,
                            user = USERNAME,
                            password = PASSWORD,
                            )

    cursor = conn.cursor()

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rmorenocueva_coderhouse.ETF_list (
                    symbol VARCHAR(50) NOT NULL,
                    name VARCHAR(200)  NOT NULL,
                    price DOUBLE PRECISION,
                    exchange VARCHAR(50),
                    exchangeShortName VARCHAR(50),
                    type VARCHAR(20),
                    date TIMESTAMP
                )
                """)

    conn.commit()

    #Ingesta de los datos por batch desde el diccionario a la tabla
    ingesta_batch = """
                    INSERT INTO rmorenocueva_coderhouse.ETF_list (
                        symbol, name, price, exchange, exchangeShortName, type, date)
                    VALUES (
                        %(symbol)s, %(name)s, %(price)s, %(exchange)s, %(exchangeShortName)s, %(type)s, %(date)s)
                    """
    execute_batch(conn.cursor(), ingesta_batch, data)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    data = get_data('etf')
    api_to_aws(data)
