import pandas as pd
from sqlalchemy import create_engine

# 1. Definir la ruta del archivo procesado
ruta_processed = './data/processed/dataset_logistica_limpio.csv'

print("Cargando el dataset limpio a la memoria...")
df = pd.read_csv(ruta_processed)

print("Conectando a la base de datos...")
# 2. Configurar la conexión a tu base de datos
usuario = 'postgres'
contrasena = 'admin123'
host = 'localhost'
puerto = '5432' 
base_de_datos = 'ecommerce_db'

# Cadena de conexión para PostgreSQL (Si usas SQL Server, avísame y te doy la correcta)
cadena_conexion = f'postgresql://{usuario}:{contrasena}@{host}:{puerto}/{base_de_datos}'
engine = create_engine(cadena_conexion)

print("Insertando datos en SQL (Esto puede tardar unos segundos)...")
# 3. Cargar los datos a SQL automáticamente
# Esto creará una tabla llamada 'hechos_entregas' y reemplazará los datos si ya existe
df.to_sql('hechos_entregas', con=engine, if_exists='replace', index=False)

print("¡Carga exitosa! Tu base de datos está lista para ser analizada.")