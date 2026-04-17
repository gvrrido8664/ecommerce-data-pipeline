# 📊 Pipeline de Análisis Logístico: E-commerce Olist Brasil

Este proyecto implementa un flujo de datos completo (End-to-End) para analizar el desempeño logístico de más de 100,000 pedidos. El objetivo principal es identificar cuellos de botella geográficos y medir la eficiencia de las entregas mediante KPIs avanzados.

---

## 🚀 Arquitectura del Proyecto

El proyecto se divide en tres fases principales que demuestran el dominio de diferentes tecnologías:

1.  **Extracción y ETL (Python):** Limpieza de datos crudos, manejo de valores nulos y cálculo de métricas de tiempo utilizando `Pandas`. Carga automatizada a base de datos mediante `SQLAlchemy`.
2.  **Almacenamiento (PostgreSQL):** Persistencia de datos en un entorno relacional para asegurar la integridad y escalabilidad de la información.
3.  **Inteligencia de Negocios (Power BI):** Modelado de datos (Esquema de Estrella) y visualización interactiva utilizando `DAX`.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguajes:** Python 3.14, SQL, DAX.
* **Librerías (Python):** Pandas, NumPy, SQLAlchemy, Psycopg2.
* **Base de Datos:** PostgreSQL / pgAdmin 4.
* **Visualización:** Power BI Desktop.

---

## 📈 Análisis y Dashboard

El dashboard final permite monitorear los siguientes indicadores clave (KPIs):

* **Total de Pedidos:** Volumen histórico de ventas.
* **% de Entregas a Tiempo:** Tasa de cumplimiento respecto a la fecha estimada.
* **Promedio de Días de Retraso:** Tiempo excedido en entregas fuera de plazo.
* **Tendencia Temporal:** Evolución de pedidos mes a mes (Eje cronológico).
* **Desempeño Geográfico:** Identificación de estados con mayores tiempos de entrega (Ej: Amapá y Pará).

### Desafíos Técnicos Resueltos:
* **Modelado de Datos:** Implementación de una **Tabla Calendario (Dim_Date)** en DAX para resolver problemas de registros duplicados por marcas de tiempo (timestamp) y permitir filtros únicos por Mes-Año.
* **Optimización de Consultas:** Normalización de tipos de datos en la carga para mejorar el rendimiento del reporte.

---

## 📂 Estructura del Repositorio

* `/scripts`: Código en Python para la limpieza y carga de datos.
* `/sql`: Scripts DDL para la creación de tablas en PostgreSQL.
* `/dashboard`: Archivo `.pbix` con el informe interactivo de Power BI.

---

## 💡 Conclusión e Insights
A través de este análisis, se determinó que a pesar de tener un **93% de cumplimiento general**, existen estados específicos cuya logística requiere optimización debido a que superan ampliamente el promedio nacional de 10.5 días de retraso. Este pipeline proporciona una base sólida para la toma de decisiones basada en datos.

---
**Autor:** Ignacio Garrido 
**Perfil:** Ingeniero en Informática | Graduado de Inacap
