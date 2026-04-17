import pandas as pd
import os

# 1. Definir las rutas (Asumiendo que ejecutas el script desde la carpeta principal)
ruta_raw = './data/raw/'
ruta_processed = './data/processed/'

print("Cargando archivos CSV...")
# 2. Cargar los datasets
ordenes = pd.read_csv(f'{ruta_raw}olist_orders_dataset.csv')
items = pd.read_csv(f'{ruta_raw}olist_order_items_dataset.csv')
clientes = pd.read_csv(f'{ruta_raw}olist_customers_dataset.csv')

print("Cruzando tablas (Merge)...")
# 3. Unir los datos (Como un INNER JOIN en SQL)
df = ordenes.merge(clientes, on='customer_id', how='inner')
df = df.merge(items, on='order_id', how='inner')

print("Limpiando datos...")
# 4. Limpieza básica
# Solo nos importan las órdenes que realmente fueron entregadas
df = df[df['order_status'] == 'delivered'].copy()

# Eliminar filas donde falte la fecha real de entrega
df = df.dropna(subset=['order_delivered_customer_date'])

print("Calculando KPIs de negocio...")
# 5. Transformación de Fechas a formato Datetime
columnas_fecha = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in columnas_fecha:
    df[col] = pd.to_datetime(df[col])

# 6. Lógica de Negocio: Calcular Días de Retraso
# Restamos la fecha real de entrega menos la fecha estimada.
# Si el resultado es > 0, significa que llegó tarde.
df['dias_diferencia'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days

# Crear una columna categórica para que en Power BI sea muy fácil hacer gráficos
df['estado_entrega'] = df['dias_diferencia'].apply(lambda x: 'Atrasado' if x > 0 else 'A Tiempo')

print("Guardando dataset limpio...")
# 7. Guardar el resultado en la carpeta processed
df.to_csv(f'{ruta_processed}dataset_logistica_limpio.csv', index=False)

print(f"¡Proceso terminado! El dataset final tiene {df.shape[0]} filas listas para analizar.")