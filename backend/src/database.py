
import os
import psycopg
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Obtiene la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """
    Establece y devuelve una conexión a la base de datos PostgreSQL usando psycopg v3.
    Lanza una excepción si la URL de la base de datos no está configurada.
    """
    if not DATABASE_URL:
        raise ValueError("La variable de entorno DATABASE_URL no está configurada o está vacía.")
    
    try:
        # La nueva sintaxis de psycopg 3 es más directa
        conn = psycopg.connect(DATABASE_URL)
        return conn
    except psycopg.OperationalError as e:
        print(f"Error al conectar con la base de datos: {e}")
        # En un futuro, podríamos añadir aquí un sistema de reintentos o de notificación.
        raise

# Ejemplo de uso para verificar la conexión (esto no se ejecutará al importar)
if __name__ == '__main__':
    try:
        print("Intentando conectar a la base de datos con psycopg v3...")
        
        if not DATABASE_URL:
            print("Error: La variable DATABASE_URL no se ha cargado. Verifica tu archivo .env y su ubicación.")
        else:
            connection = get_db_connection()
            print("¡Conexión exitosa!")
            
            # Pequeña prueba para verificar que podemos ejecutar una consulta
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print(f"Versión de la base de datos: {db_version[0]}")
            
            cursor.close()
            connection.close()
            print("Conexión cerrada.")
            
    except (ValueError, psycopg.OperationalError) as e:
        print(f"Fallo en la prueba de conexión: {e}")

