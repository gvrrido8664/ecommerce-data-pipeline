-- El ETL crea hechos_entregas_portafolio cuando no existe; no reemplaza tablas.
-- Después de la carga, ejecutar opcionalmente esta restricción:
ALTER TABLE hechos_entregas_portafolio ADD PRIMARY KEY (order_id);
