# E-commerce: ETL e indicadores de entregas

Proyecto personal de **Ignacio Garrido**, Ingeniero en Informática titulado. Desarrollo propio de la aplicación; librerías, plantillas, datos e imágenes de terceros conservan su autoría.

Transforma órdenes, clientes e ítems en una tabla con **una fila por pedido** para analizar puntualidad de entregas. Python, pandas, SQLAlchemy y PostgreSQL opcional.

![Indicadores de la demo sintética](docs/indicadores.png)

## Ejecutar sin claves ni dataset externo
Requiere Python 3.12+; comandos desde esta carpeta:
```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python demo.py
```
Abre `demo_output/reporte.html`. Se generan cuatro pedidos ficticios: dos puntuales y dos atrasados. No son resultados comerciales. La demo comprueba pedidos con varios ítems, suma de importes, retrasos inferiores a un día y rechazo de IDs duplicados.

## Fuente externa opcional
Descarga manualmente el [dataset de Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) y revisa sus condiciones de uso. Coloca `olist_orders_dataset.csv`, `olist_order_items_dataset.csv` y `olist_customers_dataset.csv` en `data/raw/`.
```powershell
python scripts/pipeline.py --raw data/raw --output data/processed/pedidos.csv
```
La carga opcional usa `DATABASE_URL` del entorno:
```powershell
$env:DATABASE_URL='postgresql://USUARIO:CONTRASENA@localhost:5432/portafolio'
python scripts/pipeline.py --raw data/raw --load-sql
```
No se leen automáticamente archivos `.env`; `.env.example` muestra el formato. La tabla `hechos_entregas_portafolio` debe ser nueva: una tabla existente produce error, no se reemplaza. Los scripts antiguos delegan al mismo ETL.

## Decisiones y límites
Agrego importes e ítems antes de cruzarlos con las órdenes. Valido claves, fechas y relación con clientes. El atraso se calcula con segundos, sin truncar retrasos parciales. Excluyo entregas sin fechas completas; los KPIs describen únicamente las filas válidas entregadas. El promedio de retraso considera solo pedidos atrasados. No se incluye PBIX; la demostración disponible es HTML. Se verificó persistencia de cuatro pedidos sintéticos en PostgreSQL 16; no se ejecutó el dataset Olist completo.

English: order-level ETL with validated joins, delivery KPIs and a self-contained synthetic demo. See `demo.py` and `scripts/pipeline.py`.
