
import os
import csv
import psycopg
from dotenv import load_dotenv

def import_country_data():
    """
    Imports country data from a CSV file into ARIA's knowledge base.
    Connects to the database, reads the CSV, and inserts formatted facts
    about each country's capital, continent, and population.
    """
    load_dotenv()

    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        print("🔴 Error: SUPABASE_DB_URL no está configurado en el archivo .env")
        return

    inserted_count = 0
    try:
        print("🔗 Conectando a la base de datos...")
        with psycopg.connect(db_url) as conn:
            print("✅ Conexión exitosa.")
            with conn.cursor() as cur:
                csv_path = "data/imports/paises_del_mundo.csv"
                print(f"📄 Leyendo el archivo de datos: {csv_path}")

                if not os.path.exists(csv_path):
                    print(f"🔴 Error: El archivo {csv_path} no fue encontrado.")
                    return

                with open(csv_path, mode='r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    
                    for row in reader:
                        pais = row['pais']
                        capital = row['capital']
                        continente = row['continente']
                        poblacion = row['poblacion_aprox']

                        # Crear "hechos" para la base de conocimiento
                        facts = [
                            ("Geografía", f"¿Cuál es la capital de {pais}?", capital),
                            ("Geografía", f"¿Dónde está {pais}?", f"{pais} está en {continente}."),
                            ("Geografía", f"¿En qué continente se encuentra {pais}?", f"{pais} se encuentra en {continente}."),
                            ("Demografía", f"¿Cuál es la población de {pais}?", f"La población aproximada de {pais} es de {poblacion} habitantes."),
                            ("Demografía", f"¿Cuántos habitantes tiene {pais}?", f"{pais} tiene aproximadamente {poblacion} habitantes.")
                        ]

                        # Insertar cada hecho en la base de datos
                        for category, question, answer in facts:
                            try:
                                cur.execute(
                                    "INSERT INTO knowledge_base (category, question, answer) VALUES (%s, %s, %s)",
                                    (category, question, answer)
                                )
                                inserted_count += 1
                            except psycopg.errors.UniqueViolation:
                                # Si el "hecho" (pregunta) ya existe, simplemente lo ignoramos.
                                conn.rollback()
                                continue
                            except Exception as e:
                                print(f"🔴 Error insertando el hecho: {e}")
                                conn.rollback()
                
                conn.commit()
                print(f"✅ ¡Importación completada! Se han añadido {inserted_count} nuevos hechos a la memoria de ARIA.")

    except psycopg.Error as e:
        print(f"🔴 Error de base de datos: {e}")
    except Exception as e:
        print(f"🔴 Ha ocurrido un error inesperado: {e}")

if __name__ == "__main__":
    import_country_data()
