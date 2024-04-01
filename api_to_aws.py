import requests
import psycopg2
from psycopg2.extras import execute_batch
import time
import os
from dotenv import load_dotenv
import hashlib
import json

load_dotenv()

# Credenciales de autenticación
USERNAME = os.getenv("username_ch")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
DATABASE = os.getenv("database")
PORT = os.getenv("port")
PUBLIC_KEY = os.getenv("public_key")
PRIVATE_KEY = os.getenv("private_key")

# Endpoint de la API de Marvel
BASE_URL = 'http://gateway.marvel.com/v1/public/'

# Función para obtener el hash de autenticación
def generate_auth_hash(ts):
    hash_input = f'{ts}{PRIVATE_KEY}{PUBLIC_KEY}'
    return hashlib.md5(hash_input.encode('utf-8')).hexdigest()

# Función para realizar una solicitud a la API de Marvel
def make_request(endpoint, params=None):
    # Generar un timestamp para la solicitud
    ts = str(int(time.time()))

    # Generar el hash de autenticación
    hash_ = generate_auth_hash(ts)

    # Parámetros de la solicitud
    params = params or {}
    params['ts'] = ts
    params['apikey'] = PUBLIC_KEY
    params['hash'] = hash_

    # Realizar la solicitud
    response = requests.get(BASE_URL + endpoint, params=params)
    return response.json()

def get_data(endpoint):
    response = make_request(endpoint)
    data = response['data']['results']
    
    # Mapeo de claves a procesar
    key_mapping = {
        'thumbnail': lambda x: x['path'] + '.' + x['extension'],
        'comics': lambda x: x['available'],
        'series': lambda x: x['available'],
        'stories': lambda x: x['available'],
        'events': lambda x: x['available']
    }
    
    # Procesar los datos
    new_data = []
    for item in data:
        new_item = {key: key_mapping[key](item[key]) if key in key_mapping else item[key] for key in item if key != 'urls'}
        new_data.append(new_item)
    
    return new_data

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
                    CREATE TABLE IF NOT EXISTS rainier_moreno_coderhouse.characters_marvel (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(255),
                    description VARCHAR(1000),
                    modified VARCHAR(50),
                    thumbnail VARCHAR(500),
                    resourceURI VARCHAR(500),
                    comics INTEGER,
                    series INTEGER,
                    stories INTEGER,
                    events INTEGER
                )
                """)

    conn.commit()

    #Ingesta de los datos por batch desde el diccionario a la tabla
    ingesta_batch = """
                    INSERT INTO rainier_moreno_coderhouse.characters_marvel (
                        id, name, description, modified, thumbnail, resourceURI, comics, series, stories, events)
                    VALUES (
                        %(id)s, %(name)s, %(description)s, %(modified)s, %(thumbnail)s, %(resourceURI)s, %(comics)s, %(series)s,%(stories)s, %(events)s)
                    """
    execute_batch(conn.cursor(), ingesta_batch, data)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    data = get_data('characters')
    api_to_aws(data)