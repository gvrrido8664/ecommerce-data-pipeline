-- Table: public.hechos_entregas

-- DROP TABLE IF EXISTS public.hechos_entregas;

CREATE TABLE IF NOT EXISTS public.hechos_entregas
(
    order_id text COLLATE pg_catalog."default",
    customer_id text COLLATE pg_catalog."default",
    order_status text COLLATE pg_catalog."default",
    order_purchase_timestamp text COLLATE pg_catalog."default",
    order_approved_at text COLLATE pg_catalog."default",
    order_delivered_carrier_date text COLLATE pg_catalog."default",
    order_delivered_customer_date text COLLATE pg_catalog."default",
    order_estimated_delivery_date text COLLATE pg_catalog."default",
    customer_unique_id text COLLATE pg_catalog."default",
    customer_zip_code_prefix bigint,
    customer_city text COLLATE pg_catalog."default",
    customer_state text COLLATE pg_catalog."default",
    order_item_id bigint,
    product_id text COLLATE pg_catalog."default",
    seller_id text COLLATE pg_catalog."default",
    shipping_limit_date text COLLATE pg_catalog."default",
    price double precision,
    freight_value double precision,
    dias_diferencia bigint,
    estado_entrega text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.hechos_entregas
    OWNER to postgres;