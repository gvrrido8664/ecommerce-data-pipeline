"""ETL a nivel pedido: nunca contar una fila por ítem como otro pedido."""
from pathlib import Path
import argparse, json, os
import pandas as pd
import math
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parents[1]

def transform(orders, items, customers):
    required = {'orders': ['order_id','customer_id','order_status','order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date'], 'items':['order_id','price','freight_value'], 'customers':['customer_id','customer_state']}
    for name, frame in [('orders',orders),('items',items),('customers',customers)]:
        missing = set(required[name]) - set(frame.columns)
        if missing:
            raise ValueError(f'{name}: faltan columnas {sorted(missing)}')
    for frame,key in [(orders,'order_id'),(customers,'customer_id')]:
        if frame[key].isna().any() or frame[key].duplicated().any():
            raise ValueError(f'{key} debe ser único y no nulo')
    if items['order_id'].isna().any():
        raise ValueError('Los ítems necesitan order_id')
    items = items.copy()
    for col in ['price','freight_value']:
        items[col] = pd.to_numeric(items[col],errors='raise')
        if not items[col].map(math.isfinite).all() or (items[col]<0).any():
            raise ValueError(f'{col} debe ser un importe no negativo')
    totals = items.groupby('order_id',as_index=False).agg(item_count=('price','size'),price=('price','sum'),freight_value=('freight_value','sum'))
    result = orders.loc[orders['order_status']=='delivered',required['orders']].copy()
    for col in ['order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date']:
        result[col] = pd.to_datetime(result[col],errors='raise',format='mixed')
    result = result.dropna(subset=['order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date'])
    result = result.merge(customers[['customer_id','customer_state']],on='customer_id',how='left',validate='many_to_one')
    result = result.merge(totals,on='order_id',how='left',validate='one_to_one')
    if result[['customer_state','item_count']].isna().any().any():
        raise ValueError('Pedidos sin cliente o ítems; revisar integridad de las fuentes')
    result['dias_diferencia'] = (result.order_delivered_customer_date-result.order_estimated_delivery_date).dt.total_seconds()/86400
    result['estado_entrega'] = result.dias_diferencia.map(lambda days:'Atrasado' if days>0 else 'A Tiempo')
    return result

def kpis(frame):
    late = frame[frame.estado_entrega=='Atrasado']
    return {'total_pedidos':int(len(frame)), 'porcentaje_a_tiempo':round(100*(len(frame)-len(late))/len(frame),2) if len(frame) else None, 'dias_retraso_promedio_solo_atrasados':round(float(late.dias_diferencia.mean()),2) if len(late) else 0}

def run(raw_dir, output):
    frame = transform(*[pd.read_csv(raw_dir/f'olist_{name}_dataset.csv') for name in ['orders','order_items','customers']])
    output.parent.mkdir(parents=True,exist_ok=True)
    frame.to_csv(output,index=False)
    output.with_suffix('.json').write_text(json.dumps(kpis(frame),ensure_ascii=False,indent=2),encoding='utf-8')
    return frame

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw',type=Path,default=ROOT/'data/raw')
    parser.add_argument('--output',type=Path,default=ROOT/'data/processed/pedidos.csv')
    parser.add_argument('--load-sql',action='store_true')
    args = parser.parse_args()
    frame = run(args.raw,args.output)
    if args.load_sql:
        url = os.environ.get('DATABASE_URL')
        if not url:
            raise SystemExit('Define DATABASE_URL en el entorno; no se guardan contraseñas en código.')
        engine = create_engine(url)
        with engine.begin() as connection:
            frame.to_sql('hechos_entregas_portafolio',connection,if_exists='fail',index=False)
        engine.dispose()
    print(json.dumps(kpis(frame),ensure_ascii=False))

if __name__ == '__main__':
    main()
